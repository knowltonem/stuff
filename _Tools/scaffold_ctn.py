#!/usr/bin/env python3
"""
scaffold_ctn.py
Create the standard 9-document-type folder structure for a new CTN.

Usage:
    python3 _Tools/scaffold_ctn.py <ProductCategory> <CTN> [--dry-run]

Examples:
    python3 _Tools/scaffold_ctn.py SBC CTN2026004
    python3 _Tools/scaffold_ctn.py ESC CTN2027001 --dry-run

Each document type folder gets:
    Drafts/              ← generated drafts go here (prefixed with Draft_)
    Examples & Templates/ ← place example/template .docx files here before generating

The script places a .gitkeep in each empty subfolder so git tracks the structure.
Running it on an existing CTN is safe — it skips folders that already exist.

Flags:
    --dry-run   Preview folders that would be created without making any changes.
"""

import sys
from pathlib import Path

DOC_TYPES = [
    "Cybersecurity Summary Report (CSR)",
    "Functionality Attestation (FA)",
    "ICR Summary Memorandum (ICR Memo)",
    "Letter Of Compliance (LoC)",
    "Military Unique Deployment Guide (MUDG)",
    "Plan of Action & Milestone (POA&M)",
    "System Description",
    "System Diagram",
    "Test Discrepancy Report (TDR)",
]

SUBFOLDERS = ["Drafts", "Examples & Templates"]


def scaffold(product_category: str, ctn: str, dry_run: bool = False) -> None:
    base = Path(__file__).resolve().parents[1] / "Product Category"
    ctn_root = base / product_category / ctn

    if dry_run:
        print(f"[DRY RUN] No files will be created. Showing what would happen for: {ctn_root}\n")
    elif ctn_root.exists():
        print(f"CTN folder already exists — adding any missing subfolders: {ctn_root}")
    else:
        print(f"Creating new CTN: {ctn_root}")

    created = 0
    skipped = 0

    for doc_type in DOC_TYPES:
        for sub in SUBFOLDERS:
            folder = ctn_root / doc_type / sub
            if folder.exists():
                skipped += 1
            else:
                if dry_run:
                    print(f"  [would create] {folder.relative_to(base.parent)}")
                else:
                    folder.mkdir(parents=True, exist_ok=True)
                    gitkeep = folder / ".gitkeep"
                    gitkeep.touch()
                    print(f"  Created: {folder.relative_to(base.parent)}")
                created += 1

    if dry_run:
        print(f"\n[DRY RUN] {created} folders would be created, {skipped} already exist.")
    else:
        print(f"\nDone — {created} folders created, {skipped} already existed.")
        if created > 0:
            print(
                f"\nNext steps:\n"
                f"  1. Place example .docx files in each doc type's 'Examples & Templates/' folder\n"
                f"  2. git add 'Product Category/{product_category}/{ctn}' && git commit\n"
                f"  3. Type 'newd' to begin DTR generation for this CTN"
            )


if __name__ == "__main__":
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if len(args) != 2:
        print("Usage: python3 _Tools/scaffold_ctn.py <ProductCategory> <CTN> [--dry-run]")
        print("Example: python3 _Tools/scaffold_ctn.py SBC CTN2026004")
        sys.exit(1)

    scaffold(args[0], args[1], dry_run=dry_run)
