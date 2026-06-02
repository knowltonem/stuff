# ICR Automation — Base Skill
> This file is loaded by ALL document type skills. It defines shared rules, prompt sequences, formatting standards, and folder logic that apply across every document type.

---

## MANDATORY SESSION-START PROTOCOL — NO EXCEPTIONS

**At the start of every session — before answering any question, taking any action, or responding to any engineer request — OpenCode must:**

1. Read `_Skills/skill_base.md` in full (this file)
2. Read `_Runbook/ICR_Automation_Runbook.md` in full

**This applies to ALL requests, including:**
- Questions about project state, DTR history, or file existence
- Requests to delete, generate, or modify files
- Any `newd`, `qac`, `/adt`, or shortcut command

**Do not rely on session summaries, memory, or prior context. Reading from disk is the only acceptable source of truth. Operating from recalled approximations is a protocol violation.**

---

## Project Context
- **Project:** Cisco ICR (Internal Compliance Review) Document Automation
- **Working Directory:** Determined live from the current environment — never hardcoded
- **Purpose:** Automate the creation and incremental updating of ICR document suites across multiple product categories, CTNs, and Cisco product lines
- **Scope:** Covers all Cisco product families — routers, switches, wireless, data center, collaboration, and others. Not limited to IOS XE or any single OS/platform type. Product-specific software versions, platform names, and OS types are defined in the per-doc-type skill file, not here.
- **Multi-engineer environment:** GitHub repository shared across the team

---

## Shortcut Commands
| Shortcut | Action |
|---|---|
| `prnts` | Print the live folder structure from disk |
| `newd` | Begin DTR generation — auto-syncs runbook first, then starts prompt sequence. **Must read `skill_base.md` before presenting any prompts. All prompts must use the `question` tool as clickable selections — never plain text lists. No exceptions.** |
| `new dtr` | Same as `newd` — alternate trigger for DTR generation. Same rules apply. |
| `finalize` | Finalize a draft — generates a Final .docx (no Draft_ prefix) and a PDF with a digital signature field, saved under `Final/<document name>/` inside the document type folder. Always offer this automatically after every successful draft generation. See per-doc-type skill for full flow. `finalize_doc.py` is implemented for all doc types; each per-doc-type skill may have additional cross-check steps. **PDF signature field injection requires manual completion in Acrobat/Adobe Sign if `pypdf` cannot inject automatically.** |
| `myb` | Show the current git branch name |
| `cm1` | Commit and push all staged changes to `main` (requires confirmation) |
| `sbh` | Show branch health — fetch latest and display ahead/behind status for all three branches vs main |
| `sync` | Sync `edknowlt` with `origin/main` — push local, pull from main, push again: `git push origin edknowlt && git pull --no-rebase origin main && git push origin edknowlt` |
| `/adt` | Run a full audit of all Python scripts and markdown files — scans for bugs, stale references, dirty code, and documentation gaps. Also triggered by `qac`. **Must read `skill_base.md` before running — no exceptions. See QAC Protocol below for mandatory review-and-confirm flow.** |
| `qac` | Same as `/adt` — alternate trigger for full audit. Same rules apply. |

---

## QAC Protocol

> **This protocol applies every time `qac` or `/adt` is triggered — no exceptions.**

### Step 1 — Audit and Report
Run the full audit (Pass 1: Python, Pass 2: Markdown). Collect all issues found.

Present a **complete issue report** to the engineer before touching any file. Format:

| # | File | Issue | Recommended Fix | Severity |
|---|---|---|---|---|
| 1 | `file.py:line` | Description of the problem | What should be changed | Critical / Warning / Info |

If no issues are found, state: **"QAC complete — no issues found."** and stop.

### Step 2 — Confirm Before Fixing
After presenting the report, prompt the engineer using the `question` tool:

> **"QAC found N issue(s). How would you like to proceed?"**
> - **Fix all** — apply every recommended fix
> - **Select fixes** — choose which issues to fix (follow-up multi-select prompt listing each issue by number)
> - **No fixes** — report only, make no changes

