#!/usr/bin/env python3
"""
runbook_updater.py
------------------
Scans all Drafts/ folders under ICR_Automation for new .docx files
and updates the runbook markdown accordingly.

Usage:
  --once    Scan once, update runbook, and exit (recommended for manual session check)
  --report  Print a JSON project state report to stdout (no runbook changes)
  (no flag) Continuous watch mode, polls every 10 seconds

Note: If invoking manually, adjust the path to match your actual project location:
  python3 "$HOME/Documents/ICR_Automation/_Runbook/runbook_updater.py" --once
  (Replace ~/Documents/ICR_Automation/ if your clone is in a different location.)
"""

import os
import re
import subprocess
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parents[1]
RUNBOOK_PATH  = BASE_DIR / '_Runbook' / 'ICR_Automation_Runbook.md'
BACKUP_DIR    = BASE_DIR / '_Runbook' / 'Backup'
STATE_FILE    = BASE_DIR / '_Runbook' / '.runbook_state.json'
POLL_INTERVAL = 10  # seconds between checks
MAX_BACKUPS_PER_ENGINEER = 10

def get_engineer_username():
    """Read git user.name; fall back to $USER."""
    try:
        result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True, text=True, cwd=BASE_DIR
        )
        name = result.stdout.strip()
        if name:
            # Normalise to lowercase, replace spaces with underscores
            return re.sub(r'\s+', '_', name.lower())
    except Exception:
        pass
    return os.environ.get('USER', 'unknown')

