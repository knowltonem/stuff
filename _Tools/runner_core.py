#!/usr/bin/env python3
"""
runner_core.py — Shared utilities for all ICR parameterized runners.

Provides:
  - XML namespace helpers (qn, NSMAP)
  - Element manipulation helpers (clone_element, get_para_text, make_body_para,
    set_para_list_paragraph, make_spacer, _set_cell_text)
  - Paragraph-level XML helpers (set_run_text, set_para_single_run_text,
    set_label_value, find_para_by_label, find_para_after_label,
    set_run_font_size, set_all_runs_font_size, strip_highlighting)
  - Post-generation validation caller (run_validate)
  - Path helpers for all document types:
      FA: fa_dir, fa_draft_path, fa_initial_path, fa_example_path
      System Description: sysdesc_dir, sysdesc_draft_path, sysdesc_initial_path, sysdesc_example_path
      ICR Memo: memo_dir, memo_draft_path, memo_initial_path
      MUDG: mudg_dir, mudg_draft_path, mudg_example_path
      TDR: tdr_dir, tdr_template_path, tdr_draft_path
      CSR: csr_dir, csr_draft_path, csr_initial_path, csr_example_path
      LOC: loc_dir, loc_draft_path, loc_example_path
      POAM: poam_dir, poam_draft_path, poam_example_path
      System Diagram: system_diagram_dir, system_diagram_draft_path, system_diagram_example_path
  - Draft Log appender (append_draft_log)
  - normalize_month_abbr (shared month name normalizer)
  - get_git_username (shared git user.name helper)
"""

import copy
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from lxml import etree

# Project root — two levels up from _Tools/runner_core.py
BASE = Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# Namespace
# ---------------------------------------------------------------------------
NSMAP = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# Half-points value for 9pt font (OOXML w:sz uses half-points: 9pt × 2 = 18)
_CELL_FONT_SZ_HALF_PT = "18"


def qn(tag: str) -> str:
    """Expand a prefixed tag like 'w:p' to its Clark-notation equivalent."""
    prefix, local = tag.split(":")
    return f"{{{NSMAP[prefix]}}}{local}"


# ---------------------------------------------------------------------------
# Shared text helpers
# ---------------------------------------------------------------------------

def normalize_month_abbr(text: str) -> str:
    """Normalize full month names to 3-letter abbreviations (e.g. 'March 2026' → 'Mar 2026').
    Shared by run_sysdesc.py, run_mudg.py, and any other runner that touches revision history dates.
    """
    month_map = {
        "January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr",
        # "May" is omitted — full and abbreviated forms are identical
        "June": "Jun", "July": "Jul", "August": "Aug", "September": "Sep",
        "October": "Oct", "November": "Nov", "December": "Dec",
    }
    for full, abbr in month_map.items():
        text = text.replace(full, abbr)
    return text


# ---------------------------------------------------------------------------
# Element helpers
# ---------------------------------------------------------------------------

def clone_element(el):
    return copy.deepcopy(el)


def get_para_text(para_el) -> str:
    return "".join(t.text or "" for t in para_el.findall(f".//{qn('w:t')}"))


# ---------------------------------------------------------------------------
# Paragraph-level XML helpers (shared by TDR, POA&M, and similar runners)
# ---------------------------------------------------------------------------

