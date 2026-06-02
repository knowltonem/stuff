# ICR Automation — Skill: Functionality Attestation (FA)
> Load `skill_base.md` first. This file defines rules specific to the **Functionality Attestation (FA)** document type only.

---

## MANDATORY PRE-GENERATION READ — NO EXCEPTIONS

**Before presenting ANY FA prompts, OpenCode MUST read from disk:**

1. **This skill file** (`_Skills/skill_fa.md`) — in full
2. **The FA runner** (`_Tools/run_fa.py`) — specifically:
   - The `SBC_CTN2026003_FA_PROFILES` section (lines ~1050-1100)
   - The `run()` function to understand required config keys
   - The `generate_dtr001()` and `generate_dtr_incremental()` functions

**Do not rely on memory from prior sessions.** The skill and runner may have changed.

---

## Document Identity
- **Full Name:** Cisco Functionality Attestation
- **Abbreviation:** FA
- **Folder:** `Functionality Attestation (FA)/`
- **Filename Suffix:** `Cisco Functionality Attestation.docx`

---

## Purpose
The FA document attests that the product under review meets the required functionality standards for the software version being certified. It replaces what was previously called the Certification document.

---

## Generation Status
- [x] Example/Template file placed in `Examples & Templates/`
- [x] Table structure documented
- [x] Paragraph patterns documented
- [x] First draft generated and validated
- [x] Skill file updated with confirmed rules

---

## Document Structure Overview

The FA document does **not** have a revision history table. Instead, DTR updates are recorded as body paragraphs in the "Test Details" section.

### Paragraph Sections (in document order)
| # | Section | Style | Notes |
|---|---|---|---|
| 1 | Date | Normal | Full date at top of document (e.g. `25 February 2026`) |
| 2 | Title | Normal | `Functionality Attestation (FA)` |
| 3 | SUBJECT line | Normal | Full subject paragraph — includes product name and software version |
| 4 | Internal Compliance Authority | Normal (Web) | Static boilerplate |
| 5 | Conditions of Attestation | Normal (Web) | Contains software version reference (`IOS XE X.X`) |
| 6 | Table 1. Conditions | — | TDR conditions table |
| 7 | System Requirements ID | List Paragraph | References software version; followed by Table 2-1 |
| 8 | Figure 2-2 | Normal | SUT Test Configuration (image) |
| 9 | System Description | List Paragraph | Static boilerplate (General Description, bullet list) |
| 10 | Management Description | List Paragraph | Static boilerplate |
| 11 | Operational Architecture | List Paragraph | Static boilerplate |
| 12 | Test Details | List Paragraph | **DTR update paragraphs inserted here** |
| 13 | Functionality Status | List Paragraph | References Tables 3, 4, 5 |
| 14 | Tables 3–5 | — | Interface status, HW/SW/FW versions, CR/FR requirements |
| 15 | Point of Contact | List Paragraph | Static boilerplate |
| 16 | Acronym List | Heading 1 | Static table |

---

## Table Map (SBC — CTN2026003)

### INITIAL Document (9 tables)

| Table Index | Table Label | Rows × Cols | Content |
|---|---|---|---|
| 0 | Table 1. Conditions | 2 × 4 | TDR# / Description / Operational Impact / Remarks |
| 1 | Table 2-1. System Requirements ID | 11 × 2 | System Name, Version, DTR ID, etc. |
| 2 | Table 3. SUT Interface Status | 8 × 4 | Network Management Interfaces |
| 3 | Table 3. (Continued) | 5 × 4 | Network Interfaces + Notes row |
| 4 | Table 4. SUT HW/SW/FW Version ID | 11 × 5 | Product Components — IWBC rows (initial naming) |
| 5 | Table 4. (Continued) | 16 × 5 | Product Components — SBC rows, ESXi, Mgmt Workstation + Notes row |
| 6 | Table 5. CR/FR Requirements | 4 × 5 | Capability Requirements (first page) |
| 7 | Table 5. (Continued) | 32 × 5 | Capability Requirements (main body) + Notes row |
| 8 | Acronym List | 53 × 2 | Static acronym definitions |

### Generated DTR001 Document (8 tables)

| Table Index | Table Label | Rows × Cols | Content |
|---|---|---|---|
| 0 | Table 1. Conditions | 2 × 4 | TDR# / Description / Operational Impact / Remarks |
| 1 | Table 2-1. System Requirements ID | 11 × 2 | System Name, Version, DTR ID, etc. |
| 2 | Table 3. SUT Interface Status (Network Mgmt) | 8 × 4 | Network Management Interfaces — `tblHeader` on rows 0+1 |
| 3 | Table 3. SUT Interface Status (Network Intf) | 6 × 4 | Network Interfaces + Notes row — `tblHeader` on rows 0+1 |
| 4 | Table 4. SUT HW/SW/FW Version ID (Product ID) | 5 × 5 | Product Identification rows |
| 5 | Table 4. (Product Components) | ~22 × 5 | Product Components — IWBC + SBC + IWG rows + Notes row — `tblHeader` on row 0 |
| 6 | Table 5. CR/FR Requirements | ~35 × 5 | Combined CR/FR rows + Notes row — `tblHeader` on row 0 |
| 7 | Acronym List | 53 × 2 | Static acronym definitions |

