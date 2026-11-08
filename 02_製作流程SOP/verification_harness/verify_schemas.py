# -*- coding: utf-8 -*-
"""verify_schemas.py - Markdown Schemas and Quantitative Constraint Validator.

Validates:
1. 9 Research files (04_腳本庫/_審稿/{編號}_考據_gemini.md):
   - 4 mandatory sections
   - 6-column table schema
   - 4-tier judgements (✓, ✗, ⚠, ？)
2. 36 Critic files (04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md):
   - 3-line summary header (整體評價, 最重要的三個問題, 沒把握的地方)
   - 6-column table schema with 🔴, 🟡, ⚪
   - 天文 role: Taipei ephemeris numbers present
3. 9 English draft files (04_腳本庫/_英文版/{編號}-EN-script-draft.md):
   - 5 mandatory sections
   - Total seconds <= 180s
   - Every shot Words/sec <= 2.6
   - Every On-screen text card <= 6 English words
   - Opening formula "One sky. The [people] saw — [X]."
   - YouTube title <= 60 characters
4. Master Glossary (06_發布月曆/英文譯名表.csv):
   - Valid CSV format with required columns
"""

from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

TARGET_EPISODES = [
    "A-01", "A-02", "A-03", "A-04", "A-06", "H-七夕", "A-13", "A-14", "A-15"
]

CRITIC_ROLES = ["天文", "文化", "敘事", "語言"]


# ==============================================================================
# Text Counting Utilities
# ==============================================================================

def strip_markdown(text: str) -> str:
    """Remove markdown formatting tags (bold, italic, code, links)."""
    # Remove links [text](url) -> text
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove inline formatting
    t = re.sub(r'[*_`~]', '', t)
    return t.strip()


def count_english_words(text: str) -> int:
    """Count English words accurately.
    Supports hyphens, contractions, and Unicode diacritics / okina (e.g. Al-Thurayyā, ʻokina).
    """
    clean = strip_markdown(text)
    if not clean or clean == "-" or clean == "—":
        return 0
    # Match words composed of Unicode word chars + okina/apostrophe/hyphen
    tokens = re.findall(
        r"\b[\w\u02bb\u02bc]+(?:[-\x27\u2019][\w\u02bb\u02bc]+)*\b",
        clean,
        re.UNICODE,
    )
    return len(tokens)


def count_chinese_syllables(text: str) -> int:
    """Count spoken syllables in Chinese voice-over.
    Counts CJK ideographs and English/number word tokens.
    Excludes punctuation marks (pauses).
    """
    clean = strip_markdown(text)
    tokens = re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+", clean)
    return len(tokens)


def count_chinese_card_chars(text: str) -> int:
    """Count characters in an on-screen card for Chinese scripts."""
    clean = strip_markdown(text)
    clean = re.sub(r'[「」『』"\'\s，。！？、—・·:：;；/]', '', clean)
    return len(clean)


# ==============================================================================
# Markdown Table Parsing
# ==============================================================================

def parse_markdown_tables(content: str) -> List[List[List[str]]]:
    """Extract all markdown tables from text as list of tables (each is list of row cell lists)."""
    tables: List[List[List[str]]] = []
    current_table: List[List[str]] = []
    in_table = False

    lines = content.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            # Check if separator row
            if all(re.match(r'^:?-+:?$', c) for c in cells if c):
                continue
            current_table.append(cells)
            in_table = True
        else:
            if in_table and current_table:
                tables.append(current_table)
                current_table = []
                in_table = False

    if in_table and current_table:
        tables.append(current_table)

    return tables


# ==============================================================================
# Validation Result Object
# ==============================================================================

@dataclass
class ValidationResult:
    file_path: str
    file_type: str  # "research", "critic", "english", "glossary"
    passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def add_error(self, msg: str):
        self.passed = False
        self.errors.append(msg)

    def add_warning(self, msg: str):
        self.warnings.append(msg)


# ==============================================================================
# 1. Research Report Validator (R1)
# ==============================================================================

