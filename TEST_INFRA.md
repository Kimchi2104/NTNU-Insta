# TEST_INFRA.md: E2E Automated Testing Infrastructure

## Overview
This document specifies the automated verification and testing infrastructure for the National Taiwan Normal University (NTNU) Astronomy Club "World Sky Cultures" (萬國星空) video series workflow.

The test suite provides exhaustive automated verification across all 9 target episodes (`A-01`, `A-02`, `A-03`, `A-04`, `A-06`, `H-七夕`, `A-13`, `A-14`, `A-15`), covering 55 deliverable files, astronomical ephemeris calculations, markdown schemas, quantitative audio/visual limits, and dual-workspace synchronization.

---

## 1. Testing Architecture Overview

```
                                  +-----------------------------------------+
                                  |    verify_all.py (Master Test Runner)   |
                                  +-----------------------------------------+
                                                       |
         +--------------------+------------------------+------------------------+---------------------+
         |                    |                                                 |                     |
         v                    v                                                 v                     v
+-----------------+  +-------------------------------------------------+  +------------------+  +-----------------+
| verify_ephemeris|  | verify_schemas.py                               |  | verify_sync.py   |  | Self-Check Suite|
| Skyfield 1.54   |  | 9 Research Files  (4 sects, 6 cols, 4 tiers)    |  | Dual-workspace   |  | Unit & Fixture  |
| local de421.bsp |  | 36 Critic Files   (3 lines, 🔴/🟡/⚪, Taipei)   |  | SHA-256 (55 f)   |  | Regression      |
| Taipei 25.03°N  |  | 9 English Drafts  (<=180s, <=2.6w/s, <=6w cards)|  | Git Immutability |  | 17 self tests   |
| 121.56°E, UTC+8 |  | 1 Glossary CSV    (Chinese/English, 9 eps)      |  | 04_腳本庫/*.md   |  | Positive/Neg    |
+-----------------+  +-------------------------------------------------+  +------------------+  +-----------------+
```