> **Note:** The Example DTR001 reference file uses a merged single Table 3 (12 rows). Generated DTR001+ keeps Table 3 as two separate tables so each section gets its own repeating header on page breaks.

---

## Key Table Details

> **Note:** All table index references in the sections below (e.g. `Table Index 0`, `Table Index 4`) refer to the **Generated DTR001 Document** index (8-table layout), not the Initial document index (9-table layout). The two layouts differ starting at index 4 due to Table 4 being split differently.

### Table 1. Conditions (Table Index 0)
- 4 columns: `TDR #` | `Description` | `Operational Impact` | `Remarks`
- INITIAL has `None` in all cells; Example DTR001 has actual TDR entries
- Update when a TDR is associated with this DTR

### Table 2-1. System Requirements Identification (Table Index 1)
- 2 columns, 11 rows — key/value pairs
- **Row 2** (`Increment and/or Version`): update to new software version
- **Row 6** (`DTR ID`): update to reflect current DTR number and platform list
- Other rows are generally static

### Table 4. SUT HW/SW/FW Version Identification (Table Indices 4–5 INITIAL, 3–5 Example)
- **This is the primary component table** — equivalent to the System Description's component table
- 5 columns: `Product Components` | `Component Name` | `Sub-Component` | `Tested Version` | `Function`
- **Row 2 (`Software Release`)**: merged header row — update to new IOS XE version
  - XML has only 2 `w:tc` elements (col 0 = "Software Release", col 1 = version spanning remaining columns)
  - Must check `len(cells) >= 2` before the `len(cells) < 4` guard, otherwise this row is skipped
- **Tested Version column (index 3)**: contains software versions to update for platform rows
- **Sub-Component column (index 2)**: update any cell containing `IOS XE` (e.g. ESXi Server Host sub-component in Table 4 row 14)
- Version replacement regex: match `IOS XE\s+\S+` and replace with new version
- INITIAL uses `IWBC` naming; DTR001+ uses `IWG/SBC` naming
- Non-IOS XE rows (ESXi version, ActivClient, Axway, SecureCRT, Windows) are **not updated** — leave as-is
- Notes row (Table 4 Product Components, last row) contains static "initially certified with" text — do **not** update

### Table 5. CR/FR Requirements (Table Indices 6–8 INITIAL, 6–7 Example)
- 5 columns: `CR/FR ID` | `UCR Requirement` | `Applicability` | `UCR 2013 Change 2` | `Status`
- Generally static — only update if test results change

---

## Platform Map (SBC — CTN2026003)

| Platform | INITIAL Naming | DTR001+ Naming | Notes |
|---|---|---|---|
| ASR 1006-X | IWBC / SBC | IWBC / SBC / IWG | Rows in Table 4 — naming unchanged from INITIAL |
| C8300 series | IWBC / SBC | IWBC / SBC / IWG | Rows in Table 4 — naming unchanged from INITIAL |
| C8200 series | IWBC / SBC | IWBC / SBC / IWG | Rows in Table 4 — naming unchanged from INITIAL |
| C8000v series | IWBC / SBC | IWBC / SBC / IWG | Rows in Table 4 — naming unchanged from INITIAL |
| ISR 4461 | IWBC / SBC | IWBC / SBC / IWG | Present in both INITIAL and Example |

> Always confirm current versions by reading the last working document before prompting.
> **IWBC is the correct col 0 value in DTR001+ — do NOT rename to IWG/SBC.**

## Product Component Map (SBC — CTN2026003)

| Component | Full Name | Acronym |
|---|---|---|
| Interworking Border Controller | Interworking Border Controller (IWBC) | IWBC |
| Interworking Gateway | Interworking Gateway (IWG) | IWG |
| Session Border Controller | Session Border Controller (SBC) | SBC |

> When listing product components in the `component_list` field of the DTR body paragraph, use this format (comma-separated, with full names in parentheses):
> `SBC, Combined SBC/Interworking Gateway (IWBC), and IWG`
> - The order is: SBC first, then IWBC (IWG/SBC combined), then IWG
> - Each component uses its full name in this context — not acronym only
> - The `component_list` string is embedded in the runner's DTR body sentence: `"...for the {component_list} on {hw_list} of router platforms."`
> - Product component selection is handled by step 7 in the prompt sequence
> - **Singular/plural rule:** If only one component is selected, use "product component" (singular). If multiple, use "product components" (plural).

---

## What Gets Updated Per DTR

### 1. GCT Banner + Document Date (Paragraph 0)
- Paragraph 0 contains both the GCT banner image and the document date as inline runs
- **Run order must be:** `[" "]` → `[drawing/banner]` → `[" DD Month YYYY"]`
- The INITIAL document does **not** have the banner — for DTR001, clone paragraph 0 from the Example DTR001 (which contains the banner drawing), update the date text, and replace the INITIAL's paragraph 0
- For DTR002+, the banner is already present — only update the date text run (the text run **after** the drawing run)
- The image relationship (`media/image1.png`) already exists in both the INITIAL and Example at `rId11` — they are the same image
- **Do NOT copy the image from Example** — this creates a duplicate `word/media/image1.png` zip entry that corrupts the file
- Instead, set the cloned banner blip's `r:embed` to `rId11` to reuse the existing image relationship
- **Never place the date text before the banner** — the date must always render below the GCT banner
- Date format: `DD Month YYYY` (e.g. `30 April 2026`)
- **Auto-generated** — use today's date at generation time (`datetime.now()`), do NOT prompt the user

