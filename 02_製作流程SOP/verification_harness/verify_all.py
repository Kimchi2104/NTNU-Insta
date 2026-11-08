# -*- coding: utf-8 -*-
"""verify_all.py - Master Test Runner for NTNU Astronomy Club Verification Suite.

Executes all verification suites:
1. Astronomical Ephemeris Verification (Skyfield 1.54, de421.bsp, Taipei 25.03°N, 121.56°E)
2. Markdown Schemas & Quantitative Constraints (4 mandatory sections, 3-line summaries,
   🔴/🟡/⚪, 180s cap, 2.6 words/sec, 6-word cards, "One sky." formula, 60-char titles)
3. Dual-Workspace Synchronization (SHA-256 equivalence across 55 deliverables)
4. Git Immutability Verification (Zero modifications to original scripts in 04_腳本庫/*.md)

Exits with code 0 if 100% of checks pass, non-zero (1) if any failure occurs.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, Optional, Any

# Ensure local imports work whether run from harness dir or repo root
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from verify_ephemeris import EphemerisVerifier, TARGET_STARS
from verify_schemas import validate_all_schemas, validate_research_file, validate_critic_file, validate_english_draft_file, validate_glossary_csv
from verify_sync import verify_dual_workspace_sync, verify_git_immutability, DEFAULT_DOWNLOADS_DIR


# ==============================================================================
# Colorized Terminal Formatting
# ==============================================================================

class TerminalColors:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled and sys.stdout.isatty()

    def _c(self, code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if self.enabled else text

    def red(self, text: str) -> str:
        return self._c("1;31", text)

    def green(self, text: str) -> str:
        return self._c("1;32", text)

    def yellow(self, text: str) -> str:
        return self._c("1;33", text)

    def cyan(self, text: str) -> str:
        return self._c("1;36", text)

    def bold(self, text: str) -> str:
        return self._c("1", text)

    def dim(self, text: str) -> str:
        return self._c("2", text)


def run_master_verification(
    worktree_dir: str,
    downloads_dir: str,
    verbose: bool = False,
    colors: Optional[TerminalColors] = None,
) -> bool:
    """Execute all verification stages and print colorized report. Returns True if all pass."""
    c = colors or TerminalColors(True)

    print(c.cyan("=" * 76))
    print(c.bold(" NTNU Astronomy Club — E2E Master Verification Runner (SOP v4.6)"))
    print(f" Target Worktree: {worktree_dir}")
    print(f" Downloads Mirror: {downloads_dir}")
    print(c.cyan("=" * 76))

    all_suites_passed = True
    suite_results: Dict[str, bool] = {}

    # --------------------------------------------------------------------------
    # Suite 1: Astronomical Ephemeris Verification (Skyfield 1.54)
    # --------------------------------------------------------------------------
    print("\n" + c.bold("[Suite 1/4] Astronomical Ephemeris Verification (Taipei 25.03°N, 121.56°E, UTC+8)"))
    print(c.dim("-" * 76))

    ephe_passed = True
    try:
        verifier = EphemerisVerifier()
        checks = verifier.verify_episode_baselines()
        for chk in checks:
            if chk["passed"]:
                status_str = c.green("PASS")
            else:
                status_str = c.red("FAIL")
                ephe_passed = False
            print(f"  [{status_str}] [{chk['episode']}] {chk['name']}")
            if verbose or not chk["passed"]:
                print(f"         {c.dim(chk['details'])}")
    except Exception as e:
        ephe_passed = False
        print(f"  [{c.red('ERROR')}] Failed to run ephemeris calculations: {e}")

    suite_results["Ephemeris (Skyfield)"] = ephe_passed
    if not ephe_passed:
        all_suites_passed = False

    # --------------------------------------------------------------------------
    # Suite 2: Original Script Immutability Verification (Git Status)
    # --------------------------------------------------------------------------
    print("\n" + c.bold("[Suite 2/4] Original Scripts Immutability (04_腳本庫/*.md)"))
    print(c.dim("-" * 76))

    immu_res = verify_git_immutability(worktree_dir)
    if immu_res["passed"]:
        print(f"  [{c.green('PASS')}] Zero modifications detected in existing original scripts.")
        suite_results["Script Immutability"] = True
    else:
        print(f"  [{c.red('FAIL')}] Original scripts were modified in git:")
        for m in immu_res["modified_original_scripts"]:
            print(f"         - {m}")
        suite_results["Script Immutability"] = False
        all_suites_passed = False

    # --------------------------------------------------------------------------
    # Suite 3: Markdown Schemas & Quantitative Constraints (55 Deliverables)
    # --------------------------------------------------------------------------
    print("\n" + c.bold("[Suite 3/4] Markdown Schemas & Quantitative Constraints Validator"))
    print(c.dim("-" * 76))

    schema_summary = validate_all_schemas(worktree_dir)

    categories = [
        ("Research Reports (R1: 4 sections, 6 cols, 4 tiers)", schema_summary["research"]),
        ("Critic Reviews (R2: 3-line summary, 🔴/🟡/⚪, Taipei ephe)", schema_summary["critic"]),
        ("English Drafts (R3: <=180s, <=2.6 w/s, <=6w cards, One sky)", schema_summary["english"]),
        ("Master Glossary (CSV, Chinese/English, 9 episodes)", schema_summary["glossary"]),
    ]

    schema_suite_passed = True
    for cat_name, cat_data in categories:
        passed_str = c.green(str(cat_data["passed"])) if cat_data["passed"] > 0 else "0"
        failed_str = c.red(str(cat_data["failed"])) if cat_data["failed"] > 0 else "0"
        missing_str = c.yellow(str(cat_data["missing"])) if cat_data["missing"] > 0 else "0"

        if cat_data["passed"] == cat_data["total"]:
            cat_badge = c.green("PASS")
        elif cat_data["failed"] > 0:
            cat_badge = c.red("FAIL")
            schema_suite_passed = False
        else:
            cat_badge = c.yellow("PENDING")
            schema_suite_passed = False

        print(f"  [{cat_badge}] {cat_name}:")
        print(f"         Total: {cat_data['total']} | Passed: {passed_str} | Failed: {failed_str} | Missing: {missing_str}")

        if verbose:
            for r in cat_data["results"]:
                if r.errors:
                    rel_name = os.path.basename(r.file_path)
                    for err in r.errors:
                        print(f"           {c.red('x')} [{rel_name}] {err}")

    suite_results["Schema & Constraints"] = schema_suite_passed
    if not schema_suite_passed:
        all_suites_passed = False

    # --------------------------------------------------------------------------
    # Suite 4: Dual-Workspace Synchronization (SHA-256 Equivalence)
    # --------------------------------------------------------------------------
    print("\n" + c.bold("[Suite 4/4] Dual-Workspace Synchronization (Mirror to Downloads)"))
    print(c.dim("-" * 76))

    sync_res = verify_dual_workspace_sync(worktree_dir, downloads_dir)
    if sync_res["passed"]:
        print(f"  [{c.green('PASS')}] All {sync_res['total_expected']} deliverables mirror identically with matching SHA-256.")
        suite_results["Dual-Workspace Sync"] = True
    else:
        suite_results["Dual-Workspace Sync"] = False
        all_suites_passed = False
        if sync_res["missing_in_worktree"]:
            cnt = len(sync_res["missing_in_worktree"])
            print(f"  [{c.yellow('PENDING')}] {cnt}/{sync_res['total_expected']} deliverables missing in worktree.")
        if sync_res["missing_in_downloads"]:
            cnt = len(sync_res["missing_in_downloads"])
            print(f"  [{c.yellow('PENDING')}] {cnt}/{sync_res['total_expected']} deliverables missing in downloads mirror.")
        if sync_res["hash_mismatches"]:
            print(f"  [{c.red('FAIL')}] SHA-256 hash mismatches detected:")
            for mm in sync_res["hash_mismatches"]:
                print(f"         - {mm['file']}")

    # --------------------------------------------------------------------------
    # Final Summary Matrix
    # --------------------------------------------------------------------------
    print("\n" + c.cyan("=" * 76))
    print(c.bold(" E2E VERIFICATION SUITE EXECUTION SUMMARY"))
    print(c.cyan("=" * 76))

    for name, st in suite_results.items():
        st_text = c.green("PASS") if st else c.red("FAIL / PENDING")
        print(f"  - {name:<35}: {st_text}")

    print(c.dim("-" * 76))
    if all_suites_passed:
        print(c.green("  >>> OVERALL RESULT: ALL 4 VERIFICATION SUITES PASSED (EXIT CODE 0) <<<"))
    else:
        print(c.yellow("  >>> OVERALL RESULT: VERIFICATION INCOMPLETE / FAILED (EXIT CODE 1) <<<"))
        print(c.dim("      (Note: Missing deliverables are expected during intermediate development milestones)"))
    print(c.cyan("=" * 76))

    return all_suites_passed


def main():
    parser = argparse.ArgumentParser(description="NTNU Video Series Master E2E Verification Runner")
    parser.add_argument("--worktree", type=str, default=".", help="Current git worktree directory")
    parser.add_argument("--downloads", type=str, default=DEFAULT_DOWNLOADS_DIR, help="Target downloads directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose reporting of file-level details")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI terminal colors")
    parser.add_argument("--self-test", action="store_true", help="Run harness unit self-tests against synthetic fixtures")
    args = parser.parse_args()

    if args.self_test:
        from test_harness_self_check import run_self_tests
        success = run_self_tests()
        sys.exit(0 if success else 1)

    worktree = os.path.abspath(args.worktree)
    downloads = os.path.abspath(args.downloads)
    colors = TerminalColors(enabled=not args.no_color)

    passed = run_master_verification(
        worktree_dir=worktree,
        downloads_dir=downloads,
        verbose=args.verbose,
        colors=colors,
    )

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
