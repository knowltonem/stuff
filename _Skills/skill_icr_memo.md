# ICR Automation — Skill: ICR Summary Memorandum (ICR Memo)
> Load `skill_base.md` first. This file defines rules specific to the **ICR Summary Memorandum (ICR Memo)** document type only.

---

## Document Identity
- **Full Name:** Cisco ICR Summary Memorandum
- **Abbreviation:** ICR Memo
- **Folder:** `ICR Summary Memorandum (ICR Memo)/`
- **Filename Suffix:** `Cisco ICR Memo.docx`

---

## Purpose
The ICR Memo is a letter-style summary memorandum that provides a high-level overview of the ICR process, findings, and outcomes for the product and software version under review. Unlike most other ICR documents, the ICR Memo has **no tables** — it is a structured letter with dated paragraphs.

---

## Platform Map (SBC — CTN2026003)
| Platform | DTR Paragraph Name |
|---|---|
| ASR 1006-X | `ASR 1006-X` |
| ISR 4461/K9 | `ISR 4461/K9` |
| Cisco Catalyst 8300 Series | `Cisco Catalyst 8300 Series` |
| Cisco Catalyst 8200 Series | `Cisco Catalyst 8200 Series` |
| Cisco Catalyst 8000v Series | `Cisco Catalyst 8000v Series` |

> **Note:** ICR Memo uses full platform names (e.g., `Cisco Catalyst 8300 Series`). FA uses abbreviated names (e.g., `C8300 series`). These are intentionally different — do not normalize. Cross-reference: `skill_fa.md` → Hardware List Format.

## Product Component Map (SBC — CTN2026003)
| Component | Full Name | Acronym |
|---|---|---|
| Interworking Border Controller | Interworking Border Controller (IWBC) | IWBC |
| Interworking Gateway | Interworking Gateway (IWG) | IWG |
| Session Border Controller | Session Border Controller (SBC) | SBC |

> When listing product components and platforms in a DTR approval paragraph, use the format: `product components IWBC, IWG, and SBC on the ASR 1006-X, ISR 4461/K9, Cisco Catalyst 8300 Series, Cisco Catalyst 8200 Series, and Cisco Catalyst 8000v Series`
> - Product components use **acronyms only** (not full names) in DTR paragraphs
> - During generation, prompt the engineer to select which product components to include

---

## Document Structure

The ICR Memo is a single-page letter with the following sections in order:

### 1. Date
- Top of document
- Format: `DD Month YYYY` (e.g. `01 May 2026`)
- Style: `Normal`
- **Alignment: Right-aligned with right indent (194 twips)** — aligns the date's right edge with the right edge of the centered header image (image 8972 twips centered in 9360-twip text area, gap each side = 194 twips)

### 2. Title
- Text: `Internal Compliance Review (ICR) Summary Memorandum`
- Style: `Normal (Web)`

### 3. SUBJECT Line
- **Format (all DTRs):** `SUBJECT: ...approval of the Cisco Session Border Controller (SBC)` — **no version in SUBJECT line**
- Matches the INITIAL document format
- When generating from a source that has a version in the SUBJECT (e.g. Example), strip the `with Software Release (Rel.) IOS XE [VERSION]` suffix
- Style: `Normal (Web)`

### 4. References
- Fixed text — do not modify:
  - `(a) Defense of Defense Instruction (DoDI) 8100.04, "Department of Defense (DoD) Unified Capabilities (UC)," 09 December 2010`
  - `(b) Office of the DoD Chief Information Officer (CIO), "DoD Unified Capabilities Requirements 2013 (UCR 2013) Change 2," September 2017`
- Style: `Normal (Web)`

### 5. Approval Summary Paragraph
- Format: `The Cisco GCT DP team has completed approval for the Cisco SBC with Software Rel. Internetwork Operating System (IOS) XE [VERSION]. This solution has passed CS scanning...`
- The version here reflects the **latest certified version**
- Style: `Normal (Web)`

### 6. FA Reference Paragraph
- **INITIAL:** `The Functionality Attestation letter containing the detailed components and configuration may be requested by email: gct-dp-icr@cisco.com`
- **Example/DTR:** `The Functionality Attestation letter containing the detailed components and configuration on this product is available at the following email: gct-dp-icr@cisco.com`
- Use whichever wording is in the source document — do not change
- Style: `Normal (Web)`