### Known Issue — INITIAL Table 1 Merged Cells
- The INITIAL document's Table 1 (TDR Conditions) row 1 has all 4 cells **merged into a single `w:tc`**
- python-docx returns the same cell object for all column positions — `zip(row.cells, values)` writes to the same cell repeatedly
- **Fix:** Clone the 4-cell data row from the Example DTR001 document, set TDR values on the cloned row, and replace the INITIAL's merged row

### 2. Table 2-1 — DTR ID Row (Row 6)
- Update to reflect the new DTR number and platform list
- **Only list updating platforms** — sustained platforms are excluded from the DTR ID
- The INITIAL has the original platform list split across multiple runs — must clear all leftover runs after setting Run 0
- Example: `001 (C8300 Series, C8200 Series, C8000v, and C8350)`

### 3. Table 2-1 — Version Row (Row 2)
- Update `Increment and/or Version` to the new software version

### 3a. Conditions of Attestation — Version (Paragraph 9)
- Paragraph 9 contains `Operating System (IOS) XE [version] (System Under Test, or SUT)...`
- The version is in **Run 4** (` XE X.X`) with a leftover digit in **Run 5** from the original `17.18`
- Update Run 4 to ` XE {new_version}` and clear Run 5 to empty string
- This must match the DTR's target software version

### 3b. System Requirements Identification — Version (Paragraph 14)
- Paragraph 14 contains `...Software Rel. IOS XE [version] (detailed in Table 2-1)...`
- The version is in **Run 9** (` IOS XE 17.1`) with leftover `8` in **Run 10**
- Update Run 9 to ` IOS XE {new_version}` and clear Run 10 to empty string

### 4. DTR Body Paragraph(s) in Test Details Section
- Each new DTR adds a paragraph describing the update
- Insert **before** the "Functionality Status" paragraph
- Format:

**For platforms updating to a new version:**
`DTR [N] was requested to update the IOS XE software version from [FROM] to [TO] for the IWG/SBC on [hw list] of router platforms.`

**For newly added platforms:**
`DTR [N] adds the IOS XE software on [hw list] of router platforms. The IOS XE software version is [TO].`

- Group updating platforms by `(from_ver, to_ver)` — one sentence per unique pair
- Hardware list format: `the ASR 1006-X, the C8300 series, the C8200 series, and the C8000v series`
  > **Note:** FA uses abbreviated platform names (`C8300 series`, `C8200 series`, `C8000v series`). ICR Memo uses full names (`Cisco Catalyst 8300 Series`, etc.). Do not normalize FA text to match Memo format — they are intentionally different. Cross-reference: `skill_icr_memo.md` → Platform Name Formats.

### 4a. Test Details — Functionality Testing Dates
- The Test Details paragraph contains `"Cisco GCT DP conducted functionality testing from [START] through [END]"`
- These dates must be updated each DTR to reflect when testing was actually conducted
- In the INITIAL document, dates are split across runs:
  - **Run 12**: start date (`"DD Month"`)
  - **Run 13 + Run 14**: start year (`" 20"` + `"YY"`, split across runs)
  - **Run 16**: end date (`"DD Month"`)
  - **Run 17**: end year (`" YYYY"`)
- Update Run 12 to new start date, Run 13 to `" {start_year}"`, clear Run 14
- Update Run 16 to new end date, Run 17 to `" {end_year}"`
- Date format: `DD Month` (e.g. `05 May`) for runs 12/16, ` YYYY` for runs 13/17

### 5. Table 4 — Software Release, Tested Version, and Sub-Components
- **Row 2 (`Software Release`)**: update merged version cell to new IOS XE version
- **Tested Version (column 3)**: update for all updating platform rows
- **Sub-Component (column 2)**: update any cell containing `IOS XE` (e.g. ESXi Server Host IOS XE sub-component)
- Use regex: replace `IOS XE\s+\S+` with new version string
- Only update IOS XE references — skip ESXi version, ActivClient, Axway, SecureCRT, Windows rows
- **Sustained platforms must be skipped entirely** — match col 1 (`Component Name`) against sustained platform identifiers (e.g. `"ASR"`, `"ISR"`) and `continue` past both the platform row update AND the sub-component catch-all. Without this guard, the sub-component regex will incorrectly update sustained platform rows.
- Do **not** update the Notes row (static "initially certified with" text)

### 6. Table 1 — TDR Conditions (if applicable)
- If a TDR is associated with this DTR, add or update the relevant row
- If no TDR, leave as-is
- **Dedup rule:** If the new TDR number matches an existing row in Table 1, **update that row in place** — do not add a duplicate
- **Update existing rows:** The engineer may also request updates to existing TDR rows (e.g. changing remarks from `OPEN` to `CLOSED`) without adding new rows

