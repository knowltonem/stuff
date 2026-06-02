# ICR Automation — Engineer Runbook
> Load this file at the start of every session to restore full context.
> **The runbook updater runs automatically when you type `newd`** — no need to run it manually at session start.
> To run it manually at any time (from repo root):
> ```
> python3 "_Runbook/runbook_updater.py" --once
> ```
> **Note:** Run this from the repo root (`ICR_Automation/`). If you are in a different directory, use the full path to the repo.

---

## Session-Start Checklist (Every Session, Every Engineer)

Before doing anything else — including asking the AI a question — verify the AI has read both files from disk:

- [ ] AI has read `_Skills/skill_base.md` in full (not from memory)
- [ ] AI has read `_Runbook/ICR_Automation_Runbook.md` in full (not from memory)

**How to enforce:** Paste this as your first message every session:
```
Read _Skills/skill_base.md and _Runbook/ICR_Automation_Runbook.md in full from disk before responding to anything.
```

> If the AI answers a question about project state, DTR history, or file existence **without reading these files first**, that is a protocol violation. Correct it by asking the AI to read both files and re-answer.

---

## Project Overview
Automate the creation and incremental updating of Cisco ICR (Internal Compliance Review) document suites. Covers all Cisco product families — routers, switches, wireless, data center, collaboration, and others. Not limited to IOS XE or any single OS/platform type. Currently covers System Description, FA, ICR Memo, MUDG, TDR, and CSR for SBC/CTN2026003 with complete parameterized runners; LoC, POA&M, and System Diagram are skeleton runners pending example docs.

**Working Directory:** Determined live from the current environment — never hardcoded

---

## Session Log
> Engineers: add an entry every session. Format: `| YYYY-MM-DD | Name | Summary | Issues |`

| Date | Engineer | Summary | Issues / Notes |
|---|---|---|---|
| 2026-04-28 | GCT DP | Built full DTR workflow. Generated DTR001 for SBC/CTN2026003. Set up folder structure for all 3 CTNs. Created Runbook. | None |
| 2026-04-28 | GCT DP | Generated test DTR runs using fictitious platforms (CS3000X, Natedogg2) to validate new platform workflow — IWG/SBC/IWG+SBC row pattern, webfetch fallback rule, adds vs updates paragraph rule. Deleted test drafts and fictitious platforms at end of session. | Test runs used placeholder versions (not 27.0/28.0) — no real DTR documents produced |
| 2026-04-29 | edknowlt | Generated real DTR001 (IOS XE 26.0) — ASR 1006-X sustained at 17.18, C8300/C8200/C8000v updated to 26.0. Added generate_dtr.py to _Tools/. *(script retired — superseded by run_fa.py et al.)* | None |
| 2026-05-13 | edknowlt | Deleted generate_dtr.py from _Tools/ — superseded by parameterized runners (run_sysdesc.py et al.) | None |
| 2026-04-30 | edknowlt | Generated DTR002 (IOS XE 26.1) — C8300/C8200/C8000v updated to 26.1, ASR 1006-X sustained at 17.18. Release notes webfetched from cisco.com (Apr 2026). Added trim_backups.py, per-engineer backup naming. Refactored skill_base.md to be product-agnostic. | None |
| 2026-04-30 | edknowlt | Audited all 5 nateric-authored scripts for hardcoded paths and missing one-off headers. Fixed hardcoded `/Users/nateric/` BASE in gen_dtr005_mudg.py and gen_dtr006_mudg.py (replaced with `__file__`-relative). Added one-off warning headers to all 5 scripts. Added all 5 to Script Inventory. | None |
| 2026-05-01 | edknowlt | Generated DTR003 System Description (IOS XE 26.6) — C8300/C8200/C8000v updated from 26.5, ASR 1006-X sustained at 17.18, similarity ESC CTN2026001 DTR05, release notes fallback Aug 2026. Fixed ASR 1006-X sustain bug in DTR002 and DTR003 component tables (rows 1-3 were incorrectly showing 26.5). Added sustained-row protection rule to skill_system_description.md (Known Issue 11). Synced all branches to main. | ASR 1006-X sustain bug traced to gen_dtr002_sbc_sysdesc_v2.py updating all rows — fixed directly in both docx files. |
| 2026-05-01 | nateric | Generated DTR005 ICR Memo (IOS XE 26.5) and DTR006 ICR Memo (IOS XE 27.0) — all platforms, pushed directly to main. | Continues direct-to-main push pattern |
| 2026-05-01 | AUTO-DETECT | New drafts synced on session start: FA DTR001/DTR002, ICR Memo DTR004/DTR005, MUDG DTR005/DTR006, System Description DTR002 | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 24.6 - Cisco ICR Memo.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR002 - SBC - IOS XE 25.0 - Cisco ICR Memo.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR003 - SBC - IOS XE 25.5 - Cisco ICR Memo.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR002 - SBC - IOS XE 26.5 - Cisco Functionality Attestation.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR003 - SBC - IOS XE 27.0 - Cisco Functionality Attestation.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR004 - SBC - IOS XE 28.2 - Cisco Functionality Attestation.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR004 - SBC - IOS XE 29.0 - Cisco ICR Memo.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR005 - SBC - IOS XE 26.5 - Cisco ICR Memo.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR006 - SBC - IOS XE 27.0 - Cisco ICR Memo.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR007 - SBC - IOS XE 28.0 - Cisco ICR Memo.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR005 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR006 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR007 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR002 - SBC - IOS XE 26.5 - Cisco ICR System Description.docx | — |
| 2026-05-12 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR003 - SBC - IOS XE 26.6 - Cisco ICR System Description.docx | — |
| 2026-05-13 | edknowlt | Parameterized runner architecture completed. Built `runner_core.py`, `run_fa.py`, `run_icr_memo.py`, `run_sysdesc.py`, `run_mudg.py`, `run_tdr.py`. Deleted all one-off scripts (FA, ICR Memo, SysDesc, MUDG, TDR) except two legacy nateric reference scripts. Script Inventory updated to reflect new runners. Disk clean — no drafts on disk going into afternoon testing. | Two legacy nateric scripts (`gen_dtr002_icr_memo.py`, `gen_dtr004_icr_memo.py`) retained on disk for reference only — not for generation. |
| 2026-05-13 | edknowlt | Deleted `gen_dtr002_icr_memo.py` and `gen_dtr004_icr_memo.py` — all logic fully superseded by `run_icr_memo.py`. Removed from Script Inventory. | None |
| 2026-05-13 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco Functionality Attestation.docx | — |
| 2026-05-14 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco ICR Memo.docx | — |
| 2026-05-14 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR002 - SBC - IOS XE 26.2 - Cisco ICR Memo.docx | — |
| 2026-05-14 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-18 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco ICR Memo.docx | — |
| 2026-05-18 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR002 - SBC - IOS XE 26.2 - Cisco ICR Memo.docx | — |
| 2026-05-18 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-18 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.1 - Cisco ICR System Description.docx | — |
| 2026-05-18 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Starting over — DTR001 will be regenerated from scratch |
| 2026-05-19 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.1 - Cisco ICR System Description.docx | — |
| 2026-05-19 | edknowlt | QAC audit complete. Fixed: added --check-deps to finalize_doc.py; added run() entry point to run_csr.py; set CSR supported=True in generate.py; removed hardcoded edknowlt fallback from run_loc.py, run_poam.py, run_system_diagram.py; updated Script Inventory (run_csr.py → COMPLETE); removed "Recording coming soon" placeholder from README.md. | 7 issues found (0 critical, 5 warning, 2 info). DTR001 SysDesc still pending regeneration. |
| 2026-05-19 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco ICR Memo.docx | — |
| 2026-05-19 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR002 - SBC - IOS XE 26.2 - Cisco ICR Memo.docx | — |
| 2026-05-19 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR003 - SBC - IOS XE 27.0 - Cisco ICR Memo.docx | — |
| 2026-05-20 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.5 - Cisco ICR CSR.docx | — |
| 2026-05-20 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco Functionality Attestation.docx | — |
| 2026-05-20 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.1 - Cisco ICR System Description.docx | — |
| 2026-05-20 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco ICR Memo.docx | — |
| 2026-05-20 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-20 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - TDR26003-02 - SBC - IOS XE 26.0 - Cisco ICR TDR.docx | — |
| 2026-05-21 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco ICR Memo.docx | — |
| 2026-05-21 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-21 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.1 - Cisco ICR System Description.docx | — |
| 2026-05-21 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR002 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-26 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR004 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-05-26 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - TDR26003-02 - SBC - IOS XE 26.5 - Cisco ICR TDR.docx | — |
| 2026-05-26 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR003 - TDR26003-03 - SBC - IOS XE 27.0 - Cisco ICR TDR.docx | — |
| 2026-05-27 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco ICR CSR.docx | — |
| 2026-05-27 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco Functionality Attestation.docx | — |
| 2026-05-27 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - Military Unique Deployment Guide.docx | — |
| 2026-06-02 | AUTO-DETECT | New draft detected: Draft_CTN2026003 - DTR001 - SBC - IOS XE 26.0 - Cisco ICR CSR.docx | — |
---