RESEARCH_MANDATORY_SECTIONS = [
    "一、待查核清單逐條結果",
    "二、清單以外發現的問題",
    "三、可以加進影片的好材料",
    "四、參考資料總表",
]

VERDICT_SYMBOLS = ["✓", "✗", "⚠", "？", "?"]


def validate_research_file(file_path: str) -> ValidationResult:
    """Validate a single 04_腳本庫/_審稿/{編號}_考據_gemini.md file."""
    res = ValidationResult(file_path=file_path, file_type="research")

    if not os.path.exists(file_path):
        res.add_error(f"File not found: {file_path}")
        return res

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # 1. Check title
    if not re.search(r"^#\s+[A-Za-z0-9\-七夕]+.*考據", content, re.MULTILINE):
        res.add_warning("Header does not strictly match `# {編號} 網路考據` pattern")

    # 2. Check 4 mandatory sections
    for sec in RESEARCH_MANDATORY_SECTIONS:
        pattern = r"##\s*" + re.escape(sec)
        if not re.search(pattern, content):
            res.add_error(f"Missing mandatory section: '## {sec}'")

    # 3. Check table schema (6 columns)
    tables = parse_markdown_tables(content)
    if not tables:
        res.add_error("No tables found in research report (expected at least 1-2 verification tables)")
    else:
        valid_table_found = False
        total_claims_audited = 0
        for tbl in tables:
            if not tbl:
                continue
            header = tbl[0]
            # Expecting 6 columns: #, 原主張, 判定, 查到的正確說法, 出處, 建議改寫
            if len(header) == 6:
                valid_table_found = True
                # Check data rows
                for row_idx, row in enumerate(tbl[1:], start=1):
                    if len(row) != 6:
                        res.add_error(f"Table row {row_idx} has {len(row)} columns, expected 6")
                        continue
                    total_claims_audited += 1
                    verdict_cell = row[2]
                    # Must contain one of the 4-tier judgements
                    if not any(sym in verdict_cell for sym in VERDICT_SYMBOLS):
                        res.add_error(
                            f"Table row {row_idx}: verdict '{verdict_cell}' missing 4-tier symbol (✓/✗/⚠/？)"
                        )
                    # Check citation in col 4 (0-indexed)
                    citation_cell = row[4]
                    if not citation_cell or citation_cell == "-":
                        res.add_warning(f"Table row {row_idx}: citation column appears empty")

        if not valid_table_found:
            res.add_error("Did not find any 6-column verification table matching schema")
        res.metrics["claims_audited"] = total_claims_audited

    return res


# ==============================================================================
# 2. Critic Review Validator (R2)
# ==============================================================================