### Step 3 — Apply Selected Fixes
- If **Fix all**: apply every fix in order, report each one as it's applied.
- If **Select fixes**: present a multi-select `question` prompt listing all issues by number + short description. Apply only the selected ones.
- If **No fixes**: acknowledge and stop — do not modify any file.

### Rules
- **Never auto-apply fixes.** The confirm prompt is mandatory — skipping it is a protocol violation.
- Apply fixes one at a time and confirm each one in output before moving to the next.
- After all fixes are applied, state the final count: **"N fix(es) applied."**

---

## Interrupted Session Recovery

If an engineer's session was interrupted, dismissed, or they want to start over at any point during a `newd` sequence, the AI must:

1. Acknowledge the interruption with a short message:
   > *"No problem — starting fresh. Type `newd` to begin a new DTR generation session."*
2. **Discard all in-progress prompt answers** from the previous sequence — do not carry forward any Product Category, CTN, Document Type, or version selections from the interrupted session
3. Wait for the engineer to type `newd` before starting again — do not auto-restart

**Triggers for this recovery:**
- Engineer says their session was interrupted, dismissed, closed, or stopped
- Engineer says "start over", "restart", "fresh start", or similar
- Engineer types `newd` after a visibly incomplete prior `newd` sequence in the same session

> **There is no resume.** Every `newd` always starts from step 1 — Product Category. This is intentional: an interrupted session may have had partial answers the engineer no longer wants.

---

## DTR Generation Prompt List

> **MANDATORY FIRST STEP — NO EXCEPTIONS:** Before presenting any prompts, OpenCode must read `_Skills/skill_base.md` in full. Do not rely on memory or session summaries. Operating from recalled approximations is a protocol violation.

> **ALL PROMPTS MUST USE THE `question` TOOL AS CLICKABLE SELECTIONS — NEVER PLAIN TEXT LISTS. NO EXCEPTIONS.** This applies to every step in the `newd` sequence including the fork, Product Category, CTN, Document Type, and all per-doc-type skill prompts.

When an engineer types `newd` or `new dtr`, the AI will:
1. Run `python3 _Runbook/runbook_updater.py --once`
2. Present the fork using the `question` tool:

> **"What would you like to do?"**
> - **New DTR** — increment an existing CTN (next DTR number on an existing product)
> - **New Initial TN** — brand new TN from scratch (new CTN, no documents yet)

---

### Fork A — New DTR

> All steps below must use the `question` tool as clickable selections. Read options live from disk — never hardcode.

1. **Product Category** — present all folder names read live from `Product Category/`, plus **"+ New Product Category"**
   - If **"+ New Product Category"** selected:
     1. Prompt: *"Enter the new product category name:"* (manual entry)
     2. Create the folder: `Product Category/<name>/`
     3. Confirm creation, then continue to Step 2 with the new category selected.

2. **CTN** — present all CTN folder names read live from the chosen product category folder, plus **"+ New CTN"**
   - If **"+ New CTN"** selected:
     1. Prompt: *"Enter the new CTN number (e.g. CTN2026004):"* (manual entry)
     2. Run: `python3 _Tools/scaffold_ctn.py <ProductCategory> <CTN>`
     3. Confirm the 9 doc type folders were created, then continue to Step 3 with the new CTN selected.

3. **Document Type** — present all doc type folder names read live from the chosen CTN folder.
   - **After step 3, immediately read the matching skill file (see Document Type Router below) before asking any further questions.**
   - All prompts from step 4 onward are defined in the per-doc-type skill file.

---

### Fork B — New Initial TN

> All steps below must use the `question` tool as clickable selections. Read options live from disk — never hardcode.

1. **Product Category** — present all folder names read live from `Product Category/`, plus **"+ New Product Category"**
   - If **"+ New Product Category"** selected:
     1. Prompt: *"Enter the new product category name:"* (manual entry)
     2. Create the folder: `Product Category/<name>/`
     3. Confirm creation, then continue to Step 2 with the new category selected.

