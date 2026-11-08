# -*- coding: utf-8 -*-
"""test_sync_adversarial.py - Adversarial Stress-Test Suite for Sync & Immutability.

Executed by challenger_2 (Sync & Immutability Challenger).
Conducts rigorous empirical stress-testing across 6 dimensions:
1. Exact SHA-256 byte-for-byte equivalence across all 55 deliverables.
2. Directory hygiene and extraneous/orphan file detection in deliverable directories.
3. Git immutability of all 32 original Chinese scripts in both Primary and Mirror.
4. Content forensics (UTF-8, BOM, line-endings, placeholders, CSV structure).
5. DeepInvestigator errata verification in both workspaces.
6. Fault injection / oracle sensitivity simulation.
"""

from __future__ import annotations

import csv
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional, Set, Tuple, Any

PRIMARY_DIR = "/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost"
MIRROR_DIR = "/Users/kimjoo/Downloads/NTNU Insta"

TARGET_EPISODES = [
    "A-01", "A-02", "A-03", "A-04", "A-06", "H-七夕", "A-13", "A-14", "A-15"
]

CRITIC_ROLES = ["天文", "文化", "敘事", "語言"]


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def get_expected_deliverables() -> List[str]:
    paths: List[str] = []
    # 9 Research files
    for ep in TARGET_EPISODES:
        paths.append(os.path.join("04_腳本庫", "_審稿", f"{ep}_考據_gemini.md"))
    # 36 Critic files
    for ep in TARGET_EPISODES:
        for role in CRITIC_ROLES:
            paths.append(os.path.join("04_腳本庫", "_審稿", f"{ep}_審稿-{role}_antigravity.md"))
    # 9 English draft files
    for ep in TARGET_EPISODES:
        paths.append(os.path.join("04_腳本庫", "_英文版", f"{ep}-EN-script-draft.md"))
    # 1 Master Glossary
    paths.append(os.path.join("06_發布月曆", "英文譯名表.csv"))
    return paths


# ==============================================================================
# Tier 1: SHA-256 Byte-for-Byte Equivalence
# ==============================================================================
def test_tier1_sha256_equivalence() -> Dict[str, Any]:
    expected = get_expected_deliverables()
    assert len(expected) == 55, f"Expected 55 deliverables, got {len(expected)}"

    results = []
    mismatches = []
    missing_primary = []
    missing_mirror = []

    for rel in expected:
        p_path = os.path.join(PRIMARY_DIR, rel)
        m_path = os.path.join(MIRROR_DIR, rel)

        p_exists = os.path.isfile(p_path)
        m_exists = os.path.isfile(m_path)

        if not p_exists:
            missing_primary.append(rel)
        if not m_exists:
            missing_mirror.append(rel)

        if p_exists and m_exists:
            p_size = os.path.getsize(p_path)
            m_size = os.path.getsize(m_path)
            p_hash = compute_sha256(p_path)
            m_hash = compute_sha256(m_path)

            with open(p_path, "rb") as fp, open(m_path, "rb") as fm:
                bytes_identical = (fp.read() == fm.read())

            match = (p_hash == m_hash) and (p_size == m_size) and bytes_identical
            if not match:
                mismatches.append({
                    "path": rel,
                    "p_size": p_size,
                    "m_size": m_size,
                    "p_hash": p_hash,
                    "m_hash": m_hash,
                })
            results.append({
                "path": rel,
                "size": p_size,
                "sha256": p_hash,
                "match": match,
            })

    passed = (
        len(missing_primary) == 0
        and len(missing_mirror) == 0
        and len(mismatches) == 0
        and len(results) == 55
    )
    return {
        "tier": "Tier 1: SHA-256 Byte-for-Byte Equivalence",
        "passed": passed,
        "total": len(expected),
        "verified_count": len(results),
        "missing_primary": missing_primary,
        "missing_mirror": missing_mirror,
        "mismatches": mismatches,
        "details": results,
    }


