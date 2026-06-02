#!/usr/bin/env python3
"""
run_icr_memo.py — Parameterized ICR Summary Memorandum runner.

Replaces all gen_dtr###_icr_memo*.py one-off scripts.
Invoked by the newd prompt sequence after Product Category, CTN, and Document Type
have been selected.

Usage (direct):
    python3 _Tools/run_icr_memo.py
"""

import copy
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from runner_core import (
    qn, get_para_text, run_validate, append_draft_log, BASE, get_git_username,
    memo_dir, memo_draft_path, memo_initial_path,
)

from lxml import etree
from docx import Document

# ---------------------------------------------------------------------------
# XML helpers (ICR Memo-specific)
# ---------------------------------------------------------------------------

def set_para_single_run_text(para_el, text: str):
    """Set text on run 0, remove all other runs."""
    runs = para_el.findall(f".//{qn('w:r')}")
    for i, r in enumerate(runs):
        if i == 0:
            t_els = r.findall(qn("w:t"))
            if t_els:
                t_els[0].text = text
                t_els[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                for extra in t_els[1:]:
                    r.remove(extra)
            else:
                t_el = etree.SubElement(r, qn("w:t"))
                t_el.text = text
                t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        else:
            r.getparent().remove(r)


def replace_version_across_runs(para_el, new_ver: str) -> bool:
    """Replace IOS XE version that may be split across multiple runs."""
    runs = para_el.findall(f".//{qn('w:r')}")
    if not runs:
        return False
    full_text = "".join(
        "".join(t.text or "" for t in r.findall(qn("w:t")))
        for r in runs
    )
    new_text = re.sub(r"XE\s+[\d.]+", f"XE {new_ver}", full_text)
    if new_text == full_text:
        return False
    for i, r in enumerate(runs):
        t_els = r.findall(qn("w:t"))
        if i == 0:
            if t_els:
                t_els[0].text = new_text
                t_els[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                for extra in t_els[1:]:
                    r.remove(extra)
            else:
                t_el = etree.SubElement(r, qn("w:t"))
                t_el.text = new_text
                t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        else:
            r.getparent().remove(r)
    return True


def update_doc_date(elements, doc_date: str):
    """Find the right-aligned date paragraph and update it."""
    for el in elements:
        if el.tag == qn("w:p"):
            text = get_para_text(el)
            if re.match(r"\d{1,2}\s+\w+\s+\d{4}", text.strip()):
                set_para_single_run_text(el, doc_date)
                pPr = el.find(qn("w:pPr"))
                if pPr is None:
                    pPr = etree.SubElement(el, qn("w:pPr"))
                    el.insert(0, pPr)
                jc = pPr.find(qn("w:jc"))
                if jc is None:
                    jc = etree.SubElement(pPr, qn("w:jc"))
                jc.set(qn("w:val"), "right")
                ind = pPr.find(qn("w:ind"))
                if ind is None:
                    ind = etree.SubElement(pPr, qn("w:ind"))
                ind.set(qn("w:right"), "194")
                return True
    return False


def build_dtr_approval_text(dtr_num: int, dtr_date: str, old_ver: str, new_ver: str,
                             component_list: str, platform_list: str) -> str:
    """Build the standard DTR approval paragraph text."""
    # Normalize both versions to always carry the full "IOS XE" prefix — prompts
    # may supply bare numbers (e.g. "26.5") or pre-prefixed strings ("IOS XE 26.5").
    # Guard against double-prefix by stripping and re-adding consistently.
    def _prefix(v):
        v = v.strip()
        return v if v.startswith("IOS XE") else f"IOS XE {v}"
    from_str = _prefix(old_ver)
    to_str   = _prefix(new_ver)
    return (
        f"On {dtr_date}, the following was approved via DTR #{dtr_num:03d} to update "
        f"the Software Rel. version from {from_str} to {to_str} for the "
        f"product components {component_list} on the "
        f"{platform_list} router platforms."
    )


def insert_dtr_paragraph(body, elements, dtr_num: int, dtr_text: str):
    """Insert a new DTR approval paragraph with spacers before the Implementation Notice."""
    # Find implementation notice anchor
    impl_el = None
    for el in elements:
        if el.tag == qn("w:p") and "This product/solution must be implemented" in get_para_text(el):
            impl_el = el
            break
    if impl_el is None:
        raise ValueError("Could not find Implementation Notice paragraph")

    # Find last existing DTR/initial approval paragraph as clone template
    last_approval_el = None
    for el in elements:
        if el.tag == qn("w:p"):
            text = get_para_text(el)
            if "was approved via DTR" in text or "initial request was approved" in text.lower():
                last_approval_el = el

    if last_approval_el is None:
        raise ValueError("Could not find any existing DTR/initial approval paragraph as template")

    # Build new paragraph
    new_para = copy.deepcopy(last_approval_el)
    set_para_single_run_text(new_para, dtr_text)

    # DTR001: also clean up empty paragraphs between initial approval and impl notice
    if dtr_num == 1:
        el = last_approval_el.getnext()
        while el is not None and el is not impl_el:
            next_el = el.getnext()
            if el.tag == qn("w:p") and not get_para_text(el).strip():
                el.getparent().remove(el)
            el = next_el
        # Spacer after initial approval
        spacer1 = copy.deepcopy(last_approval_el)
        set_para_single_run_text(spacer1, "")
        last_approval_el.addnext(spacer1)
    else:
        # DTR002+: spacer after last DTR paragraph
        spacer1 = copy.deepcopy(last_approval_el)
        set_para_single_run_text(spacer1, "")
        last_approval_el.addnext(spacer1)

    # Insert new DTR paragraph before impl notice
    impl_el.addprevious(new_para)

    # Spacer after new DTR paragraph (before impl notice)
    spacer2 = copy.deepcopy(last_approval_el)
    set_para_single_run_text(spacer2, "")
    impl_el.addprevious(spacer2)


# ---------------------------------------------------------------------------
# Generation entry point
# ---------------------------------------------------------------------------

def generate(cfg: dict):
    prod_cat = cfg["prod_cat"]
    ctn = cfg["ctn"]
    dtr_num = cfg["dtr_num"]
    new_ver = cfg["new_ver"]
    out_path = cfg["out_path"]
    doc_date = datetime.now().strftime("%d %B %Y")

    if dtr_num == 1:
        source_path = memo_initial_path(prod_cat, ctn)
    else:
        source_path = cfg["source_path"]

    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source_path}")

    doc = Document(str(source_path))
    body = doc.element.body
    elements = list(body)

    # 1. Update document date
    update_doc_date(elements, doc_date)

    # 2. Subject line — strip any version (keep it clean, matching INITIAL format)
    for el in elements:
        if el.tag == qn("w:p") and "SUBJECT:" in get_para_text(el):
            text = get_para_text(el)
            stripped = re.sub(
                r"\s+with\s+Software\s+Rel(?:ease)?\s*\(Rel\.\)\s+IOS\s+XE\s+[\d.]+",
                "", text
            )
            if stripped != text:
                set_para_single_run_text(el, stripped)
            break

    # 3. Approval summary paragraph — update version
    for el in elements:
        if el.tag == qn("w:p"):
            text = get_para_text(el)
            if ("GCT DP team has completed approval" in text
                    or ("GCT DP" in text and "has been approved" in text)):
                replace_version_across_runs(el, new_ver)
                break

    # 4. Insert new DTR approval paragraph
    dtr_text = build_dtr_approval_text(
        dtr_num, cfg["dtr_date"], cfg["old_ver"], new_ver,
        cfg["component_list"], cfg["platform_list"]
    )
    insert_dtr_paragraph(body, elements, dtr_num, dtr_text)

    # 5. Save
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        resp = input(f"WARNING: {out_path.name} already exists. Overwrite? [y/N] ").strip().lower()
        if resp != "y":
            print("Aborted — file not overwritten.")
            return
    doc.save(str(out_path))
    print(f"Saved: {out_path}")


# ---------------------------------------------------------------------------
# Profiles — DTR001 seed only; DTR002+ are fully prompted at runtime
# ---------------------------------------------------------------------------

SBC_CTN2026003_MEMO_PROFILES = {
    # DTR001 seed profile — first-production version for SBC/CTN2026003.
    # CONFIRM new_ver, old_ver, and dtr_date (DTR approval date, not generation date) before generating.
    # This profile is presented to the engineer with a y/N confirm prompt before use.
    1: {
        "dtr_num": 1,
        # new_ver and old_ver use the full "IOS XE X.Y" prefix — consistent with all other runners.
        # build_dtr_approval_text() and memo_draft_path() both handle the prefix safely.
        # ICR Memo and System Description are tracked independently — confirm this version
        # is the intended Memo DTR001 version before generating.
        "new_ver": "IOS XE 26.2",
        "old_ver": "IOS XE 17.18",
        "dtr_date": "22 May 2026",
        "component_list": "IWBC, IWG, and SBC",
        "platform_list": (
            "ASR 1006-X, ISR 4461/K9, Cisco Catalyst 8300 Series, "
            "Cisco Catalyst 8200 Series, and Cisco Catalyst 8000v Series"
        ),
    },
    # DTR002+ have no pre-baked profiles — prompted at runtime.
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(prod_cat: str, ctn: str, dtr_num: int) -> None:
    """Callable entry point — invoked by the newd prompt sequence or directly via main()."""
    profiles = {}
    if prod_cat == "SBC" and ctn == "CTN2026003":
        profiles = SBC_CTN2026003_MEMO_PROFILES

    if dtr_num in profiles:
        cfg = dict(profiles[dtr_num])
        print(f"\nLoaded profile for {prod_cat}/{ctn} DTR{dtr_num:03d}:")
        print(f"  Version: {cfg['old_ver']} → {cfg['new_ver']}")
        print(f"  DTR date: {cfg['dtr_date']}")
        confirm = input("\nProceed with these settings? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return
    else:
        print(f"\nNo profile found for {prod_cat}/{ctn} DTR{dtr_num:03d}. Manual input required.")
        cfg = {
            "dtr_num": dtr_num,
            "new_ver": input("New version number (e.g. 26.5): ").strip(),
            "old_ver": input("Old version number (e.g. 26.2): ").strip(),
            "dtr_date": input("DTR approval date (e.g. 25 May 2026): ").strip(),
            "component_list": input("Component list (e.g. IWBC, IWG, and SBC): ").strip(),
            "platform_list": input("Platform list: ").strip(),
        }

    cfg["prod_cat"] = prod_cat
    cfg["ctn"] = ctn
    cfg["out_path"] = memo_draft_path(prod_cat, ctn, dtr_num, cfg["new_ver"])

    if dtr_num > 1:
        prev_ver = cfg["old_ver"]
        cfg["source_path"] = memo_draft_path(prod_cat, ctn, dtr_num - 1, prev_ver)

    generate(cfg)

    print("\nRunning validate_doc.py...")
    run_validate(cfg["out_path"])

    engineer = input("\nEngineer username (for Draft Log): ").strip() or get_git_username() or "unknown"
    append_draft_log(
        engineer=engineer,
        action="Generated",
        ctn=ctn,
        doc_type="ICR Memo",
        dtr=f"DTR{dtr_num:03d}",
        version=cfg['new_ver'] if cfg['new_ver'].startswith("IOS XE") else f"IOS XE {cfg['new_ver']}",
        reason="Via run_icr_memo.py parameterized runner",
    )

    print("\nDone.")


def main():
    print("\n=== ICR Summary Memorandum — Parameterized Runner ===\n")
    prod_cat = input("Product Category (e.g. SBC): ").strip()
    ctn = input("CTN (e.g. CTN2026003): ").strip()
    dtr_num = int(input("DTR Number (e.g. 1): ").strip())
    run(prod_cat, ctn, dtr_num)


if __name__ == "__main__":
    main()
