# ICR Automation — Skill: System Diagram
> Load `skill_base.md` first. This file defines rules specific to the **System Diagram** document type only.

---

## Document Identity
- **Full Name:** Cisco ICR System Diagram
- **Abbreviation:** —
- **Folder:** `System Diagram/`
- **File Format:** Microsoft Visio (`.vsdx`) — NOT Word (`.docx`)
- **Filename Pattern (INITIAL):** `CTN{ctn_num} - DTR000 - INITIAL - {prod_cat} - System Diagram.vsdx`
- **Filename Pattern (Draft):** `Draft_CTN{ctn_num} - DTR{dtr:03d} - {prod_cat} - System Diagram.vsdx`
- **Filename Pattern (Final):** `CTN{ctn_num} - DTR{dtr:03d} - {prod_cat} - System Diagram.vsdx`

> Note: System Diagram filenames do NOT include the IOS XE version (similar to MUDG).

---

## Purpose
The System Diagram provides a visual and descriptive representation of the system architecture, network topology, and component relationships for the product under review. It is a standalone Visio file that engineers edit directly in Visio, then export as PNG for insertion into other ICR documents (e.g., System Description).

---

## File Format & Tooling
- **Source format:** `.vsdx` (Microsoft Visio)
- **Python library:** `vsdx` (python-vsdx) — reads and modifies `.vsdx` XML structure
- **PNG export:** Manual — engineer opens the generated `.vsdx` in Visio and exports PNG
- **No Word doc wrapper** — the System Diagram is the Visio file itself

---

## Document Structure (from INITIAL analysis)
Single-page Visio diagram (`Page-1`) with ~29 top-level shapes including:

### Metadata / Label Shapes (auto-updatable)
| Shape ID | Current Text (INITIAL) | Purpose | Auto-update? |
|---|---|---|---|
| 3 | `Cisco SBC23` | Product name | Yes — per product |
| 4 | `CTN2026003-DTR000-SBC.vsdx` | Filename label | Yes — per DTR |
| 8 | `SBC` | Product category abbreviation | Yes — per product |
| 18 | `The combined SBC and IWG allows...` | Description note | Prompted |

### Network Topology Shapes (prompted for changes)
- ASLAN, UC Network, Management Workstation, Windows Workstation
- Certified Cisco SC, Certified Ribbon SC
- RAE section: Secure NTP1, Secure NTP2, SYSLOG, Active Directory, Cisco ISE
- Router shapes: 3945/K9, IWBC, SBC labels
- Connection lines (no text)

---

## Generation Workflow

### DTR001 (from INITIAL)
1. Copy INITIAL `.vsdx` to `Drafts/` with DTR001 filename
2. Auto-update filename label shape (ID 4) → `CTN{ctn_num}-DTR001-{prod_cat}.vsdx`
3. Prompt engineer to review/update each text shape (show current value, accept or enter new)
4. Save modified `.vsdx` to Drafts
5. Engineer opens in Visio for any topology changes, then exports PNG manually

### DTR002+ (incremental)
1. Copy previous DTR draft `.vsdx` to `Drafts/` with new DTR number
2. Auto-update filename label shape
3. Prompt engineer to review/update text shapes
4. Save modified `.vsdx`
5. Engineer edits in Visio + exports PNG manually

---

## Prompt Sequence (during `newd` flow)
After product category, CTN, and DTR number are selected:

1. **Version prompt** — New IOS XE version (for metadata/tracking only — not in filename)
2. **Text field review** — For each text-containing shape in the Visio:
   - Show shape ID, current text value
   - Options: **Keep as-is** or **Enter new value**
   - Group shapes into: Metadata (auto-updated, confirm only) and Topology (prompted individually)
3. **Topology changes note** — Remind engineer: "Open the generated .vsdx in Visio for any topology/connection changes, then export PNG"

---

## Finalization
- No PDF conversion (Visio files are not converted to PDF via the standard pipeline)
- No signature field injection
- Engineer manually exports PNG from Visio when editing is complete
- Final version: copy from Drafts to Final folder (strip `Draft_` prefix)

---

## Generation Status
- [x] Example/Template file placed in `Examples & Templates/`
- [x] Shape structure documented
- [x] Text fields identified and mapped
- [x] Runner file exists (`run_system_diagram.py` — SKELETON)
- [ ] Runner fully implemented and tested
- [ ] First draft generated and validated
- [ ] Skill file finalized with confirmed rules
