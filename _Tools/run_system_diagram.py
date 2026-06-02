#!/usr/bin/env python3
"""
run_system_diagram.py — Parameterized System Diagram runner.
# STATUS: SKELETON
#
# Generates Visio (.vsdx) System Diagram files by:
#   1. Copying the source .vsdx (INITIAL for DTR001, previous draft for DTR002+)
#   2. Auto-updating the filename label shape inside the Visio
#   3. Applying any text field changes provided in the config
#   4. Saving the modified .vsdx to Drafts/
#
# PNG export is manual — engineer opens the generated .vsdx in Visio.
#
# Usage (direct):
#     python3 _Tools/run_system_diagram.py
#
# Or invoked via generate() with a config dict from the newd prompt sequence.
"""

import shutil
import sys
from pathlib import Path
from typing import Optional, List

sys.path.insert(0, str(Path(__file__).parent))
from runner_core import (
    run_validate, append_draft_log, BASE, get_git_username,
    system_diagram_dir, system_diagram_draft_path,
    system_diagram_initial_path,
)

import vsdx


# ---------------------------------------------------------------------------
# Shape text extraction — get all text-containing shapes from a .vsdx
# ---------------------------------------------------------------------------

def _collect_text_shapes(shape, results: list, depth: int = 0):
    """Recursively collect shapes that have text content."""
    text = shape.text.strip() if shape.text else ""
    if text:
        results.append({
            "shape": shape,
            "id": shape.ID if hasattr(shape, "ID") else "?",
            "text": text,
            "depth": depth,
        })
    # Recurse into child shapes
    children = shape.child_shapes if hasattr(shape, "child_shapes") else []
    for child in children:
        _collect_text_shapes(child, results, depth + 1)


def get_all_text_shapes(vsdx_file: vsdx.VisioFile) -> list:
    """Return list of dicts with shape references and their text for all pages."""
    results = []
    for page in vsdx_file.pages:
        for shape in page.child_shapes:
            _collect_text_shapes(shape, results)
    return results


# ---------------------------------------------------------------------------
# Filename label shape — auto-detect by matching pattern
# ---------------------------------------------------------------------------

def _find_filename_label_shape(text_shapes: list, ctn: str, prod_cat: str):
    """Find the shape containing the filename label (e.g. 'CTN2026003-DTR000-SBC.vsdx')."""
    ctn_num = ctn.replace("CTN", "")
    for item in text_shapes:
        text = item["text"]
        # Match patterns like "CTN2026003-DTR000-SBC.vsdx" or similar
        if f"CTN{ctn_num}" in text and prod_cat in text and ".vsdx" in text.lower():
            return item
        # Also match if it just has the CTN and ends with .vsdx
        if f"{ctn_num}" in text and text.strip().lower().endswith(".vsdx"):
            return item
    return None


# ---------------------------------------------------------------------------
# Generation — core logic
# ---------------------------------------------------------------------------

def generate(cfg: dict):
    """Generate a System Diagram .vsdx by copying source and updating text fields.

    Required cfg keys:
        prod_cat (str): Product category abbreviation (e.g. 'SBC')
        ctn (str): CTN identifier (e.g. 'CTN2026003')
        dtr_num (int): DTR number
        out_path (Path|str): Output file path
        source_path (Path|str): Source .vsdx file to copy from

    Optional cfg keys:
        text_updates (dict): Mapping of shape ID (str) -> new text value
            e.g. {"3": "Cisco SBC24", "18": "Updated description..."}
        new_ver (str): New IOS XE version (for tracking/logging only)
    """
    source_path = Path(cfg["source_path"])
    out_path = Path(cfg["out_path"])
    prod_cat = cfg["prod_cat"]
    ctn = cfg["ctn"]
    dtr_num = cfg["dtr_num"]
    text_updates = cfg.get("text_updates", {})

    if not source_path.exists():
        raise FileNotFoundError(f"Source .vsdx not found: {source_path}")

    # Ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy source to output location first
    shutil.copy2(str(source_path), str(out_path))

    # Open the copied file and modify in-place
    v = vsdx.VisioFile(str(out_path))

    # Collect all text shapes
    text_shapes = get_all_text_shapes(v)

    # --- Auto-update filename label shape ---
    fn_shape = _find_filename_label_shape(text_shapes, ctn, prod_cat)
    if fn_shape:
        ctn_num = ctn.replace("CTN", "")
        new_fn_text = f"CTN{ctn_num}-DTR{dtr_num:03d}-{prod_cat}.vsdx"
        fn_shape["shape"].text = new_fn_text
        print(f"  Updated filename label: '{fn_shape['text']}' -> '{new_fn_text}'")

    # --- Apply user-specified text updates ---
    if text_updates:
        # Build lookup by shape ID
        shape_by_id = {str(item["id"]): item for item in text_shapes}
        for shape_id, new_text in text_updates.items():
            if shape_id in shape_by_id:
                old_text = shape_by_id[shape_id]["text"]
                shape_by_id[shape_id]["shape"].text = new_text
                print(f"  Updated shape {shape_id}: '{old_text[:50]}' -> '{new_text[:50]}'")
            else:
                print(f"  WARNING: Shape ID {shape_id} not found — skipping")

    # Save modified .vsdx
    v.save_vsdx(str(out_path))
    print(f"\n  Saved: {out_path}")
    print(f"\n  NOTE: Open this file in Visio for any topology/connection edits,")
    print(f"        then export PNG manually.")


