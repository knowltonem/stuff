# ICR Automation — OpenCode Session Rules

## MANDATORY SESSION-START — NO EXCEPTIONS

At the start of every session, before responding to anything, OpenCode must read both of these files in full from disk:

1. `_Skills/skill_base.md`
2. `_Runbook/ICR_Automation_Runbook.md`

Do not rely on session summaries, memory, or prior context. Reading from disk is the only acceptable source of truth.

This applies to ALL requests — including questions about project state, DTR history, file existence, and any shortcut command (`newd`, `qac`, `/adt`, etc.).

## Project Scope Restriction

Only access files within this project folder. Do not read, write, search, or reference any files outside of this directory.

## Branch Rule — Always Return to edknowlt

After any operation that requires switching to `main` (e.g. merge, pull, conflict resolution), **always switch back to the `edknowlt` branch when done — no exceptions.** Never leave the engineer on `main`.

## Sync Command

To sync `edknowlt` with `origin/main`, always run in this order:

```bash
git push origin edknowlt
git pull --no-rebase origin main
```

- Push first to preserve local work on the remote before pulling
- Use `--no-rebase` (merge strategy) — this is the standard for this repo
- If a conflict occurs in `_Runbook/ICR_Automation_Runbook.md` Pending DTRs table, always resolve by taking the version that reflects the true current state of files on disk
- After resolving any conflict: `git add -A && GIT_EDITOR=true git commit -m "..."` then `git push origin edknowlt`

## Current Focus

Active work is on System Description documents and skills only:
- `_Tools/run_sysdesc.py`
- `_Skills/skill_system_description.md`
- `_Skills/skill_base.md`
- System Description files under `Product Category/`

