# ICR Automation — Skill: Military Unique Deployment Guide (MUDG)
> Load `skill_base.md` first. This file defines rules specific to the **Military Unique Deployment Guide (MUDG)** document type only.

---

## Document Identity
- **Full Name:** Cisco ICR Military Unique Deployment Guide
- **Abbreviation:** MUDG
- **Folder:** `Military Unique Deployment Guide (MUDG)/`
- **Filename Suffix:** `Military Unique Deployment Guide.docx`

---

## Purpose
The MUDG documents military-unique deployment configurations, requirements, and guidance for the product under review. It covers DoD-specific deployment scenarios and security configurations applicable to the software version being certified.

---

## Document Structure

The MUDG is a large configuration guide document with the following structure:

### Tables
| Table | Contents | Rows (INITIAL) | Rows (Example DTR001) |
|---|---|---|---|
| Table 0 | Revision History | 2 (header + 1 data) | 5 (header + 4 data) |
| Table 1 | Acronym List | 35 rows x 2 cols | 35 rows x 2 cols |

### Major Sections (Heading 1)
1. **Configuration Guidelines for Cisco SBC**
2. **Conditions of Fielding**
3. **Hardening and Cybersecurity Configuration** — TACACS+, MFA, IPsec, SYSLOG, session timeouts, management ports
4. **Configuration Checklist** — redundancy, cryptographic config, call routing
5. **Redundancy and Media Failover** — VRRP, IPsec tunnels, CUBE HA
6. **PKI Certificates** — hostname, RSA keys, trustpoints, CSR, CA cert import, SIP-UA TLS
7. **Call Routing Configuration** — toll fraud, UBE mode, VoIP/SIP-UA, URI classes, SIP profiles, dial-peers, media inactivity
8. **SBC Configuration Example** — full configuration walkthrough (mirrors sections above)
9. **Related Documentation**
10. **List of Acronyms**

### Title Page Elements
- Title: `Cisco Global Certification Team (GCT) Defense Programs (DP) Internal Compliance Review (ICR) Military Unique Deployment Guide (MUDG) for Session Border Controller (SBC)`
- Address: `Cisco Global Certification Team, Defense Programs` / `7025-2 Kit Creek Road, Research Triangle Park, North Carolina 27709`
- Email: `Cisco GCT DP Email: gct-dp-icr@cisco.com`
- Includes Figure 1 (SUT Test Configuration) and Figure 2 (Call Routing Configuration Example)

---

## What Gets Updated Per DTR

### 1. Revision History Row
- Auto-increment version number (e.g. `4.0` → `5.0`)
- Date format: abbreviated month + year (`Mon YYYY`)
- Change description: `Update for DTR [N]`
- Editor: `GCT DP Collaboration`
- Normalize any full month names in existing rows to abbreviated format

### 2. Body Content
- The MUDG body content (configuration guides, examples, etc.) is **static** — it does **not** change per DTR unless the engineer explicitly provides new or updated configuration content
- No IOS XE version references appear in the body text
- **Add content:** Engineer enters content via a `question` tool prompt with custom text entry (not pasted into chat). Content is appended to the end of the specified section (before the next Heading 1). All existing content in the section is preserved. Inserted text uses **normal (non-bold, non-italic) formatting** to match the surrounding body style — do not bold or italicize newly added content. Clone the run properties (`w:rPr`) from an existing Normal-style paragraph in the same section to ensure font, size, and style match exactly. **An empty spacer paragraph is always added after the inserted content.**
- **Delete content:** Engineer describes what to remove; only the specified paragraphs or subsections are deleted. Nothing else in the section is modified.
- **Spacing cleanup:** After any content change (add or delete), `collapse_empty_paragraphs()` runs automatically — collapses runs of 2+ consecutive empty paragraphs down to a maximum of 1 empty paragraph between sections. This prevents double/triple gaps left behind by deletions.

> **Key difference from other document types:** The MUDG does not have DTR-specific sections, version update paragraphs, similarity statements, POA&M paragraphs, or release notes. The only automatic change per DTR is the revision history row.

---

## Prompt Sequence (MUDG-specific — after base steps 1-3)

After selecting MUDG as the document type, the following additional prompts apply:

1. **Any configuration content updates?** — Yes / No
   - If Yes, ask: **"What kind of change?"**
      - **Add content** — engineer selects the target section (from the 10 Heading 1 sections) via clickable prompt. Then a `question` tool prompt with **no predefined options** (empty `options` array) is presented: *"Paste or type the content to add to [Section Name]:"* — this shows only the "Type your own answer" text input field. The engineer types or pastes the content directly into the text input (not into the chat). Content is appended to the end of the selected section (before the next Heading 1), preserving all existing content. **An empty spacer paragraph is always inserted after the new content.**
      - **Delete content** — engineer specifies the section and describes what to remove (specific paragraphs, a subsection, config block, etc.). Only the described content is removed.
   - After each change: **"Any more changes?"** — Yes / No. Repeat until No.
2. **Confirm DTR number and date** — auto-detected from source document

> Note: Steps 4-9 from the base prompt sequence (IOS XE version, platforms, similarity, POA&M, release notes) are **not applicable** to the MUDG — skip them entirely.

---

## File Naming
| File Type | Pattern |
|---|---|
| Initial | `CTN[number] - DTR000 - INITIAL - [ProdCat] - Military Unique Deployment Guide.docx` |
| Draft | `Draft_CTN[number] - DTR[###] - [ProdCat] - Military Unique Deployment Guide.docx` |
| Example | `Example_CTN[number] - DTR[###] - Military Unique Deployment Guide.docx` |

> Note: MUDG filenames do **not** include the IOS XE version (unlike System Description and ICR Memo).

---

## Source Document Selection
- If no drafts exist in `Drafts/`: use the highest DTR Example from `Examples & Templates/`, or `CTN* - DTR000 - INITIAL` if no Examples exist
- If drafts exist: use the highest DTR number draft from `Drafts/`
- Next DTR number = highest existing DTR + 1

---

## Known Issues

| # | Issue | Resolution |
|---|---|---|
| 1 | INITIAL has email `gct-dp-icr@cisco.com`, Example has `certteam@cisco.com` | Use whichever email is in the source document — do not change. **Canonical/preferred address is `gct-dp-icr@cisco.com`** (from INITIAL); `certteam@cisco.com` is considered legacy. Confirm with team if unsure. |
| 2 | Revision history dates may use full month names | Normalize all dates to abbreviated month format when adding new row |
| 3 | `run_mudg.py` `generate()` sources from Example instead of INITIAL when `first_dtr_num == dtr_num` | Workaround: for DTR001 from INITIAL, call `add_revision_rows()` directly on the INITIAL doc instead of using `generate()` with `first_dtr_num=1` |

---

## Generation Status
- [x] Example/Template file placed in `Examples & Templates/`
- [x] Table structure documented
- [x] Paragraph patterns documented
- [x] First draft generated and validated
- [x] Skill file updated with confirmed rules
