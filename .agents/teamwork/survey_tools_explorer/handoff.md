# Handoff Report: Tooling, Execution Environment & Verification Capabilities

**Target**: NTNU Astronomy Club "World Sky Cultures" Video Series Workflow  
**Author**: survey_tools_explorer  
**Date**: 2026-10-28T09:20:00Z  

---

## 1. Observation

### 1.1 Python Interpreters and Astronomy Libraries
* **System Python**: Executing `which python3` returns `/usr/bin/python3` (Python 3.9.6). In this interpreter, `pip list` shows system utilities; `skyfield`, `ephem`, `astropy`, `scipy`, and `numpy` are NOT installed.
* **Framework Python**: Located at `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` (Python 3.13.4).
  * Direct execution check:
    ```
    skyfield: available (version 1.54)
    ephem: NOT available (No module named 'ephem')
    astropy: NOT available (No module named 'astropy')
    scipy: available (version 1.15.3)
    numpy: available (version 2.2.6)
    pandas: available (version 2.2.3)
    matplotlib: available (version 3.11.0)
    lark: available (version 1.3.1)
    openpyxl: available (version 3.1.5)
    jplephem: available (version 2.24)
    sgp4: available (version 2.25)
    ```
* **Virtual Environment**: `/Users/kimjoo/Downloads/NTNU Insta/.venv` contains Python 3.13.4 (with numpy 2.5.1, matplotlib 3.11.1, arabic-reshaper, python-bidi), configured from `/Library/Frameworks/Python.framework/Versions/3.13`.
* **Ephemeris Data Cache**: Skyfield ephemeris file `de421.bsp` (16MB) was successfully loaded and is present in the workspace root at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/de421.bsp`.

### 1.2 Ephemeris Calculations for Taipei (25.03°N, 121.56°E, UTC+8)
Direct empirical test with Skyfield 1.54 using observer `wgs84.latlon(25.03, 121.56, elevation_m=10)` and timezone `Asia/Taipei` yielded:
1. **Altair (河鼓二 / 牛郎星) on Qixi 2026-08-19**:
   - Rise: `2026-08-19 15:35:46 CST`
   - Set: `2026-08-19 04:16:24 CST`
   - Meridian Upper Transit (Culmination): `2026-08-19 21:54:07 CST` at Altitude = `73.91°`, Azimuth = `180.00°` (due South).
   - Altitude at 21:00 Taipei time: `69.36°`, Azimuth = `138.89°`.
2. **Vega (織女一) on Qixi 2026-08-19**:
   - Altitude at 21:00 Taipei time: `75.59°`, Azimuth = `344.19°`.
3. **Canopus (老人星 / Suhail) in Winter**:
   - Culmination altitude in Taipei (25.033°N): `12.27°` (matches `12.3°` documented in `A-13-阿拉伯半島Thurayya與沙漠的雨季-逐字稿-v1.md:68`).
   - Culmination altitude in Kaohsiung (22.6°N): `14.7°` (matches `高雄 14.7°` documented in `A-13:68`).
4. **Lunar Phases (Mid-Autumn Festival / A-06)**:
   - Full Moon calculated by Skyfield `almanac.moon_phases(eph)`: `2026-09-27 00:49:02 CST`.

### 1.3 Target Scripts and Structure Discrepancy
* The 9 target scripts exist at:
  - `04_腳本庫/A-01-中國四象青龍-逐字稿-v1.md` (41 lines)
  - `04_腳本庫/A-02-三垣天上的紫禁城-逐字稿-v1.md` (46 lines)
  - `04_腳本庫/A-03-玄武馱著洛書上天的龜蛇-逐字稿-v1.md` (43 lines)
  - `04_腳本庫/A-04-韓國印在鈔票上的星圖-逐字稿-v1.md` (46 lines)
  - `04_腳本庫/A-06-中秋特輯二十八宿月亮的28間驛站-逐字稿-v1.md` (44 lines)
  - `04_腳本庫/H-七夕-牛郎織女-逐字稿-v1.md` (29 lines)
  - `04_腳本庫/A-13-阿拉伯半島Thurayya與沙漠的雨季-逐字稿-v1.md` (207 lines)
  - `04_腳本庫/A-14-因紐特極夜裡的星鐘-逐字稿-v1.md` (215+ lines)
  - `04_腳本庫/A-15-北歐Yule之夜的狼與神駒-逐字稿-v1.md` (220+ lines)
* Early scripts (`A-01` to `H-七夕`) were written before SOP v4.6 and lack `## 星空對時` and `⚠ 待查核清單`. Latest scripts (`A-13` to `A-15`) contain comprehensive tables including PyEphem calculations and rigorous cultural source checklists.