2. Prompt: *"Enter the new CTN number (e.g. CTN2026004):"* (manual entry)
   - Run: `python3 _Tools/scaffold_ctn.py <ProductCategory> <CTN>`
   - Confirm the 9 doc type folders were created.

3. **Stop and instruct the engineer:**
   > *"Folders are ready for [ProdCat]/[CTN]. Before generating any DTRs:*
   > *Place a `CTN[number] - DTR000 - INITIAL - [ProdCat] - Cisco ICR [DocType].docx` file in each document type's `Examples & Templates/` folder.*
   > *When ready, type `newd` → New DTR to begin generation."*

---

## Document Type Router

When the engineer selects a document type in step 3, immediately read the matching skill file before continuing. That skill file defines all remaining prompts, paragraph formats, table rules, and generation logic for that document type.

| Document Type Selected | Skill File to Read | Runner Script to Read |
|---|---|---|
| System Description | `_Skills/skill_system_description.md` | `_Tools/run_sysdesc.py` |
| Cybersecurity Summary Report (CSR) | `_Skills/skill_csr.md` | `_Tools/run_csr.py` |
| Functionality Attestation (FA) | `_Skills/skill_fa.md` | `_Tools/run_fa.py` |
| ICR Summary Memorandum (ICR Memo) | `_Skills/skill_icr_memo.md` | `_Tools/run_icr_memo.py` |
| Military Unique Deployment Guide (MUDG) | `_Skills/skill_mudg.md` | `_Tools/run_mudg.py` |
| Letter Of Compliance (LoC) | `_Skills/skill_loc.md` | `_Tools/run_loc.py` |
| Plan of Action & Milestone (POA&M) | `_Skills/skill_poam.md` | `_Tools/run_poam.py` |
| System Diagram | `_Skills/skill_system_diagram.md` | `_Tools/run_system_diagram.py` |
| Test Discrepancy Report (TDR) | `_Skills/skill_tdr.md` | `_Tools/run_tdr.py` |

**Full skill file path:** `[working directory]/_Skills/[skill_file]`
> Read the working directory live from the current environment — never hardcode a username or absolute path.

### Runner Handoff — Mandatory After Step 3

After step 3, OpenCode collects all remaining inputs via `question` tool (using "Type your own answer" for free-text fields), builds the complete cfg, then calls `execute_cfg()` directly via Python — no terminal required.

**Rules — no exceptions:**
- OpenCode presents ALL prompts (version, dates, platforms, TDR, notes, similarity) via `question` tool
- Free-text fields (TDR number, description, dates, etc.) use the built-in "Type your own answer" option
- After all inputs are collected, OpenCode calls `execute_cfg(cfg)` directly — never asks the engineer to open a terminal
- Do not ask the engineer to re-enter Product Category, CTN, or DTR number — already collected in steps 1–3

### Pre-Generation Read Requirements

**Before presenting ANY prompts for a document type, OpenCode MUST:**

1. **Read the skill file in full** — contains prompt sequence, formatting rules, known issues
2. **Read the runner script's profile section** — contains default values, required config keys, validation logic
3. **Check for existing drafts** — determines DTR number and source document

**This is mandatory for every `newd` session — no exceptions.** Do not rely on memory or prior sessions. The skill file and runner may have changed since the last generation.

> If the selected document type's skill file has not yet been fully built out, notify the engineer before proceeding: `"The [DocType] skill is not yet fully configured. No example documents have been templated for this document type. Proceeding with base rules only."`

---

## Commit Standard — All Engineers

After every generated or modified file is ready to commit, always prompt the engineer using a clickable selection:

> **"Ready to commit — which branch?"**

Present this as a clickable choice with the following options:
- The engineer's current branch (read live using `git branch --show-current`)
- `main`

