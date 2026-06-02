# ICR Automation — Skill: Cybersecurity Summary Report (CSR)
> Load `skill_base.md` first. This file defines rules specific to the **Cybersecurity Summary Report (CSR)** document type only.

---

## Document Identity
- **Full Name:** Cisco ICR Cybersecurity Summary Report
- **Abbreviation:** CSR
- **Folder:** `Cybersecurity Summary Report (CSR)/`
- **Filename Suffix:** `Cisco ICR CSR.docx`

---

## Purpose
The CSR documents the cybersecurity posture of the product under review. It summarizes STIG compliance findings, IP vulnerability scan results, Conditions of Fielding (CoF) mitigations, and system configurations for the software version being certified.

---

## Generation Status
> **Note:** `run_csr.py` is marked ✅ COMPLETE in the Script Inventory — the runner script can execute. However, the skill documentation below is not yet fully verified from a real generated draft. The two unchecked items below reflect skill doc status, not runner status.
- [x] Example/Template file placed in `Examples & Templates/`
- [x] Table structure documented
- [x] Paragraph patterns documented
- [x] First draft generated and validated
- [ ] Skill file updated with confirmed rules

---

## Document Structure Overview

The CSR has a **Revision History table** (Table 0) and is organized into clearly labeled sections with numbered tables throughout.

### Paragraph Sections (in document order)
| # | Section | Style | Notes |
|---|---|---|---|
| 1 | Title page | Normal | `CYBERSECURITY SUMMARY REPORT (CSR)` + boilerplate |
| 2 | SYSTEM TITLE | Default | Contains product name and software version (e.g. `IOS XE 17.18`) |
| 3 | SUMMARY | Default | References Tables 1a, 1b; describes testing scope |
| 4 | Table 1a. CS Test Summary | — | Component findings W/O-RAE vs W-RAE |
| 5 | Table 1b. IP Vulnerability Test Summary | — | IPV test date + findings |
| 6 | Table 1c. CMVP Status Summary | — | **INITIAL only** — FIPS 140 module status |
| 7 | SYSTEM DESCRIPTION | List Paragraph | General, Management, Components Under Test |
| 8 | Figure 1 (SUT Test Configuration) | Caption | Diagram image |
| 9 | Component descriptions | annotation text / Normal | One paragraph per component |
| 10 | OPERATIONAL ARCHITECTURE | List Paragraph | DoDIN hierarchy description |
| 11 | CYBERSECURITY REQUIREMENTS | Title | Introduces Desktop Review Table |
| 12 | Table 2. Desktop Review Table | — | DTR history with request dates, descriptions, results |
| 13 | Table 3. IP Vulnerability Summary | — | Per-component IPV findings |
| 14 | SYSTEM CONFIGURATIONS | List Paragraph | Introduces Table 4 |
| 15 | Table 4. SUT HW/SW/FW Version ID | — | Full system configuration |
| 16 | TESTING LIMITATIONS | List Paragraph | Usually `None.` |
| 17 | CONDITION OF FIELDING (CoF) | List Paragraph | Introduces Table 5 findings count |
| 18 | Table 5. STIG CS Requirements Summary and CoF Mitigations | Title | Split across 2 tables |
| 19 | CoF site requirements (bullet list) | List Paragraph | 10 numbered requirements — **static, do not modify per DTR** |
| 20 | TEST RESULTS AND CS FINDINGS | List Paragraph | Phase I STIG + Phase II IPV |
| 21 | STIG Findings (Phase I) | List Paragraph / Normal | Per-STIG CAT I/II/III findings |
| 22 | IPV Findings (Phase II) | List Paragraph | High/Medium/Low impact definitions |
| 23 | Table 6. Internal Findings | — | IP addresses and scan results |
| 24 | Table 8. Open Ports | — | Components, ports, FW rules |
| 25 | APPENDIX A | Normal | SAR Scorecard explanation (static) |
| 26 | APPENDIX B. Acronym List | Normal | Static acronym table |

---

## Table Map (SBC — CTN2026003)

### INITIAL Document (13 tables)

