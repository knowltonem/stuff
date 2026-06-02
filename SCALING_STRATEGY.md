# ICR Automation — Guardrails & Scaling Deployment Strategy

## PURPOSE

This document is a self-contained execution prompt. Hand it to OpenCode in a future session with the instruction: **"Read this file and execute the phase I tell you."** Each phase is independent and can be executed in any order, though the recommended sequence is Phase 1 → 5.

## CONTEXT

ICR_Automation is scaling from 3 engineers (edknowlt, jmisal, nateric) to 20+ engineers across 4 teams:

| Team | Product Focus |
|---|---|
| Collab (Collaboration) | UC/collaboration products (SBC, etc.) |
| Route/Switch | Enterprise routers and switches (ESC, etc.) |
| Wireless | Wireless infrastructure |
| Security | Network security appliances |

Each team will have its own Product Categories, CTNs, and engineers generating documents independently using the shared `_Tools/` and `_Skills/` infrastructure.

## RISK SUMMARY (from QAC scaling audit)

| # | Risk | Severity |
|---|---|---|
| 1 | No protection on `_Tools/`, `_Skills/` — any engineer can modify shared code | Critical |
| 2 | AI can modify shared code during `newd` document generation sessions | Critical |
| 3 | No document isolation — any engineer can generate/commit in any team's Product Category | Critical |
| 4 | Single `ICR_Automation_Runbook.md` touched by every operation = merge conflict bottleneck at 20 engineers | Critical |
| 5 | Branch-per-engineer (long-lived) doesn't scale — 20+ branches all merging into main | Critical |
| 6 | Direct push to main possible via `cm1` shortcut or terminal `git push` | High |
| 7 | No concurrent generation guard — two engineers generating same CTN/doc-type overwrite each other | High |
| 8 | Inexperienced engineer can prompt AI to modify runners or skill files | High |
| 9 | Cross-team CTN commits possible — no ownership validation at commit time | Medium |

---

## PHASE 1 — GitHub Protections (no code changes)

**Effort:** 30 minutes in GitHub repo settings
**Risk:** None — additive only, does not change existing behavior

### 1A. Enable Branch Protection on `main`

Go to: `wwwin-github.cisco.com` → `GCT-DP-Collaboration/ICR-Automation` → Settings → Branches → Add Rule

**Branch name pattern:** `main`

**Enable these settings:**
- [x] Require a pull request before merging
  - Required number of approvals: `1`
  - [x] Dismiss stale pull request approvals when new commits are pushed
  - [x] Require review from Code Owners
- [x] Require conversation resolution before merging
- [ ] Require status checks before merging (enable later in Phase 5 when CI exists)
- [x] Do not allow bypassing the above settings (apply to admins too)
- [ ] Allow force pushes — DISABLED
- [ ] Allow deletions — DISABLED

**What this blocks:**
- The `cm1` shortcut can no longer push directly to main — all changes go through PRs
- No engineer can `git push origin main` from their terminal
- Every PR to main requires at least 1 code owner approval

### 1B. Create CODEOWNERS File

**File:** `.github/CODEOWNERS`

```
# ═══════════════════════════════════════════════════
# ICR Automation — Code Ownership Rules
# ═══════════════════════════════════════════════════
# Code owners are automatically requested for review
# when a PR modifies files they own. With branch
# protection enabled, their approval is REQUIRED.
# ═══════════════════════════════════════════════════

# Core tooling — lead engineer approval required
_Tools/              @edknowlt
_Skills/             @edknowlt
_Runbook/            @edknowlt
.github/             @edknowlt
AGENTS.md            @edknowlt
requirements.txt     @edknowlt
.gitignore           @edknowlt

# Product categories — team-scoped ownership
# Update these as teams are assigned to categories.
# Format: path  @team-lead-username
#
# When a team is assigned, uncomment and fill in:
# Product\ Category/COLLAB/       @collab-lead-username
# Product\ Category/ROUTESWITCH/  @routeswitch-lead-username
# Product\ Category/WIRELESS/     @wireless-lead-username
# Product\ Category/SECURITY/     @security-lead-username
#
# Until teams are assigned, lead owns all:
Product\ Category/   @edknowlt
```