## Platform Version History
> Auto-updated when new drafts are detected. Manual entries allowed.

| CTN | Product | DTR | ASR 1006-X | C8300 | C8200 | C8000v | Date |
|---|---|---|---|---|---|---|---|
| CTN2026003 | SBC | DTR002 (Initial) | IOS XE 17.18 | IOS XE 26.1 | IOS XE 26.1 | IOS XE 26.1 | May 2026 |

| CTN2026003 | SBC | DTR002 | — | — | — | — | May 2026 |

## Pending / Upcoming DTRs
> Update this section at the end of each session.

| CTN | Product | Next DTR | Notes |
|---|---|---|---|
| CTN2026003 | SBC | — | SysDesc: no drafts on disk (DTR002 finalized). FA: no drafts on disk, next=DTR001. ICR Memo: DTR001 finalized; DTR002 (IOS XE 27.0) draft on disk, next=DTR003. MUDG: no drafts on disk, next=DTR005. TDR: DTR001 (TDR26003-02, IOS XE 26.5) + DTR003 (TDR26003-03, IOS XE 27.0) on disk. CSR: no drafts on disk, next=DTR001. |
| CTN2026001 | ESC | DTR001 | No docs placed yet |
| CTN2026002 | SS | DTR001 | No docs placed yet |

---

## Draft Log
> Append a row every time a draft is generated OR deleted. Never remove rows — this is the permanent history.
> Format: Date | Engineer | Action | CTN | Doc Type | DTR | Version | Reason
>
> **Why this matters for OpenCode:** OpenCode reads what is currently on disk to understand the state of the project. When drafts are deleted — especially during testing — that context is lost and OpenCode may not know what was previously generated, what was discarded, or what DTR number comes next. This log is the single source of truth that survives deletions. OpenCode reads this table at the start of every session to restore full context, even when the Drafts/ folders are empty.
>
> **Historical script names:** Many rows in this log reference one-off generation scripts (e.g. `gen_dtr001_fa_sbc.py`, `gen_dtr002_sbc_sysdesc_v2.py`) that no longer exist on disk. These are historical records only. **See Script Inventory for currently active scripts.** All one-off scripts have been superseded by the parameterized runners (`run_fa.py`, `run_sysdesc.py`, etc.).

| Date | Engineer | Action | CTN | Doc Type | DTR | Version | Reason |
|---|---|---|---|---|---|---|---|
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | First bootstrap from INITIAL source via `generate_dtr.py` *(script retired — superseded by run_sysdesc.py)* |
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | All platforms updating via `gen_dtr002_sbc_sysdesc_v2.py` |
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Initial DTR003 attempt via `gen_dtr003_sbc_sysdesc.py` — superseded (script deleted, replaced by v2) |
| 2026-04-28 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Superseded by v2 (wrong version target) |
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Corrected version — ASR sustained, C8300/C8200/C8000v updating via `gen_dtr003_sbc_sysdesc_v2.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.0 | First ICR Memo draft via `gen_dtr004_icr_memo.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Via `gen_dtr005_icr_memo.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Via `gen_dtr006_icr_memo.py` |
| 2026-04-28 | nateric | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.0 | Test draft — removed during ICR Memo skill development |
| 2026-04-28 | nateric | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Test draft — removed during ICR Memo skill development |
| 2026-04-28 | nateric | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Test draft — removed during ICR Memo skill development |
| 2026-04-28 | nateric | Generated | CTN2026003 | MUDG | DTR002 | — | Via `gen_dtr005_mudg.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | MUDG | DTR002 | — | Via `gen_dtr006_mudg.py` |
| 2026-04-28 | nateric | Deleted | CTN2026003 | MUDG | DTR002 | — | Test draft — removed during MUDG skill development |
| 2026-04-28 | nateric | Deleted | CTN2026003 | MUDG | DTR002 | — | Test draft — removed during MUDG skill development |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Via `gen_dtr001_fa_sbc.py` |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via `gen_dtr002_fa_sbc.py` |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Test draft — removed during FA skill development |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Test draft — removed during FA skill development |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.1 | Regen after skill fixes |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.1 | Test draft — removed |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.3 | Intermediate draft — superseded |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.3 | Superseded by final IOS XE 26.0 version |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Intermediate draft — superseded |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Superseded — DTR003 not current on disk |
| 2026-05-07 | nateric | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Final DTR001 FA — deleted 2026-05-12 (see fresh-start row) via `gen_dtr001_fa_sbc.py` |
| 2026-05-07 | nateric | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Deleted 2026-05-12 (see fresh-start row) via `gen_dtr002_fa_sbc.py` |
| 2026-05-07 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.0 | Deleted 2026-05-12 (see fresh-start row) via `gen_dtr001_icrmemo_sbc.py` *(script deleted 2026-05-12 — superseded by `gen_dtr001_icrmemo_sbc_new.py`)* |
| 2026-05-07 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Deleted 2026-05-12 (see fresh-start row) via `gen_dtr002_icr_memo.py` |
| 2026-05-01 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | Cleared for newd workflow verification test |
| 2026-05-01 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | Cleared for newd workflow verification test |
| 2026-05-01 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Cleared for newd workflow verification test |
| 2026-05-04 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | ASR 1006-X sustained at 17.18, C8300/C8200/C8000v updating. Via `gen_dtr001_sbc_sysdesc_v2.py` — deleted 2026-05-12 (see fresh-start row below) |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Via `gen_dtr001_fa_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Via `gen_dtr002_fa_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Via `gen_dtr003_fa_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 28.2 | Via `gen_dtr004_fa_sbc.py` — new platform 8300 Secure Router Platform; ASR1006-X (IWG/SBC) sustained |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 24.6 | Via `gen_dtr001_icrmemo_sbc.py` *(script deleted 2026-05-12 — superseded by `gen_dtr001_icrmemo_sbc_new.py`)* |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.0 | Via `gen_dtr002_icr_memo_new.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.5 | Via `gen_dtr003_icr_memo_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 29.0 | Via `gen_dtr004_icr_memo_new.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Via `gen_dtr005_icr_memo.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Via `gen_dtr006_icr_memo.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 28.0 | Via `gen_dtr007_icr_memo_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | Via `gen_dtr002_sbc_sysdesc_v2.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Via `gen_dtr003_sbc_sysdesc_v2.py` |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 28.2 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 24.6 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.5 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 29.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 28.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | Fresh start — clearing all SysDesc drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | Fresh start — clearing all SysDesc drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Fresh start — clearing all SysDesc drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via `gen_dtr001_fa_sbc.py` — all platforms updating; new platform 8300 Secure Router (IWG/SBC, SBC, IWBC); testing 05 Jun–08 Jul 2026 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Generated in error (premature); deleted immediately; not reviewed |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Architecture redesign — clearing all drafts before parameterized runner build |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Architecture redesign — clearing all drafts before parameterized runner build |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Architecture redesign — clearing all drafts before parameterized runner build |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Architecture redesign — clearing all drafts before parameterized runner build |