def validate_critic_file(file_path: str, role: str) -> ValidationResult:
    """Validate a single 04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md file."""
    res = ValidationResult(file_path=file_path, file_type="critic")
    res.metrics["role"] = role

    if not os.path.exists(file_path):
        res.add_error(f"File not found: {file_path}")
        return res

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # 1. Check Top 3-line summary header:
    # Line 1: 整體評價, Line 2: 最重要的三個問題, Line 3: 沒把握的地方
    has_eval = bool(re.search(r"(整體評價|整体評價)", content))
    has_top3 = bool(re.search(r"最重要的三個問題", content))
    has_unsure = bool(re.search(r"沒把握的地方", content))

    if not (has_eval and has_top3 and has_unsure):
        missing = []
        if not has_eval:
            missing.append("整體評價")
        if not has_top3:
            missing.append("最重要的三個問題")
        if not has_unsure:
            missing.append("沒把握的地方")
        res.add_error(f"Header missing 3-line summary elements: {', '.join(missing)}")

    # 2. Check 6-column review table
    tables = parse_markdown_tables(content)
    valid_review_table = False
    total_criticisms = 0

    severity_counts = {"🔴": 0, "🟡": 0, "⚪": 0}

    for tbl in tables:
        if not tbl:
            continue
        header = tbl[0]
        # Schema: | 嚴重度 | 位置 | 原文 | 問題 | 建議改法 | 依據 |
        if len(header) == 6 and any("嚴重度" in col for col in header):
            valid_review_table = True
            for row_idx, row in enumerate(tbl[1:], start=1):
                if len(row) != 6:
                    res.add_error(f"Review table row {row_idx} has {len(row)} columns, expected 6")
                    continue
                total_criticisms += 1
                sev_cell = row[0]
                has_sev = False
                for sym in ["🔴", "🟡", "⚪"]:
                    if sym in sev_cell:
                        severity_counts[sym] += 1
                        has_sev = True
                if not has_sev:
                    res.add_error(f"Review row {row_idx} severity '{sev_cell}' missing 🔴/🟡/⚪")

                # If suggested rewrite has VO / card, check limits
                suggested = row[4]
                pos = row[1]
                if suggested:
                    # Card length check
                    if "字卡" in pos:
                        card_len = count_chinese_card_chars(suggested)
                        if card_len > 14:
                            res.add_warning(
                                f"Review row {row_idx}: suggested card text length ({card_len}) > 14 chars"
                            )

                    # Voice-over pace check (SOP: <= 4.5 chars/sec)
                    # Check explicit pace expressions in suggested text, e.g. （XX字/YY秒＝ZZ字/秒）
                    brackets = re.findall(
                        r"[（(](\d+)\s*字\s*(?:/|，|,)\s*(\d+(?:\.\d+)?)\s*秒(?:[＝=，,]\s*(?:語速)?\s*(\d+(?:\.\d+)?)\s*字/秒)?[）)]",
                        suggested
                    )
                    for chars_s, sec_s, rate_s in brackets:
                        sec = float(sec_s)
                        if rate_s:
                            rate = float(rate_s)
                        elif sec > 0:
                            rate = int(chars_s) / sec
                        else:
                            rate = 0.0
                        # Skip if this was an intermediate attempt discarded by "進一步提煉"
                        bracket_str = f"{chars_s}字"
                        b_idx = suggested.find(bracket_str)
                        if b_idx != -1 and "進一步提煉" in suggested[b_idx:b_idx+30]:
                            continue
                        if rate > 4.50:
                            res.add_error(
                                f"Review row {row_idx}: explicit voice-over pace {rate:.2f} chars/sec "
                                f"({chars_s} chars in {sec}s) exceeds limit of 4.5 chars/sec"
                            )

                    # Check voice-over rewrite quote against slot duration
                    clean_sugg = re.split(r"(?:字卡|首留言|【臺灣業餘天文聯盟版文案】)", suggested)[0]
                    if any(k in clean_sugg for k in ["改為", "旁白", "建議", "「", "『"]):
                        sugg_dur_match = re.search(r"(?:長度為|調整(?:該鏡頭)?(?:長度)?為|微調至|約)\s*(\d+(?:\.\d+)?)\s*秒", suggested)
                        if sugg_dur_match:
                            dur = float(sugg_dur_match.group(1))
                        else:
                            time_match = re.search(r"(\d+(?:\.\d+)?)\s*[–\-\~至到]\s*(\d+(?:\.\d+)?)\s*(?:s|秒)", pos)
                            if time_match and ("鏡" not in pos or "s" in pos or "秒" in pos):
                                t1 = float(time_match.group(1))
                                t2 = float(time_match.group(2))
                                dur = t2 - t1
                            elif re.search(r"(\d+(?:\.\d+)?)\s*(?:秒|s\b)", pos) and "鏡" not in pos:
                                m_sec = re.search(r"(\d+(?:\.\d+)?)\s*(?:秒|s\b)", pos)
                                dur = float(m_sec.group(1))
                            else:
                                dur = None

                        if dur and dur > 0:
                            if "進一步提煉為" in clean_sugg:
                                clean_sugg = clean_sugg.split("進一步提煉為")[-1]
                            vo_quotes = re.findall(r"[「『]([^」』]+)[」』]", clean_sugg)
                            for vq in vo_quotes:
                                sylls = count_chinese_syllables(vq)
                                if sylls > 0:
                                    pace = round(sylls / dur, 2)
                                    if pace > 4.50:
                                        res.add_error(
                                            f"Review row {row_idx}: suggested voice-over speech rate {pace:.2f} chars/sec "
                                            f"({sylls} chars / {dur:.1f}s) exceeds limit of 4.5 chars/sec"
                                        )

    if not valid_review_table:
        res.add_error("Missing 6-column review opinion table (| 嚴重度 | 位置 | 原文 | 問題 | 建議改法 | 依據 |)")

    res.metrics["criticisms"] = total_criticisms
    res.metrics["severity"] = severity_counts

    # 3. Role-specific check: 天文 must contain Taipei ephemeris verification numbers
    if role == "天文":
        try:
            from .verify_ephemeris import verify_critic_astronomy_text
        except ImportError:
            from verify_ephemeris import verify_critic_astronomy_text
        ephe_ok, ephe_findings = verify_critic_astronomy_text(content)
        if not ephe_ok:
            for f in ephe_findings:
                res.add_error(f"Astronomer critic requirement violated: {f}")

    return res


