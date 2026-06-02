#!/usr/bin/env python3
"""
run_loc.py — Parameterized Letter Of Compliance (LoC) runner.
# STATUS: SKELETON — generation logic not yet implemented.
#
# UNBLOCKED BY: Placing example .docx files in:
#   Product Category/<ProdCat>/<CTN>/Letter Of Compliance (LoC)/Examples & Templates/
#
# TO COMPLETE THIS RUNNER:
#   1. Examine the example and INITIAL .docx files to document paragraph/table structure
#   2. Update skill_loc.md with confirmed rules
#   3. Implement generate_dtr001(cfg) and generate_dtr_incremental(cfg)
#   4. Add DTR001 seed profile for each known CTN to LOC_PROFILES
#   5. Change STATUS to COMPLETE
#
# Replaces any future gen_dtr###_loc_*.py one-off scripts.
#
# Usage (direct):
#     python3 _Tools/run_loc.py
#
# Or invoked automatically by the newd prompt sequence after doc type selection.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from runner_core import (
    run_validate, append_draft_log, BASE, get_git_username,
    loc_dir, loc_draft_path, loc_initial_path, loc_example_path,
)

# NOTE: `from docx import Document` is intentionally omitted — generation logic is not yet
# implemented. Add it back when generate_dtr001() and generate_dtr_incremental() are built.


# ---------------------------------------------------------------------------
# Generation — SKELETON (not yet implemented)
# ---------------------------------------------------------------------------

def generate_dtr001(cfg: dict):
    """Generate LoC DTR001 from INITIAL source document.

    NOT YET IMPLEMENTED — place example .docx files and document the
    paragraph/table structure before implementing.
    """
    raise NotImplementedError(
        "run_loc.py generate_dtr001() is not yet implemented.\n"
        "Place example .docx files in the LoC Examples & Templates folder first.\n"
        "See the Runner Architecture Standard in the runbook for implementation guidance."
    )


def generate_dtr_incremental(cfg: dict):
    """Generate LoC DTR002+ from the previous draft.

    NOT YET IMPLEMENTED — implement generate_dtr001() first.
    """
    raise NotImplementedError(
        "run_loc.py generate_dtr_incremental() is not yet implemented.\n"
        "Implement generate_dtr001() first."
    )


# ---------------------------------------------------------------------------
# Seed profiles — add DTR001 profile per CTN when onboarding
# ---------------------------------------------------------------------------

# Structure mirrors other runners:
# { dtr_num (int): { cfg fields } }
# DTR002+ are never pre-baked — fully prompted at runtime.
LOC_PROFILES: dict = {
    # "SBC/CTN2026003": { 1: { ... } },  # add when example docs are placed
}


def _get_profiles(prod_cat: str, ctn: str) -> dict:
    return LOC_PROFILES.get(f"{prod_cat}/{ctn}", {})


# ---------------------------------------------------------------------------
# run() — callable entry point for newd prompt sequence dispatch
# ---------------------------------------------------------------------------

def run(prod_cat: str, ctn: str, dtr_num: int) -> None:
    """Callable entry point — invoked by the newd prompt sequence or directly via main()."""
    print("\n=== Letter Of Compliance (LoC) — Parameterized Runner ===\n")
    print("STATUS: SKELETON — generation logic not yet implemented.")
    print("Place example .docx files in the LoC Examples & Templates folder to unblock.\n")

    profiles = _get_profiles(prod_cat, ctn)

    if dtr_num in profiles:
        cfg = dict(profiles[dtr_num])
        print(f"Loaded profile for {prod_cat}/{ctn} DTR{dtr_num:03d}:")
        print(f"  Version: {cfg.get('old_ver', '?')} → {cfg.get('new_ver', '?')}")
        confirm = input("\nProceed with these settings? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return
    else:
        print(f"No profile found for {prod_cat}/{ctn} DTR{dtr_num:03d}. Manual input required.")
        cfg = {
            "dtr_num": dtr_num,
            "new_ver": input("New IOS XE version (e.g. IOS XE 26.2): ").strip(),
            "old_ver": input("Old IOS XE version (e.g. IOS XE 17.18): ").strip(),
        }

    cfg["prod_cat"] = prod_cat
    cfg["ctn"] = ctn
    cfg["out_path"] = loc_draft_path(prod_cat, ctn, dtr_num, cfg["new_ver"])

    try:
        if dtr_num == 1:
            generate_dtr001(cfg)
        else:
            cfg["source_path"] = loc_draft_path(prod_cat, ctn, dtr_num - 1, cfg["old_ver"])
            generate_dtr_incremental(cfg)
    except NotImplementedError as e:
        print(f"\n[SKELETON] {e}")
        return  # Do not validate or log — no file was written

    print("\nRunning validate_doc.py...")
    run_validate(cfg["out_path"])

    engineer = input("\nEngineer username (for Draft Log): ").strip() or get_git_username() or "unknown"
    append_draft_log(
        engineer=engineer,
        action="Generated",
        ctn=ctn,
        doc_type="LoC",
        dtr=f"DTR{dtr_num:03d}",
        version=cfg["new_ver"],
        reason="Via run_loc.py parameterized runner",
    )

    print("\nDone.")


# ---------------------------------------------------------------------------
# main() — thin wrapper
# ---------------------------------------------------------------------------

def main():
    prod_cat = input("Product Category (e.g. SBC): ").strip()
    ctn = input("CTN (e.g. CTN2026003): ").strip()
    dtr_num = int(input("DTR Number (e.g. 1): ").strip())
    run(prod_cat, ctn, dtr_num)


if __name__ == "__main__":
    main()