| 2026-05-13 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via run_fa.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Test run during run_fa.py build session — deleted before afternoon testing |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via run_fa.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Test run during run_fa.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.2 | Via run_icr_memo.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.2 | Test run during run_icr_memo.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Via run_sysdesc.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Test run during run_sysdesc.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | MUDG | DTR002 | — | Via run_mudg.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Test run during run_mudg.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.4 | Via newd — ASR 1006-X sustained at 17.18; C8300/C8200/C8000v updating to 26.4; similarity ESC CTN2026001 DTR92; release notes expected Aug 2026 |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.4 | Test draft — deleted after ASR row fix and cross-check validation |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.3 | Via newd — ASR 1006-X sustained at 17.18; C8300/C8200/C8000v updating to 26.3; release notes expected Aug 2026 |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.3 | Test draft — deleted after example file fix validation |
| 2026-05-18 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-06-01 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via run_fa.py parameterized runner |
| 2026-06-01 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Via run_fa.py parameterized runner |
| 2026-06-01 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Via run_fa.py parameterized runner |
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | First bootstrap from INITIAL source via `generate_dtr.py` *(script retired — superseded by run_sysdesc.py)* |
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | All platforms updating via `gen_dtr002_sbc_sysdesc_v2.py` |
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Initial DTR003 attempt via `gen_dtr003_sbc_sysdesc.py` — superseded (script deleted, replaced by v2) |
| 2026-04-28 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Superseded by v2 (wrong version target) |
| 2026-04-28 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Corrected version — ASR sustained, C8300/C8200/C8000v updating via `gen_dtr003_sbc_sysdesc_v2.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.0 | First ICR Memo draft via `gen_dtr004_icr_memo.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Via `gen_dtr005_icr_memo.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Via `gen_dtr006_icr_memo.py` |
| 2026-04-28 | nateric | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.0 | Test draft — removed during ICR Memo skill development |
| 2026-04-28 | nateric | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Test draft — removed during ICR Memo skill development |
| 2026-04-28 | nateric | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Test draft — removed during ICR Memo skill development |
| 2026-04-28 | nateric | Generated | CTN2026003 | MUDG | DTR002 | — | Via `gen_dtr005_mudg.py` |
| 2026-04-28 | nateric | Generated | CTN2026003 | MUDG | DTR002 | — | Via `gen_dtr006_mudg.py` |
| 2026-04-28 | nateric | Deleted | CTN2026003 | MUDG | DTR002 | — | Test draft — removed during MUDG skill development |
| 2026-04-28 | nateric | Deleted | CTN2026003 | MUDG | DTR002 | — | Test draft — removed during MUDG skill development |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Via `gen_dtr001_fa_sbc.py` |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via `gen_dtr002_fa_sbc.py` |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Test draft — removed during FA skill development |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Test draft — removed during FA skill development |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.1 | Regen after skill fixes |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.1 | Test draft — removed |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.3 | Intermediate draft — superseded |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.3 | Superseded by final IOS XE 26.0 version |
| 2026-04-28 | jmisal | Generated | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Intermediate draft — superseded |
| 2026-04-28 | jmisal | Deleted | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Superseded — DTR003 not current on disk |
| 2026-05-07 | nateric | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Final DTR001 FA — deleted 2026-05-12 (see fresh-start row) via `gen_dtr001_fa_sbc.py` |
| 2026-05-07 | nateric | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Deleted 2026-05-12 (see fresh-start row) via `gen_dtr002_fa_sbc.py` |
| 2026-05-07 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.0 | Deleted 2026-05-12 (see fresh-start row) via `gen_dtr001_icrmemo_sbc.py` *(script deleted 2026-05-12 — superseded by `gen_dtr001_icrmemo_sbc_new.py`, also deleted — all superseded by `run_icr_memo.py`)* |
| 2026-05-07 | nateric | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Deleted 2026-05-12 (see fresh-start row) via `gen_dtr002_icr_memo.py` |
| 2026-05-01 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | Cleared for newd workflow verification test |
| 2026-05-01 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | Cleared for newd workflow verification test |
| 2026-05-01 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Cleared for newd workflow verification test |
| 2026-05-04 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | ASR 1006-X sustained at 17.18, C8300/C8200/C8000v updating. Via `gen_dtr001_sbc_sysdesc_v2.py` — deleted 2026-05-12 (see fresh-start row below) |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Via `gen_dtr001_fa_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Via `gen_dtr002_fa_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Via `gen_dtr003_fa_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 28.2 | Via `gen_dtr004_fa_sbc.py` — new platform 8300 Secure Router Platform; ASR1006-X (IWG/SBC) sustained |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 24.6 | Via `gen_dtr001_icrmemo_sbc.py` *(script deleted 2026-05-12 — superseded by `gen_dtr001_icrmemo_sbc_new.py`, also deleted — all superseded by `run_icr_memo.py`)* |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.0 | Via `gen_dtr002_icr_memo_new.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.5 | Via `gen_dtr003_icr_memo_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 29.0 | Via `gen_dtr004_icr_memo_new.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Via `gen_dtr005_icr_memo.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Via `gen_dtr006_icr_memo.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 28.0 | Via `gen_dtr007_icr_memo_sbc.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | Via `gen_dtr002_sbc_sysdesc_v2.py` |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Via `gen_dtr003_sbc_sysdesc_v2.py` |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.0 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 27.0 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 28.2 | Fresh start — clearing all FA drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 24.6 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 25.5 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 29.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.5 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 27.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 28.0 | Fresh start — clearing all ICR Memo drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.0 | Fresh start — clearing all SysDesc drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.5 | Fresh start — clearing all SysDesc drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.6 | Fresh start — clearing all SysDesc drafts to regenerate from DTR001 |
| 2026-05-12 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via `gen_dtr001_fa_sbc.py` — all platforms updating; new platform 8300 Secure Router (IWG/SBC, SBC, IWBC); testing 05 Jun–08 Jul 2026 |
| 2026-05-12 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.5 | Generated in error (premature); deleted immediately; not reviewed |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Architecture redesign — clearing all drafts before parameterized runner build |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Architecture redesign — clearing all drafts before parameterized runner build |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Architecture redesign — clearing all drafts before parameterized runner build |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Architecture redesign — clearing all drafts before parameterized runner build |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via run_fa.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Test run during run_fa.py build session — deleted before afternoon testing |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Via run_fa.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | FA | DTR002 | IOS XE 26.2 | Test run during run_fa.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.2 | Via run_icr_memo.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | ICR Memo | DTR002 | IOS XE 26.2 | Test run during run_icr_memo.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Via run_sysdesc.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Test run during run_sysdesc.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | MUDG | DTR002 | — | Via run_mudg.py parameterized runner |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | MUDG | DTR002 | — | Test run during run_mudg.py afternoon testing — deleted before full session commit |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.4 | Via newd — ASR 1006-X sustained at 17.18; C8300/C8200/C8000v updating to 26.4; similarity ESC CTN2026001 DTR92; release notes expected Aug 2026 |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.4 | Test draft — deleted after ASR row fix and cross-check validation |
| 2026-05-13 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.3 | Via newd — ASR 1006-X sustained at 17.18; C8300/C8200/C8000v updating to 26.3; release notes expected Aug 2026 |
| 2026-05-13 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.3 | Test draft — deleted after example file fix validation |
| 2026-05-18 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-18 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Starting over — will regenerate from scratch |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 1 of 8 during runner bug-fix session |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 1 of 8 — deleted during session |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 2 of 8 |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 2 of 8 — deleted during session |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 3 of 8 |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 3 of 8 — deleted during session |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 4 of 8 |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 4 of 8 — deleted during session |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 5 of 8 |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 5 of 8 — deleted during session |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 6 of 8 |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 6 of 8 — deleted during session |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 7 of 8 |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 7 of 8 — deleted during session |
| 2026-05-19 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py — iterative test run 8 of 8 |
| 2026-05-19 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Test run 8 of 8 — all 8 test drafts deleted; DTR001 still pending clean generation |
| 2026-05-20 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Via run_sysdesc.py parameterized runner |
| 2026-05-26 | jmisal | Generated | CTN2026003 | MUDG | DTR002 | — | Via run_mudg.py — deleted FHRP sentence from Redundancy section |
| 2026-05-26 | jmisal | Generated | CTN2026003 | TDR | DTR002 | IOS XE 26.5 | TDR26003-02 — UCR 2013 Change 2 Section 2.6.2 |
| 2026-05-26 | edknowlt | Generated | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Via run_sysdesc.py — ASR 1006-X sustained at 17.18; C8300/C8200/C8000v updating from 26.1 to 26.2; release notes expected Aug 2026 |
| 2026-05-27 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.1 | Clean slate — clearing all SysDesc drafts to regenerate from scratch |
| 2026-05-27 | edknowlt | Deleted | CTN2026003 | System Description | DTR002 | IOS XE 26.2 | Clean slate — clearing all SysDesc drafts to regenerate from scratch |
| 2026-06-02 | jmisal | Generated | CTN2026003 | CSR | DTR002 | IOS XE 26.1 | Via run_csr.py parameterized runner |
---

