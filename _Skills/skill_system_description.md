# ICR Automation — Skill: System Description
> Load `skill_base.md` first. This file defines rules specific to the **System Description** document type only.

---

## Document Identity
- **Full Name:** Cisco ICR System Description
- **Folder:** `System Description/`
- **Filename Suffix:** `Cisco ICR System Description.docx`

---

## Platform Map (SBC — CTN2026003)
| Platform | Table Row Indices | Current Version (as of DTR000 Initial) | Notes |
|---|---|---|---|
| ASR 1006-X | 1, 2, 3 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| C8300 series | 4, 5, 6 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| C8200 series | 7, 8, 9 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| C8000v series | 10, 11, 12 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| Notes row | 13 | — | Numbered list — must restart at 1 per table using `w:lvlOverride` + `w:startOverride w:val="1"` with a unique `numId` |

> Always confirm current versions by reading the last working document before prompting.

> **Other CTNs (ESC/CTN2026001, SS/CTN2026002):** When those CTNs become active, add a new `## Platform Map ([Product] — [CTN])` section here with their platform names, row indices, OS types, and initial versions. Do not assume the SBC platform map applies to other CTNs.

---

## Hardware Name Strings
Used in body paragraphs:
- `the ASR 1006-X`
- `the C8300 series`
- `the C8200 series`
- `the C8000v series`

Used in sustain paragraphs:
- `ASR 1006-X`
- `C8300 Series`
- `C8200 Series`
- `C8000v Series`

> When a new platform is added, use `the [Platform Name]` in body paragraphs and `[Platform Name]` in sustain paragraphs, matching the capitalization the engineer provides.

---

## newd Prompt Sequence (System Description)

> All prompts must use the `question` tool as clickable selections — no plain text lists.

1. **Per-platform status** — ask the first platform: Updating or Sustained
   - After **every** selection (Updating or Sustained), immediately offer the bulk shortcut (step 1a) for all remaining unasked platforms
   - If the engineer declines the bulk shortcut, ask the next platform and offer again

   **1a. Bulk shortcut** (offered after every selection, for all remaining platforms):
   > **"Are ALL remaining platforms updating to the same new version?"**
   > - Yes *(confirm list → enter one version → done)*
   > - No *(continue asking individually)*

   - If **Yes**:
     1. Show a confirmation list of which platforms this covers (clickable confirmation)
     2. Prompt for the single new IOS XE version — skip to step 3
   - If **No**: ask next platform; offer bulk shortcut again after that selection

2. **New IOS XE version** — only reached if bulk shortcut was never taken
   - One prompt if all updating platforms share the same version
   - One prompt per unique (from, to) pair if they differ

3. **Similarity statement?** — Yes / No
   - If Yes: Product Category → CTN → DTR number (manual entry)

4. **POA&M clearance statement?** — Yes / No
   - If Yes: POA&M/TDR Number → Problem Description (manual entries)

5. **Release notes** — Yes (webfetch) / No (manual date)
   - If No: manual entry for expected date (e.g. `Aug 2026`)

> **No scenario question** — do not ask "All platforms updating vs Mixed" upfront. Jump straight to per-platform status; the bulk shortcut handles the fast path.

> **No DTR approval date prompt** — the revision history date is auto-derived from today's date. Never ask for a DTR approval date for this document type.

---

## What Gets Added Per DTR

### 1. Revision History Row
- Auto-increment version (e.g. `1.0` → `2.0`)
- Normalize all existing date cells to abbreviated month format
- New row: `[version] | [Mon YYYY] | Update for DTR [N] | GCT DP Collaboration`
- Date is auto-derived from today's date (`Mon YYYY` format) — **do NOT prompt the engineer for a DTR approval date**
- The System Description has no DTR approval date field — that prompt belongs to the ICR Memo only

### 2. DTR Section Heading
- Format: `Desktop Review (DTR) [N]`
- Cloned from previous DTR heading with number updated
- **Must include `w:pageBreakBefore` in `w:pPr`** — every DTR heading starts on a new page

### 3. Main Update Paragraph
**For existing platforms updating to a new version:**
`This DTR updates the Session Border Controller (SBC) IOS XE software on [hw list] of SBC router platforms. The IOS XE software version is being updated from [FROM] to [TO].`

**For newly added platforms (no prior version):**
`This DTR adds the Session Border Controller (SBC) IOS XE software on [hw list] of SBC router platforms. The IOS XE software version is [TO].`