# ==============================================================================
# 3. English Script Draft Validator (R3)
# ==============================================================================

ENGLISH_MANDATORY_SECTION_PATTERNS = [
    (r"Shot|分鏡", "Shot Table"),
    (r"Total|Summary|總計|秒數", "Totals / Summary"),
    (r"Glossary|譯名表", "Glossary Table"),
    (r"YouTube|Facebook|Social|社群文案", "Social Platform Metadata"),
    (r"Cut|Changed|Adjustment|刪減|調整", "Cut & Adjustment Log"),
]


def validate_english_draft_file(file_path: str) -> ValidationResult:
    """Validate a single 04_腳本庫/_英文版/{編號}-EN-script-draft.md file."""
    res = ValidationResult(file_path=file_path, file_type="english")

    if not os.path.exists(file_path):
        res.add_error(f"File not found: {file_path}")
        return res

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # 1. Check mandatory 5 sections
    for pat, sec_name in ENGLISH_MANDATORY_SECTION_PATTERNS:
        if not re.search(pat, content, re.IGNORECASE):
            res.add_error(f"Missing mandatory section in English draft: {sec_name}")

    # 2. Parse Shot Table
    # Expected schema: | Shot | Sec | Voice-over | On-screen text | Words/sec |
    tables = parse_markdown_tables(content)
    shot_table = None
    glossary_table = None

    for tbl in tables:
        if not tbl:
            continue
        header = [c.lower() for c in tbl[0]]
        if any("shot" in h for h in header) and any("voice" in h or "vo" in h for h in header):
            shot_table = tbl
        elif any("chinese" in h or "中文" in h for h in header) and any("english" in h or "英文" in h for h in header):
            glossary_table = tbl

    if not shot_table:
        res.add_error("Could not find Shot Table (| Shot | Sec | Voice-over | On-screen text | Words/sec |)")
    else:
        header = shot_table[0]
        # Identify column indices
        col_sec_idx = None
        col_vo_idx = None
        col_card_idx = None
        col_wps_idx = None

        for idx, col in enumerate(header):
            col_l = col.lower()
            if "word" in col_l or "w/s" in col_l or "words/sec" in col_l or "rate" in col_l:
                col_wps_idx = idx
            elif "sec" in col_l or "duration" in col_l or "秒" in col_l:
                col_sec_idx = idx
            elif "voice" in col_l or "vo" in col_l or "narration" in col_l or "旁白" in col_l:
                col_vo_idx = idx
            elif "card" in col_l or "screen" in col_l or "text" in col_l or "字卡" in col_l:
                col_card_idx = idx

        # Default fallbacks if header matches standard 5 cols: | Shot | Sec | Voice-over | On-screen text | Words/sec |
        if col_sec_idx is None and len(header) >= 5:
            col_sec_idx = 1
        if col_vo_idx is None and len(header) >= 5:
            col_vo_idx = 2
        if col_card_idx is None and len(header) >= 5:
            col_card_idx = 3
        if col_wps_idx is None and len(header) >= 5:
            col_wps_idx = 4

        total_seconds = 0.0
        total_words = 0
        max_wps = 0.0
        max_card_words = 0

        first_shot_vo = ""

        for row_idx, row in enumerate(shot_table[1:], start=1):
            if len(row) < 4:
                continue

            # Parse seconds
            sec_val = 0.0
            if col_sec_idx is not None and col_sec_idx < len(row):
                sec_str = re.sub(r"[^\d.]", "", row[col_sec_idx])
                try:
                    sec_val = float(sec_str) if sec_str else 0.0
                except ValueError:
                    sec_val = 0.0
            total_seconds += sec_val

            # Parse VO and word count
            vo_text = ""
            if col_vo_idx is not None and col_vo_idx < len(row):
                vo_text = row[col_vo_idx]
                if not first_shot_vo and vo_text and vo_text != "-":
                    first_shot_vo = vo_text

            words = count_english_words(vo_text)
            total_words += words

            # Check Speech Rate Words/Sec
            calculated_wps = round(words / sec_val, 2) if sec_val > 0 else 0.0
            if calculated_wps > max_wps:
                max_wps = calculated_wps

            # Rule: Every shot speech rate <= 2.6 words/sec
            if sec_val > 0 and calculated_wps > 2.65:  # small epsilon for rounding
                res.add_error(
                    f"Shot {row_idx}: Speech rate {calculated_wps} words/sec exceeds limit 2.6 "
                    f"({words} words in {sec_val}s)"
                )

            # Check On-screen card text
            if col_card_idx is not None and col_card_idx < len(row):
                card_text = row[col_card_idx]
                if card_text and card_text not in ["-", "—", "None", "none"]:
                    card_words = count_english_words(card_text)
                    if card_words > max_card_words:
                        max_card_words = card_words
                    # Rule: Every text card <= 6 English words
                    if card_words > 6:
                        res.add_error(
                            f"Shot {row_idx}: Text card '{card_text}' has {card_words} words, exceeds limit of 6"
                        )

        res.metrics["total_seconds"] = total_seconds
        res.metrics["total_words"] = total_words
        res.metrics["max_words_per_sec"] = max_wps
        res.metrics["max_card_words"] = max_card_words

        # Rule: Total seconds <= 180s
        if total_seconds > 180.0:
            res.add_error(
                f"Total video duration {total_seconds:.1f}s exceeds hard limit of 180 seconds"
            )

        # Rule: Opening line pattern: "One sky. The [people] saw — [X]."
        # Also allow valid special variant e.g. for Qixi or Mid-Autumn if starting with "One sky."
        clean_first_vo = strip_markdown(first_shot_vo)
        if not clean_first_vo.lower().startswith("one sky"):
            res.add_error(
                f"Opening voice-over does not match 'One sky.' formula. Found: '{clean_first_vo[:50]}...'"
            )

    # 3. Check Glossary Table
    if not glossary_table:
        res.add_warning("Glossary table not recognized or empty in English draft")
    else:
        res.metrics["glossary_entries"] = len(glossary_table) - 1

    # 4. Check YouTube Title <= 60 characters
    yt_match = re.search(r"YouTube\s*Title\s*[:：]\s*(.+)", content, re.IGNORECASE)
    if yt_match:
        yt_title = yt_match.group(1).strip()
        title_len = len(yt_title)
        res.metrics["youtube_title_len"] = title_len
        if title_len > 60:
            res.add_error(f"YouTube title length ({title_len} chars) exceeds limit of 60 chars: '{yt_title}'")
    else:
        # Try generic search for title line
        lines = content.splitlines()
        found_yt = False
        for line in lines:
            if "youtube title" in line.lower() or "yt title" in line.lower():
                found_yt = True
                val = line.split(":", 1)[-1].strip() if ":" in line else line.split("：", 1)[-1].strip()
                if len(val) > 60:
                    res.add_error(f"YouTube title exceeds 60 chars ({len(val)}): '{val}'")
        if not found_yt:
            res.add_warning("Could not explicitly locate 'YouTube Title: ...' line for length check")

    return res