| Table Index | Table Label | Rows × Cols | Content |
|---|---|---|---|
| 0 | Revision History | 2 × 3 | Version / Date / Change Description |
| 1 | Table 1a. CS Test Summary | 4 × 4 | Component / Critical / W/O-RAE / W-RAE |
| 2 | Table 1b. IP Vulnerability Test Summary | 3 × 3 | Requirement / Date / Total Findings |
| 3 | Table 1c. CMVP Status Summary | 8 × 5 | CMVP# / Module Name / Components / Status / Sunset Date |
| 4 | Table 2. Desktop Review Table | 2 × 4 | Request Date / DTR Number / Description / Results |
| 5 | Table 3. IP Vulnerability Summary | 4 × 5 | Component / Critical / Plug-in ID / Findings / Total |
| 6 | Table 4. SUT HW/SW/FW Version ID | 11 × 5 | System Name / HW-SW Release (merged cols) |
| 7 | Table 4. (Product Components) | 8 × 5 | Product Component / Hardware / Card Name / SW FW / Similarity |
| 8 | Table 5. STIG CoF (part 1) | 13 × 6 | Requirement / CoF SRGs / CAT / Component / W/O-RAE / W-RAE |
| 9 | Table 5. STIG CoF (part 2) | 27 × 6 | Continuation |
| 10 | Table 6. Internal Findings | 6 × 3 | IP Addresses |
| 11 | Table 8. Open Ports | 9 × 5 | Components / Open Ports / Enterprise FW / Port Purpose |
| 12 | Acronym List | 35 × 2 | Static |

### Example DTR001 Document (11 tables)

| Table Index | Table Label | Rows × Cols | Content |
|---|---|---|---|
| 0 | Revision History | 6 × 3 | Version / Date / Change Description (5 entries) |
| 1 | Table 1a. CS Test Summary | 4 × 4 | Component / Critical / W/O-RAE / W-RAE |
| 2 | Table 1b. IP Vulnerability Test Summary | 3 × 3 | Requirement / Date / Total Findings |
| 3 | Table 2. Desktop Review Table | 4 × 5 | Request Date / DTR# / Description / Results / Concurrence |
| 4 | Table 3. IP Vulnerability Summary | 4 × 5 | Component / Critical / Plug-in ID / Findings / Total |
| 5 | Table 4. SUT HW/SW/FW Version ID | 25 × 5 | System Name / HW-SW Release (merged cols) |
| 6 | Table 5. STIG CoF (part 1) | 34 × 5 | Requirement / CoF SRGs / Component / W/O-RAE / W-RAE |
| 7 | Table 5. STIG CoF (part 2) | 6 × 5 | Continuation + NOTES row |
| 8 | Table 6. Internal Findings | 7 × 4 | IP Addresses |
| 9 | Table 8. Open Ports | 9 × 5 | Components / Open Ports / Enterprise FW / Port Purpose |
| 10 | Acronym List | 35 × 2 | Static |

---

## Key Differences (INITIAL → DTR001+)

| Aspect | INITIAL | DTR001+ |
|---|---|---|
| Revision History (Table 0) | 2 rows (header + initial) | Grows — 1 row per revision |
| Table 1c (CMVP) | Present (8 × 5) | **Removed** |
| Desktop Review Table | 4 cols (no Concurrence) | 5 cols (adds Concurrence) |
| Table 4 (SUT HW/SW) | Split into 2 tables (6+7) | Merged into single table |
| Table 5 (STIG CoF) | 6 cols (includes CAT column) | 5 cols (CAT column removed) |
| Table 6 (Internal Findings) | 3 cols | 4 cols |
| Component naming | `IWBC` / `Combined SBC/IWG Combined (IWBC)` | `Combined SBC/IWG` |

---

## What Gets Updated Per DTR

### 1. Revision History (Table 0)
- Add new row: Version (auto-increment), Date (**"Month YYYY"** format, e.g. `May 2026` — auto-applied from current date), Change Description (`Update for DTR [N]`)
- Follow `skill_base.md` revision history rules

### 2. SYSTEM TITLE Paragraph
- Update software version reference (e.g. `IOS XE 17.18` → `IOS XE 26.5`)
- Located at P34 (INITIAL) / P29 (Example)