- Keep "adds" and "updates" paragraphs separate — never mix new and existing platforms in the same paragraph
- Group updating platforms by `(from_ver, to_ver)` — one paragraph per unique pair
- New platforms always get their own "adds" paragraph
- List format: `A, B, and C` / `A and B` / `A`

### 4. Similarity Paragraph (if included)
`Request certification through similarity based on "[ProdCat] TN: [CTN], DTR[XX]."`
- No leading quote mark
- The TN referenced here is typically a **different** CTN than the one being worked — the engineer will select it from the live folder list at prompt time

### 5. POA&M Paragraph (if included)
`This DTR Clears POA&M/TDR Number: [NUMBER], [PROBLEM DESCRIPTION].`

> **Note:** This is an inline statement inserted into the DTR body paragraph — it is NOT the same as the **POA&M document type** (`Plan of Action & Milestone (POA&M)/`), which is a separate standalone compliance document. The inline statement here simply records that this DTR resolves a previously open finding.

### 6. Sustain Paragraph (per non-updating platform)
`The [Platform] will be sustained on the current software load of [version].`

### 7. Release Notes Paragraph
Default text (no webfetch):
`Release Notes for all devices will be provided once they become available, expected [DATE].`

If engineer accepts webfetch offer (see Release Notes Webfetch section below), replace with one paragraph per updating platform:
`Release Notes Link: [clickable short label]`
- Plain text `Release Notes Link: ` followed immediately by a Word hyperlink
- Short label format: `[Platform] Series Release Notes` (e.g. `C8300/C8200 Series Release Notes`, `C8000v Series Release Notes`)
- URL is embedded as the hyperlink target — not shown as raw text

> **Rule:** Only include release notes for platforms that are **updating** to a new version. Platforms being **sustained** on their current version do NOT get a release notes entry.
>
> **Edge case — all platforms sustained:** If every platform in this DTR is being sustained (no version updates at all), omit the release notes paragraph entirely. Do not insert a fallback paragraph with no context.

### 8. DTR Detailed Component Information Heading
- Text: `DTR Detailed Component Information` (no DTR number)
- Cloned from previous DTR detail heading
- **No `w:pageBreakBefore`** — table flows naturally onto next page if needed

### 9. Component Table
- Cloned from previous DTR's table
- Release column (index 1) updated per platform using regex replace on any `IOS XE .*` string
- Never match by specific version number
- **Sustained platforms must NOT be modified** — only apply the version regex to the row indices belonging to updating platforms. For SBC/CTN2026003, ASR 1006-X = rows 1–3; C8300 = rows 4–6; C8200 = rows 7–9; C8000v = rows 10–12. If a platform is sustained, skip its rows entirely — do not replace its version string even if it matches the regex.

#### New Platform Rows
When a new platform is added, insert **3 rows** before the Notes row, using this exact pattern:

| Column | Row 1 (IWG) | Row 2 (SBC) | Row 3 (IWG/SBC) |
|---|---|---|---|
| Component | `Interworking Gateway on [Platform]` | `Session Border Controller on [Platform]` | `Interworking Gateway/Session Border Controller on [Platform]` |
| Release | `IOS XE X.X` | `IOS XE X.X` | `IOS XE X.X` |
| Sub-component | `N/A` | `N/A` | `N/A` |
| Function | `Interworking Gateway, provides connectivity to AS-SIP trunks.` | `Session Border Controller provides connectivity to AS-SIP trunks.` | `Interworking Gateway/Session Border Controller, provides connectivity to AS-SIP trunks.` |

- Always clone an existing data row's XML as the template for new rows — never build bare rows
- The Function column wording is fixed per row type — do not vary it
- Note: "Interworking Gateway," has a comma; "Session Border Controller provides" has no comma after the subject

---

## Paragraph Order Within Each DTR Section
1. Main update paragraph(s)
2. Similarity paragraph (if included)
3. POA&M paragraph (if included)
4. Sustain paragraph(s) (one per sustained platform)
5. Release Notes paragraph

---

## Post-Generation Steps (Required Every Time)

After `doc.save(OUT)` and the numbering patch complete, always run the validator:

```python
import subprocess
result = subprocess.run(
    ["python3", "_Tools/validate_doc.py", OUT],
    capture_output=True, text=True
)
print(result.stdout)
```

---

## Post-Generation Prompt — Finalize Button