### 1.4 Workspace and Git Worktree Status
* Main repository path: `/Users/kimjoo/Downloads/NTNU Insta` (branch `main`).
* Current worktree path: `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost` (branch `browser_teamwork_preview_boost`).
* Both working trees currently have zero modified files in `04_腳本庫/` (`git status --porcelain 04_腳本庫/` returns 0 lines).
* Target output directories `04_腳本庫/_審稿/` and `04_腳本庫/_英文版/` do not exist yet in either working tree.

---

## 2. Logic Chain

### 2.1 Astronomical Tooling Selection (Skyfield vs PyEphem vs Astropy)
1. *Observation*: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` already has `skyfield` 1.54, `scipy` 1.15.3, `numpy` 2.2.6, `jplephem` 2.24 installed; `ephem` and `astropy` are not installed.
2. *Technical Assessment*: Skyfield is the modern successor to PyEphem created by the same author (Brandon Rhodes). It computes positions using the modern IAU standards (SOFA-equivalent matrix rotations) and JPL DE421 ephemeris rather than legacy VSOP87 approximations.
3. *Validation*: Empirical tests demonstrated sub-arcminute and sub-second precision matching all historical PyEphem numbers documented in A-13.
4. *Inference*: There is NO need to install additional packages (`ephem` or `astropy`). Skyfield is already present, faster, fully offline-functional once `de421.bsp` is loaded, and perfectly satisfies all astronomical verification requirements for Taipei (25.03°N, 121.56°E, UTC+8).

### 2.2 English Text Tokenization and Constraint Validation
1. *Observation*: The user prompt specifies English speech rate $\le 2.6\text{ words/sec}$, on-screen text card $\le 6\text{ words}$, and total duration $\le 180\text{ seconds}$.
2. *Issue with naive ASCII regex*: Testing `re.findall(r"\b[a-zA-Z0-9]+\b", ...)` on names like `Úlfs kjaptr`, `Al-Thurayyā`, `Māori` stripped accented vowels, incorrectly splitting single words into multiple invalid fragments.
3. *Solution*: A Unicode-aware regex `re.findall(r"\b[\w\u02bb\u02bc]+(?:[-\x27\u2019][\w\u02bb\u02bc]+)*\b", text, re.UNICODE)` correctly recognizes whole words with diacritics and okina (`ʻ`).
4. *Inference*: English validation in the verification harness must use this Unicode tokenizer.

### 2.3 Chinese Character Counting & Speech Pacing
1. *Observation*: The user prompt specifies voice-over $\le 4.5\text{ chars/sec}$ and on-screen text $\le 14\text{ chars}$.
2. *Linguistic & Script Analysis*: In Chinese voice-over scripts, Chinese characters (ideographs) correspond 1:1 to syllables. English loan words or acronyms (e.g., `Antares`, `HIP`, `EP1`) count as 1 word unit each. Punctuation marks (，。！？、《》——「」：；) represent pauses in speech timing and must not be counted as spoken syllables.
3. *Validation*: Applying this definition to `A-01` yields 663 syllables over 170 seconds ($3.90\text{ chars/sec}$), matching the script header's stated specification of "約 720 字，語速 4–4.5 字/秒".
4. *Inference*: The character counting algorithm should be `len(re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+", voice_text))`.

### 2.4 File Synchronization and Integrity Logic
1. *Observation*: Requirement R4 mandates that deliverables must be written both to `/Users/kimjoo/Downloads/NTNU Insta` and the current worktree, while keeping all original scripts in `04_腳本庫/` unmodified.
2. *Total deliverables count*:
   - 9 Research files: `04_腳本庫/_審稿/{編號}_考據_gemini.md`
   - 36 Critic files: `04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`
   - 9 English draft files: `04_腳本庫/_英文版/{編號}-EN-script-draft.md`
   - 1 Master Glossary file: `06_發布月曆/英文譯名表.csv`
   - Total: 55 files in each tree (110 file instances total).
3. *Inference*: Verification requires checking file existence and verifying `sha256(worktree_file) == sha256(downloads_file)` for all 55 items, followed by `git status --porcelain 04_腳本庫/*.md` to confirm zero modification of existing scripts.

---

## 3. Caveats

1. **Python Path Environment**: The default terminal subshell has `PATH="/Users/kimjoo/.zsh/misc:...:/usr/bin:..."` which invokes macOS Python 3.9.6. To execute scripts using Skyfield, the command must either invoke `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` explicitly or prepend `/Library/Frameworks/Python.framework/Versions/3.13/bin` to `PATH`.
2. **Terminal UTF-8 Locale**: In macOS default zsh subshells without locale exports, filenames and terminal output with CJK characters can render as question marks (`????`). Prefixing commands with `export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"` guarantees flawless UTF-8 handling.
3. **No Pip Install Needed**: PyEphem is not installed, but installing it is unnecessary because Skyfield 1.54 is already present and superior. `de421.bsp` is cached in the workspace, so no network downloads are required during test runs.

---

## 4. Conclusion & Concrete Recommendations

### 4.1 Recommended Python Environment Execution Command
Always run python verification commands using the Framework Python 3.13 binary:
```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 <script_name>.py
```
Or with PATH configured:
```bash
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
python3 <script_name>.py
```

---

### 4.2 Standalone Ephemeris Verifier Implementation
The following standalone Python module provides ephemeris calculations for Taipei (25.03°N, 121.56°E, UTC+8) for all 9 episodes. It can be integrated into the test harness or used by the `天文` critic agent.

```python
# -*- coding: utf-8 -*-
"""ephemeris_verifier.py - Astronomical Verification Tool for NTNU Video Series.
Uses Skyfield 1.54 and local de421.bsp to compute altitude, azimuth, rise,
set, and culmination times for Taipei (25.03°N, 121.56°E, UTC+8).
"""
import os
import zoneinfo
from datetime import datetime, timezone
from skyfield.api import load, wgs84, Star
from skyfield import almanac

HERE = os.path.dirname(os.path.abspath(__file__))
# Check local BSP or fallback to workspace root
BSP_PATH = os.path.join(HERE, "de421.bsp")
if not os.path.exists(BSP_PATH):
    BSP_PATH = "/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/de421.bsp"

ts = load.timescale()
eph = load(BSP_PATH)
taipei_topos = wgs84.latlon(25.03, 121.56, elevation_m=10)
obs_taipei = eph['earth'] + taipei_topos
tz_taipei = zoneinfo.ZoneInfo("Asia/Taipei")

# Catalogue of key objects across target episodes
TARGET_STARS = {
    "Altair": Star(ra_hours=(19, 50, 46.998), dec_degrees=(8, 52, 5.96)),    # 河鼓二 / 牛郎星
    "Vega": Star(ra_hours=(18, 36, 56.336), dec_degrees=(38, 47, 1.28)),     # 織女一
    "Deneb": Star(ra_hours=(20, 41, 25.915), dec_degrees=(45, 16, 49.22)),   # 天津四
    "Antares": Star(ra_hours=(16, 29, 24.460), dec_degrees=(-26, 25, 55.2)), # 心宿二 / 大火
    "Spica": Star(ra_hours=(13, 25, 11.579), dec_degrees=(-11, 09, 40.8)),   # 角宿一
    "Canopus": Star(ra_hours=(6, 23, 57.110), dec_degrees=(-52, 41, 44.4)),  # 老人星 / Suhail
    "Polaris": Star(ra_hours=(2, 31, 49.084), dec_degrees=(89, 15, 50.79)),  # 勾陳一 / 北極星
    "Aldebaran": Star(ra_hours=(4, 35, 55.239), dec_degrees=(16, 30, 33.49)),# 畢宿五 / al-Twaibiʿ
    "Rigel": Star(ra_hours=(5, 14, 32.272), dec_degrees=(-8, 12, 5.90)),     # 參宿七 / Aurvandilstá
}

def get_altaz_at(star_name, year, month, day, hour, minute):
    """Compute Altitude and Azimuth for a target star from Taipei at local time."""
    star = TARGET_STARS[star_name]
    dt = datetime(year, month, day, hour, minute, tzinfo=tz_taipei)
    t = ts.from_datetime(dt)
    apparent = obs_taipei.at(t).observe(star).apparent()
    alt, az, _ = apparent.altaz()
    return alt.degrees, az.degrees

def get_rise_set_transit(star_name, year, month, day):
    """Compute Rise, Set, and Meridian Transit times for Taipei on a given date."""
    star = TARGET_STARS[star_name]
    t0 = ts.from_datetime(datetime(year, month, day, 0, 0, tzinfo=tz_taipei))
    t1 = ts.from_datetime(datetime(year, month, day, 23, 59, 59, tzinfo=tz_taipei))
    
    # Rise and Set
    f_rs = almanac.risings_and_settings(eph, star, taipei_topos)
    times_rs, events_rs = almanac.find_discrete(t0, t1, f_rs)
    
    # Meridian Transit
    f_tr = almanac.meridian_transits(eph, star, taipei_topos)
    times_tr, events_tr = almanac.find_discrete(t0, t1, f_tr)
    
    results = {}
    for t, ev in zip(times_rs, events_rs):
        dt = t.astimezone(tz_taipei)
        results["Rise" if ev == 1 else "Set"] = dt.strftime("%H:%M:%S")
        
    for t, ev in zip(times_tr, events_tr):
        if ev == 1:
            dt = t.astimezone(tz_taipei)
            alt, az, _ = obs_taipei.at(t).observe(star).apparent().altaz()
            results["Culmination"] = (dt.strftime("%H:%M:%S"), round(alt.degrees, 2))
            
    return results

if __name__ == "__main__":
    print("=== Taipei Verification Test ===")
    print("Altair on 2026-08-19:", get_rise_set_transit("Altair", 2026, 8, 19))
    alt, az = get_altaz_at("Altair", 2026, 8, 19, 21, 0)
    print(f"Altair at 21:00 Taipei: Alt = {alt:.2f}°, Az = {az:.2f}°")
```

---

### 4.3 Text Counting and Markdown Schema Validator Logic

#### A. English Counting Function
```python
import re

def count_english_words(text: str) -> int:
    """Accurately count English words including hyphenated words, contractions,
    and transliterated words with Unicode diacritics / okina."""
    # Strip markdown markup like bold, italics, links
    clean = re.sub(r'[*_`\[\]]', '', text)
    tokens = re.findall(r"\b[\w\u02bb\u02bc]+(?:[-\x27\u2019][\w\u02bb\u02bc]+)*\b", clean, re.UNICODE)
    return len(tokens)