## Known Issues / Gotchas

| # | Issue | Resolution |
|---|---|---|
| 1 | DTR000 INITIAL doc has different component table structure (11 rows, IWBC naming) vs DTR001+ (14 rows, IWG/SBC naming) | Preserve the INITIAL table — never remove it. Clone the 14-row table from Example DTR001 and insert the full DTR section after the INITIAL table |
| 2 | Notes list numbering does not restart at 1 across tables by default | Create new `w:num` with `w:lvlOverride` + `w:startOverride val=1` and unique `numId` per table |
| 3 | `Example_*` and `Template_*` files look like source docs but are reference only | Only use files starting with `CTN*` or `Draft_*` as source |
| 4 | Version downgrades are valid in this workflow (e.g. 27.0 → 26.9) | Always confirm with user before proceeding when new version < current version |
| 5 | ~~`System Discription` folder name~~ | Corrected to `System Description` — all folders and references updated |
| 6 | Multiple platforms updating from different `from` versions need separate paragraphs | Group by `(from_ver, to_ver)` tuple, generate one paragraph per unique pair |
| 7 | DTR sections and Management Description don't start on a new page | Add `w:pageBreakBefore` to `w:pPr` of every `Desktop Review (DTR)` heading and `Management Description` only — **not** `DTR Detailed Component Information` (table flows freely) |
| 8 | New DTR body paragraphs cloned with wrong style (Heading1 instead of BodyText) | Use a `BodyText` paragraph from the DTR1 section as the clone template — not the heading element |
| 9 | New DTR headings render at wrong size (missing `w:sz`) | Clone full `w:rPr` from source run — never build bare runs without run properties |
| 10 | Detail heading incorrectly includes DTR number (`DTR 2 Detailed Component Information`) | Always use fixed text `DTR Detailed Component Information` — no number |
| 11 | TOC and `System Description` body heading don't start on a new page | On document creation: insert empty paragraph with `w:pageBreakBefore` before `<sdt>` TOC; add `w:pageBreakBefore` to `System Description` `Heading1`; remove empty `Heading1` spacer between them |
| 12 | Example DTR001 file has `IOS XE 17.15` in ASR 1006-X rows (rows 1–3) — these are reference rows only, not the actual certified version | After generating DTR001, verify ASR 1006-X rows show the correct sustained version (`IOS XE 17.18`). If the example file had a stale version, patch rows 1–3 directly in the draft. The runner's sustain logic correctly skips those rows during generation — the problem is the source data in the example file, not the runner logic. |