def set_run_text(run_el, text: str):
    """Set the text of a single <w:r> element, preserving spacing."""
    t_els = run_el.findall(qn("w:t"))
    if t_els:
        t_els[0].text = text
        t_els[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        for extra in t_els[1:]:
            run_el.remove(extra)
    else:
        t_el = etree.SubElement(run_el, qn("w:t"))
        t_el.text = text
        t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


def set_para_single_run_text(para_el, text: str):
    """Overwrite all runs with a single run containing text."""
    runs = para_el.findall(f".//{qn('w:r')}")
    for i, r in enumerate(runs):
        if i == 0:
            set_run_text(r, text)
        else:
            r.getparent().remove(r)


def set_label_value(para_el, value: str):
    """Set value portion of a bold-label:  value paragraph.

    Preserves bold label in run 0; creates a new non-bold run for the value.
    """
    runs = para_el.findall(f".//{qn('w:r')}")
    if not runs:
        return

    full_text = "".join(
        "".join(t.text or "" for t in r.findall(qn("w:t"))) for r in runs
    )

    match = re.match(r"^(.*?:\s{0,2})", full_text)
    if match:
        label = match.group(1)
        if not label.endswith("  "):
            label = label.rstrip(":").rstrip() + ":  "
    else:
        label = (full_text.split(":")[0] + ":  ") if ":" in full_text else ""

    # Run 0 = bold label
    set_run_text(runs[0], label)
    rPr = runs[0].find(qn("w:rPr"))
    if rPr is None:
        rPr = etree.SubElement(runs[0], qn("w:rPr"))
        runs[0].insert(0, rPr)
    if rPr.find(qn("w:b")) is None:
        etree.SubElement(rPr, qn("w:b"))

    # Remove all remaining runs
    for r in runs[1:]:
        r.getparent().remove(r)

    # New non-bold value run
    value_run = copy.deepcopy(runs[0])
    val_rPr = value_run.find(qn("w:rPr"))
    if val_rPr is not None:
        val_b = val_rPr.find(qn("w:b"))
        if val_b is not None:
            val_rPr.remove(val_b)
        b_off = etree.SubElement(val_rPr, qn("w:b"))
        b_off.set(qn("w:val"), "0")
    set_run_text(value_run, value)
    runs[0].addnext(value_run)


def find_para_by_label(elements: list, label: str):
    """Find the first paragraph whose text contains *label*."""
    for el in elements:
        if el.tag == qn("w:p") and label in get_para_text(el):
            return el
    return None


def find_para_after_label(elements: list, label: str):
    """Return the first non-empty paragraph after the one containing *label*."""
    found = False
    for el in elements:
        if el.tag == qn("w:p"):
            text = get_para_text(el).strip()
            if found and text:
                return el
            if label in text:
                found = True
    return None


def set_run_font_size(run_el, size_pt: float):
    """Set font size (pt) on a single run element."""
    rPr = run_el.find(qn("w:rPr"))
    if rPr is None:
        rPr = etree.SubElement(run_el, qn("w:rPr"))
        run_el.insert(0, rPr)
    for tag in [qn("w:sz"), qn("w:szCs")]:
        el = rPr.find(tag)
        if el is None:
            el = etree.SubElement(rPr, tag)
        el.set(qn("w:val"), str(int(size_pt * 2)))


def set_all_runs_font_size(para_el, size_pt: float):
    """Set font size on every run in a paragraph."""
    for r in para_el.findall(f".//{qn('w:r')}"):
        set_run_font_size(r, size_pt)


def strip_highlighting(body):
    """Remove all run-level highlighting and shading from the document body."""
    for el in body.iter():
        if el.tag == qn("w:highlight"):
            parent = el.getparent()
            if parent is not None:
                parent.remove(el)
        if el.tag == qn("w:shd"):
            parent = el.getparent()
            if parent is not None and parent.tag == qn("w:rPr"):
                parent.remove(el)


def make_body_para(template_para_el, text: str):
    """Clone a body paragraph element and set its text in run 0 only."""
    new_p = clone_element(template_para_el)
    runs = new_p.findall(f".//{qn('w:r')}")
    if runs:
        for i, r in enumerate(runs):
            t_els = r.findall(qn("w:t"))
            if i == 0:
                if t_els:
                    t_els[0].text = text
                    t_els[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                else:
                    t_el = etree.SubElement(r, qn("w:t"))
                    t_el.text = text
                    t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                for extra_t in t_els[1:]:
                    r.remove(extra_t)
            else:
                r.getparent().remove(r)
    return new_p


def set_para_list_paragraph(para_el):
    """Set a paragraph to List Paragraph style, removing first_line_indent."""
    ppr = para_el.find(qn("w:pPr"))
    if ppr is None:
        ppr = etree.SubElement(para_el, qn("w:pPr"))
    ps = ppr.find(qn("w:pStyle"))
    if ps is None:
        ps = etree.SubElement(ppr, qn("w:pStyle"))
    ps.set(qn("w:val"), "ListParagraph")
    ind = ppr.find(qn("w:ind"))
    if ind is not None:
        if ind.get(qn("w:firstLine")):
            del ind.attrib[qn("w:firstLine")]


def make_spacer(template_el):
    """Clone an empty List Paragraph spacer, clearing text and explicit indents."""
    spacer = clone_element(template_el)
    for r in spacer.findall(f".//{qn('w:r')}"):
        r.getparent().remove(r)
    ind = spacer.find(f".//{qn('w:ind')}")
    if ind is not None:
        for attr in [qn("w:left"), qn("w:firstLine")]:
            if attr in ind.attrib:
                del ind.attrib[attr]
    return spacer


def _set_cell_text(cell_el, text: str):
    """Set text in a table cell XML element, creating a run if none exists.
    Ensures Times New Roman size 9 on newly created runs."""
    p = cell_el.find(qn("w:p"))
    if p is None:
        p = etree.SubElement(cell_el, qn("w:p"))
    runs = p.findall(qn("w:r"))
    if runs:
        t_els = runs[0].findall(qn("w:t"))
        if t_els:
            t_els[0].text = text
            t_els[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        else:
            t_el = etree.SubElement(runs[0], qn("w:t"))
            t_el.text = text
            t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        for extra_t in (t_els[1:] if t_els else []):
            runs[0].remove(extra_t)
        for extra_r in runs[1:]:
            p.remove(extra_r)
        # Ensure font is set on existing run
        rpr = runs[0].find(qn("w:rPr"))
        if rpr is None:
            rpr = etree.SubElement(runs[0], qn("w:rPr"))
            runs[0].insert(0, rpr)
        if rpr.find(qn("w:rFonts")) is None:
            rf = etree.SubElement(rpr, qn("w:rFonts"))
            rf.set(qn("w:ascii"), "Times New Roman")
            rf.set(qn("w:hAnsi"), "Times New Roman")
        if rpr.find(qn("w:sz")) is None:
            sz = etree.SubElement(rpr, qn("w:sz"))
            sz.set(qn("w:val"), _CELL_FONT_SZ_HALF_PT)  # 18 half-points = 9pt
        if rpr.find(qn("w:szCs")) is None:
            szcs = etree.SubElement(rpr, qn("w:szCs"))
            szcs.set(qn("w:val"), _CELL_FONT_SZ_HALF_PT)
    else:
        r = etree.SubElement(p, qn("w:r"))
        rpr = etree.SubElement(r, qn("w:rPr"))
        r.insert(0, rpr)
        rf = etree.SubElement(rpr, qn("w:rFonts"))
        rf.set(qn("w:ascii"), "Times New Roman")
        rf.set(qn("w:hAnsi"), "Times New Roman")
        sz = etree.SubElement(rpr, qn("w:sz"))
        sz.set(qn("w:val"), _CELL_FONT_SZ_HALF_PT)
        szcs = etree.SubElement(rpr, qn("w:szCs"))
        szcs.set(qn("w:val"), _CELL_FONT_SZ_HALF_PT)
        t_el = etree.SubElement(r, qn("w:t"))
        t_el.text = text
        t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


# ---------------------------------------------------------------------------
# Table NOTES row updater (shared across FA, SysDesc, ICR Memo)
# ---------------------------------------------------------------------------

def update_notes_row(table, notes_text: str) -> bool:
    """Find the NOTES row in a table and append a new numbered note paragraph.
    Clones an existing numbered note paragraph if one exists; otherwise clones
    the NOTE(S): header paragraph and adds numPr from the first numbered para
    found anywhere in the cell.
    Returns True if the NOTES row was found and updated."""
    tbl_el = table._tbl
    for row_el in reversed(tbl_el.findall(qn("w:tr"))):
        cells = row_el.findall(qn("w:tc"))
        for cell in cells:
            cell_text = "".join(
                t.text or "" for t in cell.findall(f".//{qn('w:t')}")
            ).strip()
            if cell_text.upper().startswith("NOTE"):
                paras = cell.findall(qn("w:p"))
                if not paras:
                    return True

                # Prefer to clone an existing numbered note paragraph (has numPr)
                numbered_para = None
                for p in paras:
                    ppr = p.find(qn("w:pPr"))
                    if ppr is not None and ppr.find(qn("w:numPr")) is not None:
                        numbered_para = p

                clone_src = numbered_para if numbered_para is not None else paras[-1]
                new_p = copy.deepcopy(clone_src)

                # If cloning the header (no numPr), add numPr from existing numbered para
                new_ppr = new_p.find(qn("w:pPr"))
                if new_ppr is not None and new_ppr.find(qn("w:numPr")) is None and numbered_para is not None:
                    src_ppr = numbered_para.find(qn("w:pPr"))
                    if src_ppr is not None:
                        src_numpr = src_ppr.find(qn("w:numPr"))
                        if src_numpr is not None:
                            new_ppr.append(copy.deepcopy(src_numpr))

                # Set text in first run, clear remaining runs
                runs = new_p.findall(qn("w:r"))
                if runs:
                    t_els = runs[0].findall(qn("w:t"))
                    if t_els:
                        t_els[0].text = notes_text
                        t_els[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                    else:
                        t_el = etree.SubElement(runs[0], qn("w:t"))
                        t_el.text = notes_text
                        t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                    # Remove bold from all runs
                    for r in runs:
                        rpr = r.find(qn("w:rPr"))
                        if rpr is not None:
                            for bold_tag in [qn("w:b"), qn("w:bCs")]:
                                b = rpr.find(bold_tag)
                                if b is not None:
                                    rpr.remove(b)
                    for r in runs[1:]:
                        for t in r.findall(qn("w:t")):
                            t.text = ""
                else:
                    # No runs — build one
                    new_r = etree.SubElement(new_p, qn("w:r"))
                    t_el = etree.SubElement(new_r, qn("w:t"))
                    t_el.text = notes_text
                    t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

                if new_ppr is not None:
                    spacing = new_ppr.find(qn("w:spacing"))
                    if spacing is not None:
                        spacing.set(qn("w:after"), "0")
                cell.append(new_p)
                return True
    raise ValueError(
        f"NOTES row not found in table — cannot append notes text: \"{notes_text}\". "
        "Check that the correct table index is being used."
    )


def find_notes_tables(doc) -> dict:
    """Scan all tables and return a dict mapping first-cell label to table index
    for every table whose last row starts with 'NOTE'.

    Example return: {'Network Interfaces': 3, 'Product Components': 5, 'CR/FR ID': 6}
    """
    notes_map = {}
    for ti, tbl in enumerate(doc.tables):
        tbl_el = tbl._tbl
        rows = tbl_el.findall(qn("w:tr"))
        if not rows:
            continue
        last_cell = rows[-1].findall(qn("w:tc"))
        if not last_cell:
            continue
        txt = "".join(
            t.text or "" for t in last_cell[0].findall(f".//{qn('w:t')}")
        ).strip()
        if txt.upper().startswith("NOTE"):
            label = tbl.rows[0].cells[0].text.strip()
            notes_map[label] = ti
    return notes_map


def apply_notes_by_label(doc, label: str, notes_text: str):
    """Find the table whose first-cell header matches `label` and has a NOTES row,
    then append notes_text. Raises ValueError if no matching table found."""
    nmap = find_notes_tables(doc)
    if label not in nmap:
        # Try partial match
        matches = [k for k in nmap if label.lower() in k.lower()]
        if len(matches) == 1:
            label = matches[0]
        else:
            raise ValueError(
                f"No NOTES table found matching \"{label}\". "
                f"Available NOTES tables: {list(nmap.keys())}"
            )
    update_notes_row(doc.tables[nmap[label]], notes_text)


# ---------------------------------------------------------------------------
# keepNext + page-break helpers
# ---------------------------------------------------------------------------

TABLE_TITLE_PREFIXES = [
    # Covers Tables 1–8 and the Acronym table used across current document types.
    # CSR has Tables 6–8 (CAT I, CAT II, CAT III STIG findings) — included here so
    # keepNext is applied and orphan table titles are prevented on page breaks.
    "Table 1.", "Table 2.", "Table 3.", "Table 4.", "Table 5.",
    "Table 6.", "Table 7.", "Table 8.", "List of Acronyms"
]


def apply_keep_next(body):
    """Set keepNext on all table title paragraphs and empty spacers between them and their tables."""
    for child in list(body):
        if child.tag.endswith("}p"):
            texts = [t.text or "" for t in child.findall(f".//{qn('w:t')}")]
            text = "".join(texts).strip()
            if any(text.startswith(pfx) for pfx in TABLE_TITLE_PREFIXES):
                pPr = child.find(qn("w:pPr"))
                if pPr is None:
                    pPr = etree.SubElement(child, qn("w:pPr"))
                    child.insert(0, pPr)
                if pPr.find(qn("w:keepNext")) is None:
                    etree.SubElement(pPr, qn("w:keepNext"))
                nxt = child.getnext()
                while nxt is not None and nxt.tag.endswith("}p"):
                    nxt_texts = [t.text or "" for t in nxt.findall(f".//{qn('w:t')}")]
                    if "".join(nxt_texts).strip():
                        break
                    nxt_pPr = nxt.find(qn("w:pPr"))
                    if nxt_pPr is None:
                        nxt_pPr = etree.SubElement(nxt, qn("w:pPr"))
                        nxt.insert(0, nxt_pPr)
                    if nxt_pPr.find(qn("w:keepNext")) is None:
                        etree.SubElement(nxt_pPr, qn("w:keepNext"))
                    nxt = nxt.getnext()


def apply_acronym_page_break(body):
    """Add pageBreakBefore to 'List of Acronyms' paragraph and remove empty spacers before it."""
    acronym_para = None
    for child in body:
        if child.tag.endswith("}p"):
            texts = [t.text or "" for t in child.findall(f".//{qn('w:t')}")]
            text = "".join(texts)
            if "List of Acronyms" in (text or ""):
                acronym_para = child
                pPr = child.find(qn("w:pPr"))
                if pPr is None:
                    pPr = etree.SubElement(child, qn("w:pPr"))
                    child.insert(0, pPr)
                pb = pPr.find(qn("w:pageBreakBefore"))
                if pb is None:
                    etree.SubElement(pPr, qn("w:pageBreakBefore"))
                break
    if acronym_para is not None:
        while True:
            prev = acronym_para.getprevious()
            if prev is None or not prev.tag.endswith("}p"):
                break
            prev_texts = [t.text or "" for t in prev.findall(f".//{qn('w:t')}")]
            if "".join(prev_texts).strip():
                break
            body.remove(prev)


def strip_acronym_cell_borders(doc):
    """Remove explicit cell borders from the Acronym List table.

    The INITIAL Acronym table has cell-level borders at sz=8 (1pt) which are
    thicker than the TableGrid style defaults (sz=4 / 0.5pt) used by all other
    tables.  Stripping them lets the table fall back to style defaults.
    """
    for tbl in doc.tables:
        if tbl.rows[0].cells[0].text.strip().startswith("Acronym"):
            for row in tbl._tbl.findall(qn("w:tr")):
                for cell in row.findall(qn("w:tc")):
                    tcPr = cell.find(qn("w:tcPr"))
                    if tcPr is not None:
                        tcBorders = tcPr.find(qn("w:tcBorders"))
                        if tcBorders is not None:
                            tcPr.remove(tcBorders)
            break


def merge_tables(doc, body, src_idx: int, dst_idx: int, skip_rows: int = 1, skip_header_rows: int = None):
    """Merge rows from dst table into src table, then remove dst table and any elements between them.

    Used by run_fa.py (CR/FR table merge) and run_csr.py (STIG table merge).
    Equivalent to the private _merge_tables() helpers that previously existed in both files.

    Args:
        doc:              python-docx Document object (provides doc.tables[])
        body:             doc.element.body (lxml element)
        src_idx:          table index to merge INTO
        dst_idx:          table index to merge FROM (rows appended to src; this table is removed)
        skip_rows:        number of header rows in dst to skip (default 1)
        skip_header_rows: alias for skip_rows — accepted for backward compatibility with run_csr.py callers
    """
    effective_skip = skip_header_rows if skip_header_rows is not None else skip_rows
    tbl_src = doc.tables[src_idx]._tbl
    tbl_dst = doc.tables[dst_idx]._tbl
    dst_rows = tbl_dst.findall(qn("w:tr"))
    for row in dst_rows[effective_skip:]:
        tbl_src.append(copy.deepcopy(row))
    found_src = False
    to_remove = []
    for el in list(body):
        if el is tbl_src:
            found_src = True
            continue
        if el is tbl_dst:
            to_remove.append(el)
            break
        if found_src:
            to_remove.append(el)
    for el in to_remove:
        body.remove(el)


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def fa_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/Functionality Attestation (FA)"


def fa_draft_path(prod_cat: str, ctn: str, dtr_num: int, version: str) -> Path:
    dtr_str = f"DTR{dtr_num:03d}"
    return fa_dir(prod_cat, ctn) / f"Drafts/Draft_{ctn} - {dtr_str} - {prod_cat} - {version} - Cisco Functionality Attestation.docx"


def fa_initial_path(prod_cat: str, ctn: str) -> Path:
    return fa_dir(prod_cat, ctn) / f"Examples & Templates/{ctn} - DTR000 - INITIAL - {prod_cat} - Cisco Functionality Attestation.docx"


def fa_example_path(prod_cat: str, ctn: str) -> Path:
    """Return the first Example_* .docx found in Examples & Templates/."""
    examples_dir = fa_dir(prod_cat, ctn) / "Examples & Templates"
    matches = sorted(examples_dir.glob("Example_*.docx"))
    if not matches:
        raise FileNotFoundError(f"No Example_*.docx found in {examples_dir}")
    return matches[0]


def sysdesc_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/System Description"


def sysdesc_draft_path(prod_cat: str, ctn: str, dtr_num: int, version: str) -> Path:
    dtr_str = f"DTR{dtr_num:03d}"
    return sysdesc_dir(prod_cat, ctn) / f"Drafts/Draft_{ctn} - {dtr_str} - {prod_cat} - {version} - Cisco ICR System Description.docx"


def sysdesc_initial_path(prod_cat: str, ctn: str) -> Path:
    return sysdesc_dir(prod_cat, ctn) / f"Examples & Templates/{ctn} - DTR000 - INITIAL - {prod_cat} - Cisco ICR System Description.docx"


def sysdesc_example_path(prod_cat: str, ctn: str) -> Path:
    """Return the first Example_* .docx found in Examples & Templates/."""
    examples_dir = sysdesc_dir(prod_cat, ctn) / "Examples & Templates"
    matches = sorted(examples_dir.glob("Example_*.docx"))
    if not matches:
        raise FileNotFoundError(f"No Example_*.docx found in {examples_dir}")
    return matches[0]


def memo_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/ICR Summary Memorandum (ICR Memo)"


def memo_draft_path(prod_cat: str, ctn: str, dtr_num: int, version: str) -> Path:
    dtr_str = f"DTR{dtr_num:03d}"
    ver_num = version.replace("IOS XE ", "")  # strip prefix if present
    return memo_dir(prod_cat, ctn) / f"Drafts/Draft_{ctn} - {dtr_str} - {prod_cat} - IOS XE {ver_num} - Cisco ICR Memo.docx"


def memo_initial_path(prod_cat: str, ctn: str) -> Path:
    return memo_dir(prod_cat, ctn) / f"Examples & Templates/{ctn} - DTR000 - INITIAL - {prod_cat} - Cisco ICR Memo.docx"


def mudg_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/Military Unique Deployment Guide (MUDG)"


def mudg_draft_path(prod_cat: str, ctn: str, dtr_num: int) -> Path:
    dtr_str = f"DTR{dtr_num:03d}"
    return mudg_dir(prod_cat, ctn) / f"Drafts/Draft_{ctn} - {dtr_str} - {prod_cat} - Military Unique Deployment Guide.docx"


def mudg_example_path(prod_cat: str, ctn: str) -> Path:
    """Return the first Example_* .docx found in Examples & Templates/."""
    examples_dir = mudg_dir(prod_cat, ctn) / "Examples & Templates"
    matches = sorted(examples_dir.glob("Example_*.docx"))
    if not matches:
        raise FileNotFoundError(f"No Example_*.docx found in {examples_dir}")
    return matches[0]


def tdr_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/Test Discrepancy Report (TDR)"


def tdr_template_path(prod_cat: str, ctn: str) -> Path:
    """Return the TDR template file."""
    d = tdr_dir(prod_cat, ctn)
    candidates = sorted(d.glob("Examples & Templates/Template_*.docx"))
    if not candidates:
        raise FileNotFoundError(f"No TDR template found in: {d / 'Examples & Templates'}")
    return candidates[0]


def tdr_draft_path(prod_cat: str, ctn: str, dtr_num: int, tdr_number: str,
                   prod_cat_abbr: str, version: str) -> Path:
    dtr_str = f"DTR{dtr_num:03d}"
    ver_num = version.replace("IOS XE ", "")
    return (tdr_dir(prod_cat, ctn) / "Drafts" /
            f"Draft_{ctn} - {dtr_str} - TDR{tdr_number} - {prod_cat_abbr} - IOS XE {ver_num} - Cisco ICR TDR.docx")


def csr_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/Cybersecurity Summary Report (CSR)"


def csr_draft_path(prod_cat: str, ctn: str, dtr_num: int, version: str) -> Path:
    ver_num = version.replace("IOS XE ", "")
    ctn_num = ctn.replace("CTN", "")
    fname = f"Draft_CTN{ctn_num} - DTR{dtr_num:03d} - {prod_cat} - IOS XE {ver_num} - Cisco ICR CSR.docx"
    return csr_dir(prod_cat, ctn) / "Drafts" / fname


def csr_initial_path(prod_cat: str, ctn: str) -> Path:
    d = csr_dir(prod_cat, ctn) / "Examples & Templates"
    candidates = sorted(d.glob("*INITIAL*.docx"))
    if not candidates:
        raise FileNotFoundError(f"No INITIAL CSR found in: {d}")
    return candidates[0]


def csr_example_path(prod_cat: str, ctn: str) -> Path:
    d = csr_dir(prod_cat, ctn) / "Examples & Templates"
    candidates = [p for p in sorted(d.glob("*.docx")) if "INITIAL" not in p.name and not p.name.startswith("Draft_")]
    if not candidates:
        raise FileNotFoundError(f"No example CSR found in: {d}")
    return candidates[0]


def loc_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/Letter Of Compliance (LoC)"


def loc_draft_path(prod_cat: str, ctn: str, dtr_num: int, version: str) -> Path:
    ver_num = version.replace("IOS XE ", "")
    ctn_num = ctn.replace("CTN", "")
    fname = f"Draft_CTN{ctn_num} - DTR{dtr_num:03d} - {prod_cat} - IOS XE {ver_num} - Cisco ICR LoC.docx"
    return loc_dir(prod_cat, ctn) / "Drafts" / fname


def loc_initial_path(prod_cat: str, ctn: str) -> Path:
    d = loc_dir(prod_cat, ctn) / "Examples & Templates"
    candidates = sorted(d.glob("*INITIAL*.docx"))
    if not candidates:
        raise FileNotFoundError(f"No INITIAL LoC found in: {d}")
    return candidates[0]


def loc_example_path(prod_cat: str, ctn: str) -> Path:
    d = loc_dir(prod_cat, ctn) / "Examples & Templates"
    candidates = [p for p in sorted(d.glob("*.docx")) if "INITIAL" not in p.name and not p.name.startswith("Draft_")]
    if not candidates:
        raise FileNotFoundError(f"No example LoC found in: {d}")
    return candidates[0]


def poam_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/Plan of Action & Milestone (POA&M)"


def poam_draft_path(prod_cat: str, ctn: str, dtr_num: int, tdr_number: str,
                    prod_cat_abbr: str, version: str) -> Path:
    """POA&M draft path — includes TDR number to match example filename pattern."""
    ver_num = version.replace("IOS XE ", "")
    dtr_str = f"DTR{dtr_num:03d}"
    return (poam_dir(prod_cat, ctn) / "Drafts" /
            f"Draft_{ctn} - {dtr_str} - TDR{tdr_number} - {prod_cat_abbr} - IOS XE {ver_num} - Cisco ICR POAM.docx")


def poam_template_path(prod_cat: str, ctn: str) -> Path:
    """Return the POA&M template file."""
    d = poam_dir(prod_cat, ctn)
    candidates = sorted(d.glob("Examples & Templates/Template_*.docx"))
    if not candidates:
        raise FileNotFoundError(f"No POA&M template found in: {d / 'Examples & Templates'}")
    return candidates[0]


def poam_initial_path(prod_cat: str, ctn: str) -> Path:
    d = poam_dir(prod_cat, ctn) / "Examples & Templates"
    candidates = sorted(d.glob("*INITIAL*.docx"))
    if not candidates:
        raise FileNotFoundError(f"No INITIAL POA&M found in: {d}")
    return candidates[0]


def poam_example_path(prod_cat: str, ctn: str) -> Path:
    d = poam_dir(prod_cat, ctn) / "Examples & Templates"
    candidates = [p for p in sorted(d.glob("*.docx")) if "INITIAL" not in p.name and not p.name.startswith("Draft_")]
    if not candidates:
        raise FileNotFoundError(f"No example POA&M found in: {d}")
    return candidates[0]


def system_diagram_dir(prod_cat: str, ctn: str) -> Path:
    return BASE / f"Product Category/{prod_cat}/{ctn}/System Diagram"


def system_diagram_draft_path(prod_cat: str, ctn: str, dtr_num: int, version: str = "") -> Path:
    """Draft path for System Diagram (.vsdx). Version is NOT included in filename."""
    ctn_num = ctn.replace("CTN", "")
    fname = f"Draft_CTN{ctn_num} - DTR{dtr_num:03d} - {prod_cat} - System Diagram.vsdx"
    return system_diagram_dir(prod_cat, ctn) / "Drafts" / fname


def system_diagram_initial_path(prod_cat: str, ctn: str) -> Path:
    d = system_diagram_dir(prod_cat, ctn) / "Examples & Templates"
    # Look for .vsdx first, fall back to .docx for legacy
    candidates = sorted(d.glob("*INITIAL*.vsdx"))
    if not candidates:
        candidates = sorted(d.glob("*INITIAL*.docx"))
    if not candidates:
        raise FileNotFoundError(f"No INITIAL System Diagram found in: {d}")
    return candidates[0]


def system_diagram_example_path(prod_cat: str, ctn: str) -> Path:
    d = system_diagram_dir(prod_cat, ctn) / "Examples & Templates"
    # Look for .vsdx first, fall back to .docx for legacy
    for ext in ("*.vsdx", "*.docx"):
        candidates = [p for p in sorted(d.glob(ext))
                      if "INITIAL" not in p.name
                      and not p.name.startswith("Draft_")
                      and not p.name.startswith("Template_")]
        if candidates:
            return candidates[0]
    raise FileNotFoundError(f"No example System Diagram found in: {d}")


# ---------------------------------------------------------------------------
# Final output path helpers (Final .docx + PDF — all document types)
# ---------------------------------------------------------------------------

def _final_stem(draft_path: Path) -> str:
    """Strip the 'Draft_' prefix from a draft filename to produce the final stem."""
    name = draft_path.stem  # filename without extension
    if name.startswith("Draft_"):
        return name[len("Draft_"):]
    return name


def final_dir(draft_path: Path) -> Path:
    """Return the Final/ subfolder path for a given draft path.

    Structure:
        <doc_type_folder>/Final/<final_stem>/
    e.g.
        System Description/Final/CTN2026003 - DTR001 - SBC - IOS XE 26.2 - Cisco ICR System Description/
    """
    doc_type_folder = draft_path.parent.parent  # up from Drafts/
    stem = _final_stem(draft_path)
    return doc_type_folder / "Final" / stem


def final_docx_path(draft_path: Path) -> Path:
    """Final .docx path derived from a draft path."""
    stem = _final_stem(draft_path)
    return final_dir(draft_path) / f"{stem}.docx"


def final_pdf_path(draft_path: Path) -> Path:
    """Final .pdf path derived from a draft path."""
    stem = _final_stem(draft_path)
    return final_dir(draft_path) / f"{stem}.pdf"


# ---------------------------------------------------------------------------
# Post-generation validation
# ---------------------------------------------------------------------------

def get_git_username() -> str:
    """Return the git config user.name for this repo, or empty string on failure."""
    result = subprocess.run(
        ["git", "config", "user.name"],
        capture_output=True, text=True, cwd=str(BASE)
    )
    return result.stdout.strip()


def run_validate(out_path: Path) -> bool:
    """Run validate_doc.py on the generated file. Returns True on PASS."""
    validate_script = Path(__file__).parent / "validate_doc.py"
    result = subprocess.run(
        [sys.executable, str(validate_script), str(out_path)],
        capture_output=False
    )
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Draft Log appender
# ---------------------------------------------------------------------------

RUNBOOK_PATH = BASE / "_Runbook/ICR_Automation_Runbook.md"
DRAFT_LOG_HEADER = "| Date | Engineer | Action | CTN | Doc Type | DTR | Version | Reason |"


def append_draft_log(engineer: str, action: str, ctn: str, doc_type: str,
                     dtr: str, version: str, reason: str):
    """Append a single row to the Draft Log in the runbook."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    row = f"| {date_str} | {engineer} | {action} | {ctn} | {doc_type} | {dtr} | {version} | {reason} |"

    content = RUNBOOK_PATH.read_text(encoding="utf-8")

    # Find the last pipe-delimited row in the Draft Log table and append after it.
    # Scan line-by-line from the separator row forward to find the last | row.
    lines = content.splitlines(keepends=True)
    header_line_idx = None
    for i, line in enumerate(lines):
        if DRAFT_LOG_HEADER in line:
            header_line_idx = i
            break
    if header_line_idx is None:
        print(f"WARNING: Draft Log header not found in runbook — row not appended.")
        return

    # Find separator row (|---|...) after header
    sep_line_idx = None
    for i in range(header_line_idx + 1, len(lines)):
        if lines[i].startswith("|---|") or lines[i].startswith("| --- |"):
            sep_line_idx = i
            break
    if sep_line_idx is None:
        print("WARNING: Draft Log separator row not found — row not appended.")
        return

    # Find the last pipe-row at or after the separator
    last_pipe_idx = sep_line_idx
    for i in range(sep_line_idx, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            last_pipe_idx = i
        elif stripped and not stripped.startswith("|"):
            # Hit a non-pipe, non-blank line — table has ended
            break

    # Insert new row immediately after the last pipe row
    lines.insert(last_pipe_idx + 1, row + "\n")
    new_content = "".join(lines)

    # Atomic write: write to a temp file in the same directory then replace,
    # so a crash mid-write never leaves the runbook in a partial state.
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=RUNBOOK_PATH.parent, prefix=".runbook_tmp_", suffix=".md"
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        os.replace(tmp_path, RUNBOOK_PATH)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    print(f"Draft Log: appended [{action}] {ctn} {doc_type} {dtr} {version}")