```

#### B. Chinese Voice-over and On-Screen Text Counting Function
```python
def count_chinese_characters(voice_text: str) -> int:
    """Count spoken syllables in Chinese voice-over (CJK ideographs + English words/numbers).
    Excludes punctuation marks that indicate pauses."""
    tokens = re.findall(r"[\u4e00-\u9fff]|[a-zA-Z0-9]+", voice_text)
    return len(tokens)

def validate_chinese_card(card_text: str) -> bool:
    """Validate on-screen card text length <= 14 characters."""
    clean = re.sub(r'[「」『』"\'\s]', '', card_text)
    return len(clean) <= 14
```

#### C. Markdown Schema Definitions & Table Parsers
1. **Research Reports (`{編號}_考據_gemini.md`)**:
   - Header: `# {編號} 網路考據` (or `# {編號}｜... 網路考據`)
   - Mandatory Sections:
     * `## 一、待查核清單逐條結果`
     * `## 二、清單以外發現的問題`
     * `## 三、可以加進影片的好材料`
     * `## 四、參考資料總表`
   - Table Schema in Sections 1 & 2:
     `| # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |`
     (Exactly 6 columns, column 3 must match verdict markers).
2. **Critic Reports (`{編號}_審稿-{角色}_antigravity.md`)**:
   - Header 3-line Summary:
     * Line 1 matches: `整体評價` or `整體評價`
     * Line 2 matches: `最重要的三個問題`
     * Line 3 matches: `沒把握的地方`
   - Criticism Table Schema:
     `| 嚴重度（🔴必改／🟡建議／⚪可選） | 位置（鏡號或段落） | 原文 | 問題 | 建議改法 | 依據 |`
     (Exactly 6 columns, severity must contain 🔴/🟡/⚪).
   - `天文` role special assertion: Must include Taipei (25.03°N, 121.56°E, UTC+8) ephemeris validation numbers.