---

## Runner Architecture Standard

All document-type runners (`run_*.py`) must follow this structure without exception. When building a new runner, use an existing completed runner as the reference implementation and follow this spec exactly.

### Required File Structure

```
# 1. Module docstring — identifies doc type, replaces list, usage
# 2. Imports — stdlib, then sys.path insert, then runner_core, then lxml/docx
# 3. Path helpers — *_dir(), *_draft_path(), *_initial_path(), *_example_path()
# 4. Generation functions — generate_dtr001(cfg) and generate_dtr_incremental(cfg)
#    - Both accept a single cfg dict
#    - Both call doc.save(str(out_path)) at the end
# 5. Seed profiles dict — CTN-specific pre-baked configs for DTR001 only
#    - Key = dtr_num (int), Value = cfg dict
#    - DTR002+ have NO pre-baked profiles — fully prompted at runtime
# 6. run(prod_cat, ctn, dtr_num) — callable entry point for newd prompt sequence dispatch
#    - Loads profile if available, else prompts for all inputs
#    - Calls generate_dtr001 or generate_dtr_incremental
#    - Calls run_validate(out_path)
#    - Calls append_draft_log(...)
# 7. main() — thin wrapper: prompts for prod_cat, ctn, dtr_num, then calls run()
# 8. if __name__ == "__main__": main()
```

### Required Imports

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from runner_core import run_validate, append_draft_log, BASE
from docx import Document
```

### Required Post-Generation Steps (inside `run()`)

Every runner must call these two in order after `doc.save()`:
1. `run_validate(out_path)` — lints the generated document
2. `append_draft_log(engineer, action, ctn, doc_type, dtr, version, reason)` — logs to Draft Log

### `run()` Function Signature

```python
def run(prod_cat: str, ctn: str, dtr_num: int) -> None:
    """Callable entry point — invoked by the newd prompt sequence or directly via main()."""
```

### `main()` Wrapper Pattern

```python
def main():
    prod_cat = input("Product Category (e.g. SBC): ").strip()
    ctn = input("CTN (e.g. CTN2026003): ").strip()
    dtr_num = int(input("DTR Number (e.g. 1): ").strip())
    run(prod_cat, ctn, dtr_num)

if __name__ == "__main__":
    main()
```

### Seed Profile Rules
- DTR001 seed profile for each known CTN is pre-baked in the runner
- DTR002+ are **never** pre-baked — all inputs are prompted at runtime
- When a new CTN is onboarded, add its DTR001 profile to the relevant runner's profiles dict

### Skeleton vs Complete Runner
- **Skeleton** (`# STATUS: SKELETON`): path helpers and structure in place; `generate_dtr001` and `generate_dtr_incremental` raise `NotImplementedError`. Unblocked when example `.docx` files are placed.
- **Complete** (`# STATUS: COMPLETE`): all generation logic implemented and tested.

---

## Script Inventory

| Script | Location | Purpose |
|---|---|---|
| `runbook_updater.py` | `_Runbook/` | Auto-runs when engineer types `newd` — syncs new drafts into the runbook before generation begins. Can also be run manually at any time. |
| `validate_doc.py` | `_Tools/` | Post-generation document linter — run after every DTR generation to check structure, headings, tables, and hyperlinks. Usage: `python3 _Tools/validate_doc.py <file>` |
| `finalize_doc.py` | `_Tools/` | Finalization pipeline — copies a `Draft_*.docx` to the `Final/` subfolder (renamed without `Draft_` prefix), converts to PDF via Word AppleScript (macOS) or LibreOffice fallback, and attempts to inject an AcroForm signature field. Usage: `python3 _Tools/finalize_doc.py <Draft_*.docx>`. Run `--check-deps` first to verify converter availability. |
| `scaffold_ctn.py` | `_Tools/` | Creates the standard 9-document-type folder structure for a new CTN. Safe to run on an existing CTN — skips folders that already exist. Usage: `python3 _Tools/scaffold_ctn.py <ProductCategory> <CTN>` |
| `trim_backups.py` | `_Tools/` | Manual bulk backup trimmer — groups backups per engineer, keeps last N (default 10), supports `--dry-run` and `--summary` flags. Usage: `python3 _Tools/trim_backups.py [--keep N] [--dry-run] [--summary]` |
| `runner_core.py` | `_Tools/` | **Shared library** — XML utilities, path helpers for all doc types (`fa_*`, `sysdesc_*`, `memo_*`, `mudg_*`, `tdr_*`, `csr_*`, `loc_*`, `poam_*`, `system_diagram_*`), `run_validate`, `append_draft_log`. Imported by all `run_*.py` runners. Do not invoke directly. |
| `generate.py` | `_Tools/` | **Dispatcher** — interactive CLI that prompts for Product Category, CTN, Document Type, and DTR number, then delegates to the appropriate `run_*.py` runner's `run()` entry point. Usage: `python3 _Tools/generate.py` |
| `run_fa.py` | `_Tools/` | **Parameterized runner** ✅ COMPLETE — Functionality Attestation. Handles all DTR numbers and all CTNs. DTR001 seed profile for SBC/CTN2026003; DTR002+ fully prompted at runtime. |
| `run_icr_memo.py` | `_Tools/` | **Parameterized runner** ✅ COMPLETE — ICR Summary Memorandum. Handles all DTR numbers and all CTNs. DTR001 seed profile for SBC/CTN2026003; DTR002+ fully prompted at runtime. |
| `run_sysdesc.py` | `_Tools/` | **Parameterized runner** ✅ COMPLETE — System Description. Handles all DTR numbers and all CTNs. DTR001 seed profile for SBC/CTN2026003; DTR002+ fully prompted at runtime. |
| `run_mudg.py` | `_Tools/` | **Parameterized runner** ✅ COMPLETE — Military Unique Deployment Guide. Handles all DTR numbers and all CTNs. DTR005 seed profile for SBC/CTN2026003 (anomaly: MUDG was already at DTR004 when the parameterized runner was built — DTR005 is the first runner-generated draft); DTR006+ fully prompted at runtime. |
| `run_tdr.py` | `_Tools/` | **Parameterized runner** ✅ COMPLETE — Test Discrepancy Report. Standalone per-finding generation from Template; auto-increments TDR sequence number; all fields prompted at runtime. |
| `run_csr.py` | `_Tools/` | **Parameterized runner** ✅ COMPLETE — Cybersecurity Summary Report. Handles all DTR numbers and all CTNs. All inputs prompted at runtime. |
| `run_loc.py` | `_Tools/` | **Parameterized runner** 🔲 SKELETON — Letter Of Compliance. Unblocked when example `.docx` files are placed in LoC `Examples & Templates/`. |
| `run_poam.py` | `_Tools/` | **Parameterized runner** ✅ COMPLETE — Plan of Action & Milestone. Generates standalone POA&M documents from the Template file. All inputs prompted at runtime; product description reused from most recent TDR/POA&M via label search. |
| `run_system_diagram.py` | `_Tools/` | **Parameterized runner** 🔲 SKELETON — System Diagram. Unblocked when example `.vsdx` files are placed in System Diagram `Examples & Templates/`. |