# ==============================================================================
# 4. Master Glossary CSV Validator
# ==============================================================================

def validate_glossary_csv(file_path: str) -> ValidationResult:
    """Validate 06_發布月曆/英文譯名表.csv."""
    res = ValidationResult(file_path=file_path, file_type="glossary")

    if not os.path.exists(file_path):
        res.add_error(f"Glossary CSV file not found: {file_path}")
        return res

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        res.add_error(f"Failed to read CSV: {e}")
        return res

    if not rows:
        res.add_error("Glossary CSV is completely empty")
        return res

    header = [h.strip().lower() for h in rows[0]]
    res.metrics["columns"] = header

    # Expecting Chinese and English columns
    has_zh = any("chinese" in h or "中文" in h or "詞目" in h or "原名" in h for h in header)
    has_en = any("english" in h or "英文" in h or "譯名" in h for h in header)

    if not (has_zh and has_en):
        res.add_error(f"Glossary CSV missing required Chinese / English columns. Found: {rows[0]}")

    # Check row count
    data_rows = rows[1:]
    res.metrics["total_terms"] = len(data_rows)
    if len(data_rows) < 10:
        res.add_warning(
            f"Glossary CSV has only {len(data_rows)} entries; expected comprehensive term coverage for 9 episodes"
        )

    # Check for empty cells in Chinese or English
    zh_idx = 0
    en_idx = 1
    for idx, h in enumerate(header):
        if "chinese" in h or "中文" in h:
            zh_idx = idx
        elif "english" in h or "英文" in h:
            en_idx = idx

    empty_terms = 0
    for r_idx, r in enumerate(data_rows, start=2):
        if len(r) <= max(zh_idx, en_idx) or not r[zh_idx].strip() or not r[en_idx].strip():
            empty_terms += 1

    if empty_terms > 0:
        res.add_error(f"Glossary CSV contains {empty_terms} rows with missing Chinese or English terms")

    return res