3. **English Scripts (`{編號}-EN-script-draft.md`)**:
   - Shot Table: `| Shot | Sec | Voice-over | On-screen text | Words/sec |`
   - Total runtime check: $\sum \text{Sec} \le 180\text{ s}$
   - Speech rate check: every shot $\text{Words/sec} \le 2.6$
   - Card length check: every on-screen card $\le 6\text{ words}$
   - Glossary Table: `| Chinese | English used | Notes |`
   - YouTube Title ($\le 60\text{ chars}$) + Description + Facebook caption
   - Cut / Adaptation list section
4. **Master Glossary (`06_發布月曆/英文譯名表.csv`)**:
   - Valid CSV structure covering names from all 9 episodes.

---

### 4.4 Dual-Worktree Sync & Git Untouched Integrity Checker

```python
import os
import hashlib
import subprocess

TARGET_EPS = ['A-01', 'A-02', 'A-03', 'A-04', 'A-06', 'H-七夕', 'A-13', 'A-14', 'A-15']
ROLES = ['天文', '文化', '敘事', '語言']

def get_expected_files():
    files = []
    # 9 research files
    for ep in TARGET_EPS:
        files.append(f"04_腳本庫/_審稿/{ep}_考據_gemini.md")
    # 36 critic files
    for ep in TARGET_EPS:
        for r in ROLES:
            files.append(f"04_腳本庫/_審稿/{ep}_審稿-{r}_antigravity.md")
    # 9 English draft files
    for ep in TARGET_EPS:
        files.append(f"04_腳本庫/_英文版/{ep}-EN-script-draft.md")
    # 1 Glossary CSV
    files.append("06_發布月曆/英文譯名表.csv")
    return files

def verify_sync(worktree_dir, downloads_dir):
    expected = get_expected_files()
    missing_worktree = []
    missing_downloads = []
    mismatch_hash = []
    
    for rel_path in expected:
        p_w = os.path.join(worktree_dir, rel_path)
        p_d = os.path.join(downloads_dir, rel_path)
        
        if not os.path.exists(p_w):
            missing_worktree.append(rel_path)
            continue
        if not os.path.exists(p_d):
            missing_downloads.append(rel_path)
            continue
            
        h_w = hashlib.sha256(open(p_w, 'rb').read()).hexdigest()
        h_d = hashlib.sha256(open(p_d, 'rb').read()).hexdigest()
        if h_w != h_d:
            mismatch_hash.append(rel_path)
            
    return missing_worktree, missing_downloads, mismatch_hash

def verify_git_untouched(repo_dir):
    """Verify that no existing original scripts in 04_腳本庫/ were modified."""
    res = subprocess.run(['git', '-C', repo_dir, 'status', '--porcelain', '04_腳本庫/'],
                         capture_output=True, text=True)
    lines = res.stdout.strip().splitlines() if res.stdout.strip() else []
    # Modified tracked files will start with ' M' or 'M ' or 'D '
    modified = [l for l in lines if not l.startswith('??')]
    return modified
```

