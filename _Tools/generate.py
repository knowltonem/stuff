#!/usr/bin/env python3
"""
generate.py — ICR Automation document generation dispatcher.

Prompts for Product Category, CTN, Document Type, and DTR number, then
delegates to the appropriate parameterized runner's run() entry point.

Usage:
    python3 _Tools/generate.py

Runners dispatched:
    System Description              → run_sysdesc.run()
    Functionality Attestation (FA)  → run_fa.run()
    ICR Summary Memorandum          → run_icr_memo.run()
    MUDG                            → run_mudg.run()
    Test Discrepancy Report (TDR)   → run_tdr.run()

Skeleton runners (LoC, POA&M, System Diagram) raise NotImplementedError
until example files are placed in their Examples & Templates/ folders.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from runner_core import BASE

# ---------------------------------------------------------------------------
# Runner dispatch table
# ---------------------------------------------------------------------------

# Maps folder name substring → (display label, module name, supported flag)
RUNNER_MAP = {
    "System Description":              ("System Description",             "run_sysdesc",       True),
    "Functionality Attestation":       ("Functionality Attestation (FA)", "run_fa",            True),
    "ICR Summary Memorandum":          ("ICR Summary Memorandum",         "run_icr_memo",      True),
    "Military Unique Deployment Guide":("Military Unique Deployment Guide (MUDG)", "run_mudg", True),
    "Test Discrepancy Report":         ("Test Discrepancy Report (TDR)",  "run_tdr",           True),
    "Cybersecurity Summary Report":    ("Cybersecurity Summary Report (CSR)", "run_csr",       True),
    "Letter Of Compliance":            ("Letter Of Compliance (LoC)",     "run_loc",           False),
    "Plan of Action":                  ("Plan of Action & Milestone (POA&M)", "run_poam",      False),
    "System Diagram":                  ("System Diagram",                 "run_system_diagram",False),
}


def list_product_categories() -> list:
    prod_cat_dir = BASE / "Product Category"
    return sorted(p.name for p in prod_cat_dir.iterdir() if p.is_dir())


def list_ctns(prod_cat: str) -> list:
    ctn_dir = BASE / f"Product Category/{prod_cat}"
    return sorted(p.name for p in ctn_dir.iterdir() if p.is_dir())


def list_doc_types(prod_cat: str, ctn: str) -> list:
    ctn_dir = BASE / f"Product Category/{prod_cat}/{ctn}"
    return sorted(p.name for p in ctn_dir.iterdir() if p.is_dir())


def resolve_runner(doc_type_folder: str):
    """Return (display_label, module_name, supported) for a doc type folder name."""
    for key, value in RUNNER_MAP.items():
        if key in doc_type_folder:
            return value
    return (doc_type_folder, None, False)


def main():
    print("\n=== ICR Automation — Document Generation Dispatcher ===\n")

    # 1. Product Category
    categories = list_product_categories()
    if not categories:
        print("ERROR: No product categories found under Product Category/")
        sys.exit(1)
    print("Product Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    choice = input("Select (number): ").strip()
    try:
        prod_cat = categories[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        sys.exit(1)

    # 2. CTN
    ctns = list_ctns(prod_cat)
    if not ctns:
        print(f"ERROR: No CTNs found under Product Category/{prod_cat}/")
        sys.exit(1)
    print(f"\nCTNs under {prod_cat}:")
    for i, ctn in enumerate(ctns, 1):
        print(f"  {i}. {ctn}")
    choice = input("Select (number): ").strip()
    try:
        ctn = ctns[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        sys.exit(1)

    # 3. Document Type
    doc_types = list_doc_types(prod_cat, ctn)
    if not doc_types:
        print(f"ERROR: No document type folders found under {prod_cat}/{ctn}/")
        sys.exit(1)
    print(f"\nDocument Types:")
    for i, dt in enumerate(doc_types, 1):
        label, module, supported = resolve_runner(dt)
        status = "" if supported else " [SKELETON — not yet supported]"
        print(f"  {i}. {label}{status}")
    choice = input("Select (number): ").strip()
    try:
        doc_type_folder = doc_types[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        sys.exit(1)

    label, module_name, supported = resolve_runner(doc_type_folder)
    if not supported or module_name is None:
        print(f"\n[SKELETON] {label} is not yet fully implemented.")
        print("Place example .docx files in its Examples & Templates/ folder to unblock.")
        sys.exit(1)

    # 4. DTR Number
    dtr_num = int(input("\nDTR Number (e.g. 1): ").strip())

    # 5. Import and dispatch
    import importlib
    runner = importlib.import_module(module_name)
    print(f"\nDispatching to {module_name}.run({prod_cat!r}, {ctn!r}, {dtr_num})...\n")
    runner.run(prod_cat, ctn, dtr_num)


if __name__ == "__main__":
    main()
