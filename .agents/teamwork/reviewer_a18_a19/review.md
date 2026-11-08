# Batch 2 Round 2 Remediation Review Report: A-18 & A-19

**Reviewer**: Reviewer 2 (A-18 & A-19 Remediation Reviewer)  
**Roles**: Reviewer, Adversarial Critic  
**Date**: 2026-11-01  
**Scope**: 10 Review Files in `04_腳本庫/_審稿/` for Episodes A-18 (Ancient Egypt Sirius) and A-19 (Ancient Arabic Canopus & Ostriches).  
**Explicit Verdict**: **REQUEST_CHANGES**

---

## 1. Executive Summary & Verdict Rationale

| Dimension | Assessment | Status |
|---|---|---|
| **Provenance & Anti-Hallucination** | 9 of 10 files fully compliant; 1 file retains unverified external book page numbers | **FAIL** (1 Critical Finding) |
| **Section 2 Format Compliance** | Exactly 0 `✓ 證實` rows in both A-18 & A-19 考據 (§2 strictly contains `✗`, `⚠`) | **PASS** |
| **A-18 Specific Invariants** | 2027/01/25 Sirius timeline (8-min shift) documented; Shot 01 opening formula protected | **PASS** |
| **A-19 Specific Invariants** | Canopus atmospheric refraction timing updated to `⚪可選`; "人" preserved in Shot 01 | **PASS** |
| **Schema Validation** | All 10 files pass `verify_schemas.py` with 100% compliance | **PASS** |
| **Ephemeris Calculations** | Skyfield 1.54 + JPL DE421 ephemeris verification completely passed | **PASS** |
| **Dual-Workspace Synchronization** | Worktree and `/Users/kimjoo/Downloads/NTNU Insta/` currently match SHA-256 byte-for-byte | **PASS** (pre-remediation) |
| **Original Script Immutability** | `git status` confirms zero modifications to existing tracked scripts in `04_腳本庫/` | **PASS** |

### **Verdict**: **REQUEST_CHANGES**
**Reason**: While 9 out of 10 files and nearly all astronomical, narrative, and linguistic requirements have been implemented with exemplary rigor, an adversarial audit revealed that **`04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md` (line 17) retains guessed page numbers (`p. 31` and `pp. 243–250`) for two external books not present in `07_資料來源/` (Émile Chassinat 1897 and Juan Antonio Belmonte 2009)**. 

In `A-18_考據_gemini.md` (Row 5 & Section 4), these exact same works were correctly recognized as external and marked `（未核頁碼）`. Furthermore, the automated test script `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py` failed to detect this violation because its `external_authors` list lacked `Chassinat` and `Belmonte`. Under strict integrity guidelines, work with unverified guessed citations must NOT be approved regardless of automated test scores.

---

## 2. Findings

### [Critical] Finding 1: INTEGRITY VIOLATION / PROVENANCE DEFECT — Unremediated Guessed Page Numbers in A-18 文化審稿
- **What**: Line 17 of `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md` cites external books with specific guessed page numbers:
  `Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250`
- **Where**: 
  - `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md:17`
  - `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md:17`
