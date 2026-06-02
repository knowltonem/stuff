#!/usr/bin/env python3
"""
finalize_doc.py — Finalization pipeline for ICR documents.

Converts a Draft_*.docx into two final outputs saved under a named subfolder
inside the document type's Final/ directory:

    <doc_type_folder>/
    ├── Drafts/
    │   └── Draft_CTN... .docx          ← source
    └── Final/
        └── CTN... - Cisco ICR [DocType]/   ← subfolder named same as files
            ├── CTN... - Cisco ICR [DocType].docx
            └── CTN... - Cisco ICR [DocType].pdf  (with AcroForm /Sig field)

Steps:
    1. Locate the draft file from prod_cat / ctn / dtr_num / doc_type / version
    2. Copy it (stripping Draft_ prefix) to Final/<stem>/<stem>.docx
    3. Convert to PDF via LibreOffice headless CLI
    4. Inject an AcroForm /Sig field (bottom-right, last page) using pypdf
    5. Report output paths

Usage (direct CLI — for testing):
    python3 _Tools/finalize_doc.py

Called by the AI via:
    python3 _Tools/finalize_doc.py <prod_cat> <ctn> <dtr_num> <doc_type_key> <version>

doc_type_key values:
    sysdesc | fa | memo | mudg | tdr | csr | loc | poam | diagram

Prerequisites (one-time):
    pip install docx2pdf pypdf        ← preferred (uses Word on macOS, no system install)
    -- OR --
    brew install --cask libreoffice   ← fallback if Word is not available
    pip install pypdf

PDF conversion order:
    1. docx2pdf (Word JXA on macOS) — perfect fidelity, pip-only
    2. LibreOffice headless           — fallback if docx2pdf unavailable
"""

import shutil
import subprocess
import sys
import time
import platform
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from runner_core import (
    BASE,
    final_dir, final_docx_path, final_pdf_path,
    sysdesc_draft_path,
    fa_draft_path,
    memo_draft_path,
    mudg_draft_path,
    tdr_draft_path,
    csr_draft_path,
    loc_draft_path,
    poam_draft_path,
    system_diagram_draft_path,
)

# ---------------------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------------------

LIBREOFFICE_PATHS = [
    Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),
    Path("/usr/bin/soffice"),
    Path("/usr/local/bin/soffice"),
]


def _find_libreoffice() -> Optional[Path]:
    for p in LIBREOFFICE_PATHS:
        if p.exists():
            return p
    # Also try PATH
    found = shutil.which("soffice")
    return Path(found) if found else None


def check_dependencies() -> list[str]:
    """Return a list of missing dependency warning strings (empty = all good)."""
    missing = []

    # PDF conversion — Word via AppleScript (macOS) or LibreOffice
    has_word = False
    try:
        r = subprocess.run(
            ["osascript", "-e", 'tell application "Microsoft Word" to get version'],
            capture_output=True, text=True, timeout=10,
        )
        has_word = r.returncode == 0 and r.stdout.strip()
    except Exception:
        pass

    has_libreoffice = _find_libreoffice() is not None

    if not has_word and not has_libreoffice:
        missing.append(
            "No PDF converter found.\n"
            "  Option 1 — grant Terminal Automation permission for Microsoft Word:\n"
            "    System Settings → Privacy & Security → Automation → Terminal → Microsoft Word ✓\n"
            "  Option 2 — install LibreOffice: brew install --cask libreoffice"
        )

    try:
        import pypdf  # noqa: F401
    except ImportError:
        missing.append("pypdf not installed. Install with: pip install pypdf")
    return missing


# ---------------------------------------------------------------------------
# Draft path resolver
# ---------------------------------------------------------------------------