**Rules:**
- **Never commit without prompting first — no exceptions, including `cm1` shortcut**
- Never assume a branch — always read it live
- Always push to the branch the engineer selects
- **If the engineer selects `main` OR types `cm1`, always present a second clickable confirmation before proceeding:**
  > **"Pushing directly to main — are you sure?"**
  > - Yes, push to main
  > - No, cancel
- Do not proceed to push until the engineer explicitly confirms

---

## Delete / Modify Confirmation Standard — All Engineers

Before deleting or modifying any file, always confirm with the engineer using a clickable prompt that shows the **exact filename** of the file about to be affected.

**Rules:**
- **Never delete or modify a file without showing the exact filename first — no exceptions**
- Derive the filename from disk or from the current session context — never paraphrase or abbreviate it
- Use the `question` tool for the confirmation — clickable, not plain text
- Format:
  > **"Confirm — delete/modify this file?"**
  > `[exact filename]`
  > - Yes, proceed
  > - No, cancel
- This applies to: draft deletions, example/template file edits, runbook edits triggered by engineer request, and any other destructive or modifying operation on a `.docx` or `.md` file
- If multiple files are affected, list each filename explicitly and confirm before touching any of them

---

## Folder Structure
```
ICR_Automation/
├── _Runbook/          ← engineer wiki
├── _Skills/           ← AI skill files (this folder)
├── _Tools/            ← shared utility scripts
│   ├── validate_doc.py           ← post-generation document linter
│   └── finalize_doc.py           ← Final .docx + PDF generator (strips Draft_, injects sig field)
└── Product Category/
    ├── [Product Category]/
    │   └── [CTN]/
    │       ├── Cybersecurity Summary Report (CSR)/
    │       ├── Functionality Attestation (FA)/
    │       ├── ICR Summary Memorandum (ICR Memo)/
    │       ├── Letter Of Compliance (LoC)/
    │       ├── Military Unique Deployment Guide (MUDG)/
    │       ├── Plan of Action & Milestone (POA&M)/
    │       ├── System Diagram/
    │       ├── System Description/
    │       └── Test Discrepancy Report (TDR)/
    │           Each folder contains:
    │               ├── Drafts/
    │               ├── Examples & Templates/
    │               └── Final/
    │                   └── [Document Name]/      ← subfolder named same as the files
    │                       ├── [Document Name].docx
    │                       └── [Document Name].pdf
```

**Critical folder rules:**
- `Example_*` and `Template_*` files = reference only, never used as source
- `CTN*` and `Draft_*` files = working documents, used as source for next DTR
- All generated drafts saved to `Drafts/` subfolder, prefixed with `Draft_`
- Final outputs (no `Draft_` prefix) saved to `Final/<document name>/` — one subfolder per finalized document

---

## Document Types (9 Total)
| Folder Name | Abbreviation |
|---|---|
| System Description | — |
| Cybersecurity Summary Report | CSR |
| Functionality Attestation | FA |
| ICR Summary Memorandum | ICR Memo |
| Letter Of Compliance | LoC |
| Military Unique Deployment Guide | MUDG |
| Plan of Action & Milestone | POA&M |
| System Diagram | — |
| Test Discrepancy Report | TDR |

---

## Source Document Selection
- If no drafts exist in `Drafts/`: use `CTN* - DTR000 - INITIAL - *` from `Examples & Templates/`
- If drafts exist: use the highest DTR number draft from `Drafts/`
- Next DTR number = highest existing DTR + 1

---

## File Naming Rules
| File Type | Pattern |
|---|---|
| Initial CTN doc | `CTN[number] - DTR000 - INITIAL - [ProdCat] - Cisco ICR [DocType].docx` |
| Draft | `Draft_CTN[number] - DTR[###] - [ProdCat] - [SoftwareVersion] - Cisco ICR [DocType].docx` |
| Example (reference) | `Example_CTN[number] - DTR[###] - ...` — never used as source |
| Template (reference) | `Template_CTN0000000 - DTR000 - ...` — never used as source |