---

## Shortcut Commands

| Shortcut | Action |
|---|---|
| `newd` | Auto-syncs runbook then begins DTR generation prompt sequence. **Must read `skill_base.md` first. All prompts must be clickable selections — never plain text. No exceptions.** |
| `new dtr` | Same as `newd` — alternate trigger. Same rules apply. |
| `finalize` | Finalize a draft — generates Final .docx + PDF with signature field. Offered automatically after every successful generation. See per-doc-type skill for full flow. |
| `prnts` | Print live folder structure from disk |
| `myb` | Show current git branch name |
| `cm1` | Commit and push to `main` — always requires a second clickable confirmation |
| `sbh` | Show branch health — fetch latest and display ahead/behind status for all three branches vs main |
| `sync` | Sync `edknowlt` with `origin/main` — push, pull from main, push again |
| `/adt` | Run full audit — two-pass scan of all scripts and markdown files for bugs, stale references, and dirty code. Also triggered by `qac`. **Must read `skill_base.md` before running — no exceptions.** |
| `qac` | Same as `/adt` — alternate trigger for full audit. Same rules apply. |

---

## DTR Generation Prompt List

When you type `newd` or `new dtr`, the AI will ask these questions in order:

1. **Product Category** — which product category? *(read live from folders)*
2. **CTN** — which CTN? *(read live from folders)*
3. **Document Type** — which document type? *(read live from folders)*
   - After step 3, the AI immediately loads the matching skill file for that document type
   - **All prompts from step 4 onward are defined in the per-doc-type skill file** — they will differ across document types
   - See `_Skills/skill_[doctype].md` for the full prompt list and generation rules for each document type

### If Your Session Was Interrupted

If your session was dismissed, closed, or interrupted mid-`newd`:

1. Just type `newd` again — the AI will start fresh from step 1
2. There is no resume — every `newd` starts from the beginning
3. No partial work is saved from an interrupted session — nothing will be committed or written until you complete the full sequence and confirm

> This is intentional. Starting clean is always safe.

---

## Commit Standard — All Engineers
After every file is ready to commit, the AI will always present a **clickable branch selection**:

> **"Ready to commit — which branch?"**

| Option | When to use |
|---|---|
| Your personal branch (e.g. `edknowlt`) | Day-to-day work, drafts in progress |
| `main` | Approved, reviewed work only — AI will ask for confirmation before pushing |

**Rules:**
- The AI reads your current branch live — never hardcoded
- Never commit without this prompt appearing first
- Pushing to `main` requires a second confirmation — it is the source of truth
- All draft generation work stays on your personal branch until reviewed and approved

---

## Skills Reference
AI skill files live in `_Skills/`. Each session should load `skill_base.md` first — it contains all shared rules and the **Document Type Router**.

### How the Document Type Router Works
When an engineer selects a document type during the prompt sequence (step 3), the AI automatically reads the matching skill file from `_Skills/` before continuing. This ensures every engineer on every machine follows the exact same generation rules for that document type.

- If the skill file is **fully built** → AI proceeds with doc-type-specific rules
- If the skill file is **scaffolded only** (no example docs templated yet) → AI warns the engineer and proceeds with base rules only

### Skill File Map
| Skill File | Document Type | Status |
|---|---|---|
| `skill_base.md` | Shared rules + Document Type Router | Complete |
| `skill_system_description.md` | System Description | Complete |
| `skill_fa.md` | Functionality Attestation (FA) | Complete |
| `skill_icr_memo.md` | ICR Summary Memorandum (ICR Memo) | Complete |
| `skill_mudg.md` | Military Unique Deployment Guide (MUDG) | Complete |
| `skill_csr.md` | Cybersecurity Summary Report (CSR) | Complete |
| `skill_loc.md` | Letter Of Compliance (LoC) | Scaffolded |
| `skill_poam.md` | Plan of Action & Milestone (POA&M) | Complete |
| `skill_system_diagram.md` | System Diagram | Scaffolded |
| `skill_tdr.md` | Test Discrepancy Report (TDR) | Complete |

> To fully build out a scaffolded skill: place an example document in that doc type's `Examples & Templates/` folder, then work with the AI to extract the structure and update the skill file. Mark the Generation Status checklist items complete as you go.

---

## Folder Structure

```
ICR_Automation/
├── _Runbook/
│   ├── ICR_Automation_Runbook.md        ← this file
│   ├── runbook_updater.py               ← auto-update watcher
│   ├── runbook_updater_launcher.sh      ← shell wrapper for launchd auto-run
│   ├── com.icr.runbook_updater.plist    ← launchd job definition (runs --once on login)
│   ├── runbook_updater.log              ← stdout log from launchd runs
│   ├── runbook_updater_error.log        ← stderr log from launchd runs
│   └── Backup/
└── Product Category/
    ├── ESC/
    │   └── CTN2026001/
    │       ├── Cybersecurity Summary Report (CSR)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Functionality Attestation (FA)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── ICR Summary Memorandum (ICR Memo)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Letter Of Compliance (LoC)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Military Unique Deployment Guide (MUDG)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Plan of Action & Milestone (POA&M)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── System Diagram/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── System Description/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       └── Test Discrepancy Report (TDR)/
    │           ├── Drafts/
    │           └── Examples & Templates/
    ├── SBC/
    │   └── CTN2026003/
    │       ├── Cybersecurity Summary Report (CSR)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Functionality Attestation (FA)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── ICR Summary Memorandum (ICR Memo)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Letter Of Compliance (LoC)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Military Unique Deployment Guide (MUDG)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── Plan of Action & Milestone (POA&M)/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── System Diagram/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       ├── System Description/
    │       │   ├── Drafts/
    │       │   └── Examples & Templates/
    │       │       ├── CTN2026003 - DTR000 - INITIAL - SBC - Cisco ICR System Description.docx
    │       │       └── Example_CTN2026003 - DTR001 - SBC - IOS XE 17.15 - Cisco ICR System Description.docx
    │       └── Test Discrepancy Report (TDR)/
    │           ├── Drafts/
    │           └── Examples & Templates/
    └── SS/
        └── CTN2026002/
            ├── Cybersecurity Summary Report (CSR)/
            ├── Functionality Attestation (FA)/
            ├── ICR Summary Memorandum (ICR Memo)/
            ├── Letter Of Compliance (LoC)/
            ├── Military Unique Deployment Guide (MUDG)/
            ├── Plan of Action & Milestone (POA&M)/
            ├── System Diagram/
            ├── System Description/
            └── Test Discrepancy Report (TDR)/
                ├── Drafts/
                └── Examples & Templates/
```