### 7. DTR Approval Paragraphs
- **One paragraph per DTR**, added chronologically (oldest first, newest last)
- Format: `On [DATE], the following was approved via DTR #[NNN] to update the Software Rel. version from IOS XE [FROM] to [TO] for the product components [COMPONENT_LIST] on the [PLATFORM_LIST] router platforms.`
- **Product components** listed as acronyms, comma-separated with Oxford comma (e.g. `IWBC, IWG, and SBC`)
- **Platforms** listed after `on the` (e.g. `ASR 1006-X, ISR 4461/K9, Cisco Catalyst 8300 Series, Cisco Catalyst 8200 Series, and Cisco Catalyst 8000v Series`)
- DTR paragraphs may also include additional context (e.g. POA&M clearance, ESXi updates) — preserve any such trailing text from existing paragraphs
- Date format: `DD Month YYYY` (e.g. `13 December 2024`)
- DTR number format: `#001`, `#002`, `#003` (zero-padded to 3 digits)
- Each new DTR adds a **new paragraph** — previous DTR paragraphs are preserved unchanged
- **After each DTR approval paragraph, insert an empty paragraph as a spacer between DTR entries**
- Style: `Normal (Web)`

> **Note on INITIAL approval paragraph:** The INITIAL doc uses full platform names (`Cisco Catalyst 8300 Series`, `Cisco Catalyst 8200 Series`, `Cisco Catalyst 8000v Series`) and a different format (`this initial request was approved to update the Software Rel. to [VERSION] for product component...`). Preserve this paragraph as-is when carrying forward — do not reformat it to match DTR paragraph style.

### 8. Implementation Notice
- Fixed text: `This product/solution must be implemented only in the configuration that was tested. Please utilize this solution's deployment guide and product-specific Security Technical Implementation Guidelines (STIGs)...`
- Style: `Normal (Web)`

### 9. CSR Reference
- Format: `The Cybersecurity Summary Report (CSR) is included in the Cybersecurity Summary Report Package (CSRP) and may be requested by email: gct-dp-icr@cisco.com`
- Style: `Normal (Web)`

### 10. Signature Block
- Name: `Robbie Horgan`
- Title: `Leader, GCT DP`
- Style: `Normal (Web)`
- **Do not modify** — always preserve as-is
- **If signatory changes:** update this skill file AND `_Tools/validate_doc.py` → `ICR_MEMO_SIGNATORY` constant together

---

## What Gets Added Per DTR

### 1. Date (top of document)
- Auto-generated from `datetime.now().strftime("%d %B %Y")` — always reflects the date the document is created

### 2. SUBJECT Line Version
- **Do not add a version to the SUBJECT line** — SUBJECT always matches the INITIAL format (no version)
- If the source document has a version in the SUBJECT, strip it

### 3. Approval Summary Version
- Update the IOS XE version to the new certified version

### 4. New DTR Approval Paragraph
- Insert **before** the Implementation Notice paragraph
- Use the format described in section 7 above
- The date for the new DTR paragraph may differ from the document date — always prompt separately for both

---

## DTR001-Specific Generation Rules (Source = INITIAL)

When no drafts exist in `Drafts/`, the source is the INITIAL document and DTR number is 001. The following differences apply compared to DTR002+:

### Source Document
- Use `CTN* - DTR000 - INITIAL - *` from `Examples & Templates/`
- The INITIAL doc has **no existing DTR paragraphs** — only the initial approval paragraph

### Date Handling
- The INITIAL doc's date may be split across multiple runs (e.g., run 9 in paragraph 1). Use `replace_version_across_runs`-style logic or iterate runs to find and replace the date text.
- Same rule applies: set to `datetime.now().strftime("%d %B %Y")`, right-aligned with 194-twip indent

### SUBJECT Line
- The INITIAL SUBJECT line already has **no version** — no stripping needed
- Do not add a version to it

### Approval Summary Version
- The INITIAL doc's approval summary paragraph contains the original version (e.g., `XE 17.18`)
- Update to the new certified version using `replace_version_across_runs()` — the version may be split across multiple runs in the INITIAL

### Initial Approval Paragraph
- The INITIAL doc contains a paragraph starting with `"...this initial request was approved..."` — this uses **full platform names** (e.g., `Cisco Catalyst 8300 Series`) and a different format than DTR paragraphs
- **Preserve this paragraph exactly as-is** — do not reformat, do not change platform names

### DTR #001 Paragraph Insertion
- Insert the new DTR #001 paragraph **after** the initial approval paragraph
- Add an **empty spacer paragraph** between the initial approval paragraph and the new DTR #001 paragraph
- Add an **empty spacer paragraph** after the DTR #001 paragraph (before the Implementation Notice)
- Use the initial approval paragraph as the **clone template** for formatting (font, style)