After the draft is saved and validated, always present this clickable prompt using the `question` tool:

> **"Draft saved. What would you like to do next?"**
> - **Finalize** — generate Final .docx + PDF (with signature field)
> - **Commit draft to branch** — skip finalization for now
> - **Done for now** — no further action

### If "Finalize" is selected:

1. Present a confirmation using the `question` tool, showing the exact draft filename:
   > **"Confirm finalization for:"**
   > `[exact Draft_* filename]`
   > - Yes, finalize
   > - Cancel

2. Check prerequisites before running:
   ```bash
   python3 _Tools/finalize_doc.py --check-deps
   ```
   If LibreOffice or pypdf is missing, stop and show the engineer:
   > **"Missing prerequisites for finalization:"**
   > - LibreOffice: `brew install --cask libreoffice`
   > - pypdf: `pip install pypdf`

3. If prerequisites are met, run:
   ```bash
   python3 _Tools/finalize_doc.py [prod_cat] [ctn] [dtr_num] sysdesc "[version]"
  # Use the actual prod_cat, ctn, dtr_num, and version from the current session — do not hardcode.
   ```
   Use the actual prod_cat, ctn, dtr_num, and version from the current session.

4. Report the two output paths on success:
   > **"Finalization complete."**
   > - Final .docx: `System Description/Final/[stem]/[stem].docx`
   > - Final PDF:   `System Description/Final/[stem]/[stem].pdf`
   > *(PDF contains a digital signature field, bottom-right of last page.)*
   > **"Ready to commit?"** → offer the standard branch commit prompt

### Finalize Rules (System Description)
- Only finalize from a validated draft — never from an `Example_*` or `Template_*` file
- `Draft_` prefix is stripped from the filename in all Final outputs — no other filename changes
- The Final folder is named identically to the Final files (without extension)
- The signature field in the PDF is a **placeholder only** — it does not apply a cryptographic signature; it allows a human to sign later in Adobe Acrobat or Adobe Sign
- This is a **test/preview** implementation for System Description; the FA document will have its signature field placed at the existing signature block location in a future update

---

## First DTR from Initial Doc (Special Case)

When building DTR001 from a `DTR000 - INITIAL` document:
- INITIAL doc has different component table structure (11 rows, `IWBC`/`SBC` naming, no Notes row)
- **Preserve the INITIAL component table — do not remove or replace it**
- Use the **Example DTR001** file's component table (14 rows, IWG/SBC naming) as the DTR1 component table
- Insert the full DTR1 section (heading, body paragraphs, detail heading, 14-row table) **after** the INITIAL component table
- Copy `abstractNum` definition from the Example doc into the source doc if not already present

---

## Notes List Numbering
- `numId=13` / `abstractNumId` is the numbered list definition used for Notes rows in **CTN2026003's INITIAL document** — this value is specific to that source doc. For other CTNs, read the actual `numId` from the source document's `word/numbering.xml` before patching.
- Each table's Notes list must restart at `1.`
- Create a new `w:num` with `w:lvlOverride` + `w:startOverride val=1` and unique `numId` per table

---

## Release Notes Webfetch

At Step 9 of the prompt sequence (release notes date), always offer the engineer a clickable option to webfetch the official Cisco release notes for the version(s) being certified.

### Prompt
> **"Would you like to webfetch official Cisco release notes for the new version(s)?"**
> - Yes — fetch and include the release date and URL in the document
> - No — use the expected date entered manually

### Rules
- Only fetch from official `cisco.com` URLs — no third-party sources
- If fetching, extract the **Updated:** date from the page and use it as the release date
- Always present the URL in the document alongside the date
- If a version has no confirmed URL in the table below, warn the engineer and fall back to manual entry
- If the webfetch returns a 404, non-200 status, or does not contain the expected release notes content, do NOT error out — instead prompt the engineer:
  > **"Release notes page not found for [Platform] IOS XE [version]. What is the expected availability date?"**
  - Use the entered date in the standard fallback paragraph: `Release Notes for all devices will be provided once they become available, expected [DATE].`
  - This fallback applies per-platform — a successful fetch and a failed fetch can coexist in the same DTR

### Known Release Notes URLs by Platform and Version