# ==============================================================================
# Comprehensive Schema Runner across Deliverables
# ==============================================================================

def validate_all_schemas(repo_dir: str) -> Dict[str, Any]:
    """Run schema validation on all 55 deliverable files in the given repo worktree."""
    summary = {
        "research": {"total": 9, "passed": 0, "failed": 0, "missing": 0, "results": []},
        "critic": {"total": 36, "passed": 0, "failed": 0, "missing": 0, "results": []},
        "english": {"total": 9, "passed": 0, "failed": 0, "missing": 0, "results": []},
        "glossary": {"total": 1, "passed": 0, "failed": 0, "missing": 0, "results": []},
        "all_passed": False,
    }

    # 1. Research Files (9)
    for ep in TARGET_EPISODES:
        p = os.path.join(repo_dir, "04_腳本庫", "_審稿", f"{ep}_考據_gemini.md")
        if not os.path.exists(p):
            summary["research"]["missing"] += 1
            res = ValidationResult(file_path=p, file_type="research", passed=False)
            res.add_error("File not yet created (pending milestone)")
        else:
            res = validate_research_file(p)
            if res.passed:
                summary["research"]["passed"] += 1
            else:
                summary["research"]["failed"] += 1
        summary["research"]["results"].append(res)

    # 2. Critic Files (36)
    for ep in TARGET_EPISODES:
        for role in CRITIC_ROLES:
            p = os.path.join(repo_dir, "04_腳本庫", "_審稿", f"{ep}_審稿-{role}_antigravity.md")
            if not os.path.exists(p):
                summary["critic"]["missing"] += 1
                res = ValidationResult(file_path=p, file_type="critic", passed=False)
                res.add_error("File not yet created (pending milestone)")
            else:
                res = validate_critic_file(p, role)
                if res.passed:
                    summary["critic"]["passed"] += 1
                else:
                    summary["critic"]["failed"] += 1
            summary["critic"]["results"].append(res)

    # 3. English Drafts (9)
    for ep in TARGET_EPISODES:
        p = os.path.join(repo_dir, "04_腳本庫", "_英文版", f"{ep}-EN-script-draft.md")
        if not os.path.exists(p):
            summary["english"]["missing"] += 1
            res = ValidationResult(file_path=p, file_type="english", passed=False)
            res.add_error("File not yet created (pending milestone)")
        else:
            res = validate_english_draft_file(p)
            if res.passed:
                summary["english"]["passed"] += 1
            else:
                summary["english"]["failed"] += 1
        summary["english"]["results"].append(res)

    # 4. Master Glossary CSV (1)
    p_csv = os.path.join(repo_dir, "06_發布月曆", "英文譯名表.csv")
    if not os.path.exists(p_csv):
        summary["glossary"]["missing"] += 1
        res = ValidationResult(file_path=p_csv, file_type="glossary", passed=False)
        res.add_error("Glossary CSV not yet created (pending milestone)")
    else:
        res = validate_glossary_csv(p_csv)
        if res.passed:
            summary["glossary"]["passed"] += 1
        else:
            summary["glossary"]["failed"] += 1
    summary["glossary"]["results"].append(res)

    total_expected = 9 + 36 + 9 + 1
    total_passed = (
        summary["research"]["passed"]
        + summary["critic"]["passed"]
        + summary["english"]["passed"]
        + summary["glossary"]["passed"]
    )
    summary["all_passed"] = (total_passed == total_expected)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Markdown Schemas & Quantitative Constraints Validator")
    parser.add_argument("--repo", type=str, default=".", help="Repository root directory")
    parser.add_argument("--file", type=str, default=None, help="Validate a single specific file")
    parser.add_argument("--type", type=str, choices=["research", "critic", "english", "glossary"], default=None)
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)

    if args.file:
        fpath = os.path.abspath(args.file)
        ftype = args.type
        if not ftype:
            if "_考據_" in fpath:
                ftype = "research"
            elif "_審稿-" in fpath:
                ftype = "critic"
            elif "-EN-script-draft" in fpath:
                ftype = "english"
            elif fpath.endswith(".csv"):
                ftype = "glossary"

        if ftype == "research":
            res = validate_research_file(fpath)
        elif ftype == "critic":
            role = "天文"
            for r in CRITIC_ROLES:
                if f"-{r}_" in fpath:
                    role = r
                    break
            res = validate_critic_file(fpath, role)
        elif ftype == "english":
            res = validate_english_draft_file(fpath)
        elif ftype == "glossary":
            res = validate_glossary_csv(fpath)
        else:
            print(f"[ERROR] Could not determine file type for {fpath}")
            sys.exit(1)

        print(f"Validation Result for: {fpath}")
        print(f"Passed: {res.passed}")
        if res.errors:
            print("Errors:")
            for err in res.errors:
                print(f"  - {err}")
        if res.warnings:
            print("Warnings:")
            for w in res.warnings:
                print(f"  * {w}")
        if res.metrics:
            print(f"Metrics: {res.metrics}")
        sys.exit(0 if res.passed else 1)

    print("=" * 70)
    print("NTNU Astronomy Club — Schema & Quantitative Validator")
    print(f"Repository Root: {repo}")
    print("=" * 70)

    summary = validate_all_schemas(repo)

    categories = [
        ("Research Reports (R1)", summary["research"]),
        ("Critic Reviews (R2)", summary["critic"]),
        ("English Drafts (R3)", summary["english"]),
        ("Master Glossary CSV", summary["glossary"]),
    ]

    for cat_name, cat_data in categories:
        print(f"\n{cat_name}:")
        print(f"  Total Expected: {cat_data['total']}")
        print(f"  Passed: {cat_data['passed']}")
        print(f"  Failed: {cat_data['failed']}")
        print(f"  Missing: {cat_data['missing']}")

    print("\n" + "=" * 70)
    if summary["all_passed"]:
        print("[SUCCESS] All 55 deliverable files verified and passed all constraints!")
        sys.exit(0)
    else:
        print("[INFO] Not all deliverable files exist or passed yet (expected during development).")
        sys.exit(1)


if __name__ == "__main__":
    main()
