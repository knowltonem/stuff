# ICR Automation — Skill: Plan of Action & Milestone (POA&M)
> Load `skill_base.md` first. This file defines rules specific to the **Plan of Action & Milestone (POA&M)** document type only.

---

## Document Identity
- **Full Name:** Cisco ICR Plan of Action & Milestone
- **Abbreviation:** POA&M
- **Folder:** `Plan of Action & Milestone (POA&M)/`
- **Filename Suffix:** `Cisco ICR POAM.docx`

---

## Purpose
The POA&M documents open security findings, deficiencies, or vulnerabilities identified during the ICR review process, along with planned corrective actions and target completion milestones. Each POA&M is a **standalone document for a single finding** — one finding per POA&M, tied to a specific TDR number. POA&Ms are only created when a new finding requires a corrective action plan.

> **Important — POA&M disambiguation:**
> The `skill_base.md` "POA&M Inline Statement" section describes the **inline statement** inserted into other document types (e.g. System Description) in the format `This DTR Clears POA&M/TDR Number: [NUMBER], [PROBLEM DESCRIPTION].`
> This skill file (`skill_poam.md`) governs the **standalone POA&M document type** (`Plan of Action & Milestone (POA&M)/`), which is a separate deliverable with its own paragraph structure and generation rules.
> Do not confuse the two. The inline statement rules in `skill_base.md` do NOT describe how to generate the POA&M document.

---

## Document Structure

The POA&M is a **paragraph-based document with no tables**. All paragraphs use the `Normal` style — section differentiation is done through bold formatting within runs, not through paragraph styles. The structure is nearly identical to the TDR, with two additional sections at the end.

### Paragraph Layout

| Para Index | Content | Notes |
|---|---|---|
| P00 | Cisco logo image | Do not modify |
| P01 | (empty) | Spacer |
| P02 | `Plan Of Action and Milestone (POA&M)` | Title — bold, centered |
| P03 | (empty) | Spacer |
| P04 | `Cisco GCT DP Session Border Controller (SBC)` | Product name — **auto-populated** |
| P05 | `with Software Release IOS XE [VERSION]` | Software version — **auto-populated** |
| P06-07 | (empty) | Spacers |
| P08 | `TDR Number:  [NUMBER]` | TDR number — **manual entry** (references the associated TDR) |
| P09 | (empty) | Spacer |
| P10 | `Requirement:  [UCR section(s)]` | **Auto-formatted** from clickable prompt — same grouped prompt as TDR (see `skill_tdr.md` Requirement Prompt) |
| P11 | (empty) | Spacer |
| P12 | `Criticality:  [UCR req] [Required: ...] [Optional: ...]` | **Manual entry** |
| P13 | (empty) | Spacer |
| P14 | `Finding:  [SHORT DESCRIPTION]` | **Manual entry** — entered as-is (not forced to all caps) |
| P15 | (empty) | Spacer |
| P16 | `Description of product:` | Section header (bold) |
| P17 | Product description text | **Auto-populated** from existing TDR/POA&M or example |
| P18-21 | (empty) | Spacers |
| P22 | `Problem Description:` | Section header (bold) |
| P23 | (empty) | Spacer |
| P24 | Problem description text | **Manual entry** |
| P25 | (empty) | Spacer |
| P26 | `Condition of test:` | Section header (bold) |
| P27 | (empty) | Spacer |
| P28 | `Test Scenario:` | Sub-header |
| P29+ | Test scenario steps | **Manual entry** |
| — | (empty) | Spacer |
| — | `Test Result:` | Section header (bold) |
| — | Test result steps | **Manual entry** |
| — | (empty) | Spacer |
| — | `Note:  [optional note]` | Optional note field |
| — | (empty) | Spacer |
| — | `Expected behavior:` | Section header (bold) |
| — | Expected behavior text | **Manual entry** |
| — | (empty) | Spacer |
| — | `Component(s) Affected:  [components]` | **Auto-formatted** from clickable prompts — same two-step prompt as TDR (see `skill_tdr.md` Components Affected Prompt) |
| — | (empty) | Spacer |
| — | `Cisco GCT DP Evaluation:` | Section header (bold) — **POA&M-specific** |
| — | Evaluation text (may be multi-paragraph) | **Manual entry** |
| — | (empty) | Spacer(s) |
| — | `Cisco GCT DP Plan of Action & Milestones:` | Section header (bold) — **POA&M-specific** |
| — | Plan of action text | **Manual entry** |