| Platform | IOS XE Version | Release Notes URL |
|---|---|---|
| ASR 1006-X | 17.18.x | `https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/xe-17-18/asr1000-rel-notes-xe-17-18.html` |
| ASR 1006-X | 17.16.x | `https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/xe-17-16/asr1000-rel-notes-xe-17-16.html` |
| ASR 1006-X | 17.15.x | `https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/xe-17-15/asr1000-rel-notes-xe-17-15.html` |
| C8300 / C8200 | 26.1.x | `https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/rel_notes/26-x/release-notes-catalyst-8200-and-catalyst-8300-series-edge-platforms-release-26-1-x.html` |
| C8300 / C8200 | 17.18.x | `https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/rel_notes/17-18-x/release-notes-catalyst-8200-and-catalyst-8300-series-edge-platforms-release-17-18-x.html` |
| C8300 / C8200 | 17.16.x | `https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/rel_notes/17-16-x/cat8200-and-8300-rel-notes-xe-17-16-x.html` |
| C8000v | 26.1 | `https://www.cisco.com/c/en/us/td/docs/routers/C8000V/Release-Notes/c8000v-releasenotes-26-1.html` |
| C8000v | 17.18.x | `https://www.cisco.com/c/en/us/td/docs/routers/C8000V/Release-Notes/c8000v-releasenotes-17-18.html` |

> **URL pattern notes:**
> - ASR 1000: `.../asr1000/release/notes/xe-[version]/asr1000-rel-notes-xe-[version].html`
> - C8300/C8200 (17.x): `.../cloud_edge/c8300/rel_notes/[version]/cat8200-and-8300-rel-notes-xe-[version].html`
> - C8300/C8200 (26.x): `.../cloud_edge/c8300/rel_notes/26-x/release-notes-catalyst-8200-and-catalyst-8300-series-edge-platforms-release-26-1-x.html`
> - C8000v (17.x): `.../C8000V/Release-Notes/c8000v-releasenotes-[version].html`
> - C8000v (26.x): `.../C8000V/Release-Notes/c8000v-releasenotes-26-1.html`
>
> For any version not in this table, construct the URL from the pattern and verify it with a live webfetch before presenting to the engineer.

---

## Known Issues

| # | Issue | Resolution |
|---|---|---|
| 1 | Reference doc component table version differs from expected (e.g. `17.15` not `17.18`) | Replace any `IOS XE .*` in Release column — never match specific version |
| 2 | INITIAL doc table has 11 rows with `IWBC` naming — wrong structure for DTR001+ | Clone table from Example DTR001 reference file instead |
| 3 | Notes list numbering resets incorrectly across tables | Use `w:lvlOverride` + unique `numId` per table |
| 4 | Word lock file (`~$*.docx`) appears when doc is open | Close the document in Word before regenerating |
| 5 | New DTR body paragraphs cloned as wrong style (Heading1 instead of BodyText) | Identify a `BodyText` paragraph from DTR1 section as clone template — not the heading element |
| 6 | New DTR headings render at wrong size (missing `w:sz`) | Clone full `w:rPr` from source run when building new paragraphs — don't build bare runs |
| 7 | Detail heading incorrectly numbered (`DTR 2 Detailed Component Information`) | Always use fixed text `DTR Detailed Component Information` — no DTR number in this heading |
| 8 | DTR sections and Management Description don't start on a new page | Add `w:pageBreakBefore` to `w:pPr` of every `Desktop Review (DTR)` heading and `Management Description` heading only — **not** `DTR Detailed Component Information` (table must flow freely) |
| 9 | TOC and `System Description` body heading don't start on a new page | On document creation: insert an empty paragraph with `w:pageBreakBefore` before the `<sdt>` TOC block; add `w:pageBreakBefore` to the `System Description` `Heading1` paragraph; remove any empty `Heading1` spacer between them |
| 10 | Detail heading text doubles (`DTR Detailed Component InformationDTR Detailed...`) when cloned from example | Example heading has 3 runs — set text in run 0 only, blank all other runs; never iterate all runs and set text on each |
| 11 | Sustained platform rows in component table get version-updated anyway | The version regex must only be applied to row indices of **updating** platforms — skip sustained platform rows by index. For SBC/CTN2026003: ASR 1006-X = rows 1–3 (skip if sustained), C8300 = 4–6, C8200 = 7–9, C8000v = 10–12. |

---

## Generation Status

- [x] Example/Template file placed in `Examples & Templates/`
- [x] Table structure documented
- [x] Paragraph patterns documented
- [x] First draft generated and validated
- [x] Skill file updated with confirmed rules