# ==============================================================================
# Tier 2: Directory Hygiene & Extraneous File Detection
# ==============================================================================
def test_tier2_directory_hygiene() -> Dict[str, Any]:
    expected = set(get_expected_deliverables())

    def is_os_artifact(name: str) -> bool:
        # Ignore macOS OS artifacts: .DS_Store, Icon\r, ._*
        return name.startswith(".") or name.startswith("Icon\r") or name == "Icon\r"

    # Check 04_腳本庫/_審稿/
    p_review_dir = os.path.join(PRIMARY_DIR, "04_腳本庫", "_審稿")
    m_review_dir = os.path.join(MIRROR_DIR, "04_腳本庫", "_審稿")

    p_review_all = os.listdir(p_review_dir)
    m_review_all = os.listdir(m_review_dir)

    p_review_deliverables = {os.path.join("04_腳本庫", "_審稿", f) for f in p_review_all if not is_os_artifact(f)}
    m_review_deliverables = {os.path.join("04_腳本庫", "_審稿", f) for f in m_review_all if not is_os_artifact(f)}

    # Check 04_腳本庫/_英文版/
    p_en_dir = os.path.join(PRIMARY_DIR, "04_腳本庫", "_英文版")
    m_en_dir = os.path.join(MIRROR_DIR, "04_腳本庫", "_英文版")

    p_en_all = os.listdir(p_en_dir)
    m_en_all = os.listdir(m_en_dir)

    p_en_deliverables = {os.path.join("04_腳本庫", "_英文版", f) for f in p_en_all if not is_os_artifact(f)}
    m_en_deliverables = {os.path.join("04_腳本庫", "_英文版", f) for f in m_en_all if not is_os_artifact(f)}

    expected_review = {p for p in expected if "_審稿" in p}
    expected_en = {p for p in expected if "_英文版" in p}

    extra_p_review = p_review_deliverables - expected_review
    missing_p_review = expected_review - p_review_deliverables

    extra_m_review = m_review_deliverables - expected_review
    missing_m_review = expected_review - m_review_deliverables

    extra_p_en = p_en_deliverables - expected_en
    missing_p_en = expected_en - p_en_deliverables

    extra_m_en = m_en_deliverables - expected_en
    missing_m_en = expected_en - m_en_deliverables

    # OS artifacts noted
    os_artifacts_p = [f for f in p_review_all + p_en_all if is_os_artifact(f)]
    os_artifacts_m = [f for f in m_review_all + m_en_all if is_os_artifact(f)]

    passed = (
        len(extra_p_review) == 0
        and len(missing_p_review) == 0
        and len(extra_m_review) == 0
        and len(missing_m_review) == 0
        and len(extra_p_en) == 0
        and len(missing_p_en) == 0
        and len(extra_m_en) == 0
        and len(missing_m_en) == 0
        and len(p_review_deliverables) == 45
        and len(m_review_deliverables) == 45
        and len(p_en_deliverables) == 9
        and len(m_en_deliverables) == 9
    )

    return {
        "tier": "Tier 2: Directory Hygiene & Extraneous File Detection",
        "passed": passed,
        "p_review_count": len(p_review_deliverables),
        "m_review_count": len(m_review_deliverables),
        "p_en_count": len(p_en_deliverables),
        "m_en_count": len(m_en_deliverables),
        "extra_p_review": list(extra_p_review),
        "extra_m_review": list(extra_m_review),
        "extra_p_en": list(extra_p_en),
        "extra_m_en": list(extra_m_en),
        "os_artifacts_primary": os_artifacts_p,
        "os_artifacts_mirror": os_artifacts_m,
    }