### 7. Similarity Paragraph (if included)
`Request certification through similarity based on "[ProdCat] TN: [CTN], DTR[XX]."`
- No leading quote mark before "Request"
- The TN referenced is typically a **different** CTN than the one being worked
- Prompt order:
  1. TN Product Category — read live from `Product Category/` subfolders
  2. TN CTN — always prompt from disk (list available CTNs under the selected Product Category).
  3. DTR number — manual entry
- Insert after the DTR body paragraph(s) in the Test Details section

### 8. IWBC Naming (Table 4 — DTR001 only)
- **IWBC is the correct col 0 name in both INITIAL and DTR001+** — do NOT rename to IWG/SBC
- Step 15 (IWBC rename) was removed from `generate_dtr001()` — it caused incorrect output
- New platform rows must use `group: "IWBC"` (not `"IWG/SBC"`) when targeting the IWBC product component group

### 9. Bold+Underline Tested Components (Table 4 — Product Components)
- First prompt: select which platform families were tested (ASR 1006-X, C8200, C8300, C8000v, ISR 4461, ESXi Server Host, Management Workstation)
- If C8200 selected: follow-up prompt listing individual C8200 models (C8200-1N-4T, C8200L-1N-4T)
- If C8300 selected: follow-up prompt listing individual C8300 models (C8300-1N1S-4T2X, C8300-2N2S-4T2X, C8300-1N1S-6T, C8300-2N2S-6T)
- Per-model bold+underline: each model name is its own run in the XML — set bold+underline per run
- **Exact match only** — compare each run's stripped text with `==` against the selected model names, NOT substring `in`. This prevents e.g. `C8200-1N-4T` from also matching `C8200L-1N-4T`
- **Clear all bold+underline first**, then apply to matching models only — prevents stale bold from previous DTRs carrying forward
- Unselected models: remove bold + underline (set to normal)
- Skip header rows, duplicate header rows, and NOTES row

### 10. Keep Table Titles With Their Tables
- Set `keepNext` on all table title paragraphs: `Table 1.`, `Table 2`, `Table 3.`, `Table 4.`, `Table 5.`, `List of Acronyms`
- Also set `keepNext` on any empty spacer paragraphs between the title and the table — this chains `title → spacer → table` so Word never separates them across pages
- Do **NOT** remove spacer paragraphs — they provide intended spacing (e.g. Table 5 has one)
- Do **NOT** include `Figure 2` — its content is in drawing paragraphs with no `w:t` text; the spacer removal/chaining would delete the diagram image

### 11. Page Break Before "List of Acronyms"
- Set `pageBreakBefore` on the "List of Acronyms" heading paragraph so it always starts at the top of its own page
- Remove empty spacer paragraphs immediately **before** "List of Acronyms" — they create a blank page when combined with `pageBreakBefore`

### Code Step Mapping

> **Sync note:** This table must be kept in sync with the step-comment headers in `run_fa.py`. If you add, remove, or reorder steps in the script, update this table in the same commit.

**DTR002/DTR003 gen scripts (14 steps):**

| Step | Description |
|---|---|
| 1 | Update document date |
| 2 | Update functionality testing dates |
| 3 | Update reference (c) IOS XE version |
| 4 | Update Conditions of Attestation version |
| 5 | Update System Requirements paragraph version |
| 6 | Update Table 2-1 — System Requirements ID |
| 7 | Update Table 1 — TDR Conditions (add/replace row) |
| 8 | Insert DTR body paragraph(s) in Test Details |
| 9 | Update Table 4 — Software Release, Tested Version, Sub-Components |
| 10 | Insert new platform rows in Table 4 (if applicable) |
| 11 | Bold+underline tested models in Table 4 |
| 12 | Keep table titles with their tables (keepNext + spacer chaining) |
| 13 | Page break before "List of Acronyms" + remove spacers before it |
| 14 | Save |

**DTR001 gen script (21 steps):**

| Step | Description |
|---|---|
| 1 | Update document date + add GCT banner |
| 2 | Fix "Conditions of Certification" → "Conditions of Attestation" (if stale) |
| 3 | Update Conditions of Attestation IOS XE version |
| 4 | Update reference (c) IOS XE version (content-search replace) |
| 5 | Update functionality testing dates |
| 6 | Update System Requirements paragraph version |
| 7 | Update Table 1 — TDR Conditions (clone 4-cell row from example if TDR provided) |
| 8 | Update Table 2-1 — System Requirements ID |
| 9 | Insert DTR body paragraph(s) in Test Details |
| 10 | Update Table 4 — Software Release, Tested Version, Sub-Components |
| 11 | Scale Figure 2-2 diagram to 90% |
| 12 | Table 3 — keep as 2 separate tables, set tblHeader on rows 0+1 of each |
| 13 | Merge Table 4 (INITIAL tables 4+5) + split into Product ID and Product Components |
| 14 | Set tblHeader on Product Components table (row 0) |
| 15 | (removed — IWBC is the correct col 0 name in DTR001+; no rename needed) |
| 16 | Bold+underline tested components in Product Components tables |
| 17 | Remove empty paragraphs between Product Components tables 5 and 6 |
| 18 | Insert new platform rows into Product Components table (per group) |
| 19 | Merge Table 5 (INITIAL CR/FR tables 6+7), set tblHeader |
| 20 | Apply NOTES rows for Table 3, Table 4 (Product Components), Table 5 (CR/FR) — **must run before step 20a** |
| 20a | Remove duplicate column header row from Table 6 (Product Components continuation) |
| 21 | Save |