**Key rules:**
- DTR number AND software version must both be updated in the filename
- Software version format is defined by the product family (e.g. `IOS XE 17.18`, `NX-OS 10.3`, `FXOS 2.14`) — follow the per-doc-type skill file
- All new drafts saved to `Drafts/` subfolder, prefixed with `Draft_`

---

## Revision History Rules
- Auto-increment version number (e.g. `1.0` → `2.0`)
- Date format: always 3-letter abbreviated month + year — `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec`
- After cloning rows from source doc: normalize any full month names (e.g. `March 2026` → `Mar 2026`) in ALL existing rows
- Change description: `Update for DTR [N]`
- Editor: always `GCT DP Collaboration`

---

## Version Downgrade Warning
If the requested new version is lower than the current platform version, always confirm with the user before proceeding.

---

## Table Version Replacement Rule
- Always target the Release column (index 1) only
- Replace the existing software version string with the new version
- Never match by specific version number — the reference doc may contain a different version than expected
- The exact regex pattern to use is defined in the per-doc-type skill file (version strings differ by OS type)

---

## Notes List Numbering Fix
- Every DTR component table has a Notes row with a numbered list that must restart at `1.`
- Fix: create a new `w:num` entry with `w:lvlOverride` + `w:startOverride val=1` and assign a unique `numId` per table
- Source `numId` and `abstractNumId` from the reference document's numbering part

---

## Adding a New CTN

Every CTN must have the same standard folder structure — 9 document type folders, each with `Drafts/` and `Examples & Templates/` subfolders.

**When an engineer adds a new CTN, always scaffold it first using:**
```bash
python3 _Tools/scaffold_ctn.py <ProductCategory> <CTN>
```
Example:
```bash
python3 _Tools/scaffold_ctn.py SBC CTN2026004
```

- Safe to run on an existing CTN — skips folders that already exist
- Places a `.gitkeep` in each empty subfolder so git tracks the structure
- After scaffolding: place example `.docx` files in each doc type's `Examples & Templates/` folder, commit, then type `newd`

**Never create CTN folders manually** — use the script to guarantee consistency across all engineers and machines.

---

## Restricted Folders
- Any folder named `Test_doc_update/` on any engineer's machine — OFF LIMITS, do not access

---

## Similarity Statement (Shared Rule)

When an engineer includes a similarity statement, always use this exact format:

`Request certification through similarity based on "[ProdCat] TN: [CTN], DTR[XX]."`

- No leading quote mark before "Request"
- The TN referenced is typically a **different** CTN than the one being worked — prompt the engineer to select from the live folder list
- Prompt order:
  1. TN Product Category — read live from `Product Category/` subfolders
  2. TN CTN — read live from subfolders under chosen Product Category
  3. DTR number — manual entry

---

## POA&M Inline Statement (Shared Rule)

> **Important:** The POA&M inline statement and the POA&M document type are two separate things:
> - **POA&M inline statement** — a single sentence inserted into a DTR body paragraph, recording that this DTR resolves an open finding
> - **POA&M document type** — a standalone compliance document (`Plan of Action & Milestone (POA&M)/`) that tracks all open findings with corrective actions and milestones

When an engineer includes a POA&M clearance statement, always use this exact format:

`This DTR Clears POA&M/TDR Number: [NUMBER], [PROBLEM DESCRIPTION].`

- Prompt order:
  1. POA&M/TDR Number — manual entry (e.g. `26003-01`)
  2. Problem Description — manual entry

---

## Runbook Reference
Full engineer operational details in:
`[working directory]/_Runbook/ICR_Automation_Runbook.md`

---

## Backup Management

Runbook backups are stored in `_Runbook/Backup/` and managed automatically.

**Filename format:** `ICR_Automation_Runbook_<username>_<YYYY-MM-DD_HHMMSS>.md`
- Username is read live from `git config user.name` (normalised: lowercase, spaces → underscores), falling back to `$USER`
- Each engineer has their own rolling window of backups — trimming is per-engineer, not global

