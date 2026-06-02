#!/usr/bin/env python3
"""
trim_backups.py
---------------
Trims _Runbook/Backup/ to keep only the N most recent backups per engineer.

Backup filename format (set by runbook_updater.py):
    ICR_Automation_Runbook_<username>_<YYYY-MM-DD_HHMMSS>.md

Usage:
    python3 _Tools/trim_backups.py                  # trim, keep 10 per engineer
    python3 _Tools/trim_backups.py --keep 5         # trim, keep 5 per engineer
    python3 _Tools/trim_backups.py --dry-run        # preview only, no deletions
    python3 _Tools/trim_backups.py --summary        # print counts per engineer, no action

The script resolves the project root from its own location — no hardcoded paths.
"""

import argparse
import re
from collections import defaultdict
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
DEFAULT_KEEP = 10
BACKUP_PATTERN = re.compile(r'^ICR_Automation_Runbook_(.+?)_(\d{4}-\d{2}-\d{2}_\d{6})\.md$')

def resolve_backup_dir():
    """Locate Backup/ relative to this script's position in _Tools/."""
    tools_dir = Path(__file__).resolve().parent
    project_root = tools_dir.parent
    return project_root / '_Runbook' / 'Backup'

def group_by_engineer(backup_dir: Path) -> dict:
    """Return {username: [sorted list of Path objects oldest→newest]}."""
    groups = defaultdict(list)
    for f in backup_dir.glob('ICR_Automation_Runbook_*.md'):
        m = BACKUP_PATTERN.match(f.name)
        if m:
            username = m.group(1)
            groups[username].append(f)
    # Sort each group oldest → newest by filename (timestamp is lexicographically sortable)
    for username in groups:
        groups[username].sort(key=lambda p: p.name)
    return dict(groups)

def trim(backup_dir: Path, keep: int, dry_run: bool):
    if not backup_dir.exists():
        print(f'[trim_backups] Backup directory not found: {backup_dir}')
        return

    groups = group_by_engineer(backup_dir)

    if not groups:
        print('[trim_backups] No backups found.')
        return

    total_deleted = 0

    for username in sorted(groups):
        files = groups[username]
        to_delete = files[:-keep] if len(files) > keep else []
        to_keep   = files[-keep:]

        print(f'\n[{username}]  {len(files)} backup(s) found — keeping {len(to_keep)}, removing {len(to_delete)}')

        for f in to_keep:
            print(f'  KEEP   {f.name}')

        for f in to_delete:
            if dry_run:
                print(f'  DELETE {f.name}  (dry-run — not deleted)')
            else:
                f.unlink()
                print(f'  DELETE {f.name}')
                total_deleted += 1

    if dry_run:
        print('\n[trim_backups] Dry-run complete — no files were deleted.')
    else:
        print(f'\n[trim_backups] Done — {total_deleted} file(s) deleted.')

def summary(backup_dir: Path):
    if not backup_dir.exists():
        print(f'[trim_backups] Backup directory not found: {backup_dir}')
        return
    groups = group_by_engineer(backup_dir)
    if not groups:
        print('[trim_backups] No backups found.')
        return
    total = sum(len(v) for v in groups.values())
    print(f'\nBackup summary — {total} file(s) across {len(groups)} engineer(s):\n')
    for username in sorted(groups):
        files = groups[username]
        newest = files[-1].name if files else '—'
        print(f'  {username:<20} {len(files):>3} backup(s)   newest: {newest}')
    print()

# ── ENTRY POINT ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='Trim _Runbook/Backup/ — keep last N backups per engineer.'
    )
    parser.add_argument('--keep',    type=int, default=DEFAULT_KEEP,
                        help=f'Number of backups to keep per engineer (default: {DEFAULT_KEEP})')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview deletions without removing any files')
    parser.add_argument('--summary', action='store_true',
                        help='Print backup counts per engineer and exit')
    args = parser.parse_args()

    backup_dir = resolve_backup_dir()
    print(f'[trim_backups] Backup directory: {backup_dir}')

    if args.summary:
        summary(backup_dir)
    else:
        trim(backup_dir, keep=args.keep, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
