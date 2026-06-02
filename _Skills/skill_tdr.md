# ICR Automation — Skill: Test Discrepancy Report (TDR)
> Load `skill_base.md` first. This file defines rules specific to the **Test Discrepancy Report (TDR)** document type only.

---

## Document Identity
- **Full Name:** Cisco ICR Test Discrepancy Report
- **Abbreviation:** TDR
- **Folder:** `Test Discrepancy Report (TDR)/`
- **Filename Suffix:** `Cisco ICR TDR.docx`

---

## Purpose
The TDR documents test discrepancies identified during the ICR testing process. Each TDR is a **standalone document for a single finding** — one finding per TDR. TDRs are only created when a new finding is discovered; they are **not updated per DTR** (unlike other document types that get carried forward with each DTR).

TDR numbers are referenced in other documents' POA&M inline statements:
`This DTR Clears POA&M/TDR Number: [NUMBER], [PROBLEM DESCRIPTION].`

---

## TDR Number Format
- Format: `[CTN last 5 digits]-[sequence]` (zero-padded to 2 digits)
- Examples: `26003-01`, `26003-02`, `26003-03`
- **Auto-incremented:** Read existing TDRs from `Examples & Templates/` and `Drafts/` to determine the next sequence number
- The TDR number appears in both the filename and the `TDR Number:` field in the document

---

## Document Structure

The TDR is a **paragraph-based document with no tables**. All paragraphs use the `Normal` style — section differentiation is done through bold formatting within runs, not through paragraph styles.

### Paragraph Layout

| Para Index | Content | Notes |
|---|---|---|
| P00 | Cisco logo image | Do not modify |
| P01 | (empty) | Spacer |
| P02 | `Test Discrepancy Report (TDR)` | Title — bold, centered |
| P03 | (empty) | Spacer |
| P04 | `Cisco GCT DP Session Border Controller (SBC)` | Product name — **auto-populated** |
| P05-06 | (empty) | Spacers |
| P07 | `TDR Number:  [NUMBER]` | TDR number — **auto-populated** |
| P08 | `*Note: TDR number is...` | TDR numbering note — **remove when generating** |
| P09 | (empty) | Spacer |
| P10 | `Requirement:  [UCR section(s)]` | **Auto-formatted** from clickable prompt — see Requirement Prompt below |
| P11 | (empty) | Spacer |
| P12 | `Criticality:  [UCR req] [Required: ...] [Optional: ...]` | **Manual entry** |
| P13 | (empty) | Spacer |
| P14 | `Finding:  [SHORT DESCRIPTION]` | **Manual entry** |
| P15 | (empty) | Spacer |
| P16 | `Description of product:` | Section header (bold) |
| P17 | (empty) | Spacer |
| P18 | Product description text | **Auto-populated** from previous TDRs |
| P19 | (empty) | Spacer |
| P20 | `Problem Description:` | Section header (bold) |
| P21 | (empty) | Spacer |
| P22 | Problem description text | **Manual entry** |
| P23 | (empty) | Spacer |
| P24 | `Condition of test:` | Section header (bold) |
| P25 | (empty) | Spacer |
| P26 | `Test Scenario:` | Sub-header |
| P27 | Test scenario / diagram placeholder | **Manual entry** |
| P28-29 | (empty) | Spacers |
| P30 | `Test Result:` | Section header (bold) |
| P31 | (empty) | Spacer |
| P32 | Test result text | **Manual entry** |
| P33-34 | (empty) | Spacers |
| P35 | `Expected behavior:` | Section header (bold) |
| P36 | (empty) | Spacer |
| P37 | Expected behavior text | **Manual entry** |
| P38 | (empty) | Spacer |
| P39 | `Component(s) Affected:  [components]` | **Auto-formatted** from clickable prompts — label pluralizes with count when multiple selected |

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
| TDR Number (P07) | Auto-incremented | Read existing TDRs, increment sequence |
| Description of product (P18) | Previous TDR or INITIAL | Reuse product description paragraph |