- **Why**: 
  1. Neither Émile Chassinat's *Le Temple d'Edfou* nor Juan Antonio Belmonte's *In Search of Cosmic Order* exists as primary textual material in `07_資料來源/` (the local directory contains only `egyptian_star_chart.rtf`).
  2. The mandate in `ORIGINAL_REQUEST.md` (## 2026-10-31T21:03:02Z, Item 1) and the dispatch instructions explicitly order that for all external books not in `07_資料來源/`, guessed page numbers must be removed and marked `（未核頁碼）`.
  3. In `04_腳本庫/_審稿/A-18_考據_gemini.md` (line 13, Row 5 and lines 69, 78 in Section 4), both Chassinat and Belmonte are correctly cited as `（未核頁碼）`. Retaining `p. 31` and `pp. 243–250` in the cultural review file creates an internal contradiction and represents an unverified provenance claim.
  4. The automated verification script `verify_batch2_r2_rules.py` had a blind spot in `check_external_pages()` because `external_authors` lacked `Chassinat` and `Belmonte`.
- **Required Action**: 
  In `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md` (and the synchronized Downloads file), replace line 17's citation:
  ```markdown
  | Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II（未核頁碼）；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*（未核頁碼） |
  ```
  Also update `verify_batch2_r2_rules.py` to include `Chassinat` and `Belmonte` in `external_authors`.

---

## 3. Detailed Verification of Requirements

### 3.1 Provenance & Anti-Hallucination Audit
1. **`A-18_考據_gemini.md`**:
   - Censorinus (21.10; 未核頁碼), Parker 1950 (未核頁碼), Neugebauer & Parker 1960/1969 (未核頁碼), Hurst 1952 (未核頁碼), Ball 1939 (未核頁碼), Petrie 1883 (未核頁碼), Dorner 1981 (未核頁碼), Lehner 1997 (未核頁碼), Chassinat 1897 (未核頁碼), Belmonte & Shaltout 2009 (未核頁碼), Buchwald & Josefowicz 2010 (未核頁碼), Champollion 1822 (未核頁碼), Erman & Grapow 1930 (未核頁碼), Gardiner 1957 (未核頁碼), Wilkinson 2010 (未核頁碼), Sethe 1908 (未核頁碼), Edwards 1993 (未核頁碼), Gantenbrink 1997 (未核頁碼), Bauval & Gilbert 1994 (未核頁碼), Budge 1904 (未核頁碼), Assmann 2005 (未核頁碼), Cauville 1997 (未核頁碼), Leitz 2002 (未核頁碼).
   - Journal papers (Schaefer 2000 JHA, Cauville & Aubourg 1995 BIFAO, Aubourg 1995 BIFAO, Belmonte 2001 JHA, Trimble 1964 MIOB, Roth 1993 JEA, Symons 2015 JHA) properly cite journal volume and page range.
   - Status: **PASSED**
2. **`A-18_審稿-天文_antigravity.md`**:
   - Cites Skyfield, JPL DE421, Capitaine et al. 2003, Schaefer 2000, Neugebauer & Parker 1960, Gantenbrink 1997 without guessed pages.
   - Status: **PASSED**
3. **`A-18_審稿-文化_antigravity.md`**:
   - Lines 15-16 properly mark `EAT III（未核頁碼）`, `Assmann 2001（未核頁碼）`, `Parker 1950（未核頁碼）`, `Gardiner 1957（未核頁碼）`.
   - Line 17 retains `Chassinat p. 31` and `Belmonte pp. 243–250`.
   - Status: **FAILED** (See Finding 1)
4. **`A-18_審稿-敘事_antigravity.md` & `A-18_審稿-語言_antigravity.md`**:
   - Fully compliant with SOP standards; zero external book hallucinations.
   - Status: **PASSED**
5. **`A-19_考據_gemini.md`**:
   - All external Arabic & Western works (Ibn Durayd 1987, Ibn Manzur, Ibn al-Jawzi, Ibn Hibban, Lane 1863, Kunitzsch 1961, Kunitzsch & Smart 2006, Ibn Qutayba 1956, al-Sufi 2021, Diwan Umar ibn Abi Rabi'a) have guessed page numbers removed and marked `（未核頁碼）`.
   - The contradictory pattern "guessed page + 未核頁碼" has been completely eliminated.
   - Status: **PASSED**
6. **`A-19_審稿-{天文,文化,敘事,語言}_antigravity.md`**:
   - All citations in 審稿-天文, 審稿-文化, 審稿-敘事, 審稿-語言 are clean; external books cited with `（未核頁碼）`.
   - Status: **PASSED**

---

### 3.2 Section 2 Format Compliance (`## 二、清單以外發現的問題`)
- **Rule**: Section 2 must strictly contain `✗`, `⚠`, `？` and ZERO `✓ 證實` rows.
- **Audit Results**:
  - `A-18_考據_gemini.md`: 6 rows total (1 `✗ 錯誤`, 5 `⚠ 部分正確或需限定`, 0 `✓ 證實`).
  - `A-19_考據_gemini.md`: 3 rows total (3 `⚠ 部分正確或需限定`, 0 `✓ 證實`).
- Status: **PASSED**

---

### 3.3 Episode-Specific Invariants Audit

#### A-18 (Ancient Egypt Sirius & Nile Inundation)
1. **Taipei 2027/01/25 Sirius Timeline (8-min shift)**:
   - Evaluated in `A-18_考據_gemini.md` Section 2 Row 6:
     *Verified: 16:52 CST rise -> 21:00 CST alt 43.7° (az 152.5°) -> 22:21 CST culmination alt 48.2° -> 03:51 CST set (accounting for 7.9 min shift over 2 days).*
   - Included in `A-18_審稿-天文_antigravity.md` (header line 4, table item 1 line 13, and report lines 39–44).
   - Status: **PASSED**
2. **Shot 01 Opening Formula Protection**:
   - `A-18_審稿-敘事_antigravity.md` explicitly mandates:
     *"開場白「同一片星空，古埃及人看見——一顆叫醒尼羅河的星」文字必須一字不差完整保留，嚴禁在定式前添加任何自創句子！... 正確做法是將固定定式移至全片第一句破題，隨後再銜接轉場..."*
   - Status: **PASSED**

#### A-19 (Ancient Arabic Canopus & Ostriches)
1. **Canopus Atmospheric Refraction Timing**:
   - Refracted transit on 2027/01/29 in Taipei verified by Skyfield: 18:11 CST rise -> 21:44 CST culmination (12.3°) -> 01:17 CST set.
   - In `A-19_審稿-天文_antigravity.md` (Row 4, line 16), the critique was revised from a defect to a `⚪可選` note confirming that the script's `18:10` rise and `01:17` set times are physically accurate when including -34' atmospheric refraction.
   - Status: **PASSED**
2. **Shot 01 Opening Formula Protection ("人" Retention)**:
   - `A-19_審稿-敘事_antigravity.md` (Row 2, line 14) explicitly states:
     *"依系列統一定式規範，「同一片星空，古阿拉伯人看見——」必須一字不差完整保留，絕不可更動「人」字！"*
   - Status: **PASSED**

---

### 3.4 Verification Tooling & Empirical Reproduction

1. **Automated Rules Verifier (`verify_batch2_r2_rules.py`)**:
   - Result: Reported `PASS` across all 7 checks.
   - Adversarial finding: Revealed an incomplete author filter list that masked Finding 1.
2. **Batch 2 Ephemeris Rigorous Audit (`verify_batch2_ephemeris.py`)**:
   - Result: All astronomical claims (A-16 Canopus/Alkaid, A-17 Pleiades/Big Dipper, A-18 Sirius/Full Moon/Precession, A-19 Canopus/Galactic coords/Distances/Fluxes) verified 100% reproducible with Skyfield 1.54 + JPL DE421.
3. **Schema Validator (`verify_schemas.py`)**:
   - Result: All 10 files for A-18 and A-19 passed schema and metric validation.
4. **Dual Workspace SHA-256 Synchronization**:
   - Result: All 10 files matched identically between `04_腳本庫/_審稿/` and `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`.

---

## 4. Required Remediation Steps

The worker agent (`worker_batch2_r2`) must perform the following actions:

1. **Modify `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md`**:
   In row 5 of the review table (line 17), update the `依據` column to remove `p. 31` and `pp. 243–250`, replacing them with `（未核頁碼）`:
   ```markdown
   | ⚪可選 | 14 鏡 | 後來的神廟牆上就寫著：國王跟女神拉起繩子定位，眼睛看著那條牛腿，立下神廟的四個角。 | 神廟拉繩奠基儀式（pḏ šs）與塞夏特女神（Seshat）。在托勒密王朝埃德富神廟與丹德拉神廟奠基銘文中，法老並非孤身測量，而是與頭頂七芒星智慧神符的文字與丈量女神塞夏特共同牽引金線繩索。此儀式最早可追溯至第二王朝卡塞凱姆威（Khasekhemwy，約前 2700 年）之石刻浮雕，展現了埃及王權「以天度地、依星建廟」延續近三千年的崇高聖神信仰。 | 維持原旁白；首留言引錄埃德富銘文法老祈禱詞：「我握木槌、執木樁，與塞夏特共牽準繩；我的雙眼緊盯北斗牛腿，於星光下奠定四方殿角。」 | Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II（未核頁碼）；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*（未核頁碼） |
   ```

2. **Synchronize to Downloads Workspace**:
   Sync the updated `A-18_審稿-文化_antigravity.md` to `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md` and verify identical SHA-256.

3. **Enhance Verification Script**:
   In `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py`, append `"Chassinat"` and `"Belmonte"` to `external_authors` in `check_external_pages()` to prevent future regression.

---

## 5. Conclusion
Upon completion of the above single-line remediation and synchronization, all 10 files for A-18 and A-19 will achieve 100% full compliance across all requirements. Until this remediation is applied, the verdict remains **REQUEST_CHANGES**.