---

## Paragraph Order Within Test Details Section
1. Existing DTR paragraphs (from previous DTRs — do not modify)
2. **[empty spacer]** — empty `List Paragraph` between each DTR block
3. New DTR body paragraph(s)
4. Sustain paragraphs (if partial platform update)
5. Similarity paragraph (if included)
6. **[empty spacer]** — before Functionality Status

The "Functionality Status" paragraph always comes **after** all DTR paragraphs.

---

## FA-Specific Prompt Sequence (Steps 4+ after base steps 1–3)

> **HANDOFF RULE — NO EXCEPTIONS:**
> After step 3 (Document Type selected), OpenCode collects all remaining inputs via `question` tool (using "Type your own answer" for free-text fields — TDR number, description, dates, etc.), builds the complete cfg, then calls `execute_cfg(cfg)` directly via Python. No terminal required. Never ask the engineer to open a terminal or re-run the script manually.

> **PROFILE PATH RULE — NO EXCEPTIONS:**
> When a seed profile exists for the CTN/DTR, it provides **defaults only**. OpenCode MUST still ask ALL steps 4–12 in order. Never skip a step because the profile pre-fills it. The engineer must explicitly confirm or override every value — especially steps 5 (new platforms) and 6 (which platforms are updating / what was tested / bold+underline models). Profile values for `new_platforms`, `updating_platforms_table`, `updating_display`, and `bold_underline_models` are starting points — not final answers.

> **STEP CHECKLIST — verify every step is asked before calling execute_cfg():**
> - [ ] 4. New software version
> - [ ] 5. Add a new platform? (display name, groups, sub-component, tested version — repeat until done)
> - [ ] 6. Which platforms are updating? (C8200 model follow-up, C8300 model follow-up, bold+underline derived)
> - [ ] 7. Product components (component_list)
> - [ ] 9. TDR — add or update?
> - [ ] 10. Testing dates (start date, start year, end date, end year)
> - [ ] 11. Table NOTES
> - [ ] 12. Similarity statement

4. **New software version** — what version is being certified?
5. **Add a new platform?** — Yes / No
   - If Yes:
     1. Platform name (free text)
     2. Which Product Component group(s) does it belong to? (multi-select — `IWBC`, `SBC`, `IWG`). One row is inserted per selected group.
     3. Sub-component — free text, or `NA` if none
     4. Display name for DTR sentence (e.g. `C8300 series`) — defaults to platform name if blank
     5. Tested version defaults to the new software version — confirm or override
   - Repeat until user selects done
6. **Which platforms are updating to the new version?** — Multi-select from existing platforms in the source document.
   - Selected platforms get the new version **and** are bold+underlined
   - Unselected platforms keep their current version (sustained — not bold+underlined)
   - **New platforms added in step 5 are automatically included** — they do not appear in this prompt
   - If C8200 selected: follow-up for individual C8200 models to bold+underline
   - If C8300 selected: follow-up for individual C8300 models to bold+underline
   - **`hw_list` is auto-built** from the selected platforms + new platform display names — no separate prompt
7. **DTR Statement: Product Component(s)?** — Multi-select from Product Component Map (e.g. `IWBC`, `SBC`, `IWG`). Selection drives the `component_list` in the DTR body paragraph — **auto-built from selections, no separate prompt**.
   - **Singular/plural rule:** If only one component is selected, use "product component" (singular). If multiple, use "product components" (plural).
8. **DTR ID suffix** — auto-built from updating + new platforms (same list as `hw_list` without "the" prefixes). Written to Table 2-1 Row 6 as `00{N} (platform list)`. No prompt needed.
9. **Table 1. Conditions: TDR — add or update?** — Yes / No
   - A single prompt handles both adding a new row and updating an existing row. If the TDR number entered matches an existing row, that row is updated in place. If it does not match, a new row is appended.
   - If Yes, prompt sequentially:
     - TDR Number (e.g. `2026003-1`)
     - TDR Description
     - Operational Impact (e.g. `OPEN`, `CLOSED`) — goes in col 2, not Remarks
     - Remarks
   - If No: Table 1 is left unchanged
10. **Functionality testing dates?** — Prompt sequence:
    1. **Start date** — free text (e.g. `05 Jun`)
    2. **Start year** — free text (e.g. `2026`)
    3. **End date** — free text (e.g. `08 Jul`)
    4. **End year** — free text (e.g. `2026`)