# ── HELPERS ───────────────────────────────────────────────────────────────────
def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {'known_files': []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def find_all_drafts():
    """Find all .docx files in any Drafts/ subfolder."""
    return [
        str(p) for p in BASE_DIR.rglob('Drafts/*.docx')
        if not p.name.startswith('~$')
    ]

def parse_draft_filename(filepath):
    """
    Parse a draft filename and return metadata dict.
    Expected pattern: Draft_CTN[num] - DTR[num] - [ProdCat] - [Version] - Cisco ICR [DocType].docx
    """
    name = Path(filepath).stem
    result = {
        'ctn': None, 'dtr': None, 'product': None,
        'version': None, 'doc_type': None,
        'path': filepath, 'date': datetime.now().strftime('%b %Y')
    }
    ctn_match = re.search(r'(CTN\d+)', name)
    if ctn_match:
        result['ctn'] = ctn_match.group(1)
    dtr_match = re.search(r'DTR0*(\d+)', name)
    if dtr_match:
        result['dtr'] = int(dtr_match.group(1))
    prod_match = re.search(r'DTR\d+ - ([A-Z]+) -', name)
    if prod_match:
        result['product'] = prod_match.group(1)
    ver_match = re.search(r'(IOS XE [\d.]+|NX-OS [\d.]+|FXOS [\d.]+|CUCM [\d.]+)', name)
    if ver_match:
        result['version'] = ver_match.group(1)
    parts = Path(filepath).parts
    for i, part in enumerate(parts):
        if part == 'Drafts' and i > 0:
            result['doc_type'] = parts[i-1]
            break
    return result

def read_runbook():
    with open(RUNBOOK_PATH, 'r') as f:
        return f.read()

def backup_runbook():
    """Copy the current runbook to Backup/ before overwriting it.
    Filename includes engineer username so per-engineer trimming works correctly.
    """
    BACKUP_DIR.mkdir(exist_ok=True)
    username  = get_engineer_username()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    backup_path = BACKUP_DIR / f'ICR_Automation_Runbook_{username}_{timestamp}.md'
    backup_path.write_text(RUNBOOK_PATH.read_text())
    print(f'[runbook_updater] Backup saved: {backup_path.name}')

    # Trim: keep only the MAX_BACKUPS_PER_ENGINEER most recent backups for this engineer
    pattern = f'ICR_Automation_Runbook_{username}_*.md'
    engineer_backups = sorted(BACKUP_DIR.glob(pattern))
    for old in engineer_backups[:-MAX_BACKUPS_PER_ENGINEER]:
        old.unlink()
        print(f'[runbook_updater] Old backup removed: {old.name}')

def write_runbook(content):
    """Atomically overwrite the runbook with new content.

    Strategy:
    1. Backup the existing runbook (for recovery).
    2. Write content to a sibling temp file (.tmp suffix).
    3. Rename temp → runbook in a single atomic OS operation.
    This prevents partial-write corruption if the process is killed mid-write.
    """
    backup_runbook()
    tmp_path = RUNBOOK_PATH.with_suffix(".tmp")
    # Write to temp first, then atomically rename — avoids truncating the live file on failure
    tmp_path.write_text(content, encoding="utf-8")
    tmp_path.replace(RUNBOOK_PATH)

def update_version_history(content, meta):
    """Add a new row to the Platform Version History table."""
    if meta['doc_type'] != 'System Description':
        return content
    new_row = (
        f"| {meta['ctn']} | {meta['product']} | DTR{meta['dtr']:03d} "
        f"| — | — | — | — | {meta['date']} |"
    )
    marker = '## Pending / Upcoming DTRs'
    if new_row in content:
        return content
    content = content.replace(marker, f"{new_row}\n\n{marker}", 1)  # third positional arg=1: replace only first occurrence
    return content

def update_pending_dtrs(content, meta):
    """Update the Pending DTRs table — increment the next DTR for this CTN."""
    if meta['ctn'] is None or meta['dtr'] is None:
        return content
    next_dtr = meta['dtr'] + 1
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if f"| {meta['ctn']} |" in line and '| Next DTR |' not in line:
            line = re.sub(r'DTR\d+', f'DTR{next_dtr:03d}', line, count=1)
        new_lines.append(line)
    return '\n'.join(new_lines)

def append_auto_log(content, meta):
    """Append an auto-detected entry to the session log."""
    note = (
        f"| {datetime.now().strftime('%Y-%m-%d')} | AUTO-DETECT | "
        f"New draft detected: {Path(meta['path']).name} | — |"
    )
    if note in content:
        return content
    marker = '\n---\n\n## Platform Version History'
    content = content.replace(marker, f"\n{note}{marker}")
    return content

# ── REPORT ────────────────────────────────────────────────────────────────────
def report():
    """Print a JSON project state report to stdout. No runbook changes."""
    all_drafts = find_all_drafts()

    # Group drafts by CTN and doc type
    by_ctn: dict = {}
    for filepath in sorted(all_drafts):
        meta = parse_draft_filename(filepath)
        ctn = meta['ctn'] or 'unknown'
        doc_type = meta['doc_type'] or 'unknown'
        if ctn not in by_ctn:
            by_ctn[ctn] = {}
        if doc_type not in by_ctn[ctn]:
            by_ctn[ctn][doc_type] = []
        by_ctn[ctn][doc_type].append({
            'file': Path(filepath).name,
            'dtr': meta['dtr'],
            'version': meta['version'],
        })

    # Determine next DTR per CTN/doc type
    state_report = {
        'generated_at': datetime.now().isoformat(),
        'draft_count': len(all_drafts),
        'ctns': {}
    }
    for ctn, doc_types in sorted(by_ctn.items()):
        state_report['ctns'][ctn] = {}
        for doc_type, drafts in sorted(doc_types.items()):
            dtr_nums = [d['dtr'] for d in drafts if d['dtr'] is not None]
            max_dtr = max(dtr_nums) if dtr_nums else 0
            state_report['ctns'][ctn][doc_type] = {
                'drafts_on_disk': len(drafts),
                'dtrs': sorted(set(dtr_nums)),
                'next_dtr': max_dtr + 1,
                'files': [d['file'] for d in drafts],
            }

    # Also list CTNs with no drafts on disk
    prod_cat_dir = BASE_DIR / 'Product Category'
    if prod_cat_dir.exists():
        for prod_cat_dir_entry in sorted(prod_cat_dir.iterdir()):
            if not prod_cat_dir_entry.is_dir():
                continue
            for ctn_dir in sorted(prod_cat_dir_entry.iterdir()):
                if not ctn_dir.is_dir():
                    continue
                ctn = ctn_dir.name
                if ctn not in state_report['ctns']:
                    state_report['ctns'][ctn] = {}

    print(json.dumps(state_report, indent=2))


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
def run(once=False):
    mode = "one-time scan" if once else "continuous watch"
    print(f'[runbook_updater] Starting {mode} — {BASE_DIR}')
    state = load_state()
    known = set(state.get('known_files', []))

    while True:
        current = set(find_all_drafts())
        new_files = current - known

        if new_files:
            for filepath in sorted(new_files):
                print(f'[runbook_updater] New draft detected: {Path(filepath).name}')
                meta = parse_draft_filename(filepath)
                content = read_runbook()
                content = update_version_history(content, meta)
                content = update_pending_dtrs(content, meta)
                content = append_auto_log(content, meta)
                write_runbook(content)
                print(f'[runbook_updater] Runbook updated')
            known = current
            save_state({'known_files': list(known)})
        else:
            print(f'[runbook_updater] No new drafts found.')

        if once:
            print(f'[runbook_updater] Done.')
            break

        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    if '--report' in sys.argv:
        report()
    else:
        once_mode = '--once' in sys.argv
        run(once=once_mode)