> **Note:** Paragraph indices after P17 shift depending on the length of the product description and number of test scenario / test result steps. The layout above uses `—` for paragraphs whose index is dynamic.

### Label Format
- Inline label fields use **double space** after the colon: `Label:  value`
- Section headers end with a colon and are on their own line: `Problem Description:`
- Empty spacer paragraphs separate each section

---

## Field Classification

### Auto-Populated Fields
| Field | Source | Notes |
|---|---|---|
| Product Name (P04) | CTN / product category | `Cisco GCT DP Session Border Controller (SBC)` for SBC |
| Software Version (P05) | Current DTR version | `with Software Release IOS XE [VERSION]` |
| Description of product | Previous TDR/POA&M or example | Reuse product description paragraph |

### Manual Entry Fields
| Field | Prompt Text |
|---|---|
| TDR Number | Clickable selection from existing TDR documents on disk (with POA&M status) |
| Requirement | Clickable grouped multi-select prompt — same as TDR (see `skill_tdr.md` Requirement Prompt) |
| Criticality | `Criticality (e.g. SCM-012040 [Required: AEI, SC, SS] [Optional: PEI]):` |
| Finding | `Finding summary (short description):` |
| Problem Description | `Problem description (what went wrong):` |
| Test Scenario Steps | `Test scenario steps (one per line):` |
| Test Diagram | Clickable prompt: **Provide file path**, **Paste image**, or **No image (add later)** |
| Test Result Steps | `Test result steps (one per line):` |
| Note | `Optional note (leave blank to skip):` |
| Expected Behavior | `Expected behavior:` |
| Components Affected | Two-step clickable prompt — same as TDR (see `skill_tdr.md` Components Affected Prompt) |
| Cisco GCT DP Evaluation | `Cisco GCT DP Evaluation (multi-line, blank line to finish):` |
| Plan of Action & Milestones | `Cisco GCT DP Plan of Action & Milestones:` |

---

## Shared Prompts with TDR

The following prompts are **identical** to the TDR document type and follow the same rules defined in `skill_tdr.md`:

1. **Requirement Prompt** — two-step grouped clickable multi-select (Groups A/B/C with "None from this group" option)
2. **Components Affected Prompt** — two-step clickable (component multi-select + per-component IWBC/SBC/Both classification with label pluralization)
3. **Test Diagram Prompt** — three clickable options: Provide file path, Paste image, No image (add later)

> When implementing these prompts during `newd`, follow the exact same flow documented in `skill_tdr.md`. Do not duplicate the prompt definitions here — reference `skill_tdr.md`.

---

## POA&M-Specific Sections (not in TDR)

### Cisco GCT DP Evaluation
- Section header: `Cisco GCT DP Evaluation:` (bold)
- Content is **multi-paragraph** — engineer enters lines one at a time (blank line to finish)
- Each line becomes a separate paragraph in the document
- Empty spacer paragraph between the header and the first content paragraph
- Describes Cisco's technical analysis of the finding

### Cisco GCT DP Plan of Action & Milestones
- Section header: `Cisco GCT DP Plan of Action & Milestones:` (bold)
- Content is typically a **single paragraph** — engineer enters the corrective action and timeline
- Empty spacer paragraph between the header and the content paragraph
- Example: `Cisco will provide a fix by Q4 FY2024.`

---

## Prompt Sequence (POA&M-specific — after base steps 1-3)

After selecting POA&M as the document type, the following prompts apply:

1. **IOS XE Version** — software version for this POA&M
2. **TDR Number** — clickable selection from existing TDR documents on disk:
   - Scan the TDR folder (`Test Discrepancy Report (TDR)/`) for all TDR numbers (from filenames in `Examples & Templates/`, `Drafts/`, and `Final/`; exclude `Template_*` and `Example_*` prefixed files that don't contain a real TDR number)
   - Scan the POA&M folder (`Plan of Action & Milestone (POA&M)/`) for existing POA&M drafts/finals
   - Present each TDR number as a clickable option with status:
     - `TDR 26003-01 — no POA&M yet` (available)
     - `TDR 26003-02 — POA&M exists` (already has one — warn but allow selection)
   - Custom entry option is enabled for TDR numbers not yet on disk
3. **Requirement** — clickable grouped multi-select from UCR sections (same as TDR)
4. **Criticality** — UCR requirement + required/optional products
5. **Finding** — short description
6. **Problem Description** — what went wrong
7. **Test Scenario Steps** — one per line (multi-line entry)
8. **Test Diagram Image** — clickable prompt: Provide file path, Paste image, or No image (add later)
9. **Test Result Steps** — one per line (multi-line entry)
10. **Note** — optional note (can skip)
11. **Expected Behavior** — what should have happened
12. **Components Affected** — two-step clickable prompt (same as TDR)
13. **Cisco GCT DP Evaluation** — multi-line entry (blank line to finish)
14. **Plan of Action & Milestones** — corrective action and timeline

> Product name and description of product are auto-populated — no prompt needed.

---

## File Naming
| File Type | Pattern |
|---|---|
| Source/Reference | `CTN[number] - DTR[###] - TDR[number] - [ProdCat] - IOS XE [ver] - Cisco ICR POAM.docx` |
| Draft | `Draft_CTN[number] - DTR[###] - TDR[number] - [ProdCat] - IOS XE [ver] - Cisco ICR POAM.docx` |
| Template | `Template_CTN0000000 - DTR000 - TDR00000-00 - ProdCat - Prod&Ver - Cisco ICR POAM.docx` |
| Example | `Example_CTN[number] - DTR[###] - TDR[number] - [ProdCat] - IOS XE [ver] - Cisco ICR POAM.docx` |

- TDR number in filename matches the associated TDR finding
- DTR number reflects which DTR the finding was discovered during

---

## Source Document Selection
- Always use the **Template** file as the base: `Template_CTN0000000 - DTR000 - TDR00000-00 - ProdCat - Prod&Ver - Cisco ICR POAM.docx`
- For the **Description of product** field: extract from the most recent existing TDR or POA&M (or from the DTR001 example if none exist)
- POA&Ms are standalone — they do not chain from one to the next like DTR documents

---

## Product Name Map (SBC — CTN2026003)
| Product Category | Product Name (P04) |
|---|---|
| SBC | `Cisco GCT DP Session Border Controller (SBC)` |

---

## Differences from TDR

| Aspect | TDR | POA&M |
|---|---|---|
| Extra sections | None | Cisco GCT DP Evaluation + Plan of Action & Milestones |
| TDR Number field | Auto-incremented | Manual entry (references the associated TDR) |
| Purpose | Documents the finding | Documents the corrective action plan for the finding |
| Document suffix | `Cisco ICR TDR.docx` | `Cisco ICR POAM.docx` |

---

## Known Issues

| # | Issue | Resolution |
|---|---|---|
| 1 | Template has a TDR numbering note at P08 | Remove this note paragraph when generating a draft |
| 2 | Template has `<insert ...>` placeholders | Replace all placeholders with actual values |
| 3 | Template has no test diagram image | Insert engineer-provided image at the correct position |
| 4 | Example Finding is ALL CAPS | Finding field is entered as-is — do not force case |
| 5 | Example product name includes "23" suffix (`SBC 23`) | Use standard product name from Product Name Map — no numeric suffix |

---

## Generation Status
- [x] Example/Template file placed in `Examples & Templates/`
- [x] Table structure documented (no tables — paragraph-based)
- [x] Paragraph patterns documented
- [x] First draft generated and validated
- [x] Skill file updated with confirmed rules