**Trim policy:** Keep last 10 backups per engineer
- `runbook_updater.py` trims automatically every time it writes a new backup
- `_Tools/trim_backups.py` can be run manually for bulk cleanup or auditing

**Manual trim commands:**
```bash
python3 _Tools/trim_backups.py                # trim all engineers, keep 10 each
python3 _Tools/trim_backups.py --keep 5       # override keep count
python3 _Tools/trim_backups.py --dry-run      # preview deletions without removing files
python3 _Tools/trim_backups.py --summary      # show backup counts per engineer, no action
```

**At scale (15 engineers × 10 backups):** max ~150 files in `Backup/` at any time.

---

## DOCX XML Reference
> This project uses `python-docx` with direct XML manipulation. The rules below apply to all document generation and editing tasks.

### Tooling
| Task | Approach |
|---|---|
| Read / analyze content | `python-docx` `Document()` |
| Edit existing document | `python-docx` + direct `lxml` XML manipulation |
| Create new document | Clone from existing source doc — never from scratch |

### Element Order in `w:pPr`
Always maintain this order inside `<w:pPr>`:
`<w:pStyle>` → `<w:numPr>` → `<w:pageBreakBefore>` → `<w:spacing>` → `<w:ind>` → `<w:jc>` → `<w:rPr>` last

### Whitespace
Add `xml:space="preserve"` to any `<w:t>` element with leading or trailing spaces:
```xml
<w:t xml:space="preserve"> leading or trailing space </w:t>
```

### Run Properties — Always Clone `w:rPr`
When building new paragraphs by cloning a template element, always copy the full `<w:rPr>` block from the source run into the new run. Never build bare `<w:r>` elements without run properties — font size (`w:sz`), bold, and other formatting will be lost.

### Page Breaks
Use `w:pageBreakBefore` in `w:pPr` for paragraph-level page breaks (preferred):
```xml
<w:pPr>
  <w:pageBreakBefore/>
</w:pPr>
```
Do NOT use a `<w:br w:type="page"/>` run inside an otherwise empty paragraph — this creates a blank page.

### Page Break Rules
Page break behavior is document-type specific — defined in the per-doc-type skill file. The general rule is:
- Major section headings start on a new page — use `w:pageBreakBefore` in `w:pPr`
- Component tables flow freely — do NOT add a page break before the detail heading that precedes a table

### Smart Quotes
When adding text containing quotes or apostrophes in raw XML, use XML entities for professional typography:
| Entity | Character |
|---|---|
| `&#x2018;` | ' (left single) |
| `&#x2019;` | ' (right single / apostrophe) |
| `&#x201C;` | " (left double) |
| `&#x201D;` | " (right double) |

### RSIDs
Must be 8-digit hex (e.g. `00AB1234`). Always preserve existing RSIDs when cloning elements.

### Tracked Changes (if ever needed)
**Insertion:**
```xml
<w:ins w:id="1" w:author="GCT DP Collaboration" w:date="2026-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```
**Deletion:**
```xml
<w:del w:id="2" w:author="GCT DP Collaboration" w:date="2026-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```
- Use `<w:delText>` (not `<w:t>`) inside `<w:del>`
- Keep changes minimal — only mark what actually changed
- Always use `GCT DP Collaboration` as author unless engineer specifies otherwise

---

## `/adt` — ICR Automation Audit

> Triggered by `/adt` or `qac`. Runs two sequential passes across all Python scripts and markdown files. Complete each pass fully before starting the next.

> **MANDATORY FIRST STEP — NO EXCEPTIONS:** Before running any checks, OpenCode must read `_Skills/skill_base.md` in full to load the current protocol. Do not rely on memory or session summaries. If this file has not been read in the current session, read it now before proceeding. Operating from recalled approximations instead of the live file is a protocol violation.