**Deployment steps:**
1. Create file at `.github/CODEOWNERS` in the repo
2. Commit to `main` (this is the one time you push directly — branch protection isn't active yet)
3. Then enable branch protection (1A above)
4. Test: create a test branch, modify a file in `_Tools/`, open a PR — verify edknowlt is auto-requested as reviewer

---

## PHASE 2 — AI Session Guardrails (AGENTS.md + skill_base.md)

**Effort:** 1-2 hours, markdown edits only
**Risk:** Low — adds restrictions, does not change generation logic

### 2A. Add Role-Based Restrictions to AGENTS.md

Append this section to `AGENTS.md` after the existing "Current Focus" section:

```markdown
## Engineer Roles & Permissions

### Tool Protection Rule — MANDATORY

During any `newd`, `new dtr`, `finalize`, or document generation session:
- **NEVER modify any file in `_Tools/`** — no exceptions
- **NEVER modify any file in `_Skills/`** — no exceptions
- **NEVER modify `AGENTS.md`** — no exceptions
- **NEVER modify `_Runbook/ICR_Automation_Runbook.md`** — no exceptions (runbook_updater.py handles this automatically)

If an engineer reports a bug in a runner, skill file, or tool:
1. Acknowledge the issue
2. Log the details (file, line, expected vs actual behavior)
3. Instruct the engineer: "This requires a lead engineer to fix. Please report it to the project lead with the details above."
4. Continue the current session without modifying the tool

The ONLY files that may be created or modified during a `newd` session are:
- `.docx` files in `Product Category/*/CTN*/[DocType]/Drafts/`
- `.docx` and `.pdf` files in `Product Category/*/CTN*/[DocType]/Final/`

### Lead Override

If the current git username is `edknowlt` AND the engineer explicitly says
"I'm working on tools" or "switch to tool development mode", then `_Tools/`
and `_Skills/` modifications are permitted. This override does NOT apply
during `newd` sessions — even the lead must exit the generation flow first.
```

### 2B. Update `cm1` Shortcut in skill_base.md

Replace the `cm1` row in the Shortcut Commands table:

**Before:**
```
| `cm1` | Commit and push all staged changes to `main` (requires confirmation) |
```

**After:**
```
| `cm1` | **DEPRECATED** — Direct push to main is no longer permitted. Use `pr` instead. Opens a pull request from the current branch to main. |
```

### 2C. Add `pr` Shortcut to skill_base.md

Add a new row to the Shortcut Commands table:

```
| `pr` | Push current branch and open a pull request to `main`. Shows a summary of changed files and asks for a PR title before creating. Requires branch protection approval before merge. |
```

**Implementation:** The `pr` shortcut should:
1. Run `git push origin <current-branch>`
2. Show `git diff --stat origin/main..HEAD`
3. Prompt for PR title
4. Run `gh pr create --base main --title "<title>" --body "QAC-generated PR from <branch>"`
5. Return the PR URL

---

## PHASE 3 — Split the Runbook (architecture change)

**Effort:** 4-8 hours, Python refactor + markdown restructuring
**Risk:** Medium — changes how draft logging works, requires careful testing

### Problem

`ICR_Automation_Runbook.md` is a single file modified by:
- `runbook_updater.py` on every `newd` (syncs draft state)
- `append_draft_log()` in `runner_core.py` after every generation
- Engineers manually (session log entries)

At 20 engineers, this file will merge-conflict on nearly every `git pull`.

### Solution — Split Into 3 Components

```
_Runbook/
├── ICR_Automation_Runbook.md        ← static reference (lead-only edits)
├── draft_log.jsonl                  ← append-only structured log (auto-generated)
├── pending/                         ← per-engineer pending DTR tracker
│   ├── edknowlt.md
│   ├── jmisal.md
│   └── nateric.md
├── runbook_updater.py               ← updated to write per-engineer files
├── runbook_updater_launcher.sh
├── com.icr.runbook_updater.plist
└── Backup/
```

### 3A. Create `draft_log.jsonl` Format

Each generation appends one JSON line:
```json
{"timestamp": "2026-06-02T14:30:00", "engineer": "edknowlt", "prod_cat": "SBC", "ctn": "CTN2026003", "doc_type": "System Description", "dtr": "DTR003", "version": "IOS XE 17.18", "file": "Draft_CTN2026003 - DTR003 - SBC - IOS XE 17.18 - Cisco ICR System Description.docx", "status": "generated"}
```

**Why JSONL:** Each engineer appends exactly one line. Git auto-merges appended lines with zero conflicts. No table formatting issues. Machine-parseable for dashboards later.

### 3B. Refactor `append_draft_log()` in `runner_core.py`

Replace the current Markdown table append logic (lines ~857-915) with:

```python
def append_draft_log(entry: dict):
    """Append a single JSON line to the draft log."""
    log_path = BASE / "_Runbook" / "draft_log.jsonl"
    entry["timestamp"] = datetime.now().isoformat()
    entry["engineer"] = get_git_username()
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

### 3C. Create Per-Engineer Pending Files

Instead of a shared "Pending DTRs" table in the runbook, each engineer gets their own file:

```markdown
# Pending DTRs — edknowlt

| Product Cat | CTN | Doc Type | Next DTR | Status |
|---|---|---|---|---|
| SBC | CTN2026003 | System Description | DTR004 | Ready |
| SBC | CTN2026003 | FA | DTR001 | Ready |
```

`runbook_updater.py` scans disk and writes ONLY the current engineer's file (based on `git config user.name` or `get_git_username()`).

### 3D. Strip Dynamic Content from Runbook

Remove from `ICR_Automation_Runbook.md`:
- Session Log table (rows after the header) → replaced by `draft_log.jsonl`
- Pending DTRs table → replaced by `pending/<engineer>.md`
- Keep: Script Inventory, Shortcut Commands, DTR Generation Prompt List, Known Issues, Key Decisions Log (all static reference content)

---

## PHASE 4 — Team-Scoped Document Isolation

**Effort:** 2-4 hours, new config file + skill_base.md update + generate.py filter
**Risk:** Low — additive filtering, does not change generation logic

### 4A. Create `teams.json`

**File:** `_Tools/teams.json`

```json
{
  "_comment": "Maps git usernames to teams and permitted product categories.",
  "_comment2": "Use ['*'] for lead engineers who can access all categories.",
  "edknowlt":  {"team": "lead",          "categories": ["*"]},
  "jmisal":    {"team": "collab",         "categories": ["SBC"]},
  "nateric":   {"team": "route-switch",   "categories": ["ESC", "SS"]}
}
```

**Update this file as engineers are onboarded.** New engineers must be added here before they can generate documents.

### 4B. Add Team Filtering to `newd` Prompt Sequence

Update `skill_base.md`'s `newd` flow (step 1 — Product Category selection):

```markdown
Before presenting Product Category options:
1. Read `_Tools/teams.json`
2. Look up the current engineer's git username
3. If the engineer is not in teams.json, STOP and display:
   "You are not registered in teams.json. Contact the project lead to be added."
4. Filter the Product Category folder list to only show categories
   the engineer is permitted to access
5. If the engineer has ["*"], show all categories
```

### 4C. Add Team Validation to `generate.py`

Add a check at the top of the dispatch flow:

```python
def validate_team_access(prod_cat: str) -> bool:
    """Check if the current engineer is permitted to generate for this product category."""
    teams_path = Path(__file__).parent / "teams.json"
    if not teams_path.exists():
        return True  # No teams.json = no restrictions (backward compatible)
    with open(teams_path) as f:
        teams = json.load(f)
    username = get_git_username()
    if username not in teams:
        print(f"ERROR: {username} is not registered in teams.json")
        return False
    allowed = teams[username].get("categories", [])
    if "*" in allowed:
        return True
    return prod_cat in allowed
```

### 4D. Pre-Commit Team Validation Hook (optional)

Create `.githooks/pre-commit`:

```bash
#!/bin/bash
# Validate that staged files are in the engineer's permitted product categories
ENGINEER=$(git config user.name)
# Parse teams.json for allowed categories
# Warn (not block) if files outside permitted categories are staged
```

---

## PHASE 5 — CI/CD & Hardening

**Effort:** Ongoing, incremental
**Risk:** None — additive only

### 5A. GitHub Actions Workflow — Lint & Validate

**File:** `.github/workflows/ci.yml`

```yaml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt
      - name: Syntax check all Python files
        run: |
          for f in _Tools/*.py _Runbook/*.py; do
            python -c "import ast; ast.parse(open('$f').read())" || exit 1
          done
      - name: Validate imports resolve
        run: |
          cd _Tools && python -c "
          import runner_core
          import generate
          print('All imports OK')
          "

  guard-tools:
    runs-on: ubuntu-latest
    if: github.event.pull_request.user.login != 'edknowlt'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Block non-lead tool changes
        run: |
          CHANGED=$(git diff --name-only origin/main...HEAD)
          TOOL_CHANGES=$(echo "$CHANGED" | grep -E '^(_Tools/|_Skills/|AGENTS\.md)' || true)
          if [ -n "$TOOL_CHANGES" ]; then
            echo "::error::Non-lead engineer modifying protected files:"
            echo "$TOOL_CHANGES"
            echo "::error::Only the project lead may modify _Tools/, _Skills/, or AGENTS.md"
            exit 1
          fi
```

### 5B. Generation Lock File (concurrent write protection)

Add to `runner_core.py`:

```python
def acquire_generation_lock(drafts_dir: Path, doc_type: str) -> Path:
    """Create a lock file to prevent concurrent generation."""
    lock = drafts_dir / f".generating_{doc_type}.lock"
    if lock.exists():
        with open(lock) as f:
            info = f.read()
        raise RuntimeError(
            f"Another generation is in progress for {doc_type}:\n{info}\n"
            f"If this is stale, delete {lock}"
        )
    lock.write_text(f"{get_git_username()} at {datetime.now().isoformat()}")
    return lock

def release_generation_lock(lock_path: Path):
    """Remove the lock file after generation completes."""
    if lock_path.exists():
        lock_path.unlink()
```

### 5C. Skill File Integrity Check (future)

At session start, hash all `_Skills/*.md` files and compare against known-good hashes stored in a `_Skills/.checksums` file on `main`. If any skill file has been modified on the engineer's branch, warn before proceeding.

---

## DEPLOYMENT CHECKLIST

```
Phase 1 — GitHub Protections
  [ ] Enable branch protection on main (require PR, require CODEOWNERS review)
  [ ] Create .github/CODEOWNERS file
  [ ] Test: open a test PR touching _Tools/ — verify edknowlt is auto-requested
  [ ] Test: attempt direct push to main — verify it is rejected

Phase 2 — AI Session Guardrails
  [ ] Update AGENTS.md with Tool Protection Rule
  [ ] Update AGENTS.md with Lead Override rule
  [ ] Deprecate cm1 shortcut in skill_base.md
  [ ] Add pr shortcut to skill_base.md
  [ ] Test: start a newd session and ask AI to modify a runner — verify it refuses

Phase 3 — Split the Runbook
  [ ] Create _Runbook/draft_log.jsonl (empty file)
  [ ] Create _Runbook/pending/ directory
  [ ] Create per-engineer pending files
  [ ] Refactor append_draft_log() in runner_core.py to write JSONL
  [ ] Refactor runbook_updater.py to write per-engineer pending files
  [ ] Strip dynamic content from ICR_Automation_Runbook.md
  [ ] Test: run newd and verify draft_log.jsonl gets appended
  [ ] Test: verify merge from two engineers has zero conflicts

Phase 4 — Team-Scoped Isolation
  [ ] Create _Tools/teams.json with current engineers
  [ ] Add validate_team_access() to generate.py
  [ ] Update skill_base.md newd flow to filter by team
  [ ] Test: engineer sees only their team's product categories in newd
  [ ] Onboard team leads: add their usernames to teams.json and CODEOWNERS

Phase 5 — CI/CD & Hardening
  [ ] Create .github/workflows/ci.yml
  [ ] Add guard-tools job blocking non-lead tool changes
  [ ] Add generation lock file mechanism
  [ ] Enable "Require status checks" in branch protection (after CI is green)
  [ ] (Future) Add skill file integrity checksums
```

---

## HOW TO USE THIS DOCUMENT

In a future OpenCode session, say:

> Read `_Runbook/SCALING_STRATEGY.md` and execute Phase [N].

Or:

> Read `_Runbook/SCALING_STRATEGY.md` and execute all phases in order.

The AI will have all the context, file paths, code snippets, and deployment steps needed to implement each phase without additional research.
