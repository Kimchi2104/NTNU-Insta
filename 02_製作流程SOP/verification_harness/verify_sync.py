# -*- coding: utf-8 -*-
"""verify_sync.py - Dual-Worktree Mirroring and Git Immutability Verifier.

Verifies:
1. All 55 deliverable files exist identically in both the active worktree
   and /Users/kimjoo/Downloads/NTNU Insta (verified via SHA-256).
2. Zero modifications to original scripts in 04_腳本庫/*.md via git status --porcelain.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from typing import Dict, List, Optional, Tuple, Any

TARGET_EPISODES = [
    "A-01", "A-02", "A-03", "A-04", "A-06", "H-七夕", "A-13", "A-14", "A-15"
]

CRITIC_ROLES = ["天文", "文化", "敘事", "語言"]

DEFAULT_DOWNLOADS_DIR = "/Users/kimjoo/Downloads/NTNU Insta"


def get_expected_deliverable_relative_paths() -> List[str]:
    """Return the list of all 55 expected relative file paths."""
    paths: List[str] = []

    # 1. 9 Research files (04_腳本庫/_審稿/{編號}_考據_gemini.md)
    for ep in TARGET_EPISODES:
        paths.append(os.path.join("04_腳本庫", "_審稿", f"{ep}_考據_gemini.md"))

    # 2. 36 Critic files (04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md)
    for ep in TARGET_EPISODES:
        for role in CRITIC_ROLES:
            paths.append(os.path.join("04_腳本庫", "_審稿", f"{ep}_審稿-{role}_antigravity.md"))

    # 3. 9 English draft files (04_腳本庫/_英文版/{編號}-EN-script-draft.md)
    for ep in TARGET_EPISODES:
        paths.append(os.path.join("04_腳本庫", "_英文版", f"{ep}-EN-script-draft.md"))

    # 4. 1 Master Glossary file (06_發布月曆/英文譯名表.csv)
    paths.append(os.path.join("06_發布月曆", "英文譯名表.csv"))

    return paths


def compute_sha256(filepath: str) -> str:
    """Compute hex SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_git_immutability(repo_dir: str) -> Dict[str, Any]:
    """Check git status --porcelain 04_腳本庫/*.md to ensure original scripts are untouched.
    Note: New files inside 04_腳本庫/_審稿/ and 04_腳本庫/_英文版/ are deliverables,
    not modifications to original scripts.
    """
    cmd = ["git", "-C", repo_dir, "status", "--porcelain", "04_腳本庫/"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = proc.stdout.strip()
    except Exception as e:
        return {
            "passed": False,
            "error": f"Failed to execute git status: {e}",
            "modified_original_scripts": [],
        }

    lines = output.splitlines() if output else []
    modified_original_scripts: List[str] = []

    for line in lines:
        if not line.strip():
            continue
        status = line[:2]
        path = line[3:].strip()

        # Deliverables in subdirectories are allowed (and expected) untracked or added
        if path.startswith("04_腳本庫/_審稿/") or path.startswith("04_腳本庫/_英文版/"):
            continue

        # If a tracked file directly under 04_腳本庫/ is modified (M), deleted (D), or renamed (R)
        if any(c in status for c in ["M", "D", "R"]):
            modified_original_scripts.append(f"{status} {path}")

    passed = len(modified_original_scripts) == 0
    return {
        "passed": passed,
        "raw_git_output": output,
        "modified_original_scripts": modified_original_scripts,
    }


def verify_dual_workspace_sync(
    worktree_dir: str, downloads_dir: str
) -> Dict[str, Any]:
    """Verify all 55 deliverable files exist identically in worktree and downloads folder."""
    expected_files = get_expected_deliverable_relative_paths()

    missing_in_worktree: List[str] = []
    missing_in_downloads: List[str] = []
    hash_mismatches: List[Dict[str, str]] = []
    identical_files: List[str] = []

    for rel_path in expected_files:
        w_path = os.path.join(worktree_dir, rel_path)
        d_path = os.path.join(downloads_dir, rel_path)

        w_exists = os.path.exists(w_path)
        d_exists = os.path.exists(d_path)

        if not w_exists:
            missing_in_worktree.append(rel_path)
        if not d_exists:
            missing_in_downloads.append(rel_path)

        if w_exists and d_exists:
            h_w = compute_sha256(w_path)
            h_d = compute_sha256(d_path)
            if h_w == h_d:
                identical_files.append(rel_path)
            else:
                hash_mismatches.append({
                    "file": rel_path,
                    "sha256_worktree": h_w,
                    "sha256_downloads": h_d,
                })

    passed = (
        len(missing_in_worktree) == 0
        and len(missing_in_downloads) == 0
        and len(hash_mismatches) == 0
        and len(identical_files) == len(expected_files)
    )

    return {
        "passed": passed,
        "total_expected": len(expected_files),
        "identical_count": len(identical_files),
        "missing_in_worktree": missing_in_worktree,
        "missing_in_downloads": missing_in_downloads,
        "hash_mismatches": hash_mismatches,
    }


def main():
    parser = argparse.ArgumentParser(description="Dual-Workspace Sync & Git Immutability Verifier")
    parser.add_argument("--worktree", type=str, default=".", help="Current git worktree directory")
    parser.add_argument("--downloads", type=str, default=DEFAULT_DOWNLOADS_DIR, help="Target downloads directory")
    parser.add_argument("--check-immutability-only", action="store_true", help="Only check original scripts immutability")
    parser.add_argument("--check-sync-only", action="store_true", help="Only check dual-workspace sync")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    worktree = os.path.abspath(args.worktree)
    downloads = os.path.abspath(args.downloads)

    print("=" * 70)
    print("NTNU Astronomy Club — Sync & Script Immutability Verification")
    print(f"Active Worktree: {worktree}")
    print(f"Downloads Mirror: {downloads}")
    print("=" * 70)

    overall_passed = True

    # 1. Immutability Check
    if not args.check_sync_only:
        immu = verify_git_immutability(worktree)
        print("\n1. Original Script Immutability Check (git status 04_腳本庫/*.md):")
        if immu["passed"]:
            print("   [PASS] Zero modifications detected in original scripts.")
        else:
            print("   [FAIL] Original scripts modified:")
            for m in immu["modified_original_scripts"]:
                print(f"      - {m}")
            overall_passed = False

    # 2. Sync Check
    if not args.check_immutability_only:
        sync = verify_dual_workspace_sync(worktree, downloads)
        print("\n2. Dual-Workspace Synchronization Check (55 Deliverables SHA-256):")
        print(f"   Total Expected Files: {sync['total_expected']}")
        print(f"   Identical & Verified: {sync['identical_count']}")
        print(f"   Missing in Worktree: {len(sync['missing_in_worktree'])}")
        print(f"   Missing in Downloads: {len(sync['missing_in_downloads'])}")
        print(f"   SHA-256 Mismatches: {len(sync['hash_mismatches'])}")

        if sync["passed"]:
            print("   [PASS] 100% of 55 files match identically between worktree and downloads.")
        else:
            if sync["missing_in_worktree"] and not args.verbose:
                print("   [INFO] Files pending generation in worktree (first 3 shown):")
                for f in sync["missing_in_worktree"][:3]:
                    print(f"      - {f}")
            if sync["hash_mismatches"]:
                print("   [FAIL] Checksum mismatches found:")
                for mm in sync["hash_mismatches"]:
                    print(f"      - {mm['file']}")
            overall_passed = False

    print("\n" + "=" * 70)
    if overall_passed:
        print("[SUCCESS] All synchronization and immutability checks passed.")
        sys.exit(0)
    else:
        print("[INFO] Synchronization checks incomplete (deliverables pending completion).")
        sys.exit(1)


if __name__ == "__main__":
    main()