### 3. Desktop Review Table (Table 2)
- Add new row with each DTR:
  - **Request Date** — prompted from engineer
  - **DTR Number** — `DTR [N]`
  - **Description** — DTR statement (prompted from engineer — what was requested)
  - **Results of Testing** — prompted from engineer
  - **Concurrence** — prompted from engineer (e.g. `Tester: N. Richards`)
- INITIAL has 4 columns; DTR001+ has 5 columns (adds Concurrence)
  - For DTR001 from INITIAL: always add the Concurrence column to the table

### 4. Table 4. SUT HW/SW/FW Version Identification
- Update software versions for components that were updated in this DTR
- May add new rows for new hardware/software components
- **INITIAL has this split across 2 tables (indices 6+7)** — DTR001 merges them

### 5. Table 5. STIG CoF (if findings change)
- Generally static — only update if new findings are identified or mitigated
- **INITIAL has 6 columns; DTR001+ has 5 columns (CAT column removed)**
- INITIAL split across 2 tables (indices 8+9) — DTR001 keeps as 2 tables

### 6. Table 1a. CS Test Summary
- **Auto-calculated from Table 5** — do not prompt the engineer for these values
- W/O-RAE and W-RAE finding counts per component are derived by summing Table 5 (both parts)
- Must recalculate whenever Table 5 changes
- Total Findings row = sum of component rows
- **Formatting:** Each CAT level (I, II, III) must be a **separate paragraph** in the cell — not `\n` in a single paragraph. This ensures they stack vertically in Word.

### 7. Table 3. IP Vulnerability Summary (if IPV results change)
- Update findings per component

### 8. STIG Findings Section (Phase I)
- Update per-STIG CAT I/II/III findings text
- Format: `CAT I: None.` or list specific findings with TDR ID and POAM ID

### 9. CMVP Table (Table 1c — DTR001 from INITIAL only)
- **Remove this table** when generating DTR001 from INITIAL
- Not present in DTR001+ documents

### 10. CoF Findings Count
- Update the number in the CONDITION OF FIELDING paragraph (e.g. `The 70 findings shown below...`)
- This number = sum of all W-RAE column values across Table 5 (both parts)
- **Dedup rule:** Table 5 is split across 2 tables (part 1 + part 2). Count rows from BOTH tables but do NOT double-count — each row appears in only one part
- The NOTES row at the bottom of Table 5 part 2 is NOT a finding — exclude it from the count
- Must match actual Table 5 data — recalculate from the table, never hardcode

---

## DTR001 from INITIAL — Special Rules

When building DTR001 from a `DTR000 - INITIAL` document:
- **Remove Table 1c (CMVP)** — not present in DTR001+ docs
- **Add Concurrence column** to Desktop Review Table (Table 2 after CMVP removal shifts indices)
- **Remove CAT column** from Table 5 (STIG CoF) — DTR001+ uses 5 cols instead of 6
- **Merge Table 4** (INITIAL tables 6+7) into single table
- **Rename `IWBC`** → `Combined SBC/IWG` in component references
- **Rename `Combined SBC/IWG Combined (IWBC)`** → `Combined SBC/IWG` in System Description
- Table index shifts after CMVP removal — recalculate all references

### Post-Generation Table Indices (DTR001+)
0=RevHistory, 1=CSTestSummary, 2=IPVulnTestSummary, 3=DesktopReview, 4=IPVulnSummary, 5=SUTHWSW(SystemName), 6=SUTHWSW(ProductComponent), 7=STIGCoF(merged), 8=InternalFindings, 9=OpenPorts, 10=Acronym

---

## Platform Map (SBC — CTN2026003)

| Platform | INITIAL Naming | DTR001+ Naming |
|---|---|---|
| SBC | SBC | Cisco SBC |
| Combined SBC/IWG | Combined SBC/IWG Combined (IWBC) | Combined SBC/IWG |

---

## CSR-Specific Prompt Sequence (Steps 4+ after base steps 1–3)