def resolve_draft_path(
    prod_cat: str,
    ctn: str,
    dtr_num: int,
    doc_type_key: str,
    version: str,
    *,
    tdr_number: str = "",
    prod_cat_abbr: str = "",
) -> Path:
    """Return the expected draft Path for the given doc type and parameters."""
    key = doc_type_key.lower().replace(" ", "").replace("_", "")
    if key in ("sysdesc", "systemdescription"):
        return sysdesc_draft_path(prod_cat, ctn, dtr_num, version)
    if key in ("fa", "functionalityattestation"):
        return fa_draft_path(prod_cat, ctn, dtr_num, version)
    if key in ("memo", "icrmemo", "icrsummarymemorandum"):
        return memo_draft_path(prod_cat, ctn, dtr_num, version)
    if key in ("mudg", "militaryuniquedeploymentguide"):
        return mudg_draft_path(prod_cat, ctn, dtr_num)
    if key in ("tdr", "testdiscrepancyreport"):
        return tdr_draft_path(prod_cat, ctn, dtr_num, tdr_number, prod_cat_abbr or prod_cat, version)
    if key in ("csr", "cybersecuritysummaryreport"):
        return csr_draft_path(prod_cat, ctn, dtr_num, version)
    if key in ("loc", "letterofcompliance"):
        return loc_draft_path(prod_cat, ctn, dtr_num, version)
    if key in ("poam", "planofactionmilestone"):
        return poam_draft_path(prod_cat, ctn, dtr_num, tdr_number, prod_cat_abbr or prod_cat, version)
    if key in ("diagram", "systemdiagram"):
        return system_diagram_draft_path(prod_cat, ctn, dtr_num, version)
    raise ValueError(f"Unknown doc_type_key: '{doc_type_key}'")


# ---------------------------------------------------------------------------
# Step 1 — Copy .docx to Final/
# ---------------------------------------------------------------------------