11. **Table NOTES update?** — Multi-select: `Table 3 (Network Interfaces)`, `Table 4 (Product Components)`, `Table 5 (CR/FR)`, or none to skip.
    - For each selected table: free text for new NOTES content. Appends as a new numbered paragraph to existing NOTES. Each note is cloned from the first existing numbered paragraph in the notes row (carries `numPr`/`numId` so numbering restarts at 1).
12. **Similarity statement?** — Yes / No (follow `skill_base.md` shared rules)
    - If Yes:
      1. TN Product Category — read live from `Product Category/` subfolders
      2. TN CTN — read live from subfolders under selected Product Category
      3. DTR number — free text
    - Builds canonical sentence: `Request certification through similarity based on "[ProdCat] TN: [CTN], DTR[XX]."`
    - **DTR001 should always prompt for similarity** — do not assume empty

> **Steps 4–12 complete the generation.** The draft is generated in a single pass. Table 4 (Product Components) no longer has vertically merged cells, so Word's native `tblHeader` repeat handles page breaks automatically.

---

## DTR001 from INITIAL — Special Rules

When building DTR001 from a `DTR000 - INITIAL` document:
- INITIAL uses `IWBC` naming in Table 4 — DTR001+ uses `IWG/SBC` naming
- INITIAL Table 3 (Network Mgmt + Network Interfaces) is split across two tables (indices 2–3) — **keep as two separate tables** (do NOT merge). Set `tblHeader` on rows 0+1 of each table so both the section header and column headers repeat on page breaks. Remove empty spacer paragraphs between the two tables.
- INITIAL Table 4 (Product Components) is a single table (index 5) with no vertically merged cells — set `tblHeader` on row 0 and `tblLayout type="fixed"` for native header repeat on page breaks. Remove any inherited `tblBorders` from the deepcopy (Product Identification has explicit `sz=6` borders that should not carry over — Product Components uses `TableGrid` style defaults).
- INITIAL Table 5 (CR/FR) is split across two tables (indices 6–7) — merge into one table with header row repeat
- **Acronym List (index 8) is a separate table** — do NOT merge it into Table 5. After earlier merges shift indices, Acronym becomes index 7; only merge CR/FR tables (indices 6+7 after Table 4 merge+split)
- Remove all "Table continues on the next page" and "Table X (Continued)" paragraphs between merged tables
- **Post-generation table indices:** 0=Cond, 1=SysReq, 2=IntfMgmt, 3=IntfNet, 4=ProdID, 5=ProdComp, 6=CR/FR, 7=Acronym
- Preserve the INITIAL document's static content (boilerplate paragraphs, acronym list)

### Page Layout Rules (DTR001)
- **Page break before System Requirements paragraph** (paragraph 14) — prevents splitting across pages
- **Figure 2-2 diagram scaling** — scale to 90% (`SCALE = 0.90`) so it fits under the "Figure 2-2" label
- **Remove 2 empty paragraphs before "System Description"** — moves it up to the top of its page
- **Reference (c) IOS XE version** — locate the paragraph containing "Test Details" and "functionality testing from", then update by run index: run 12 = start date, run 13 = start year (with leading space), run 14 = cleared, run 16 = end date, run 17 = end year (with leading space). Run indices are content-derived from the known template structure.

---

## Differences from System Description

| Aspect | System Description | Functionality Attestation |
|---|---|---|
| Revision history table | Yes (Table 0) | No — no revision history table |
| DTR section heading | `Desktop Review (DTR) [N]` with page break | No separate DTR heading — paragraphs in Test Details |
| Component table | Dedicated table per DTR section | Single Table 4 updated in place |
| Version column index | 1 (Release) | 3 (Tested Version) |
| Component naming | IWG / SBC / IWG/SBC (3 rows per platform) | IWG/SBC (single row per platform) |
| Detail heading | `DTR Detailed Component Information` | None |
| Document date | Not present at top | Present at paragraph 0 |
| Table 2-1 DTR ID | Not present | Row 6 — must be updated |

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

The validator is FA-aware and runs these FA-specific checks:
- Test Details paragraph exists with testing dates (warns if dates are INITIAL defaults)
- At least one DTR body paragraph exists (`DTR N was requested...`)
- Functionality Status paragraph exists
- Product Components table has no `IWBC` (should be `IWG/SBC` for DTR001+)
- Skips: revision history table, DTR heading, CTN body presence (CTN is in header)
---

## Known Issues

> Superseded issues are retained for historical reference and marked with ~~strikethrough~~. They may be pruned once the resolution has been stable for two or more DTR cycles.