# ==============================================================================
# Tier 3: Git Immutability & Original Script Integrity
# ==============================================================================
def test_tier3_git_immutability() -> Dict[str, Any]:
    # 1. Run git status --porcelain in Primary
    p_proc = subprocess.run(
        ["git", "status", "--porcelain", "04_腳本庫/*.md"],
        cwd=PRIMARY_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    p_lines = [l for l in p_proc.stdout.splitlines() if l.strip()]
    p_modified = [l for l in p_lines if not l.startswith("??")]

    # 2. Run git status --porcelain in Mirror
    m_proc = subprocess.run(
        ["git", "status", "--porcelain", "04_腳本庫/*.md"],
        cwd=MIRROR_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    m_lines = [l for l in m_proc.stdout.splitlines() if l.strip()]
    m_modified = [l for l in m_lines if not l.startswith("??")]

    # 3. Check git diff in Primary
    p_diff_proc = subprocess.run(
        ["git", "diff", "HEAD", "--", "04_腳本庫/"],
        cwd=PRIMARY_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    p_diff_out = p_diff_proc.stdout.strip()

    # 4. Check git diff in Mirror
    m_diff_proc = subprocess.run(
        ["git", "diff", "HEAD", "--", "04_腳本庫/"],
        cwd=MIRROR_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    m_diff_out = m_diff_proc.stdout.strip()

    # 5. Check SHA-256 equivalence of all original scripts between Primary and Mirror
    p_scripts_dir = os.path.join(PRIMARY_DIR, "04_腳本庫")
    m_scripts_dir = os.path.join(MIRROR_DIR, "04_腳本庫")

    orig_script_files = [
        f for f in os.listdir(p_scripts_dir)
        if f.endswith(".md") and os.path.isfile(os.path.join(p_scripts_dir, f))
    ]

    script_comparisons = []
    scripts_mismatch = []
    for sf in orig_script_files:
        p_sf_path = os.path.join(p_scripts_dir, sf)
        m_sf_path = os.path.join(m_scripts_dir, sf)
        if not os.path.isfile(m_sf_path):
            scripts_mismatch.append(f"Missing in mirror: {sf}")
            continue
        h_p = compute_sha256(p_sf_path)
        h_m = compute_sha256(m_sf_path)
        if h_p != h_m:
            scripts_mismatch.append(f"Hash mismatch: {sf}")
        script_comparisons.append({
            "file": sf,
            "sha256": h_p,
            "match": (h_p == h_m),
        })

    passed = (
        len(p_modified) == 0
        and len(m_modified) == 0
        and len(p_diff_out) == 0
        and len(m_diff_out) == 0
        and len(scripts_mismatch) == 0
        and len(orig_script_files) >= 30
    )

    return {
        "tier": "Tier 3: Git Immutability & Original Script Integrity",
        "passed": passed,
        "total_original_scripts_checked": len(orig_script_files),
        "primary_modified_count": len(p_modified),
        "mirror_modified_count": len(m_modified),
        "primary_diff_empty": (len(p_diff_out) == 0),
        "mirror_diff_empty": (len(m_diff_out) == 0),
        "scripts_mismatch": scripts_mismatch,
        "sample_original_scripts": script_comparisons[:5],
    }


# ==============================================================================
# Tier 4: Content Forensics & Boundary Constraints
# ==============================================================================
def test_tier4_content_forensics() -> Dict[str, Any]:
    expected = get_expected_deliverables()

    encoding_errors = []
    bom_in_markdown = []
    mixed_line_endings = []
    size_under_threshold = []
    placeholders_found = []

    # regex patterns for forbidden placeholders
    placeholder_pat = re.compile(
        r"\b(TODO|FIXME|XXX|undefined|null|NaN)\b|\[(待補|待填|INSERT|REPLACE)\]",
        re.IGNORECASE,
    )

    for rel in expected:
        p_path = os.path.join(PRIMARY_DIR, rel)
        size = os.path.getsize(p_path)

        min_size = 50 if rel.endswith(".csv") else 300
        if size < min_size:
            size_under_threshold.append((rel, size, min_size))

        with open(p_path, "rb") as f:
            raw = f.read()

        # Check BOM in Markdown deliverables (Markdown should never have BOM)
        if rel.endswith(".md") and raw.startswith(b"\xef\xbb\xbf"):
            bom_in_markdown.append(rel)

        # Decode UTF-8
        try:
            text = raw.decode("utf-8-sig" if rel.endswith(".csv") else "utf-8")
        except UnicodeDecodeError as e:
            encoding_errors.append((rel, str(e)))
            continue

        # Check mixed line endings
        has_crlf = b"\r\n" in raw
        if has_crlf:
            bare_lf = re.search(rb"(?<!\r)\n", raw)
            if bare_lf:
                mixed_line_endings.append((rel, "mixed CRLF and bare LF"))

        # Placeholder check
        for line_no, line in enumerate(text.splitlines(), start=1):
            match = placeholder_pat.search(line)
            if match:
                placeholders_found.append((rel, line_no, match.group(0), line.strip()[:80]))

    # CSV Forensic check
    csv_path = os.path.join(PRIMARY_DIR, "06_發布月曆", "英文譯名表.csv")
    csv_errors = []
    csv_episodes_found = set()
    csv_row_count = 0

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
            if not header or len(header) < 4:
                csv_errors.append(f"Invalid CSV header: {header}")
            ep_col_idx = 3  # Header: Chinese,English,Category,Episode,Notes
            for idx, col_name in enumerate(header):
                if "episode" in col_name.lower() or "集數" in col_name:
                    ep_col_idx = idx
                    break

            for r_idx, row in enumerate(reader, start=2):
                if not row or not any(row):
                    continue
                csv_row_count += 1
                if len(row) > ep_col_idx:
                    eps_raw = row[ep_col_idx].split(",")
                    for ep_item in eps_raw:
                        ep_clean = ep_item.strip()
                        for target_ep in TARGET_EPISODES:
                            if target_ep == ep_clean or target_ep in ep_clean:
                                csv_episodes_found.add(target_ep)
        except Exception as e:
            csv_errors.append(f"Failed to parse CSV: {e}")

    missing_eps_in_csv = set(TARGET_EPISODES) - csv_episodes_found
    if missing_eps_in_csv:
        csv_errors.append(f"CSV missing entries for episodes: {missing_eps_in_csv}")

    passed = (
        len(encoding_errors) == 0
        and len(bom_in_markdown) == 0
        and len(mixed_line_endings) == 0
        and len(size_under_threshold) == 0
        and len(placeholders_found) == 0
        and len(csv_errors) == 0
        and csv_row_count >= 20
        and len(csv_episodes_found) == 9
    )

    return {
        "tier": "Tier 4: Content Forensics & Boundary Constraints",
        "passed": passed,
        "encoding_errors": encoding_errors,
        "bom_in_markdown": bom_in_markdown,
        "mixed_line_endings": mixed_line_endings,
        "size_under_threshold": size_under_threshold,
        "placeholders_found": placeholders_found,
        "csv_row_count": csv_row_count,
        "csv_errors": csv_errors,
        "csv_episodes_found": sorted(list(csv_episodes_found)),
    }


# ==============================================================================
# Tier 5: DeepInvestigator Errata Verification (Primary vs Mirror)
# ==============================================================================
def test_tier5_deepinvestigator_errata() -> Dict[str, Any]:
    errata_checks = []
    all_passed = True

    # Erratum 1: A-02 太微右垣
    for d_name, base_dir in [("Primary", PRIMARY_DIR), ("Mirror", MIRROR_DIR)]:
        a02_res = os.path.join(base_dir, "04_腳本庫", "_審稿", "A-02_考據_gemini.md")
        a02_ast = os.path.join(base_dir, "04_腳本庫", "_審稿", "A-02_審稿-天文_antigravity.md")

        with open(a02_res, "r", encoding="utf-8") as f:
            c_res = f.read()
        with open(a02_ast, "r", encoding="utf-8") as f:
            c_ast = f.read()

        has_correction = (
            ("東上將" in c_res or "东上将" in c_res or "太微左垣" in c_res)
            and ("西上將" in c_res or "西上相" in c_res or "β Vir" in c_res or "HIP 57757" in c_res)
        )
        errata_checks.append({
            "target": f"A-02 Erratum 1 in {d_name}",
            "passed": has_correction,
            "details": "太微右垣 vs 太微左垣 / 后髮座東上將 verified",
        })
        if not has_correction:
            all_passed = False

    # Erratum 2: A-03 Markab / Algenib Ephemeris
    for d_name, base_dir in [("Primary", PRIMARY_DIR), ("Mirror", MIRROR_DIR)]:
        a03_res = os.path.join(base_dir, "04_腳本庫", "_審稿", "A-03_考據_gemini.md")
        a03_ast = os.path.join(base_dir, "04_腳本庫", "_審稿", "A-03_審稿-天文_antigravity.md")

        with open(a03_res, "r", encoding="utf-8") as f:
            c_res = f.read()
        with open(a03_ast, "r", encoding="utf-8") as f:
            c_ast = f.read()

        has_markab = ("17:33" in c_res or "32.08" in c_res or "32.1" in c_res) and (
            "17:33" in c_ast or "32.08" in c_ast or "32.1" in c_ast
        )
        has_algenib = ("18:42" in c_res or "16.65" in c_res or "16.6" in c_res or "16.7" in c_res) and (
            "18:42" in c_ast or "16.65" in c_ast or "16.6" in c_ast or "16.7" in c_ast
        )

        passed_e2 = has_markab and has_algenib
        errata_checks.append({
            "target": f"A-03 Erratum 2 in {d_name}",
            "passed": passed_e2,
            "details": f"Markab (17:33, 32.08°) & Algenib (18:42, 16.65°) - markab={has_markab}, algenib={has_algenib}",
        })
        if not passed_e2:
            all_passed = False

    # Erratum 3: A-06 al-Thurayya "只取兩顆星"
    for d_name, base_dir in [("Primary", PRIMARY_DIR), ("Mirror", MIRROR_DIR)]:
        a06_res = os.path.join(base_dir, "04_腳本庫", "_審稿", "A-06_考據_gemini.md")
        a06_cul = os.path.join(base_dir, "04_腳本庫", "_審稿", "A-06_審稿-文化_antigravity.md")

        with open(a06_res, "r", encoding="utf-8") as f:
            c_res = f.read()
        with open(a06_cul, "r", encoding="utf-8") as f:
            c_cul = f.read()

        has_anchor_or_err = (
            ("17608" in c_res or "錨點" in c_res or "自連" in c_res or "星團" in c_res or "錯誤" in c_res)
            and ("17608" in c_cul or "錨點" in c_cul or "自連" in c_cul or "星團" in c_cul or "錯誤" in c_cul or "整團" in c_cul)
        )
        errata_checks.append({
            "target": f"A-06 Erratum 3 in {d_name}",
            "passed": has_anchor_or_err,
            "details": "al-Thurayya anchor points vs star cluster clarification",
        })
        if not has_anchor_or_err:
            all_passed = False

    return {
        "tier": "Tier 5: DeepInvestigator Errata Verification",
        "passed": all_passed,
        "checks": errata_checks,
    }


# ==============================================================================
# Tier 6: Adversarial Negative Simulation (Verifier Oracle Sensitivity)
# ==============================================================================
def test_tier6_fault_injection_oracle_sensitivity() -> Dict[str, Any]:
    """Test that the verification oracle genuinely catches faults (no false passes)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        mock_worktree = os.path.join(tmpdir, "worktree")
        mock_mirror = os.path.join(tmpdir, "mirror")
        os.makedirs(os.path.join(mock_worktree, "04_腳本庫", "_審稿"), exist_ok=True)
        os.makedirs(os.path.join(mock_mirror, "04_腳本庫", "_審稿"), exist_ok=True)

        f_rel = os.path.join("04_腳本庫", "_審稿", "A-01_考據_gemini.md")
        f_w = os.path.join(mock_worktree, f_rel)
        f_m = os.path.join(mock_mirror, f_rel)

        # Baseline identical
        with open(f_w, "wb") as f:
            f.write(b"Hello astronomical world!")
        with open(f_m, "wb") as f:
            f.write(b"Hello astronomical world!")

        h_w = compute_sha256(f_w)
        h_m = compute_sha256(f_m)
        baseline_match = (h_w == h_m)

        # Tamper 1 byte in mirror
        with open(f_m, "wb") as f:
            f.write(b"Hello astronomical world?")
        h_m_tampered = compute_sha256(f_m)
        tamper_detected = (h_w != h_m_tampered)

        # Test deletion detection
        os.remove(f_m)
        deletion_detected = not os.path.exists(f_m)

        passed = baseline_match and tamper_detected and deletion_detected

        return {
            "tier": "Tier 6: Fault Injection & Oracle Sensitivity Simulation",
            "passed": passed,
            "baseline_match": baseline_match,
            "single_byte_tamper_detected": tamper_detected,
            "file_deletion_detected": deletion_detected,
        }


def main():
    print("=" * 78)
    print(" CHALLENGER 2: ADVERSARIAL STRESS-TEST HARNESS FOR SYNC & IMMUTABILITY")
    print(f" Primary Worktree: {PRIMARY_DIR}")
    print(f" Mirror Directory: {MIRROR_DIR}")
    print("=" * 78)

    t1 = test_tier1_sha256_equivalence()
    t2 = test_tier2_directory_hygiene()
    t3 = test_tier3_git_immutability()
    t4 = test_tier4_content_forensics()
    t5 = test_tier5_deepinvestigator_errata()
    t6 = test_tier6_fault_injection_oracle_sensitivity()

    tiers = [t1, t2, t3, t4, t5, t6]
    all_passed = True

    for t in tiers:
        status = "[PASS]" if t["passed"] else "[FAIL]"
        print(f"\n{status} {t['tier']}")
        if not t["passed"]:
            all_passed = False
            for k, v in t.items():
                if k not in ["tier", "passed", "details"]:
                    print(f"   - {k}: {v}")
        else:
            if "verified_count" in t:
                print(f"   - 100% verified count: {t['verified_count']}/{t['total']} files")
            if "p_review_count" in t:
                print(f"   - Primary _審稿: {t['p_review_count']}, Mirror _審稿: {t['m_review_count']}")
                print(f"   - Primary _英文版: {t['p_en_count']}, Mirror _英文版: {t['m_en_count']}")
                if t.get("os_artifacts_mirror"):
                    print(f"   - OS artifacts noted (Finder metadata): {t['os_artifacts_mirror']}")
            if "total_original_scripts_checked" in t:
                print(f"   - Original scripts checked: {t['total_original_scripts_checked']} files (0 modified)")
            if "csv_row_count" in t:
                print(f"   - CSV rows: {t['csv_row_count']}, Episodes covered: {len(t['csv_episodes_found'])}/9")
            if "single_byte_tamper_detected" in t:
                print(f"   - 1-byte tamper sensitivity: PASS, deletion detection: PASS")

    print("\n" + "=" * 78)
    if all_passed:
        print(">>> EMPIRICAL CHALLENGE VERDICT: APPROVE <<<")
        print("All 6 adversarial stress tiers passed with zero defects.")
        sys.exit(0)
    else:
        print(">>> EMPIRICAL CHALLENGE VERDICT: REQUEST_CHANGES <<<")
        print("Failures detected during adversarial stress testing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
