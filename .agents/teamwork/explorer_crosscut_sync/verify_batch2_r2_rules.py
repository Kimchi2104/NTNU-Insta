#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_batch2_r2_rules_patched.py - Enhanced Rules Verifier for Batch 2 R2.

Patched & Enhanced Check 5:
- Covers ALL external authors across A-16, A-17, A-18, A-19 (including Chassinat,
  Belmonte, Umar ibn Abi Rabi'a, Wissler 1911/1912, etc.).
- Correctly parses Roman numeral volumes (e.g. 'Vol. II, p. 31', 'Tome II', 'Band I').
- Detects lingering guessed pages without '未核頁碼' (Error Mode A).
- Detects contradictory patterns where page numbers appear with/before '未核頁碼' (Error Mode B).
- Gracefully handles valid peer-reviewed journal article page ranges (JHA, BIFAO, JEA, MIOB, A&A).
- Accurately respects verified local sources (Childrey 2004, Wissler & Duvall 1908, McClintock 1910).
- Splits citations by semicolon to prevent inter-citation bleeding within table cells.
"""

import os
import re
import sys
import hashlib
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DOWNLOADS_ROOT = "/Users/kimjoo/Downloads/NTNU Insta"

EPISODES = ["A-16", "A-17", "A-18", "A-19"]
ROLES = ["天文", "文化", "敘事", "語言"]

def get_sha256(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def check_a16_v0():
    findings = []
    w_path = os.path.join(REPO_ROOT, "04_腳本庫", "A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md")
    d_path = os.path.join(DOWNLOADS_ROOT, "04_腳本庫", "A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md")
    if not os.path.exists(w_path):
        findings.append("A-16 v0 does NOT exist in worktree 04_腳本庫/")
    elif not os.path.exists(d_path):
        findings.append("A-16 v0 does NOT exist in Downloads 04_腳本庫/")
    else:
        w_h = get_sha256(w_path)
        d_h = get_sha256(d_path)
        if w_h != d_h:
            findings.append(f"A-16 v0 hash mismatch: worktree={w_h} vs downloads={d_h}")
    return findings

def check_git_immutability():
    findings = []
    cmd = ["git", "-C", REPO_ROOT, "status", "--porcelain", "04_腳本庫/"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        for line in proc.stdout.splitlines():
            if not line.strip():
                continue
            status = line[:2]
            path = line[3:].strip()
            if path.startswith("04_腳本庫/_審稿/") or path.startswith("04_腳本庫/_英文版/"):
                continue
            if any(c in status for c in ["M", "D", "R"]):
                findings.append(f"Original script modified: {status} {path}")
    except Exception as e:
        findings.append(f"Failed to check git status: {e}")
    return findings

def check_research_section2():
    findings = []
    for ep in EPISODES:
        path = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", f"{ep}_考據_gemini.md")
        if not os.path.exists(path):
            findings.append(f"Missing file: {path}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        m = re.search(r"##\s*二、清單以外發現的問題(.*?)(?=##\s*三、|\Z)", c, re.DOTALL)
        if not m:
            findings.append(f"[{ep} 考據] Missing Section 2 (## 二、清單以外發現的問題)")
            continue
        sec2 = m.group(1)
        lines = [l for l in sec2.splitlines() if l.strip().startswith("|") and not l.strip().startswith("|---") and "原主張" not in l]
        for l in lines:
            parts = [p.strip() for p in l.split("|")[1:-1]]
            if len(parts) >= 3:
                verdict = parts[2]
                if "✓" in verdict or "✔" in verdict:
                    findings.append(f"[{ep} 考據 Sec 2] Row {parts[0]} contains forbidden '✓' verdict: '{verdict}'")
    return findings

def check_toelken_hallucination():
    findings = []
    for ep in EPISODES:
        for suffix in ["_考據_gemini.md"] + [f"_審稿-{r}_antigravity.md" for r in ROLES]:
            fname = f"{ep}{suffix}"
            path = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", fname)
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            if "Anguish of Arrival" in c:
                findings.append(f"[{fname}] Contains hallucinated book title 'Anguish of Arrival'")
    return findings

def check_external_pages():
    """Check 5 (Enhanced): Exhaustive check for external non-local book page citations."""
    findings = []
    
    # Comprehensive catalog of external authors across A-16, A-17, A-18, A-19
    external_authors = [
        # A-18 Egyptian external sources
        "Chassinat", "Belmonte", "Censorinus", "Parker", "Neugebauer", "Hurst", "Ball", "Petrie",
        "Buchwald", "Josefowicz", "Sethe", "Allen", "Otto", "Assmann", "Gardiner", "Gantenbrink",
        "Bauval", "Gilbert", "Edwards", "Lehner", "Dorner", "Erman", "Grapow", "Leitz",
        # A-19 Arabic external sources
        "Ibn Qutayba", "al-Sufi", "al-Ṣūfī", "Ibn Durayd", "Ibn Manzur", "Ibn Manẓūr", "Ibn al-Jawzi",
        "Ibn al-Jawzī", "Ibn Hibban", "Ibn Ḥibbān", "Kunitzsch", "Smart", "Lane",
        "Umar ibn Abi Rabi", "Rabīʿa", "Rabia",
        # A-16 Navajo external sources
        "Toelken", "Haile", "Griffin-Pierce", "Kluckhohn", "Leighton", "Young &", "Young and", "Jayne",
        "Newcomb", "Witherspoon", "Matthews", "Chamberlain", "Schaafsma", "IEI",
        "Indigenous Education Institute", "Radin",
        # A-17 Blackfoot external sources
        "Frantz", "Russell", "Miller", "Dorsey",
    ]

    # Verified academic journal patterns (peer-reviewed articles with legitimate pagination)
    journal_pattern = re.compile(r"\b(JHA|BIFAO|JEA|MIOB|A&A|Journal for the History of Astronomy)\b", re.I)
    
    # Local verified books in 07_資料來源/ (permitted and expected to retain real pages)
    local_source_pattern = re.compile(r"\b(Childrey|Wissler\s*&\s*Duvall|Wissler\s+and\s+Duvall|McClintock)\b", re.I)
    
    # Page citation pattern: p. 12, pp. 12-14, vol. 1, p. 12, Vol. II, p. 31, Tome II, p. 31
    page_number_pattern = re.compile(
        r"(?:(?:vol\.|volume|tome|band)\s*([0-9ivxlcdm]+)[,\s]+)?\bpp?\.?\s*(\d+)",
        re.I
    )

    for ep in EPISODES:
        for suffix in ["_考據_gemini.md"] + [f"_審稿-{r}_antigravity.md" for r in ROLES]:
            fname = f"{ep}{suffix}"
            path = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", fname)
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line_no, line in enumerate(lines, 1):
                # Segment lines into discrete cells/lines
                segments = [line]
                if line.strip().startswith("|"):
                    segments = [c.strip() for c in line.split("|")[1:-1]]
                
                for seg in segments:
                    # Segment by semicolon (both Western ';' and Chinese '；') to prevent cross-citation bleed
                    citations = re.split(r"[;；]", seg)
                    for cit in citations:
                        cit_clean = cit.strip()
                        if not cit_clean:
                            continue
                        
                        # Match external authors
                        matched_authors = []
                        for author in external_authors:
                            if re.search(r"\b" + re.escape(author) + r"\b", cit_clean, re.I):
                                matched_authors.append(author)
                        
                        # Check Clark Wissler external monographs (1911/1912) vs 1908 local work
                        if "wissler" in cit_clean.lower() and not local_source_pattern.search(cit_clean):
                            if any(y in cit_clean for y in ["1911", "1912"]):
                                matched_authors.append("Wissler (1911/1912)")
                        
                        if not matched_authors:
                            continue
                        
                        # Skip if this citation clause primarily refers to a verified local source
                        if local_source_pattern.search(cit_clean):
                            continue
                        
                        # Skip legitimate peer-reviewed journal articles
                        if journal_pattern.search(cit_clean):
                            continue
                        
                        page_match = page_number_pattern.search(cit_clean)
                        has_unverified = "未核頁碼" in cit_clean
                        
                        for auth in matched_authors:
                            if page_match and has_unverified:
                                # Contradictory pattern: page number stated AND marked '未核頁碼'
                                findings.append(
                                    f"[{fname}:{line_no}] CONTRADICTION: Guessed page numbers '{page_match.group(0)}' "
                                    f"appear before/with '未核頁碼' for author '{auth}' in: {cit_clean}"
                                )
                            elif page_match and not has_unverified:
                                # Lingering guessed page number without '未核頁碼'
                                findings.append(
                                    f"[{fname}:{line_no}] GUESSED PAGE: External author '{auth}' has guessed "
                                    f"page numbers '{page_match.group(0)}' without '未核頁碼': {cit_clean}"
                                )

    return findings

def check_episode_specifics():
    findings = []
    # A-16: Shot 16 Canopus color; 01 opening intact; 05 hooghan kept
    a16_res = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-16_考據_gemini.md")
    a16_ast = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-16_審稿-天文_antigravity.md")
    a16_nar = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-16_審稿-敘事_antigravity.md")
    a16_lan = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-16_審稿-語言_antigravity.md")
    
    if os.path.exists(a16_ast):
        with open(a16_ast, "r", encoding="utf-8") as f:
            c = f.read()
        if "大氣消光" not in c and "消光" not in c and "黃白" not in c:
            findings.append("[A-16 審稿-天文] Missing Canopus yellowish-white / atmospheric extinction explanation")
    if os.path.exists(a16_nar):
        with open(a16_nar, "r", encoding="utf-8") as f:
            c = f.read()
        if re.search(r"01\s*鏡.*?(刪除|刪改|修改.*同一片星空)", c):
            findings.append("[A-16 審稿-敘事] Must NOT suggest altering Shot 01 opening sentence")
    if os.path.exists(a16_lan):
        with open(a16_lan, "r", encoding="utf-8") as f:
            c = f.read()
        if re.search(r"05\s*鏡.*?(刪除|拿掉).*hooghan", c):
            findings.append("[A-16 審稿-語言] Must NOT suggest deleting hooghan in Shot 05")

    # A-17: Shot 18 Jupiter kept; Four-Tail Lodge p. 42
    a17_ast = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-17_審稿-天文_antigravity.md")
    a17_nar = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-17_審稿-敘事_antigravity.md")
    if os.path.exists(a17_ast):
        with open(a17_ast, "r", encoding="utf-8") as f:
            c = f.read()
        if re.search(r"18\s*鏡.*?(刪除|拿掉|不應提).*木星", c):
            findings.append("[A-17 審稿-天文] Must NOT suggest deleting Jupiter in Shot 18")
    if os.path.exists(a17_nar):
        with open(a17_nar, "r", encoding="utf-8") as f:
            c = f.read()
        if re.search(r"18\s*鏡.*?(刪除|拿掉|不應提).*木星", c):
            findings.append("[A-17 審稿-敘事] Must NOT suggest deleting Jupiter in Shot 18")

    # A-18: 2027/01/25 Sirius timing in Sec 2 ⚠ & 天文 critic; 01 opening intact
    a18_res = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-18_考據_gemini.md")
    a18_ast = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-18_審稿-天文_antigravity.md")
    a18_nar = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-18_審稿-敘事_antigravity.md")
    if os.path.exists(a18_res):
        with open(a18_res, "r", encoding="utf-8") as f:
            c = f.read()
        if "16:52" not in c and "22:21" not in c and "43.7" not in c:
            findings.append("[A-18 考據] Missing 2027/01/25 Sirius timing (16:52 rise / 21:00 alt 43.7° / 22:21 culm / 03:51 set)")
    if os.path.exists(a18_ast):
        with open(a18_ast, "r", encoding="utf-8") as f:
            c = f.read()
        if "16:52" not in c and "22:21" not in c:
            findings.append("[A-18 審稿-天文] Missing 2027/01/25 Sirius timing (16:52 rise / 22:21 culm)")
    if os.path.exists(a18_nar):
        with open(a18_nar, "r", encoding="utf-8") as f:
            c = f.read()
        if re.search(r"01\s*鏡.*?(插入|前加|前置)", c):
            findings.append("[A-18 審稿-敘事] Must NOT suggest inserting text before Shot 01 opening sentence")

    # A-19: Canopus refraction timing is ⚪可選; 01 opening retains "人"
    a19_ast = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-19_審稿-天文_antigravity.md")
    a19_nar = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", "A-19_審稿-敘事_antigravity.md")
    if os.path.exists(a19_ast):
        with open(a19_ast, "r", encoding="utf-8") as f:
            c = f.read()
        if re.search(r"🔴.*?(18:10|18:11|01:17|算錯|大氣折射)", c):
            findings.append("[A-19 審稿-天文] Canopus refraction critique must be ⚪可選, not 🔴")
    if os.path.exists(a19_nar):
        with open(a19_nar, "r", encoding="utf-8") as f:
            c = f.read()
        if re.search(r"刪除.*?「人」|刪掉.*?「人」|不要「人」", c):
            findings.append("[A-19 審稿-敘事] Must NOT suggest deleting '人' from opening sentence")

    return findings

def check_dual_workspace_sync():
    findings = []
    for ep in EPISODES:
        for suffix in ["_考據_gemini.md"] + [f"_審稿-{r}_antigravity.md" for r in ROLES]:
            fname = f"{ep}{suffix}"
            wp = os.path.join(REPO_ROOT, "04_腳本庫", "_審稿", fname)
            dp = os.path.join(DOWNLOADS_ROOT, "04_腳本庫", "_審稿", fname)
            if not os.path.exists(wp):
                findings.append(f"Worktree missing: {fname}")
            elif not os.path.exists(dp):
                findings.append(f"Downloads missing: {fname}")
            else:
                wh = get_sha256(wp)
                dh = get_sha256(dp)
                if wh != dh:
                    findings.append(f"SHA-256 mismatch for {fname}: worktree={wh} vs downloads={dh}")
    return findings

def main():
    print("=" * 78)
    print(" Batch 2 Round 2 Remediation - Automated Rules Verifier (Patched)")
    print("=" * 78)
    
    checks = [
        ("1. A-16 v0 Worktree Presence & Hash Match", check_a16_v0),
        ("2. Git Immutability on Original Scripts", check_git_immutability),
        ("3. Research Section 2 (Only ✗, ⚠, ？ - zero ✓)", check_research_section2),
        ("4. Hallucinated Book Title Check ('Anguish of Arrival')", check_toelken_hallucination),
        ("5. External Books Guessed Pages Check (must be '未核頁碼' & no contradiction)", check_external_pages),
        ("6. Episode-Specific Astronomical & Narrative Rules", check_episode_specifics),
        ("7. Dual-Workspace 20 Files SHA-256 Synchronization", check_dual_workspace_sync),
    ]

    all_passed = True
    for title, fn in checks:
        print(f"\n[{title}]")
        issues = fn()
        if not issues:
            print("  -> PASS")
        else:
            all_passed = False
            print(f"  -> FAIL ({len(issues)} issues):")
            for iss in issues[:10]:
                print(f"     - {iss}")
            if len(issues) > 10:
                print(f"     ... and {len(issues) - 10} more issues")

    print("\n" + "=" * 78)
    if all_passed:
        print(" OVERALL RESULT: ALL BATCH 2 R2 REMEDIATION CHECKS PASSED")
    else:
        print(" OVERALL RESULT: REMEDIATION REQUIRED (SEE FAILURES ABOVE)")
    print("=" * 78)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