---

## File Naming Rules

| File Type | Naming Pattern | Notes |
|---|---|---|
| Initial CTN doc | `CTN[number] - DTR000 - INITIAL - [ProdCat] - Cisco ICR [DocType].docx` | Base document, no DTR yet |
| Draft (in progress) | `Draft_CTN[number] - DTR[###] - [ProdCat] - [Version] - Cisco ICR [DocType].docx` | Saved to `Drafts/` folder |
| Example (reference) | `Example_CTN[number] - DTR[###] - ...` | INFO ONLY — never used as source |
| Template | `Template_CTN0000000 - DTR000 - ...` | INFO ONLY — never used as source |

**Key rules:**
- `Example_*` and `Template_*` files = reference/learning only, never used as source
- `CTN*` and `Draft_*` files = working documents, used as source for next DTR
- DTR number AND IOS XE version must both be updated in the filename
- All new drafts saved to the `Drafts/` subfolder

---

## Document Types (9 Total)

1. System Description (`System Description/`) ← note spelling
2. ICR Summary Memorandum (ICR Memo)
3. Functionality Attestation (FA)
4. Military Unique Deployment Guide (MUDG)
5. Cybersecurity Summary Report (CSR)
6. System Diagram
7. Plan of Action & Milestone (POA&M)
8. Letter Of Compliance (LoC)
9. Test Discrepancy Report (TDR)

---

## Prompt Order (Every New DTR)

When you type `newd` or `new dtr`, the AI first asks:

> **"What would you like to do?"**
> - **New DTR** — increment an existing CTN
> - **New Initial TN** — brand new TN from scratch

---

### New DTR

1. **Product Category** — read live from `Product Category/` subfolders, plus **"+ New Product Category"**
   - If selected: prompt for name → create folder → continue
2. **CTN** — read live from subfolders under chosen Product Category, plus **"+ New CTN"**
   - If selected: prompt for CTN number → run `scaffold_ctn.py` → confirm → continue
3. **Document Type** — read live from subfolders under chosen CTN
   - AI loads the matching skill file — all remaining prompts are doc-type specific

### New Initial TN

1. **Product Category** — read live, plus **"+ New Product Category"**
2. **New CTN number** (manual entry) → `scaffold_ctn.py` runs automatically → confirms folders created
3. **Stop** — AI instructs engineer to place `CTN* - DTR000 - INITIAL - *` docs in each doc type's `Examples & Templates/` folder, then type `newd` → New DTR when ready

---

## Platform Map (System Description — SBC)

| Platform | Table Row Indices | Current Version (as of DTR000 Initial) | Notes |
|---|---|---|---|
| ASR 1006-X | 1, 2, 3 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| C8300 series | 4, 5, 6 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| C8200 series | 7, 8, 9 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| C8000v series | 10, 11, 12 | IOS XE 17.18 | Rows: IWG, SBC, IWG/SBC |
| Notes row | 13 | — | Numbered list — must restart at 1 per table using `w:lvlOverride` |

> **Always confirm current versions by reading the last working document before prompting.**

---

## DTR Generation Logic (System Description)

### Source Document Selection
- If no drafts exist in `Drafts/`: use the `CTN* - DTR000 - INITIAL - *` doc from `Examples & Templates/`
- If drafts exist: use the highest DTR number draft from `Drafts/`
- Next DTR number = highest existing DTR + 1

### What Gets Added Per DTR
1. **Revision history row**: auto-increment version (e.g. `1.0` → `2.0`), date = current month/year, change = `Update for DTR [N]`, editor = `GCT DP Collaboration`
2. **DTR heading**: `Desktop Review (DTR) [N]` — cloned from previous DTR heading, number updated; **must include `w:pageBreakBefore`** so each DTR starts on a new page
3. **Main update paragraph** — two variants depending on whether the platform is new or existing:
   - **Existing platform updating**: `This DTR updates the Session Border Controller (SBC) IOS XE software on [hw list] of SBC router platforms. The IOS XE software version is being updated from [FROM] to [NEW].`
   - **New platform being added** (no prior version): `This DTR adds the Session Border Controller (SBC) IOS XE software on [hw list] of SBC router platforms. The IOS XE software version is [NEW].`
   - Keep "adds" and "updates" paragraphs separate — never mix new and existing platforms in the same paragraph
4. **Similarity paragraph** (if included): `Request certification through similarity based on "[Product Category] TN: [CTN], DTR[XX]."` — always this exact format; the referenced TN is typically a **different** CTN than the one being worked; prompted with TN Product Category (dynamic from folders), TN CTN (dynamic from folders), DTR number (manual entry)
5. **POA&M paragraph** (if included): `This DTR Clears POA&M/TDR Number: [NUMBER], [PROBLEM DESCRIPTION].` — prompted with POA&M/TDR Number (manual) and Problem Description (manual)
6. **Sustain paragraph** (for each platform NOT updating): `The [Platform] will be sustained on the current software load of [version].`
7. **Release Notes paragraph**: if engineer accepted webfetch, use fetched date + URL per platform; otherwise use: `Release Notes for all devices will be provided once they become available, expected [DATE].`
   - **Only include release notes for platforms that are updating. Sustained platforms do not get a release notes entry.**
   - **If the webfetch returns a 404 or no usable content**, prompt the engineer for an expected date and use the standard fallback paragraph instead — do not error out
   - A successful fetch and a fallback can coexist in the same DTR (e.g. one platform fetched, another not yet published)
8. **DTR Detailed Component Information heading**: cloned from previous; text is always `DTR Detailed Component Information` (no DTR number); **no `w:pageBreakBefore`** — table flows naturally
9. **Component table**: cloned from previous DTR's table, versions updated per platform

### Hardware Name Strings (used in paragraphs)
- `the ASR 1006-X`
- `the C8300 series`
- `the C8200 series`
- `the C8000v series`

### Sustain Paragraph Name Strings
- `ASR 1006-X`
- `C8300 Series`
- `C8200 Series`
- `C8000v Series`

### Multi-Platform Grouping
- If multiple platforms update from the **same** version → combine into one sentence
- If platforms update from **different** versions → one paragraph per unique `from` version
- List format: `A, B, and C` / `A and B` / `A`

### Notes List Numbering Fix
- Every DTR component table has a Notes row with a numbered list
- Each table's list must restart at `1.`
- Fix: create a new `w:num` entry with `w:lvlOverride` + `w:startOverride val=1` and assign unique `numId`
- Source `numId=13` / `abstractNumId` from the reference document's numbering part — **this value is specific to CTN2026003's INITIAL document; verify against the actual source doc for other CTNs**

---

## First DTR from Initial Doc (Special Case)