4. **New software version** — what version is being certified?
5. **Desktop Review Table entry:**
   - **Request Date?** — free text (e.g. `20 August 2024`)
    - **Description** — auto-generated using the same format as the FA DTR body paragraph, placed in the Description cell:
      - `DTR [N] was requested to update the IOS XE software version from [FROM] to [TO] for the IWG/SBC on [hw list] of router platforms.`
      - **5b**: Multi-select which platforms are updating → selected = updating, unselected = sustained. Read platform list live from the existing platforms in the source document.
      - **5c**: For each platform NOT selected in 5b (sustained), ask what version it is sustained on. Do NOT ask "any sustained platforms?" — unselected from 5b are automatically sustained.
      - New platform variant: `DTR [N] was requested to add the IOS XE software on [hw list] of router platforms. The IOS XE software version is [TO].`
      - Sustained platforms get a separate line appended to the description: `The [Platform] will be sustained on the current software load of [version].`
   - **Similarity statement?** — Yes / No (follow `skill_base.md` shared rules). If Yes, appended to Description cell on a new line.
   - **POA&M inline statement?** — Yes / No (follow `skill_base.md` shared rules). If Yes, appended to Description cell on a new line.
   - **Results of Testing?** — free text (e.g. `Testing was successful.`, `No testing required.`)
   - **Concurrence?** — free text (e.g. `Tester: N. Richards`)
6. **Table 4 (SUT HW/SW) updates?**
   - **6a. Updating versions** — Multi-select which existing platforms are updating. For each selected platform: prompt new version. Unselected platforms retain their current version.
   - **6b. New platforms** — Are any new hardware platforms being added to Table 4? Yes / No.
     - If Yes: for each new platform, collect:
       - **Hardware** — hardware model name (e.g. `C8500-12X`)
       - **Card Name / Part Number** — or `NA`
       - **Software Version** — defaults to new version if IOS XE; otherwise prompt
       - **Hardware certified by Similarity** — model name or `NA`
       - **Components** — multi-select: `SBC`, `IWBC`, `IWG` — one row inserted per selected component, grouped with existing rows for that component in Table 4
7. **STIG findings changed (Phase I)?** — Yes / No
   - If Yes: **Which section(s) need updating?** — Multi-select from:
     - Network Device Management SRG
     - Network Infrastructure Policy STIG
     - VMware vSphere 7.0 VM STIG
     - Voice/Video over Internet Protocol (VVoIP) STIG
     - Voice Video Session Management SRG
     - Voice Video Services Policy Security STIG
   - For each selected section: prompt for updated CAT I, CAT II, CAT III values
8. **IPV findings changed?** — Yes / No (only when a new scan was conducted — not every DTR)
   - If Yes:
     - **Scan date?** — free text (e.g. `26 May 2026`)
     - **Which risk levels have findings?** — multi-select: `High Risk`, `Medium Risk`, `Low Risk`
     - For each selected risk level: **How many [High/Medium/Low] Risk findings?** — enter count
     - Unselected risk levels default to "No [Level] Risk"
     - Updates Table 1b (date + findings text) and Table 3 (per-component + total)
9. **Open Ports (Table 8) update?** — Yes / No
   - If Yes: **Add or remove?** — multi-select: `Add port(s)`, `Remove port(s)`
     - If Add: prompt for Component, Port number, Enterprise FW rule
       - **Port Purpose**: auto-fetched from Cisco's port usage guide for the specific software version being tested (e.g. IOS XE 17.18 port usage guide on cisco.com). Present the fetched purpose to the engineer for confirmation before inserting. If the auto-fetch fails or the page is unavailable, prompt the engineer to enter the port purpose manually.
     - If Remove: list existing ports, multi-select which to remove

> **Steps 4–9 complete the generation.** The draft is generated in a single pass.

---

## Post-Generation Steps (Required Every Time)

After `doc.save(OUT)`, always run the validator:

```python
import subprocess
result = subprocess.run(
    ["python3", "_Tools/validate_doc.py", OUT],
    capture_output=True, text=True
)
print(result.stdout)
```

---

## Table Header Repeat Rules

All multi-row tables must have `tblHeader` set on their header row(s) so column headers repeat on page breaks:

| Table | Header Row(s) |
|---|---|
| Table 0 (Revision History) | Row 0 |
| Table 1a (CS Test Summary) | Row 0 |
| Table 1b (IP Vulnerability Test Summary) | Row 0 |
| Table 2 (Desktop Review) | Row 0 |
| Table 3 (IP Vulnerability Summary) | Row 0 |
| Table 4 (SUT HW/SW/FW) | **No tblHeader** — continuous single table, header does not repeat on page breaks. Do NOT split into two tables. |
| Table 5 (STIG CoF part 1) | Row 0 |
| Table 5 (STIG CoF part 2) | Row 0 |
| Table 6 (Internal Findings) | Row 0 |
| Table 8 (Open Ports) | Row 0 |
| Acronym List | Row 0 |

- Set `tblHeader` on header rows during DTR001 generation from INITIAL
- For DTR002+, verify headers are already set — only add if missing

---

## Known Issues

| # | Issue | Resolution |
|---|---|---|
| 1 | ~~INITIAL has CMVP table (Table 1c) not present in DTR001+~~ | ~~Remove during DTR001 generation~~ Table 1c is now **retained** in DTR001+ |
| 2 | INITIAL Desktop Review Table has 4 columns; DTR001+ has 5 (Concurrence) | Add column during DTR001 generation |
| 3 | INITIAL Table 5 (STIG CoF) has 6 columns; DTR001+ has 5 (CAT removed) | Remove CAT column during DTR001 generation |
| 4 | ~~INITIAL Table 4 split across 2 tables (indices 6+7)~~ | **RESOLVED:** Updated INITIAL has Table 4 as a single continuous table (index 6). No merge step needed. |
| 5 | INITIAL uses `IWBC` / `Combined SBC/IWG Combined (IWBC)` naming | Rename to `Combined SBC/IWG` for DTR001+ |
| 6 | Table index shifts after CMVP removal | Recalculate all table references after removal |
| 7 | INITIAL Table 6 (Internal Findings) has 3 cols; DTR001+ has 4 | Add column during DTR001 generation. Only IP addresses and test tool version get updated per DTR — other content is static. |
| 8 | ~~Table 4 Product Component header doesn't repeat on page breaks~~ | **RESOLVED (by design):** Table 4 is a single continuous table with **no `tblHeader`** — header does not repeat on page breaks. Do not split Table 4 or add `tblHeader`. |
| 9 | Table 1a CAT counts render on one line instead of stacked | W/O-RAE and W-RAE cells must use **3 separate paragraphs** (one per CAT level), not `\n` in a single paragraph. Use `_set_cell_cat_lines()` helper. |
| 10 | Step 7 component version matching fails — checks wrong column | Match component name against `cells[0]` (Product Component) **and** `cells[1]` (Hardware) combined, not just `cells[0]` which is always "Cisco SBC". |
| 11 | CSR revision history date format differs from other doc types | CSR uses **"Month YYYY"** format (e.g. `May 2026`), not `DD Mon YYYY`. Auto-applied from `datetime.now().strftime("%B %Y")`. |
| 12 | Internal Findings 4th column grid expansion | INITIAL has 3 grid cols; DTR001+ has 4. R0-R1 (IP/Connectivity): merged cell gridSpan 2→3. R2-R4 (Test Tools): Functions cell gridSpan 1→2. R5 (NOTE): gridSpan 3→4. Add 4th gridCol by splitting last col width. |
| 13 | Product Component col 4 (Hardware certified by Similarity) not centered | All data cells in col 4 must have `jc=center`. Applied in step 13 table quality fixes. |
| 14 | DTR001 generation missing STIG/IPV/Ports updates | `generate_dtr001()` now includes steps 14-16 for STIG Phase I updates, IPV findings (High/Medium/Low breakdown), and Open Ports table additions. |
| 15 | IPV findings prompt asked for total count instead of risk breakdown | IPV prompt now: (1) multi-select which risk levels have findings, (2) for each selected level, enter count. Unselected levels default to "No [Level] Risk". Updates Table 1b and Table 3. |
