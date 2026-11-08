# Deep Dive Analysis: Check 5 Failure in Rule Verifier Script & Comprehensive Patch

**Agent**: Explorer It2-2 (Rule Verifier Script Explorer)  
**Date**: 2026-11-01  
**Working Directory**: `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/explorer_it2_2`  
**Target Script**: `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py`  
**Target Bug File**: `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md:17`

---

## 1. Executive Summary

During Round 2 remediation verification for Batch 2 (`A-16`, `A-17`, `A-18`, `A-19`), Reviewer 2 discovered that `A-18_審稿-文化_antigravity.md:17` verbatim contained unverified, guessed book citations:
```markdown
| ⚪可選 | 14 鏡 | 後來的神廟牆上就寫著：國王跟女神拉起繩子定位，眼睛看著那條牛腿，立下神廟的四個角。 | ... | 維持原旁白；首留言引錄埃德富銘文法老祈禱詞... | Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250 |
```
Despite this blatant violation of `ORIGINAL_REQUEST.md` (2026-10-31T21:03:02Z, Item 1), running the automated verifier `verify_batch2_r2_rules.py` reported:
```
OVERALL RESULT: ALL BATCH 2 R2 REMEDIATION CHECKS PASSED
```

This investigation identified the exact technical reasons why Check 5 (`check_external_pages`) failed to flag the issue, audited all 20 delivery files across the workspace, and formulated a comprehensive, battle-tested patch that strictly detects lingering guessed pages, contradictory `pp. 123... 未核頁碼` patterns, and Roman numeral volumes, while correctly preserving legitimate peer-reviewed journal article pagination and verified local sources.

---

## 2. Root Cause Analysis: Why Check 5 Failed

Examination of lines 111–134 in `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py` revealed four distinct defects:

### Defect 1: Hardcoded Author Whitelist Blindspot
In `verify_batch2_r2_rules.py:113-120`, the `external_authors` list was defined as:
```python
external_authors = [
    "Toelken", "Haile", "Griffin-Pierce", "Kluckhohn", "Young &", "Young and", "Jayne",
    "Newcomb", "Witherspoon", "Matthews", "Chamberlain", "Schaafsma", "IEI",
    "Frantz", "Russell", "Censorinus", "Parker", "Neugebauer", "Hurst", "Ball", "Petrie",
    "Buchwald", "Josefowicz", "Sethe", "Allen", "Otto", "Ibn Qutayba", "al-Sufi", "al-Ṣūfī",
    "Ibn Durayd", "Ibn Manzur", "Ibn Manẓūr", "Ibn al-Jawzi", "Ibn al-Jawzī", "Ibn Hibban",
    "Ibn Ḥibbān", "Kunitzsch", "Smart", "Lane"
]
```
- **"Chassinat"** (Émile Chassinat, *Le Temple d'Edfou*) was **completely missing**.
- **"Belmonte"** (Juan Antonio Belmonte, *In Search of Cosmic Order*) was **completely missing**.
- **"Umar ibn Abi Rabi'a" / "Rabīʿa"** was missing.
- **"Wissler 1911/1912"** (Clark Wissler's external monographs, distinct from Wissler & Duvall 1908 in `07_資料來源/`) was missing.
- Other external authors mentioned in the reviews/texts (`Assmann`, `Gardiner`, `Gantenbrink`, `Bauval`, `Gilbert`, `Edwards`, `Lehner`, `Dorner`, `Dorsey`, `Radin`) were missing.

Because the verification loop was `for author in external_authors:`, neither `Chassinat` nor `Belmonte` was ever evaluated against any regex.

### Defect 2: Regex Volume Limitation (`\d+` vs Roman Numerals)
In `verify_batch2_r2_rules.py:130`:
```python
matches = re.findall(rf"({author}[^|\n]*?(?:pp?\.?\s*\d+|vol\.\s*\d+[^|\n]*?p\.?\s*\d+))", c, re.IGNORECASE)
```
The volume regex strictly required Arabic digits: `vol\.\s*\d+`. In classical humanities and Egyptology (e.g. Chassinat's *Le Temple d'Edfou*), volume numbers are frequently designated with Roman numerals (`Vol. II`, `Vol. I`, `Tome II`, `Band I`). Any volume-based pattern checking `vol\.\s*\d+` would fail to match `Vol. II, p. 31`.

### Defect 3: Incomplete Logic & Dead Comment for Contradiction Detection
In `verify_batch2_r2_rules.py:132`:
```python
for m in matches:
    # Ignore if it contains '未核頁碼' and no guessed page numbers
    findings.append(f"[{fname}] Guessed page number for external author '{author}': {m.strip()}")
```
The developer placed a comment `# Ignore if it contains '未核頁碼' and no guessed page numbers` but did not implement the logic. Crucially, `ORIGINAL_REQUEST.md` (2026-10-31T21:03:02Z, Item 1) strictly mandated:
> 「一律移除推測的頁碼數字（如 pp. 45–48、vol. 1, p. 488 等），直接標註「（未核頁碼）」！切勿出現「既寫出猜測頁碼 p. 488 又在後面寫 未核頁碼」的自相矛盾寫法。」

The script had zero logic to detect the **contradictory pattern** where a citation retains page numbers *and* adds `未核頁碼` (e.g. `Author, p. 488（未核頁碼）`).

### Defect 4: Semicolon / Cell Boundary Bleeding
In markdown tables (especially in 考據 and 審稿 tables), table cells often bundle multiple citations separated by semicolons (`;` or `；`), such as:
```markdown
Childrey (2004) pp. 37–39; Gary Witherspoon (1977)（未核頁碼）
```
or
```markdown
Virginia Trimble (1964), "Astronomical Investigation...", *MIOB*, 10, pp. 183–187; Rudolf Gantenbrink (1997), *The Upuaut Project*（未核頁碼）
```
If a regex operates over `[^|\n]*` without splitting citations by semicolons, a verified local source's page numbers (e.g. Childrey) or a journal article's pagination (e.g. Trimble) will bleed into adjacent external author citations on the same line, producing false positives or incorrect matching boundaries.

---

## 3. Comprehensive Audit Across All 20 Files

An exhaustive programmatic scan of all 20 delivery files (`A-16`, `A-17`, `A-18`, `A-19` across 考據 and 4 審稿 roles) was conducted using our enhanced parser.

### Audit Findings:
1. **Lingering Guessed Page Numbers (Error Mode A)**:
   - **`04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md:17`**:
     - `Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31` -> **VIOLATION** (Guessed page `Vol. II, p. 31`).
     - `Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250` -> **VIOLATION** (Guessed page `pp. 243–250`).
   - **All other 19 files**: **0 VIOLATIONS**.
2. **Contradictory Patterns `pp. 123... 未核頁碼` (Error Mode B)**:
   - **All 20 files**: **0 VIOLATIONS**. No file exhibited the contradictory pattern where guessed pages were retained prior to `未核頁碼`.
3. **Journal Article Pagination**:
   - The following academic journal articles possess legitimate peer-reviewed volume and page spans, which were verified and correctly preserved without false-positive flagging:
     - Bradley E. Schaefer (2000), *JHA*, 31(2), pp. 149–155 (`A-18_考據_gemini.md:9, 73`)
     - Juan Antonio Belmonte (2001), *JHA*, 32, pp. S1–S20 (`A-18_考據_gemini.md:20, 68`)
     - Sarah Symons (2015), *JHA*, 46(2), pp. 203–224 (`A-18_考據_gemini.md:15`)
     - Sylvie Cauville & Éric Aubourg (1995), *BIFAO*, 95, pp. 251–284 (`A-18_考據_gemini.md:16, 70`)
     - Éric Aubourg (1995), *BIFAO*, 95, pp. 1–10 (`A-18_考據_gemini.md:16, 71`)
     - Ann Macy Roth (1993), *JEA*, 79, pp. 57–79 (`A-18_考據_gemini.md:81`)
     - Virginia Trimble (1964), *MIOB*, 10, pp. 183–187 (`A-18_考據_gemini.md:35, 82`)
4. **Local Sources in `07_資料來源/`**:
   - Verified page ranges for `Don Childrey (2004)`, `Clark Wissler & D. C. Duvall (1908)`, and `Walter McClintock (1910)` were correctly identified as local and preserved.

---

## 4. Remediation Specifications

### Remediation for `A-18_審稿-文化_antigravity.md:17`
- **Target File**: `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md:17`
- **Before**:
  ```markdown
  Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250
  ```
- **After**:
  ```markdown
  Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II（未核頁碼）；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*（未核頁碼）
  ```
- **Synchronization**:
  After modification, synchronize byte-for-byte to `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md`.

---

## 5. Comprehensive Python Patch for `verify_batch2_r2_rules.py`

The updated `check_external_pages()` function has been implemented and verified in:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/explorer_it2_2/verify_batch2_r2_rules_patched.py`
and exported as a unified diff patch at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/explorer_it2_2/patch_verify_batch2_r2_rules.patch`

### The Enhanced `check_external_pages()` Implementation:

```python
def check_external_pages():
    """Check 5 (Enhanced): Exhaustive check for external non-local book page citations."""
    findings = []
    
    # Comprehensive catalog of external authors across A-16, A-17, A-18, A-19
    external_authors = [
        # A-18 Egyptian external sources
        "Chassinat", "Belmonte", "Censorinus", "Parker", "Neugebauer", "Hurst", "Ball", "Petrie",
        "Buchwald", "Josefowicz", "Sethe", "Allen", "Otto", "Assmann", "Gardiner", "Gantenbrink",
        "Bauval", "Gilbert", "Edwards", "Lehner", "Dorner", "Erman", "Grapow",
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
    
    # Page citation pattern: supports 'p. 12', 'pp. 12-14', and Roman numerals 'Vol. II, p. 31', 'Tome II, p. 31'
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
```

---

## 6. Empirical Verification & Test Results

### 1. Test against current repository state:
Running `python3 .agents/teamwork/explorer_it2_2/verify_batch2_r2_rules_patched.py`:
```
==============================================================================
 Batch 2 Round 2 Remediation - Automated Rules Verifier (Patched)
==============================================================================

[1. A-16 v0 Worktree Presence & Hash Match]
  -> PASS

[2. Git Immutability on Original Scripts]
  -> PASS

[3. Research Section 2 (Only ✗, ⚠, ？ - zero ✓)]
  -> PASS

[4. Hallucinated Book Title Check ('Anguish of Arrival')]
  -> PASS

[5. External Books Guessed Pages Check (must be '未核頁碼' & no contradiction)]
  -> FAIL (2 issues):
     - [A-18_審稿-文化_antigravity.md:17] GUESSED PAGE: External author 'Chassinat' has guessed page numbers 'Vol. II, p. 31' without '未核頁碼': Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31
     - [A-18_審稿-文化_antigravity.md:17] GUESSED PAGE: External author 'Belmonte' has guessed page numbers 'pp. 243' without '未核頁碼': Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250

[6. Episode-Specific Astronomical & Narrative Rules]
  -> PASS

[7. Dual-Workspace 20 Files SHA-256 Synchronization]
  -> PASS

==============================================================================
 OVERALL RESULT: REMEDIATION REQUIRED (SEE FAILURES ABOVE)
==============================================================================
```
**Result**: The patched script instantly detected the two lingering guessed pages in `A-18_審稿-文化_antigravity.md:17` with zero false positives across all 20 files.

### 2. Synthetic Test against Contradictory Citations (`pp. 123... 未核頁碼`):
When tested against synthetic inputs containing contradictory patterns:
- `Parker (1950), pp. 24–28（未核頁碼）` -> Correctly flags `CONTRADICTION: Guessed page numbers 'pp. 24' appear before/with '未核頁碼' for author 'Parker'`.
- `Petrie (1883), p. 123（未核頁碼）` -> Correctly flags `CONTRADICTION: Guessed page numbers 'p. 123' appear before/with '未核頁碼' for author 'Petrie'`.
- `Sethe (1908), vol. 1, p. 488（未核頁碼）` -> Correctly flags `CONTRADICTION: Guessed page numbers 'vol. 1, p. 488' appear before/with '未核頁碼' for author 'Sethe'`.

---

## 7. Instructions for Application

To apply the patch to the primary verification script:
```bash
patch -p1 .agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py < .agents/teamwork/explorer_it2_2/patch_verify_batch2_r2_rules.patch
```
Or copy `.agents/teamwork/explorer_it2_2/verify_batch2_r2_rules_patched.py` over `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py`.