### Manual Entry Fields
| Field | Prompt Text |
|---|---|
| Requirement (P10) | Clickable multi-select prompt (see Requirement Prompt below) |
| Criticality (P12) | `Criticality (e.g. SCM-012040 [Required: AEI, SC, SS] [Optional: PEI]):` |
| Finding (P14) | `Finding summary (short description):` |
| Problem Description (P22) | `Problem description (what went wrong):` |
| Test Scenario (P27) | `Test scenario steps (one per line):` |
| Test Diagram | Clickable prompt: **Provide file path** or **No image (add later)** |
| Test Result (P32) | `Test result steps (one per line):` |
| Expected behavior (P37) | `Expected behavior:` |
| Components Affected (P39) | Two-step clickable prompt (see Components Affected Prompt below) |

---

## Test Scenario Diagram
- Engineer is prompted with a clickable selection:
  1. **Provide file path** — enter the absolute path to the image file on disk
  2. **No image (add later)** — skip the diagram; the engineer will add it manually after generation
- Inserted at the diagram position (P27 in Template)
- Captioned with `Figure 1: SUT Test Scenario` (added by engineer or runner after image insertion)

---

## Requirement Prompt

The Requirement field (P10) uses a **two-step grouped clickable prompt** to avoid UI issues with large option lists.

> **Why grouped?** The question tool's multi-select breaks when presented with 30+ options. Splitting into groups keeps each prompt under 15 options.

### Step 1 — Select UCR group(s) (multi-select enabled):

| Label | Description |
|---|---|
| Sections 2.6–2.12 | Sections 2.6.1, 2.6.2, 2.7, 2.7.1, 2.7.2, 2.7.4, 2.11, 2.11.2, 2.12.4, 2.12.4.1, 2.12.4.2, 2.12.4.3 |
| Sections 2.16–2.17 | Sections 2.16, 2.16.13, 2.17, 2.17.1–2.17.11 |
| Sections 2.19, 4.2 & Other | Sections 2.19, 2.19.1, 2.19.2, 4.2, ASSIP, IPv6 |

> The Question tool's `custom` option is enabled — the engineer can also type a custom requirement not in the list, skipping step 2.

### Step 2 — Select specific section(s) within each chosen group (multi-select enabled):

> Each group prompt includes a **"None from this group"** option as the first choice. If selected, skip that group and move to the next. At least one section must be selected across all groups (do not allow all groups to return "None").

**Group A — Sections 2.6–2.12** (12 options + None):
| Option |
|---|
| None from this group |
| Section 2.6.1 |
| Section 2.6.2 |
| Section 2.7 |
| Section 2.7.1 |
| Section 2.7.2 |
| Section 2.7.4 |
| Section 2.11 |
| Section 2.11.2 |
| Section 2.12.4 |
| Section 2.12.4.1 |
| Section 2.12.4.2 |
| Section 2.12.4.3 |

**Group B — Sections 2.16–2.17** (13 options + None):
| Option |
|---|
| None from this group |
| Section 2.16 |
| Section 2.16.13 |
| Section 2.17 |
| Section 2.17.1 |
| Section 2.17.2 |
| Section 2.17.3 |
| Section 2.17.4 |
| Section 2.17.5 |
| Section 2.17.6 |
| Section 2.17.7 |
| Section 2.17.8 |
| Section 2.17.9 |
| Section 2.17.10 |
| Section 2.17.11 |

**Group C — Sections 2.19, 4.2 & Other** (6 options + None):
| Option |
|---|
| None from this group |
| Section 2.19 |
| Section 2.19.1 |
| Section 2.19.2 |
| Section 4.2 |
| ASSIP |
| IPv6 |

> If multiple groups are selected, present each group's multi-select prompt sequentially. Combine all selections into a single output.

**Output format:** `UCR 2013 Change 2, [selections joined with ", "]`
- Example (single): `UCR 2013 Change 2, Section 2.7.1`
- Example (multiple): `UCR 2013 Change 2, Section 2.7.1, Section 2.17.3`
- Example (non-section): `UCR 2013 Change 2, ASSIP`
- Example (mixed): `UCR 2013 Change 2, Section 2.6.1, IPv6`

---

## Components Affected Prompt

The Components Affected field (P43) uses a two-step clickable prompt:

**Step 1 — Select component(s)** (multi-select enabled):
| Option | Label |
|---|---|
| c8000v | c8000v |
| c8200 | c8200 |
| c8300 | c8300 |
| ISR 4461/K9 | ISR 4461/K9 |
| ASR-1006 | ASR-1006 |

**Step 2 — Classify each selected component** (one prompt per component):
> For each component selected in step 1, present a clickable prompt:
> `"Classification for [component]:"`
> - **IWBC**
> - **SBC**
> - **Both (IWBC, SBC)**