### Execution Environment
- **Interpreter**: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`
- **Libraries**: `skyfield` 1.54, `numpy` 2.2.6, `scipy` 1.15.3, `pandas` 2.2.3, `jplephem` 2.24
- **Ephemeris Data**: Local `de421.bsp` (16 MB)
- **Observer Location**: Taipei, Taiwan (25.03°N, 121.56°E, Elevation 10m, Timezone `Asia/Taipei` UTC+8)
- **Primary Worktree**: `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost`
- **Mirror Target**: `/Users/kimjoo/Downloads/NTNU Insta`

---

## 2. Multi-Tier Testing Methodology

The verification suite enforces a 5-tier testing architecture:

### Tier 1: Feature Coverage (>= 5 Test Cases per Feature)
Every feature defined in `PROJECT.md` is covered by at least 5 distinct test assertions verifying normal operation, correct file generation, and schema adherence.

### Tier 2: Boundary & Corner Cases (>= 5 Test Cases per Feature)
Explicit testing of edge limits:
- Exact 180.0s vs 180.1s video runtime
- Exact 2.60 words/sec vs 2.61 words/sec speech rate
- Exact 6 words vs 7 words graphic card text
- Exact 60 characters vs 61 characters YouTube title
- Spica rising at 19:47 CST (0° elevation) vs 20:00 CST (2.3° elevation)
- Canopus maximum elevation in Taipei (12.27°) vs Kaohsiung (14.68°)
- Unicode diacritics in Arabic (`Al-Thurayyā`, `al-Wasm`, `al-Murabbaʿāniyya`), Polynesian (`ʻokina`, `kahakō`), Inuktitut (`Aagjuuk`), and Old Norse (`Úlfs kjaptr`)

### Tier 3: Cross-Feature Pipeline Integration
End-to-end integration across production phases:
1. `R1 (網路考據)` findings feed into `R2 (四角色審稿)`.
2. `R2 (天文)` verifies exact ephemeris recalculated by `verify_ephemeris.py`.
3. `R2 (文化)` verifies classical chapter citations matched against Chinese canons.
4. `R3 (英文版改寫)` adapts facts established in R1/R2, enforces `< 180s` and `<= 2.6 w/s`, and populates `06_發布月曆/英文譯名表.csv`.
5. `R4 (雙向同步與原稿保護)` mirrors all 55 generated files to `/Users/kimjoo/Downloads/NTNU Insta` with 100% SHA-256 equivalence, and checks `git status` to ensure 0 changes to original scripts.

### Tier 4: Real-World Scenarios
Real-world delivery conditions:
1. **Vertical Short Video Constraints**: Instagram Reels / YouTube Shorts 9:16 layout limits (word density, card reading time, retention hook in first 3 seconds).
2. **Taiwan Amateur Astronomy Scrutiny**: "臺灣業餘天文聯盟" 60,000-member community audit — zero tolerance for fabricated coordinates or unverified celestial claims.
3. **Historical Precession Drift**: Explaining the shift of "龍抬頭" (Horn mansion rising in dusk) from the Han dynasty / 3,000 BCE to modern March/April skies.
4. **Indigenous Cultural Sovereignty**: Respecting seasonal taboos (e.g., Navajo winter storytelling) and retaining accurate Indigenous orthography.

### Tier 5: Adversarial Hardening
Adversarial test cases designed to catch subtle corruption:
1. **Encoding Integrity**: Unicode NFC/NFD normalization, zero-width spaces (`\u200b`), non-breaking spaces (`\u00a0`), right-to-left marks in Arabic script.
2. **Markdown Parsing Resiliency**: Irregular table pipes, unescaped delimiters, mixed Windows (`\r\n`) and Unix (`\n`) newlines.
3. **Boundary Flooding**: Excessively long strings, zero-duration shots (`sec = 0`), empty lines within tables.

---

## 3. Exhaustive Feature Test Matrix (31 Features × 5+ Test Cases)

| Feature ID | Feature Name | Tier 1 (Coverage >= 5) | Tier 2 (Boundary >= 5) | Automated Verifier |
|---|---|---|---|---|
| **R1-DEST** | 9 Research Output Paths | TC-R1D-01 to 05 (Verify existence of all 9 `{編號}_考據_gemini.md`) | TC-R1D-B01 to B05 (Wrong suffix, wrong dir, missing prefix, empty file, non-md extension) | `verify_schemas.py` |
| **R1-SECT** | 4 Mandatory Sections | TC-R1S-01 to 05 (Verify Sections 一, 二, 三, 四 present) | TC-R1S-B01 to B05 (Omitted Sec 4, misnumbered Sec 2, empty Sec 1, swapped Sec 1/2, heading typo) | `verify_schemas.py` |
| **R1-TABL** | 6-Column Research Table & 4 Tiers | TC-R1T-01 to 05 (6 columns present, verdicts `✓`, `✗`, `⚠`, `？`) | TC-R1T-B01 to B05 (5 cols, 7 cols, invalid verdict icon, missing citations, empty rows) | `verify_schemas.py` |
| **R1-COLL** | Classical Text Collation | TC-R1C-01 to 05 (Verify book, chapter, edition citations) | TC-R1C-B01 to B05 (Vernacular paraphrases, missing edition, fake page num, missing dynasty, vague "古籍") | `verify_schemas.py` |
| **R1-ETHN** | Ethnographic Provenance Tracing | TC-R1E-01 to 05 (Traced to anthropologist, recorder, year) | TC-R1E-B01 to B05 (Stellarium-only citations, blog references, missing recorder name, unsourced folklore, modern embellishments) | `verify_schemas.py` |
| **R1-ASTR** | Ephemeris Cross-Check for Taipei | TC-R1A-01 to 05 (Verification of coordinates, distances, mags) | TC-R1A-B01 to B05 (Mismatched coordinates, ignored precession, wrong distance unit, incorrect azimuth, unreferenced source) | `verify_ephemeris.py` |
| **R2-QUAD** | 4-Role Critic Independence | TC-R2Q-01 to 05 (36 files across 天文, 文化, 敘事, 語言) | TC-R2Q-B01 to B05 (Missing role file, duplicate role, merged report, incorrect filename delimiter, wrong directory) | `verify_schemas.py` |
| **R2-SUMM** | 3-Line Summary Header | TC-R2S-01 to 05 (整體評價, 最重要的三個問題, 沒把握的地方) | TC-R2S-B01 to B05 (Only 2 lines, missing "沒把握", header merged into table, missing "三個問題", reversed order) | `verify_schemas.py` |
| **R2-TABL** | 6-Column Critic Table & Severity | TC-R2T-01 to 05 (嚴重度, 位置, 原文, 問題, 建議改法, 依據; 🔴, 🟡, ⚪) | TC-R2T-B01 to B05 (Missing severity icon, 4 columns, missing recommendation, unrated opinions, invalid emoji) | `verify_schemas.py` |
| **R2-VOSP** | Voice-over Pace Limit (<= 4.5 c/s) | TC-R2V-01 to 05 (Verify Chinese syllable counting in suggested VO) | TC-R2V-B01 to B05 (Exactly 4.50 c/s, 4.51 c/s, punctuation exclusion, loan words, numbers in speech) | `verify_schemas.py` |
| **R2-CARD** | On-screen Card Limit (<= 14 chars) | TC-R2C-01 to 05 (Verify Chinese card length in suggested rewrites) | TC-R2C-B01 to B05 (14 chars pass, 15 chars fail, punctuation stripping, middle dot `・`, quotes) | `verify_schemas.py` |
| **R2-LANG** | Taiwan Phrasing & Terminology | TC-R2L-01 to 05 (Audit for Taiwanese phrasing in 語言 role) | TC-R2L-B01 to B05 (視頻 vs 短影音, 質量 vs 品質/質量, 信息 vs 訊息, 軟件 vs 軟體, 網絡 vs 網路) | `verify_schemas.py` |
| **R2-FORM** | Opening Formula & Closing Teaser | TC-R2F-01 to 05 (「同一片星空，◯◯看見——◯◯。」 & Next episode teaser) | TC-R2F-B01 to B05 (Deviating opening, missing em-dash, missing closing teaser, mismatched upcoming title, missing colon) | `verify_schemas.py` |
| **R2-TAIP** | Taipei Sky Clocking in 天文 Role | TC-R2P-01 to 05 (References to 25.03°N, 121.56°E, UTC+8, Alt/Az) | TC-R2P-B01 to B05 (Missing coordinates, missing elevation, no time zone specified, no rise/set times, vague "晚上看") | `verify_ephemeris.py` |
| **R3-DEST** | 9 English Draft Output Paths | TC-R3D-01 to 05 (Verify `{編號}-EN-script-draft.md` in `04_腳本庫/_英文版/`) | TC-R3D-B01 to B05 (Wrong folder, wrong prefix, underscore instead of hyphen, missing `-EN-`, empty file) | `verify_schemas.py` |
| **R3-TIME** | Total Video Duration (<= 180s) | TC-R3T-01 to 05 (Sum of shot seconds verified) | TC-R3T-B01 to B05 (180.0s pass, 180.1s fail, 240s fail, float precision, zero duration shot) | `verify_schemas.py` |
| **R3-PACE** | Shot Speech Rate (<= 2.6 w/s) | TC-R3P-01 to 05 (Words/sec verified for every shot row) | TC-R3P-B01 to B05 (2.60 w/s pass, 2.61 w/s fail, contractions, hyphenated words, diacritics, decimal rounding) | `verify_schemas.py` |
| **R3-CARD** | English Card Limit (<= 6 words) | TC-R3C-01 to 05 (Word count per on-screen graphic card) | TC-R3C-B01 to B05 (6 words pass, 7 words fail, empty card, hyphenated compound, bracketed subtitle) | `verify_schemas.py` |
| **R3-FORM** | English Opening Formula | TC-R3F-01 to 05 (*"One sky. The [people] saw — [X]."* pattern) | TC-R3F-B01 to B05 (Missing "One sky", lowercase, missing period, missing em-dash, arbitrary narrative opening) | `verify_schemas.py` |
| **R3-TABL** | Shot Table Schema | TC-R3B-01 to 05 (`| Shot | Sec | Voice-over | On-screen text | Words/sec |`) | TC-R3B-B01 to B05 (Swapped cols, missing Sec, missing VO, unaligned pipe delimiters, non-numeric sec) | `verify_schemas.py` |
| **R3-SECT** | 5 English Draft Sections | TC-R3S-01 to 05 (Shot Table, Totals, Glossary, Social Copy, Cut Log) | TC-R3S-B01 to B05 (Omitted Cut Log, missing Totals, missing Glossary, missing Social copy, mislabeled headings) | `verify_schemas.py` |
| **R3-GLOS** | Central Glossary CSV Maintenance | TC-R3G-01 to 05 (`06_發布月曆/英文譯名表.csv` valid CSV, 9 episodes) | TC-R3G-B01 to B05 (Missing header, blank cells, missing episode tag, comma in unquoted cell, duplicate terms) | `verify_schemas.py` |
| **R3-ROMA** | Multi-Lingual Romanization | TC-R3R-01 to 05 (Pinyin asterisms, RR, Hepburn, IAST, Arabic/Indigenous diacritics) | TC-R3R-B01 to B05 (Stripped macron, missing ʻokina, calling asterisms constellations, JikNyeo vs Jingnyeo, missing IAST diacritics) | `verify_schemas.py` |
| **R3-METS** | YouTube Title (<= 60 chars) & Copy | TC-R3M-01 to 05 (Title length, description 3-5 lines, FB caption) | TC-R3M-B01 to B05 (60 chars pass, 61 chars fail, description missing citations, missing FB caption, empty title) | `verify_schemas.py` |
| **R4-IMMU** | Original Script Immutability | TC-R4I-01 to 05 (`git status --porcelain 04_腳本庫/*.md` is clean) | TC-R4I-B01 to B05 (Modified original file, staged edit, deleted original file, renamed original file, untracked root file) | `verify_sync.py` |
| **R4-SYNC** | Dual-Workspace Synchronization | TC-R4S-01 to 05 (Mirror 55 files to `/Users/kimjoo/Downloads/NTNU Insta`) | TC-R4S-B01 to B05 (Missing file in mirror, byte discrepancy, 1-byte SHA mismatch, missing subdir, permission mismatch) | `verify_sync.py` |
| **T-HARN** | Test Harness CLI Orchestration | TC-THN-01 to 05 (Master runner executes all suites and handles flags) | TC-THN-B01 to B05 (Invalid flag, missing python library, exit code 0 on pass, exit code 1 on fail, missing argument) | `verify_all.py` |
| **T-EPHE** | Skyfield Ephemeris Verifier CLI | TC-TEP-01 to 05 (Taipei coordinates, rise/set, culmination, separation) | TC-TEP-B01 to B05 (Missing `de421.bsp`, unknown star, boundary latitude, leap year date, negative elevation) | `verify_ephemeris.py` |
| **T-SCHM** | Schema & Threshold Verifier CLI | TC-TSC-01 to 05 (Individual file validation via `--file` and repo scan) | TC-TSC-B01 to B05 (Corrupted markdown, non-UTF8 encoding, empty file, non-existent path, invalid type argument) | `verify_schemas.py` |
| **T-SYNC** | Workspace Hash Verifier CLI | TC-TSY-01 to 05 (SHA-256 equivalence verification across 55 deliverables) | TC-TSY-B01 to B05 (Worktree missing, downloads missing, single file corrupted, symlink vs real file, empty folder) | `verify_sync.py` |
| **V-GATE** | 100% E2E Victory Gate Audit | TC-VGT-01 to 05 (End-to-end full audit passing with exit code 0) | TC-VGT-B01 to B05 (54/55 files generated, single threshold violation, missing critic review, unverified sky claim, uncommitted change) | `verify_all.py` |

---

## 4. Verification Harness Module Architecture

```
02_製作流程SOP/verification_harness/
├── __init__.py                  # Package exports and version metadata
├── verify_all.py                # Master CLI test runner and colorized summary generator
├── verify_ephemeris.py          # Skyfield astronomical calculation & audit engine
├── verify_schemas.py            # Markdown schema parser and quantitative constraint validator
├── verify_sync.py               # Dual-worktree SHA-256 equivalence & git immutability verifier
└── test_harness_self_check.py   # Unit & fixture regression suite (17 comprehensive test cases)
```

### Module Responsibilities:
1. **`verify_ephemeris.py`**:
   - Computes topocentric Alt/Az, rise, set, and meridian transit times for Taipei (25.03°N, 121.56°E, UTC+8).
   - Validates astronomical claims:
     - `H-七夕`: Vega (25.04 ly), Altair (16.73 ly), angular separation 34.2°, true distance 14.63 ly, Altair culmination at 21:54 CST (Alt 73.91°).
     - `A-13`: Canopus (Suhail) culmination in Taipei = 12.27° (script: 12.3°), Kaohsiung = 14.68° (script: 14.7°).
     - `A-01`: Spica rising in East-Southeast at dusk (~19:47 CST rise, Alt = 2.29° at 20:00 CST).
     - `A-02`: Polaris elevation in Taipei = 24.40° (matching 25.03° latitude).
     - `A-03`: Antares summer transit Alt = 38.48°.
     - `A-06`: Lunar full moon phase timing for Mid-Autumn Festival.
     - `A-14`: Inuit polar constellations (Rigel Alt = 55.87°, Dubhe Alt = 19.32° at midnight).
     - `A-15`: Yule winter solstice Rigel transit Alt = 56.80°.

2. **`verify_schemas.py`**:
   - Parses markdown tables, handles Unicode tokens with diacritics (`ā, ē, ī, ō, ū, ṛ, ʻokina, ʿayn`).
   - Verifies 4 mandatory sections in research files (`04_腳本庫/_審稿/{編號}_考據_gemini.md`).
   - Verifies 3-line summaries and 6-column tables with `🔴/🟡/⚪` in critic files.
   - Enforces English video constraints (`<= 180s`, `<= 2.6 words/sec`, `<= 6 words/card`, `One sky.` formula, `<= 60 char title`).
   - Validates CSV schema and completeness in `06_發布月曆/英文譯名表.csv`.

3. **`verify_sync.py`**:
   - Verifies 100% SHA-256 match for all 55 deliverables between active worktree and `/Users/kimjoo/Downloads/NTNU Insta`.
   - Runs `git status --porcelain 04_腳本庫/*.md` to guarantee zero modification to original scripts.

4. **`verify_all.py`**:
   - Orchestrates all 4 verification suites.
   - Outputs ANSI color-coded terminal matrices.
   - Returns exit code `0` on 100% pass, `1` on any failure or missing deliverable.

5. **`test_harness_self_check.py`**:
   - 17 self-contained unit tests covering tokenizers, boundary cases, validators, and ephemeris calculators.
   - Run via `python3 02_製作流程SOP/verification_harness/verify_all.py --self-test` or `python3 02_製作流程SOP/verification_harness/test_harness_self_check.py`.

---

## 5. Verification Commands

### 1. Run Complete E2E Master Suite
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_all.py"
```

### 2. Run with Verbose Failure Details
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_all.py" -v
```

### 3. Run Self-Check Unit & Fixture Regression Suite
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_all.py" --self-test
```

### 4. Run Standalone Astronomical Ephemeris Verifier
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_ephemeris.py" -v
```

### 5. Validate a Single Specific File
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_schemas.py" --file "04_腳本庫/_審稿/A-01_考據_gemini.md"
```

### 6. Verify Dual-Workspace Sync & Immutability Only
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_sync.py" -v
```