### Version Format in DTR Text
- DTR001 scripts use full version strings in the DTR text: `from IOS XE 17.18 to IOS XE 26.0` (with `IOS XE` prefix on both)
- DTR002+ scripts use: `from IOS XE 27.0 to 27.5` (prefix only on the "from" version)
- Follow whichever convention matches the source/example documents for the CTN
- **Default for new CTNs with no prior documents:** use the DTR001 full-prefix convention (`from IOS XE X.X to IOS XE Y.Y`) for all DTRs until a prior-version document establishes a different pattern
- **Track per-CTN:** Once a CTN produces its first finalized ICR Memo, record which version-string convention was used in that CTN's seed profile or the Runbook session log, so future DTRs for that CTN stay consistent.

### Summary: DTR001 vs DTR002+ Generation Steps

| Step | DTR001 (from INITIAL) | DTR002+ (from previous draft) |
|---|---|---|
| Source | INITIAL doc from `Examples & Templates/` | Highest DTR draft from `Drafts/` |
| Date update | Find date across runs (may be split) | Find date by regex match |
| SUBJECT line | Already clean — no action | Strip version if present |
| Approval summary | Update version (may be split across runs) | Update version (may be split across runs) |
| DTR paragraph anchor | Insert after initial approval paragraph | Insert after last DTR paragraph |
| Clone template | Initial approval paragraph | Last DTR paragraph |
| Spacers | Before and after DTR #001 | Before and after new DTR |

---

## Prompt Sequence (ICR Memo-specific — after base steps 1-3)

After selecting ICR Memo as the document type, the following additional prompts apply:

> **Note on base steps:** Base steps 1-3 (Product Category, CTN, Document Type) are handled by `skill_base.md`. The prompts below continue from step 4. Base step 5 (Release Notes webfetch) does **not** apply to the ICR Memo — this document type has no release notes section.

1. **IOS XE Version** — new version being certified (from base step 4)
2. **All platforms updating?** — Yes / No (from base step 6)
   - If No: per-platform prompt (keep current or update)
3. **Product components** — multi-select from IWBC, IWG, SBC (default: all three)
4. **DTR approval date** — date for the new DTR approval paragraph (may differ from the document date; default: today)
   - Document date is auto-generated from `datetime.now()` — no prompt needed

> Note: Similarity and POA&M statements are **not included** in the ICR Memo — those appear only in the System Description and other technical documents.

---

## File Naming
| File Type | Pattern |
|---|---|
| Initial | `CTN[number] - DTR000 - INITIAL - [ProdCat] - Cisco ICR Memo.docx` |
| Draft | `Draft_CTN[number] - DTR[###] - [ProdCat] - [Version] - Cisco ICR Memo.docx` |
| Example | `Example_CTN[number] - DTR[###] - [ProdCat] - [Version] - Cisco ICR Memo.docx` |

---

## Source Document Selection
- If no drafts exist in `Drafts/`: use `CTN* - DTR000 - INITIAL - *` from `Examples & Templates/`
- If drafts exist: use the highest DTR number draft from `Drafts/`
- Next DTR number = highest existing DTR + 1

---

## Known Issues

| # | Issue | Resolution |
|---|---|---|
| 1 | INITIAL doc has single approval paragraph with no DTR-specific entries | First DTR generation must add the initial DTR approval paragraph after the FA reference paragraph |
| 2 | Date at top of document not auto-updated | Always update the date to the current generation date |
| 3 | INITIAL SUBJECT line has no version; Example SUBJECT uses "Software Release (Rel.)" | Always strip version from SUBJECT — match INITIAL format (no version) |
| 4 | FA reference wording differs between INITIAL and Example | Preserve whichever wording is in the source document |
| 5 | INITIAL uses full platform names (e.g. "Cisco Catalyst 8300 Series"); Example uses abbreviated (e.g. "C8300 series") | Preserve existing paragraph text — do not normalize platform names in carried-forward paragraphs |
| 6 | Example DTR #001 includes POA&M clearance text at end of paragraph | Preserve any trailing context in existing DTR paragraphs — do not strip |

---

## Generation Status
- [x] Example/Template file placed in `Examples & Templates/`
- [x] Table structure documented (no tables — letter format)
- [x] Paragraph patterns documented
- [x] First draft generated and validated
- [x] Skill file updated with confirmed rules