When building DTR001 from a `DTR000 - INITIAL` document:
- The initial doc has a different component table structure (11 rows, `IWBC`/`SBC` naming, no Notes row)
- Use the **Example DTR001** file's component table structure as the template for the new DTR table (14 rows with Notes row)
- Clone all DTR section elements (heading, body paragraphs, detail heading, table) from the Example file
- Insert after the `Detailed Component Information` heading in the initial doc
- Copy the numbering `abstractNum` definition from the reference doc into the source doc if not present

---

## Version Downgrade Warning
If the requested new version is **lower** than the current platform version, always confirm with the user before proceeding.

---

## Release Notes Webfetch

At Step 9 of the prompt sequence, the AI will offer to webfetch official Cisco release notes for the version(s) being certified. This is presented as a clickable option.

**Rules:**
- Only official `cisco.com` URLs are used — never third-party sources
- The AI extracts the **Updated:** date from the fetched page and uses it as the release date
- If a URL is not in the known table, the AI constructs it from the URL pattern and verifies it live before presenting to the engineer
- If the fetch fails, the AI falls back to manual date entry

**Known release notes URL patterns (confirmed live):**

| Platform | Version | URL |
|---|---|---|
| ASR 1006-X | 17.18.x | `https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/xe-17-18/asr1000-rel-notes-xe-17-18.html` |
| ASR 1006-X | 17.16.x | `https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/xe-17-16/asr1000-rel-notes-xe-17-16.html` |
| ASR 1006-X | 17.15.x | `https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/xe-17-15/asr1000-rel-notes-xe-17-15.html` |
| C8300 / C8200 | 26.1.x | `https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/rel_notes/26-x/release-notes-catalyst-8200-and-catalyst-8300-series-edge-platforms-release-26-1-x.html` |
| C8300 / C8200 | 17.18.x | `https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/rel_notes/17-18-x/release-notes-catalyst-8200-and-catalyst-8300-series-edge-platforms-release-17-18-x.html` |
| C8300 / C8200 | 17.16.x | `https://www.cisco.com/c/en/us/td/docs/routers/cloud_edge/c8300/rel_notes/17-16-x/cat8200-and-8300-rel-notes-xe-17-16-x.html` |
| C8000v | 26.1 | `https://www.cisco.com/c/en/us/td/docs/routers/C8000V/Release-Notes/c8000v-releasenotes-26-1.html` |
| C8000v | 17.18.x | `https://www.cisco.com/c/en/us/td/docs/routers/C8000V/Release-Notes/c8000v-releasenotes-17-18.html` |

Full URL table is maintained in `_Skills/skill_system_description.md` under **Release Notes Webfetch**.

---

## Restricted Folders
- Any folder named `Test_doc_update/` on any engineer's machine — **OFF LIMITS**, do not access

---

## Adding a New CTN

Every CTN must have the same standard folder structure — 9 document type folders, each with `Drafts/` and `Examples & Templates/` subfolders. **Always use `scaffold_ctn.py` — never create CTN folders manually.**

```bash
python3 _Tools/scaffold_ctn.py <ProductCategory> <CTN>

# Example:
python3 _Tools/scaffold_ctn.py SBC CTN2026004
```

After scaffolding:
1. Place example `.docx` files in each doc type's `Examples & Templates/` folder
2. `git add` the new CTN folders and commit
3. Add the CTN to the Pending DTRs table above
4. Type `newd` to begin generation

Running the script on an existing CTN is safe — it skips folders that already exist.

---

## Auto-Run Setup (New Mac Onboarding)
The runbook updater runs **once at login** via a macOS launchd job to sync any new drafts that landed since the last session. A new engineer must install this once after cloning the repo.

> **Important:** The plist is configured with `--once` and `KeepAlive false` — it runs a single scan on login and exits. It does NOT run as a continuous background daemon. Running it continuously caused a race condition where the background watcher would rewrite the runbook mid-session, causing inconsistent `newd` prompts. The `newd` shortcut also triggers a manual `--once` scan at the start of every generation session.

**Files involved:**
- `_Runbook/com.icr.runbook_updater.plist` — launchd job definition (runs `--once` on login)
- `_Runbook/runbook_updater_launcher.sh` — shell wrapper ensuring correct PATH for launchd

**One-time install steps (Mac Terminal):**

```bash
# 1. Make the launcher executable
chmod +x ~/Documents/ICR_Automation/_Runbook/runbook_updater_launcher.sh

# 2. Copy the plist to the launchd agents folder
cp ~/Documents/ICR_Automation/_Runbook/com.icr.runbook_updater.plist \
   ~/Library/LaunchAgents/com.icr.runbook_updater.plist

# 3. Load the job (starts immediately and on every login)
launchctl load ~/Library/LaunchAgents/com.icr.runbook_updater.plist
```

**To verify it ran on login (check the log):**
```bash
tail -5 ~/Documents/ICR_Automation/_Runbook/runbook_updater.log
```

**Log files** (for debugging):
- `_Runbook/runbook_updater.log` — stdout
- `_Runbook/runbook_updater_error.log` — stderr

> Note: If you see errors in `runbook_updater_error.log` referencing an old path (e.g. `Desktop/openCode_P1/`), the plist was loaded before the repo was in its correct location. Unload, fix the path in the plist if needed, and reload:
> ```bash
> launchctl unload ~/Library/LaunchAgents/com.icr.runbook_updater.plist
> launchctl load ~/Library/LaunchAgents/com.icr.runbook_updater.plist
> ```

---

## Key Decisions Log

| Decision | Detail |
|---|---|
| File prefix | All generated files prefixed with `Draft_` |
| Output location | All drafts saved to `Drafts/` subfolder |
| Example files | Reference only, never used as source |
| Folder naming | `System Description` |
| Notes numbering | Fixed per-table using `w:lvlOverride` + unique `numId` |
| Revision history date format | Always use 3-letter abbreviated month + year: `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec`. After cloning revision rows from source doc, normalize any full month names (e.g. `March 2026` → `Mar 2026`) in all existing rows. |
| Editor field | Always `GCT DP Collaboration` |
| POA&M statement format | Always: `This DTR Clears POA&M/TDR Number: [NUMBER], [PROBLEM DESCRIPTION].` — prompt separately for number and description |
| Similarity statement format | Always: `Request certification through similarity based on "[ProdCat] TN: [CTN], DTR[XX]."` — no leading quote; prompt for TN Product Category (dynamic from folders), CTN (dynamic), DTR number (manual) |
| Table version replacement | Always target Release column (index 1) only; replace existing software version string with the new version — exact regex defined in per-doc-type skill file; never match by specific version number |
| Page breaks | Major section headings start on a new page — use `w:pageBreakBefore`. Component table detail headings do NOT get a page break — table flows freely. Specific heading names defined in per-doc-type skill file. |
| Backup filename format | `ICR_Automation_Runbook_<username>_<YYYY-MM-DD_HHMMSS>.md` — username from `git config user.name` (normalised), falling back to `$USER` |
| Backup trim policy | Keep last 10 per engineer — trimmed automatically by `runbook_updater.py` on every write; manual bulk trim via `python3 _Tools/trim_backups.py` |