### Standing Rules (Always Active)
- No hardcoded absolute paths (`/Users/nateric`, `/Users/edknowlt`, `/Users/jmisal`, or any `/Users/` path)
- All one-off scripts must have the standard `ONE-OFF SCRIPT —` warning header
- All `SOURCE` file references must point to files that actually exist on disk
- All `OUT` paths must write to the correct `Drafts/` subfolder for the doc type
- No magic numbers — row indices, twip values, and numId values must be documented with inline comments explaining what they target
- No copy-paste errors — version strings, date variables, and DTR numbers must be consistent within each script
- No dead code — unused variables, imports, or unreachable branches
- No stale markdown references — every script, file, or folder mentioned in any `.md` file must exist on disk

---

### Pass 1 — Python Script Audit

Scan every `.py` file in `_Tools/` and `_Runbook/`:

**1A — Correctness**
- Logic errors, wrong variable used, off-by-one on row indices
- `SOURCE` variable points to a file that does not exist on disk → script will crash
- `OUT` path writes to wrong folder or wrong doc type subfolder
- Date variables out of chronological sequence across scripts for the same CTN (DTR005 date should be after DTR004, etc.)
- Sustained platform versions set to the same value as the updating version — sustained platforms must carry their prior version, not the new one
- Version strings in docstring/header that contradict the script's own constants
- **Do NOT flag version mismatches between different document type runners** (e.g. run_sysdesc.py vs run_fa.py). Each document type is at its own DTR and version independently — this is expected and correct, especially during test phase.

**1B — Cleanliness**
- Hardcoded `/Users/` absolute paths anywhere in the file
- Missing `ONE-OFF SCRIPT —` warning header on any one-off generation script
- Unused imports or variables
- Duplicate logic copy-pasted between scripts that should be shared
- Magic numbers with no inline comment (e.g. row index `4` with no comment saying which platform it targets)
- Non-descriptive variable names

**1C — Safety**
- Any script that writes test/debug content to the output document (e.g. `"This is a test"` paragraphs)
- Any script that could silently overwrite an existing draft without warning
- Missing `if __name__ == "__main__":` guard on scripts that should not run on import

### Pass 1 Output Format
For every issue:
```
File     : path/to/script.py
Line(s)  : line number(s)
Severity : Critical | Warning | Info
Category : Correctness | Cleanliness | Safety
Issue    : clear description
Fix      : exact correction or precise instruction
```
End with a summary table. Then print: **`PASS 1 COMPLETE. BEGINNING PASS 2.`**

---

### Pass 2 — Markdown & Documentation Audit

Scan every `.md` file in `_Skills/`, `_Runbook/`, and the repo root:

**2A — Stale References**
- Any script name mentioned in any `.md` file that no longer exists in `_Tools/` or `_Runbook/`
- Any folder path or file path referenced that does not exist on disk
- Script Inventory in runbook — every entry must match an actual file; every file must have an entry
- Draft Log entries marked "current on disk" where the file is actually missing

**2B — Consistency**
- Shortcut command tables — `skill_base.md`, `README.md`, and runbook must all list identical shortcuts
- Skill File Map statuses — must match actual state of each skill file
- Version numbers referenced in the runbook session log or Platform Version History that contradict what the scripts actually produce

**2C — Completeness**
- Any `TODO`, `FIXME`, `coming soon`, or placeholder text in any live file
- Generation status checkboxes in skill files — unchecked boxes that should be checked based on scripts that exist
- `cek` shortcut referenced anywhere in any live file (it was retired — flag any occurrence)

### Pass 2 Output Format
For every issue:
```
File     : path/to/file.md
Line(s)  : line number(s)
Severity : Critical | Warning | Info
Category : Stale Reference | Consistency | Completeness
Issue    : clear description
Fix      : exact correction or precise instruction
```
End with a summary table. Then print: **`PASS 2 COMPLETE. AUDIT DONE.`**

---

### Final Audit Summary
```
Total Issues Found    : [n]
Total Critical        : [n]
Total Warnings        : [n]
Total Info            : [n]
Scripts Audited       : [n]
Markdown Files Audited: [n]
Overall Health        : [one sentence assessment]
```