# ---------------------------------------------------------------------------
# Helpers for newd prompt sequence
# ---------------------------------------------------------------------------

def get_text_shape_summary(source_path) -> List[dict]:
    """Read a .vsdx and return a summary of all text shapes for prompt display.

    Returns list of dicts with keys: id, text, depth
    """
    v = vsdx.VisioFile(str(source_path))
    shapes = get_all_text_shapes(v)
    return [{"id": str(s["id"]), "text": s["text"], "depth": s["depth"]} for s in shapes]


def find_previous_draft(prod_cat: str, ctn: str, dtr_num: int) -> Optional[Path]:
    """Find the most recent draft .vsdx for DTR numbers less than dtr_num."""
    drafts_dir = system_diagram_dir(prod_cat, ctn) / "Drafts"
    if not drafts_dir.exists():
        return None
    # Look for any Draft_ .vsdx files with lower DTR numbers
    candidates = sorted(drafts_dir.glob("Draft_*.vsdx"), reverse=True)
    for c in candidates:
        # Extract DTR number from filename
        name = c.stem  # e.g. "Draft_CTN2026003 - DTR001 - SBC - System Diagram"
        for part in name.split(" - "):
            part = part.strip()
            if part.startswith("DTR") and part[3:].isdigit():
                found_dtr = int(part[3:])
                if found_dtr < dtr_num:
                    return c
    return None


# ---------------------------------------------------------------------------
# Seed profiles — add DTR001 profile per CTN when onboarding
# ---------------------------------------------------------------------------

# Structure mirrors other runners:
# { dtr_num (int): { cfg fields } }
# DTR002+ are never pre-baked — fully prompted at runtime.
SYSTEM_DIAGRAM_PROFILES: dict = {
    # "SBC/CTN2026003": { 1: { ... } },  # add when example docs are placed
}


def _get_profiles(prod_cat: str, ctn: str) -> dict:
    return SYSTEM_DIAGRAM_PROFILES.get(f"{prod_cat}/{ctn}", {})


# ---------------------------------------------------------------------------
# run() — callable entry point for newd prompt sequence dispatch
# ---------------------------------------------------------------------------

def run(prod_cat: str, ctn: str, dtr_num: int) -> None:
    """Callable entry point — invoked by the newd prompt sequence or directly via main()."""
    print("\n=== System Diagram — Parameterized Runner ===\n")
    print("STATUS: SKELETON — generation logic not yet implemented.")
    print("Place example .vsdx files in the System Diagram Examples & Templates folder to unblock.\n")

    profiles = _get_profiles(prod_cat, ctn)

    if dtr_num in profiles:
        cfg = dict(profiles[dtr_num])
        print(f"Loaded profile for {prod_cat}/{ctn} DTR{dtr_num:03d}:")
        print(f"  Version: {cfg.get('old_ver', '?')} → {cfg.get('new_ver', '?')}")
        confirm = input("\nProceed with these settings? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return
    else:
        print(f"No profile found for {prod_cat}/{ctn} DTR{dtr_num:03d}. Manual input required.")
        cfg = {
            "dtr_num": dtr_num,
            "new_ver": input("New IOS XE version (e.g. IOS XE 26.2): ").strip(),
            "old_ver": input("Old IOS XE version (e.g. IOS XE 17.18): ").strip(),
        }

    cfg["prod_cat"] = prod_cat
    cfg["ctn"] = ctn
    cfg["out_path"] = system_diagram_draft_path(prod_cat, ctn, dtr_num, cfg["new_ver"])

    try:
        raise NotImplementedError(
            "run_system_diagram.py is a SKELETON — generation logic not yet implemented. "
            "Place example .vsdx files in System Diagram Examples & Templates/ to unblock."
        )
    except NotImplementedError as e:
        print(f"\n[SKELETON] {e}")
        return  # Do not validate or log — no file was written

    print("\nRunning validate_doc.py...")
    run_validate(cfg["out_path"])

    engineer = input("\nEngineer username (for Draft Log): ").strip() or get_git_username() or "unknown"
    append_draft_log(
        engineer=engineer,
        action="Generated",
        ctn=ctn,
        doc_type="System Diagram",
        dtr=f"DTR{dtr_num:03d}",
        version=cfg["new_ver"],
        reason="Via run_system_diagram.py parameterized runner",
    )

    print("\nDone.")


# ---------------------------------------------------------------------------
# main() — thin wrapper for direct CLI use
# ---------------------------------------------------------------------------

def main():
    prod_cat = input("Product Category (e.g. SBC): ").strip()
    ctn = input("CTN (e.g. CTN2026003): ").strip()
    dtr_num = int(input("DTR Number (e.g. 1): ").strip())

    # Determine source
    if dtr_num == 1:
        source_path = system_diagram_initial_path(prod_cat, ctn)
        print(f"Source (INITIAL): {source_path}")
    else:
        prev = find_previous_draft(prod_cat, ctn, dtr_num)
        if prev:
            source_path = prev
            print(f"Source (previous draft): {source_path}")
        else:
            source_path = system_diagram_initial_path(prod_cat, ctn)
            print(f"Source (INITIAL, no previous draft found): {source_path}")

    out_path = system_diagram_draft_path(prod_cat, ctn, dtr_num)

    cfg = {
        "prod_cat": prod_cat,
        "ctn": ctn,
        "dtr_num": dtr_num,
        "source_path": source_path,
        "out_path": out_path,
    }

    generate(cfg)


if __name__ == "__main__":
    main()