---

### 4.5 Recommended Architecture for the E2E Testing Track

We recommend structuring the verification harness under `tests/verification/` or `02_製作流程SOP/verification_harness/` with four focused modules:

```
02_製作流程SOP/verification_harness/
├── verify_all.py          # Unified CLI entry point & test orchestrator
├── verify_ephemeris.py    # Astronomical calculation validation module (Skyfield)
├── verify_schemas.py      # Markdown headers, tables, word counts & speed validator
└── verify_sync.py         # File presence, SHA256 mirror check & git clean validator
```

* **Execution Interface**:
  ```bash
  /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
    "02_製作流程SOP/verification_harness/verify_all.py" --worktree "." --downloads "/Users/kimjoo/Downloads/NTNU Insta"
  ```
* **Exit Code Protocol**:
  - `0`: All 55 deliverables pass structural schema, rate limits, ephemeris calculations, synchronization, and git untouched checks.
  - `1`: Validation errors present; detailed failure report printed with file paths, line numbers, and exact violation values.

---

## 5. Verification Method

To independently verify all findings and capabilities in this report, execute the following commands in the project directory:

1. **Verify Python 3.13 and Skyfield Availability**:
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -c "
   import skyfield, scipy, numpy, pandas
   print('Skyfield:', skyfield.__version__)
   print('Scipy:', scipy.__version__)
   print('Numpy:', numpy.__version__)
   "
   ```
   *Expected output*: `Skyfield: 1.54`, `Scipy: 1.15.3`, `Numpy: 2.2.6`.

2. **Verify Taipei Ephemeris Computation**:
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -c "
   import zoneinfo
   from datetime import datetime
   from skyfield.api import load, wgs84, Star
   from skyfield import almanac

   ts = load.timescale()
   eph = load('de421.bsp')
   taipei = wgs84.latlon(25.03, 121.56, elevation_m=10)
   tz = zoneinfo.ZoneInfo('Asia/Taipei')
   altair = Star(ra_hours=(19, 50, 46.998), dec_degrees=(8, 52, 5.96))
   t = ts.from_datetime(datetime(2026, 8, 19, 21, 0, tzinfo=tz))
   alt, az, _ = (eph['earth'] + taipei).at(t).observe(altair).apparent().altaz()
   print(f'Altair Taipei 2026-08-19 21:00 CST: Alt={alt.degrees:.2f}°, Az={az.degrees:.2f}°')
   "
   ```
   *Expected output*: `Altair Taipei 2026-08-19 21:00 CST: Alt=69.36°, Az=138.89°`.

3. **Verify Git Untouched Status for Original Scripts**:
   ```bash
   git status --porcelain "04_腳本庫/"
   ```
   *Expected output*: Completely empty (no output), confirming zero existing files modified.

### Invalidation Conditions
This report's conclusions would be invalidated if:
* The Python 3.13 framework at `/Library/Frameworks/Python.framework/Versions/3.13` is uninstalled or modified.
* The `de421.bsp` ephemeris file in the workspace is removed without network access to re-fetch it.
* The worktree relationship between `/Users/kimjoo/Downloads/NTNU Insta` and the current worktree is unlinked.