def copy_to_final(draft_path: Path) -> Path:
    """Copy draft .docx to Final/<stem>/<stem>.docx, stripping the Draft_ prefix."""
    out = final_docx_path(draft_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        confirm = input(f"\n  [finalize_doc] Final .docx already exists: {out.name}\n  Overwrite? [y/N]: ")
        if confirm.strip().lower() != "y":
            raise FileExistsError(f"Aborted — will not overwrite existing final file: {out}")
    shutil.copy2(str(draft_path), str(out))
    print(f"  [1/3] Final .docx saved:  {out.relative_to(BASE)}")
    return out


# ---------------------------------------------------------------------------
# Step 2 — Convert .docx → PDF via LibreOffice
# ---------------------------------------------------------------------------

def convert_to_pdf(final_docx: Path) -> Path:
    """Convert a .docx to PDF. Tries Word via AppleScript first, falls back to LibreOffice."""
    out_dir = final_docx.parent
    expected_pdf = out_dir / f"{final_docx.stem}.pdf"

    if expected_pdf.exists():
        raise FileExistsError(
            f"Aborted — PDF already exists and will not be overwritten: {expected_pdf}\n"
            "Delete or rename the existing PDF before re-running finalize."
        )

    # --- Attempt 1: Word via AppleScript (macOS only, perfect fidelity, no system install) ---
    if platform.system() != "Darwin":
        print("  [2/3] Skipping Word AppleScript (macOS only) — falling through to LibreOffice.")
    else:
        word_script = f'''
tell application "Microsoft Word"
    open POSIX file "{final_docx}"
    set theDoc to active document
    save as theDoc file name "{expected_pdf}" file format format PDF
    close theDoc saving no
end tell
'''
        try:
            print("  [2/3] Converting via Microsoft Word (AppleScript)...")
            result = subprocess.run(
                ["osascript", "-e", word_script],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0 and expected_pdf.exists():
                print(f"  [2/3] PDF converted:       {expected_pdf.relative_to(BASE)}")
                return expected_pdf
            else:
                err = result.stderr.strip() or "PDF not found after conversion"
                print(f"  [2/3] Word AppleScript failed ({err}) — falling back to LibreOffice.")
        except Exception as e:
            print(f"  [2/3] Word AppleScript error ({e}) — falling back to LibreOffice.")

    # --- Attempt 2: LibreOffice headless ---
    lo = _find_libreoffice()
    if lo is None:
        raise EnvironmentError(
            "No PDF converter available.\n"
            "Option 1 — grant Terminal Automation permission in:\n"
            "  System Settings → Privacy & Security → Automation → Terminal → Microsoft Word ✓\n"
            "Option 2 — install LibreOffice: brew install --cask libreoffice"
        )

    print("  [2/3] Converting via LibreOffice headless...")
    result = subprocess.run(
        [str(lo), "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(final_docx)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"LibreOffice conversion failed (exit {result.returncode}):\n{result.stderr.strip()}"
        )

    lo_pdf = out_dir / f"{final_docx.stem}.pdf"
    for _ in range(20):
        if lo_pdf.exists():
            break
        time.sleep(0.5)

    if not lo_pdf.exists():
        raise FileNotFoundError(f"LibreOffice did not produce expected PDF: {lo_pdf}")

    print(f"  [2/3] PDF converted:       {lo_pdf.relative_to(BASE)}")
    return lo_pdf


# ---------------------------------------------------------------------------
# Step 3 — Inject AcroForm /Sig field (bottom-right, last page)
# ---------------------------------------------------------------------------

# Signature field geometry (US Letter = 612 × 792 pts; origin = bottom-left)
# Placed bottom-right: x1=310, y1=72, x2=540, y2=126 (1.75"×0.75" at 1" from bottom)
SIG_RECT = (310.0, 72.0, 540.0, 126.0)   # PDF user-space points: (x1, y1, x2, y2), origin bottom-left
                                           # x1=310, y1=72  → left edge, bottom of sig box
                                           # x2=540, y2=126 → right edge, top of sig box
                                           # Positions the field in the lower-right signature block area
SIG_FIELD_NAME = "Authorized_Signature"
SIG_FIELD_LABEL = "Authorized Signature"


def inject_signature_field(pdf_path: Path) -> Path:
    """Add an unsigned AcroForm /Sig field to the last page of the PDF.

    The field is a visual placeholder — it does not apply a cryptographic signature.
    Adobe Acrobat, Adobe Sign, and DocuSign will detect and use it for signing.

    SigFlags=3: bit0 (signatures exist) + bit1 (append-only after signing).
    """
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import (
            ArrayObject,
            BooleanObject,
            DictionaryObject,
            NameObject,
            NumberObject,
            create_string_object,
        )
    except ImportError:
        raise EnvironmentError(
            "pypdf not installed.\n"
            "Install with: pip install pypdf"
        )

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)

    last_page_idx = len(writer.pages) - 1
    last_page = writer.pages[last_page_idx]

    # Build the AcroForm /Sig widget annotation
    sig_field = DictionaryObject()
    sig_field.update(
        {
            NameObject("/Type"):    NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"):      NameObject("/Sig"),
            NameObject("/T"):       create_string_object(SIG_FIELD_NAME),
            NameObject("/TU"):      create_string_object(SIG_FIELD_LABEL),  # tooltip
            NameObject("/Ff"):      NumberObject(0),   # no flags (not read-only, not required)
            NameObject("/F"):       NumberObject(4),   # Print flag
            NameObject("/Rect"):    ArrayObject([
                NumberObject(SIG_RECT[0]),
                NumberObject(SIG_RECT[1]),
                NumberObject(SIG_RECT[2]),
                NumberObject(SIG_RECT[3]),
            ]),
        }
    )

    # Add page reference
    sig_field[NameObject("/P")] = last_page.indirect_reference

    # Add widget to page /Annots
    if "/Annots" in last_page:
        last_page["/Annots"].append(sig_field)
    else:
        last_page[NameObject("/Annots")] = ArrayObject([sig_field])

    # Add or update /AcroForm in the document catalog
    root = writer._root_object
    if "/AcroForm" not in root:
        root[NameObject("/AcroForm")] = DictionaryObject(
            {
                NameObject("/Fields"):   ArrayObject([sig_field]),
                NameObject("/SigFlags"): NumberObject(3),  # signatures exist + append-only
            }
        )
    else:
        acroform = root["/AcroForm"]
        if "/Fields" in acroform:
            acroform["/Fields"].append(sig_field)
        else:
            acroform[NameObject("/Fields")] = ArrayObject([sig_field])
        # Set SigFlags = 3
        acroform[NameObject("/SigFlags")] = NumberObject(3)

    # Overwrite the pdf in place
    with open(str(pdf_path), "wb") as f:
        writer.write(f)

    print(f"  [3/3] Signature field:     injected on page {last_page_idx + 1} (bottom-right)")
    return pdf_path


# ---------------------------------------------------------------------------
# Main finalization entry point
# ---------------------------------------------------------------------------

def finalize(
    draft_path: Path,
    *,
    skip_signature: bool = False,
) -> dict:
    """
    Run the full finalization pipeline for a given draft path.

    Returns a dict with keys: 'docx', 'pdf'
    Raises on any step failure.
    """
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft not found: {draft_path}")

    print(f"\n=== Finalizing: {draft_path.name} ===\n")

    # 1. Copy .docx
    final_docx = copy_to_final(draft_path)

    # 2. Convert to PDF
    pdf_path = convert_to_pdf(final_docx)

    # 3. Inject signature field
    if not skip_signature:
        try:
            inject_signature_field(pdf_path)
        except Exception as e:
            print(f"  [3/3] Signature field:     skipped — pypdf error: {e}")
            print("        PDF is still valid. Add signature field manually in Acrobat/Adobe Sign.")
    else:
        print("  [3/3] Signature field:     skipped (--no-sig flag)")

    print(f"\n  Final folder: {final_dir(draft_path).relative_to(BASE)}")
    print(f"  Files ready for review and commit.\n")

    return {"docx": final_docx, "pdf": pdf_path}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """
    CLI usage:
        python3 _Tools/finalize_doc.py <prod_cat> <ctn> <dtr_num> <doc_type_key> <version>

    Example:
        python3 _Tools/finalize_doc.py SBC CTN2026003 1 sysdesc "IOS XE 26.2"

    Interactive mode (no args):
        python3 _Tools/finalize_doc.py
    """
    # Dependency check — warn early; exit if any dependency is missing
    missing = check_dependencies()
    if missing:
        print("\n[finalize_doc] Missing dependencies:")
        for m in missing:
            print(f"  • {m}")
        print()
        sys.exit(1)  # Exit on any missing dependency — do not attempt partial finalization

    args = sys.argv[1:]

    # Dependency check shortcut — used by skill_system_description.md pre-flight step
    if args and args[0] == "--check-deps":
        missing = check_dependencies()
        if missing:
            for m in missing:
                print(f"  MISSING: {m}")
            sys.exit(1)
        else:
            print("OK — all dependencies present.")
            sys.exit(0)

    if len(args) >= 5:
        prod_cat      = args[0]
        ctn           = args[1]
        dtr_num       = int(args[2])
        doc_type_key  = args[3]
        version       = args[4]
        tdr_number    = args[5] if len(args) > 5 else ""
        prod_cat_abbr = args[6] if len(args) > 6 else ""
    else:
        print("\n=== ICR Document Finalizer ===\n")
        prod_cat      = input("Product Category (e.g. SBC): ").strip()
        ctn           = input("CTN (e.g. CTN2026003): ").strip()
        dtr_num       = int(input("DTR Number (e.g. 1): ").strip())
        doc_type_key  = input("Doc type (sysdesc / fa / memo / mudg / tdr / csr / loc / poam / diagram): ").strip()
        version       = input("Software version (e.g. IOS XE 26.2): ").strip()
        tdr_number    = ""
        prod_cat_abbr = ""

    draft_path = resolve_draft_path(
        prod_cat, ctn, dtr_num, doc_type_key, version,
        tdr_number=tdr_number,
        prod_cat_abbr=prod_cat_abbr,
    )

    result = finalize(draft_path)

    print("Done.")
    print(f"  .docx: {result['docx']}")
    print(f"  .pdf:  {result['pdf']}")


if __name__ == "__main__":
    main()