| # | Issue | Resolution |
|---|---|---|
| 1 | ~~INITIAL Table 4 uses `IWBC` naming — wrong for DTR001+~~ | **RESOLVED (reverted):** `IWBC` is the correct col 0 name in both INITIAL and DTR001+. The rename step was removed. Do not rename IWBC → IWG/SBC. |
| 2 | INITIAL Table 3 split across two tables | Example DTR001 merges into single table |
| 3 | Non-IOS XE rows in Table 4 (ESXi, ActivClient, etc.) should not be updated | Only match `IOS XE\s+\S+` pattern — other version strings are left as-is |
| 4 | Filename suffix differs from System Description | FA uses `Cisco Functionality Attestation.docx`, not `Cisco ICR Functionality Attestation.docx` |
| 5 | INITIAL document missing GCT banner image | Clone paragraph 0 from Example DTR001 (contains inline drawing), copy image relationship, replace INITIAL's paragraph 0 |
| 6 | Date renders above banner when run order is wrong | Ensure run order: `[space]` → `[drawing]` → `[date text]` — never place date text run before drawing run |
| 7 | INITIAL Table 1 row 1 has all cells merged (single `w:tc`) | Clone 4-cell row from Example DTR001 and replace the merged row |
| 8 | Old INITIAL used "Conditions of Certification" (paragraph 8) — should be "Conditions of Attestation" | Updated INITIAL now uses correct wording; ensure gen scripts do not reintroduce "Certification" |
| 9 | INITIAL Table 4 previously split across two tables with "Continued" label | **RESOLVED:** Updated INITIAL has Product Components as a single table (index 5) with no merged cells. No merge or split step needed for Table 4. |
| 10 | INITIAL Table 5 split across two tables with "Continued" label | Merge into one table with header row repeat — do NOT merge Acronym List table (separate 2-col table) |
| 11 | Figure 2-2 diagram too large — pushes content to next page | Scale to 90% in gen script (`SCALE = 0.90`) |
| 12 | System Requirements paragraph splits across pages | Add `pageBreakBefore` to keep it on one page |
| 13 | Reference (c) IOS XE version not updated | ~~Update runs 65-66 in paragraph 4, clear runs 67-68~~ — **SUPERSEDED by Known Issue #22** (hardcoded run indices broke across DTRs; use scan-based approach instead) |
| 14 | No spacer between DTR blocks in Test Details | Insert empty `List Paragraph` spacer between each DTR block |
| 15 | Word `tblHeader` does not repeat when table has `vMerge` cells | **RESOLVED:** Updated INITIAL removed merged cells from Table 4 (Product Components). Word's native `tblHeader` now handles header repeat on page breaks. `TABLE4_HEADER_BEFORE` config and two-pass generation are no longer needed. Legacy code retained but skipped when set to `None`. |
| 16 | Bold+underline from previous DTR carries forward into next DTR | Clear all bold+underline on col 1 runs first, then apply only to current DTR's tested models |
| 17 | Validator falsely fails FA docs (no DTR heading, no revision history) | Validator now FA-aware: skips revision history/DTR heading checks, runs FA-specific checks (Test Details dates, DTR paragraphs, Functionality Status, IWBC rename, Acronym List separation) |
| 18 | IWBC text split across runs in INITIAL (`"IW"` + `"BC"`) | Match on concatenated cell text, not individual run text — set first run to `"IWG/SBC"`, clear subsequent runs |
| 19 | Acronym List not starting on its own page | Add `pageBreakBefore` to the "List of Acronyms" heading paragraph. Also remove empty spacer paragraphs immediately before it (they create a blank page when combined with `pageBreakBefore`) |
| 20 | Table title on separate page from its table | Set `keepNext` on all table title paragraphs (`Table 1.`, `Table 2`, `Table 3.`, `Table 4.`, `Table 5.`, `List of Acronyms`). Also set `keepNext` on any empty spacer paragraphs between the title and the table to chain them together. Do NOT remove spacer paragraphs — they provide intended spacing (e.g. Table 5 has one). Do NOT include `Figure 2` in this list — Figure 2-2's content is in drawing paragraphs that look empty (no `w:t` text) and would be incorrectly removed or chained |
| 21 | Sustained platform versions overwritten in Table 4 | The sub-component catch-all regex (`IOS XE\s+\S+`) was updating ALL rows — including sustained platforms (ASR, ISR). Fix: after checking `UPDATING_PLATFORMS_TABLE`, add a second check for sustained platform identifiers (`"ASR"`, `"ISR"` in col 1 text) and `continue` to skip them entirely. Without this, sustained platforms cascade wrong versions through subsequent DTRs |
| 22 | Reference (c) IOS XE version not updated properly — duplicate `IOS XE 17.1 IOS XE 26.0` | The version in Reference (c) is split across multiple runs in the INITIAL (e.g. `" IOS XE "` + `"17.1"` + `"8"`). Hardcoded run indices broke across DTRs. Fix: scan runs between `(c)` and `(d)` for `IOS XE`, concatenate the range, regex-replace all `IOS XE [\d.]+` occurrences with the new version, write back to first run and clear the rest |
| 23 | Table 3 header repeat shows wrong section header | **RESOLVED:** Table 3 is now kept as two separate tables (Network Mgmt Interfaces + Network Interfaces). Each table has `tblHeader` on rows 0+1 (section header + column headers), so the correct header repeats on page breaks regardless of which section the break falls in. |
| 24 | Table 4 (Product Components) `tblHeader` not repeating in Word | The deepcopy from Product Identification table omits `tblLayout type="fixed"`. Word requires `tblLayout fixed` for `tblHeader` to work. Fix: add `tblLayout type="fixed"` to the new Product Components table's `tblPr`. |
| 25 | Table 4 (Product Components) border weights thicker than other tables | The deepcopy from Product Identification carries explicit `tblBorders sz=6` (0.75pt) into Product Components. Other tables use `TableGrid` style defaults (`sz=4` / 0.5pt). Fix: remove inherited `tblBorders` from the new Product Components table's `tblPr`. |
| 26 | New platform row col 0 blank when INITIAL has no vMerge | Old logic forced `vMerge continue` on col 0 of cloned rows, but updated INITIAL has no vMerge — causing blank cells. Fix: check if source table uses vMerge; if not, set col 0 text to the target group name instead. |
| 27 | DTR body paragraphs misaligned with Test Details section | DTR body and sustain paragraphs used `Normal` style with `firstLine=720` but no `left` indent — first line was indented 0.5" from page margin while body text started at the margin, neither matching the Test Details paragraph's `List Paragraph` left indent (720 twips). Fix: set `left=720` and remove `firstLine` so text aligns flush with Test Details. The INITIAL P47 source paragraph carries `firstLine=720` from the original document — must explicitly remove it and add `left=720` after replacing runs. |
| 28 | Table 3 "Network Interfaces" header separated from data rows on page break | **RESOLVED:** Table 3 is now kept as two separate tables (issue #23 fix). Each table has `tblHeader` on rows 0+1, so section headers always repeat with their data. `keepNext` row chaining is no longer needed. |
| 29 | Table 2-1 DTR ID row has double parentheses and includes sustained platforms | The INITIAL's DTR ID text is split across multiple runs. Setting Run 0 to the new value without clearing runs 1+ leaves the old text appended. Also, sustained platforms should not appear in the DTR ID — only updating platforms are listed. Fix: set Run 0 to new value, clear all subsequent runs. |
| 30 | ~~IWBC rename misses Table 3; C8350 inserted in wrong table~~ | **RESOLVED (superseded):** The IWBC rename step has been removed entirely — IWBC is correct in DTR001+. New platform insertion uses exact group matching (`group: "IWBC"` targets IWBC rows only). |
| 31 | Product ID table column lines misaligned with Product Components | Product ID table (deepcopy) inherits auto layout — Word auto-adjusts column widths, shifting the col 0 divider out of alignment with Product Components (which has `tblLayout fixed`). Fix: add `tblLayout type="fixed"` to Product ID table's `tblPr` after the split. |
| 32 | Acronym List table border weights thicker than other tables | INITIAL Acronym table has explicit cell-level `tcBorders sz=8` (1pt) on every cell. Other tables use `TableGrid` style defaults (`sz=4` / 0.5pt). Fix: strip all `tcBorders` from Acronym table cells so it falls back to style defaults. Uses `strip_acronym_cell_borders()` from `runner_core.py`. |
| 33 | Table headers and borders inconsistent across drafts | **RESOLVED:** Consolidated all table fixes into `_apply_final_table_fixes()` which runs at the end of both DTR001 and DTR002+ generation. Sets `tblHeader` on tables 0,2,3,4,5,6 and adds bottom border to Table 3 last data row. This ensures consistency for every draft. |
| 34 | Table 4 NOTES lookup fails after column header row removed from Table 6 | `find_notes_tables()` labels tables by their first cell's text. After step 20a removes the duplicate column header row from Table 6, that table's first cell becomes `'IWG'` (first data row) — not `'Product Components'`. This causes the Table 4 notes label lookup to fail silently. Fix: **always apply Table 4 notes (step 20) before removing the Table 6 header row (step 20a)**. Order is mandatory. |
| 35 | New platform rows for C8300 all inserted at end of table regardless of group | Old `_insert_new_platforms_dtr001()` used a broad match that caused all rows to land after the last IWBC entry. Fix: use exact group matching — `match_groups = {target_group}` for all groups including IWBC. Rows now insert at the end of their specific group block. Use `group: "IWBC"` (not `"IWG/SBC"`) in `new_platforms` cfg. |

---

## Post-Generation Table Quality Checks

After generation, verify the following table properties for every table in the output document. These checks ensure visual consistency when the document is opened in Word.

### 1. Column Alignment Between Adjacent Tables
When a single INITIAL table is split into two tables (e.g. Product ID + Product Components), the resulting tables must have:
- **Identical `tblGrid` column widths** — the `w:gridCol` values must match so vertical lines align
- **Both tables must have `tblLayout type="fixed"`** — without this, Word auto-adjusts column widths and lines drift out of alignment
- **Same `tblInd`** (table indent) — different indents shift the entire table horizontally

### 2. Border Weights
- Tables using `TableGrid` style defaults get `sz=4` (0.5pt) borders — do NOT add explicit `tblBorders`
- Product ID table intentionally uses explicit `sz=6` (0.75pt) borders — this is by design
- When deepcopying a table with explicit borders, **remove inherited `tblBorders`** from the copy's `tblPr` if the copy should use style defaults
- Set bottom border of the last Product ID row to `nil` to prevent double-thick line where two tables meet

### 3. Cell Width Consistency
- Every cell's `tcW` width must match the sum of the `gridCol` values it spans
- If a cell has `gridSpan=N`, its `tcW` must equal the sum of the N corresponding `gridCol` widths