**Output format:** Comma-separated list: `Cisco [component] ([class]), Cisco [component] ([class])`
- Example (single): `Cisco c8200 (IWBC)`
- Example (multiple): `Cisco c8200 (IWBC), Cisco ASR-1006 (SBC)`
- Example (both): `Cisco c8300 (IWBC, SBC)`

**Label pluralization:**
- 1 component selected → label is `Component Affected:  [value]`
- 2+ components selected → label is `Components Affected (x[N]):  [value]`
- Examples:
  - `Component Affected:  Cisco c8200 (IWBC)`
  - `Components Affected (x3):  Cisco c8200 (IWBC), Cisco ASR-1006 (SBC), Cisco c8300 (IWBC, SBC)`

---

## Prompt Sequence (TDR-specific — after base steps 1-3)

After selecting TDR as the document type, the following prompts apply:

1. **IOS XE Version** — software version for this TDR (auto-populates P05)
2. **TDR Number** — auto-suggested based on existing TDRs; confirm or override
3. **Requirement** — clickable multi-select from UCR sections, or type custom
4. **Criticality** — UCR requirement + required/optional products
5. **Finding** — short description
6. **Problem Description** — what went wrong
7. **Test Scenario Steps** — one per line (multi-line entry)
8. **Test Diagram Image** — clickable prompt: Provide file path or No image (add later)
9. **Test Result Steps** — one per line (multi-line entry)
10. **Note** — optional note (can skip)
11. **Expected Behavior** — what should have happened
12. **Components Affected** — two-step clickable prompt: select component(s), then classify each as IWBC/SBC/Both

> Product name and description of product are auto-populated — no prompt needed.

---

## File Naming
| File Type | Pattern |
|---|---|
| Source/Reference | `CTN[number] - DTR[###] - TDR[number] - [ProdCat] - IOS XE [ver] - Cisco ICR TDR.docx` |
| Draft | `Draft_CTN[number] - DTR[###] - TDR[number] - [ProdCat] - IOS XE [ver] - Cisco ICR TDR.docx` |
| Template | `Template_CTN0000000 - DTR000 - TDR00000-00 - ProdCat - Prod&Ver - Cisco ICR TDR.docx` |

- TDR number in filename matches the `TDR Number:` field in the document
- DTR number reflects which DTR the finding was discovered during

---

## Source Document Selection
- Always use the **Template** file as the base: `Template_CTN0000000 - DTR000 - TDR00000-00 - ProdCat - Prod&Ver - Cisco ICR TDR.docx`
  > **Note:** Some machines may have a `(2)` download artifact in the filename. Verify the canonical template filename on disk using a glob (`Template_*TDR*.docx`) and use whichever file is present.
- For the **Description of product** field: extract from the most recent existing TDR (or from the DTR001 example if no previous TDRs exist)
- TDRs are standalone — they do not chain from one to the next like DTR documents

---

## Product Name Map (SBC — CTN2026003)
| Product Category | Product Name (P04) |
|---|---|
| SBC | `Cisco GCT DP Session Border Controller (SBC)` |

---

## Known Issues

| # | Issue | Resolution |
|---|---|---|
| 1 | Template has a TDR numbering note at P08 | Remove this note paragraph when generating a draft |
| 2 | Template has `<insert ...>` placeholders | Replace all placeholders with actual values |
| 3 | Template has no test diagram image | Insert engineer-provided image at the correct position |
| 4 | DTR001 example uses `IOS XE 17.12` in P05 but filename says `IOS XE 17.18` | Filename version may differ from body version — always use the version provided by the engineer, never pull version from the filename |
| 5 | IO Example file (`Example IO_TDR_Vendor_POAMs_...`) uses a different format (no Criticality, different header, Vendor Evaluation/POA&M sections) | **Reference only** — not used for generation. Uses an older external IO format with different TDR numbering (`CIS-1824-001`) and component labeling. Our generation follows the Template and DTR001 Example format. |

---

## Generation Status
- [x] Example/Template file placed in `Examples & Templates/`
- [x] Table structure documented (no tables — paragraph-based)
- [x] TDR numbering confirmed
- [x] Paragraph patterns documented
- [x] First draft generated and validated
- [x] Skill file updated with confirmed rules
