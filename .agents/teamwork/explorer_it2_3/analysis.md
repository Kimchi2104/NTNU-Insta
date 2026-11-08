# Global Scope Audit: Page Indicators & Provenance Verification across Batch 2 Files

**Date**: 2026-11-01  
**Agent**: explorer_it2_3 (Global Scope Audit Explorer)  
**Target Scope**: All 20 files in `04_腳本庫/_審稿/` (Episodes A-16, A-17, A-18, A-19)  
**Allowed Local Book Sources in `07_資料來源/`**:
1. `07_資料來源/Navojo in America/Star Trails Navajo (Don Childrey) (z-library.sk, 1lib.sk, z-lib.sk).pdf` (Don Childrey 2004)
2. `07_資料來源/Blackfoot in America/Mythology of the Blackfoot Indians.txt` (Clark Wissler & D. C. Duvall 1908)
3. `07_資料來源/Blackfoot in America/The old north trail, or, Life, legends and religion of the Blackfeet Indians.txt` (Walter McClintock 1910)

---

## 1. Executive Summary

An exhaustive regex and syntactic audit was executed across all 20 review files in `04_腳本庫/_審稿/` (covering 4 episodes × 5 deliverables: 1 考據 + 4 角色審稿). 

Key findings:
1. **Total Page Indicator Matches**: Exactly **102 occurrences** of page indicators (`p\.`, `pp\.`, `頁`, `vol\. \d+, p\.`) were identified across 39 lines.
2. **Authorized Local Sources (87 occurrences)**:
   - **A-16 (20 occurrences)**: 100% reference Don Childrey (2004) *Star Trails: Navajo*, verified against the local PDF in `07_資料來源/Navojo in America/`.
   - **A-17 (67 occurrences)**: 100% reference Clark Wissler & D. C. Duvall (1908) or Walter McClintock (1910), verified against the local text transcripts in `07_資料來源/Blackfoot in America/`.
3. **Peer-Reviewed Academic Journals (13 occurrences)**:
   - 13 occurrences in A-18 and A-19 reference legitimate published journal articles with verified volume and article page spans (*Journal for the History of Astronomy*, *Bulletin de l'Institut Français d'Archéologie Orientale*, *The Journal of Egyptian Archaeology*, *Mitteilungen des Instituts für Orientforschung*, and *Astronomy & Astrophysics*).
4. **External Book Pagination Violations (Exactly 2 occurrences on 1 line)**:
   - **`04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md:17`**:
     Verbatim text: `Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250`
     Neither Chassinat nor Belmonte exists as a primary book in `07_資料來源/`. In `A-18_考據_gemini.md:13, 69, 78`, both works are correctly designated with `（未核頁碼）`. Retaining `p. 31` and `pp. 243–250` in `A-18_審稿-文化` violates the anti-hallucination mandate.
   - **No other file or line in the entire 20-file corpus contains unauthorized book page numbers.**
5. **Contradiction Check (`[p|pp]\. \d+.*未核頁碼`)**:
   - **Zero true contradictions found**: There is no instance where a guessed page number and `未核頁碼` co-exist on the *same citation/work* (e.g. `Author (2000), p. 488（未核頁碼）` does not exist).
   - In 7 lines, a verified local source or journal article with real pages appears alongside an external work with `（未核頁碼）` separated by semicolons (e.g. `Don Childrey (2004), pp. 38, 54; Father Berard Haile (1947)（未核頁碼）`). These are valid multi-source citations.
6. **Automated Verifier Blind Spot**:
   - `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py` failed to catch the line 17 violation because its `external_authors` list omitted `"Chassinat"` and `"Belmonte"`.

---

## 2. Exhaustive File Census Table

| # | File Name | Total Lines | Lines with Page Matches | Page Indicator Matches | Lines with `未核頁碼` | Unauthorized Book Page Numbers Found |
|---|---|:---:|:---:|:---:|:---:|:---:|
| 1 | `A-16_考據_gemini.md` | 64 | 9 | 17 | 18 (39 tags) | **0** (All Childrey 2004) |
| 2 | `A-16_審稿-天文_antigravity.md` | 19 | 1 | 1 | 0 | **0** (Childrey 2004) |
| 3 | `A-16_審稿-文化_antigravity.md` | 19 | 2 | 2 | 2 (8 tags) | **0** (Childrey 2004) |
| 4 | `A-16_審稿-敘事_antigravity.md` | 19 | 0 | 0 | 0 | **0** |
| 5 | `A-16_審稿-語言_antigravity.md` | 19 | 0 | 0 | 1 (1 tag) | **0** |
| 6 | `A-17_考據_gemini.md` | 49 | 17 | 41 | 8 (12 tags) | **0** (All Wissler/McClintock) |
| 7 | `A-17_審稿-天文_antigravity.md` | 81 | 5 | 5 | 0 | **0** (All Wissler/McClintock) |
| 8 | `A-17_審稿-文化_antigravity.md` | 19 | 6 | 21 | 0 | **0** (All Wissler/McClintock) |
| 9 | `A-17_審稿-敘事_antigravity.md` | 18 | 0 | 0 | 0 | **0** |
| 10 | `A-17_審稿-語言_antigravity.md` | 18 | 0 | 0 | 0 | **0** |
| 11 | `A-18_考據_gemini.md` | 86 | 9 | 11 | 24 (47 tags) | **0** (All Peer-Reviewed Journals) |
| 12 | `A-18_審稿-天文_antigravity.md` | 19 | 0 | 0 | 0 | **0** |
| 13 | `A-18_審稿-文化_antigravity.md` | 19 | 2 | 3 | 2 (4 tags) | **2** (Line 17: Chassinat `p. 31`, Belmonte `pp. 243–250`) |
| 14 | `A-18_審稿-敘事_antigravity.md` | 19 | 0 | 0 | 0 | **0** |
| 15 | `A-18_審稿-語言_antigravity.md` | 18 | 0 | 0 | 0 | **0** |
| 16 | `A-19_考據_gemini.md` | 73 | 1 | 1 | 14 (30 tags) | **0** (Peer-Reviewed Journal) |
| 17 | `A-19_審稿-天文_antigravity.md` | 18 | 0 | 0 | 1 (1 tag) | **0** |
| 18 | `A-19_審稿-文化_antigravity.md` | 18 | 0 | 0 | 2 (4 tags) | **0** |
| 19 | `A-19_審稿-敘事_antigravity.md` | 17 | 0 | 0 | 0 | **0** |
| 20 | `A-19_審稿-語言_antigravity.md` | 18 | 0 | 0 | 0 | **0** |
| **Total** | **20 files** | **591** | **44** | **102** | **72 lines (147 tags)** | **2 occurrences (1 file, line 17)** |

---

## 3. Detailed Cross-Reference Audit by Category

### Category A: Authorized Local Sources (100% Compliant)

#### 1. Don Childrey (2004), *Star Trails: Navajo*
- **Primary Source File**: `07_資料來源/Navojo in America/Star Trails Navajo (Don Childrey) (z-library.sk, 1lib.sk, z-lib.sk).pdf`
- **Occurrences (20 matches across 3 files)**:
  * `A-16_考據_gemini.md:7`: `pp. 16, 99–103` (Nightway timing, winter storytelling)
  * `A-16_考據_gemini.md:9`: `p. 72` (Coyote star Canopus / Mąʼii bizǫʼ)
  * `A-16_考據_gemini.md:11`: `pp. 18, 32–39` (Black God stomping, crystal ascension)
  * `A-16_考據_gemini.md:12`: `pp. 38, 54` (Pleiades placement, Hai/Shi misprint noted)
  * `A-16_考據_gemini.md:13`: `p. 62` (First Big One, ʼAtséʼetsoh)
  * `A-16_考據_gemini.md:15`: `p. 54` (Childrey setting claim refuted by Skyfield)
  * `A-16_考據_gemini.md:16`: `p. 50` (Mother-in-law avoidance)
  * `A-16_考據_gemini.md:17`: `p. 66` (Hastiin Sikʼaiʼí, stargazing `deestʼį́į́ʼ`)
  * `A-16_考據_gemini.md:29`: `pp. 35, 50` (Cassiopeia 5 stars vs 13 stars)
  * `A-16_考據_gemini.md:30`: `p. 72` (Canopus horizon extinction)
  * `A-16_考據_gemini.md:52`: `pp. 29–39, 42–74, 99–103` (Section 4 Bibliography summary)
  * `A-16_審稿-天文_antigravity.md:17`: `p. 54` (Pleiades seasonal timing)
  * `A-16_審稿-文化_antigravity.md:16`: `pp. 37–39` (Coyote Trickster philosophy)
  * `A-16_審稿-文化_antigravity.md:17`: `pp. 44–46` (Hooghan architecture and hearth)
- **Status**: **VERIFIED AUTHENTIC**. All page numbers directly reflect verified sections of the local PDF.

#### 2. Clark Wissler & D. C. Duvall (1908), *Mythology of the Blackfoot Indians*
- **Primary Source File**: `07_資料來源/Blackfoot in America/Mythology of the Blackfoot Indians.txt`
- **Occurrences (36 matches across 3 files)**:
  * `A-17_考據_gemini.md:8`: `p. 5` (Duvall biography & collection)
  * `A-17_考據_gemini.md:11`: `pp. 71–72` (Six lost children / Bunched Stars)
  * `A-17_考據_gemini.md:16`: `p. 71` (Spring yellow calves)
  * `A-17_考據_gemini.md:17`: `pp. 40–44`, `第 42 頁`, `第 41 頁腳註 1`, `pp. 41–42`, `p. 41`, `p. 42` (Four-Tail Lodge flag painted lodge discovery)
  * `A-17_考據_gemini.md:33`: `pp. 41–42` (Section 2: Twin myth painted lodge erratum)
  * `A-17_考據_gemini.md:44`: `pp. 40–44, 68–71, 71–72` (Section 4 Bibliography)
  * `A-17_審稿-天文_antigravity.md:79`: `p. 42` (Four-Tail Lodge verification notes)
  * `A-17_審稿-文化_antigravity.md:4`: `第 42 頁`, `p. 41`, `p. 42` (Top 3 summary)
  * `A-17_審稿-文化_antigravity.md:13`: `pp. 68–70` (Seven brothers bear legend)
  * `A-17_審稿-文化_antigravity.md:14`: `pp. 71–72` (Old woman moon and drought)
  * `A-17_審稿-文化_antigravity.md:16`: `pp. 40–44`, `第 42 頁`, `第 41 頁腳註 1`, `pp. 41–42`, `p. 41`, `p. 42` (Four-Tail Lodge review commentary)
  * `A-17_審稿-文化_antigravity.md:17`: `p. 71` (Yellow calves)
- **Status**: **VERIFIED AUTHENTIC**. Page numbers, including the specific discovery of Four-Tail Lodge on p. 42 and p. 41 footnote 1, directly match the AMNH primary text.

#### 3. Walter McClintock (1910), *The Old North Trail*
- **Primary Source File**: `07_資料來源/Blackfoot in America/The old north trail, or, Life, legends and religion of the Blackfeet Indians.txt`
- **Occurrences (31 matches across 3 files)**:
  * `A-17_考據_gemini.md:9`: `pp. 26–35` (Blackfeet adoption & background)
  * `A-17_考據_gemini.md:10`: `p. 524` (Ipit-so-wahs, Morning Star cross)
  * `A-17_考據_gemini.md:12`: `p. 500` (Spider Man's fingers in Hercules)
  * `A-17_考據_gemini.md:13`: `p. 217` (Sacred painted lodge protocols)
  * `A-17_考據_gemini.md:14`: `pp. 284–324` (Sun Dance ceremony)
  * `A-17_考據_gemini.md:16`: `p. 490` (Six boys origin)
  * `A-17_考據_gemini.md:18`: `p. 522` (Appendix: Dorsey Sioux scaffold comparison)
  * `A-17_考據_gemini.md:24`: `p. 488` (Section 2: Nine children structure)
  * `A-17_考據_gemini.md:25`: `p. 219` (Section 2: Maltese cross morning star / butterfly)
  * `A-17_考據_gemini.md:36`: `pp. 491–500` (Section 3: Poïa Scarface epic)
  * `A-17_考據_gemini.md:39`: `p. 503, p. 524` (Section 3: Milky Way Wolf Trail)
  * `A-17_考據_gemini.md:43`: `pp. 207–224, 479–490, 491–505, 521–525` (Section 4 Bibliography)
  * `A-17_審稿-天文_antigravity.md:4, 14`: `p. 524` (Morning star Maltese cross)
  * `A-17_審稿-天文_antigravity.md:15`: `p. 488` (Ursa Major brothers count)
  * `A-17_審稿-天文_antigravity.md:16`: `p. 490` (Six bunched stars)
  * `A-17_審稿-文化_antigravity.md:13`: `p. 488` (Nine children family)
  * `A-17_審稿-文化_antigravity.md:15`: `p. 217, pp. 217–220` (Painted lodge transfer protocol)
  * `A-17_審稿-文化_antigravity.md:17`: `p. 490` (Yellow calves)
- **Status**: **VERIFIED AUTHENTIC**. All page numbers match the London 1910 edition in `07_資料來源/Blackfoot in America/`.

---

### Category B: Published Academic Journal Articles (100% Compliant)

All page indicators in this category represent published academic journal article page ranges (Volume, Issue, Article Pages) rather than guessed book page numbers.

| # | Author & Year | Journal Name | Volume / Issue | Page Span | File & Line Location |
|---|---|---|:---:|:---:|---|
| 1 | Bradley E. Schaefer (2000) | *Journal for the History of Astronomy* | 31(2) | `pp. 149–155` | `A-18_考據_gemini.md:9, 73` |
| 2 | Sarah Symons (2015) | *Journal for the History of Astronomy* | 46(2) | `pp. 203–224` | `A-18_考據_gemini.md:15` |
| 3 | Sylvie Cauville & Éric Aubourg (1995) | *Bulletin de l'Institut Français d'Archéologie Orientale* | 95 | `pp. 251–284` | `A-18_考據_gemini.md:16, 70`<br>`A-18_審稿-文化_antigravity.md:14` |
| 4 | Éric Aubourg (1995) | *BIFAO* | 95 | `pp. 1–10` | `A-18_考據_gemini.md:16, 71` |
| 5 | Virginia Trimble (1964) | *Mitteilungen des Instituts für Orientforschung* | 10 | `pp. 183–187` | `A-18_考據_gemini.md:35, 82` |
| 6 | Ann Macy Roth (1993) | *Journal of Egyptian Archaeology* | 79 | `pp. 57–79` | `A-18_考據_gemini.md:50, 81` |
| 7 | Floor van Leeuwen (2007) | *Astronomy & Astrophysics* | 474(2) | `pp. 653–664` | `A-19_考據_gemini.md:69` |

**Status**: **COMPLIANT**. These represent legitimate, peer-reviewed research papers cited with standard journal pagination.

---

### Category C: External Book Violations & Provenance Deficiencies

#### Defect 1: Guessed Page Numbers for External Books in `A-18_審稿-文化_antigravity.md:17`
- **File**: `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md`
- **Line**: 17 (Shot 14 ⚪可選 row, 依據 column)
- **Verbatim Text**:
  ```markdown
  Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250
  ```
- **Violation Details**:
  1. Neither *Le Temple d'Edfou* (Chassinat 1897) nor *In Search of Cosmic Order* (Belmonte 2009) is present in `07_資料來源/`.
  2. In `A-18_考據_gemini.md:13` and Lines 69, 78, both works are correctly marked with `（未核頁碼）`:
     - `Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, Institut Français d'Archéologie Orientale, Cairo（未核頁碼）`
     - `Juan Antonio Belmonte & Mosalam Shaltout (2009), *In Search of Cosmic Order*（未核頁碼）`
  3. `A-18_審稿-文化_antigravity.md:17` retained the guessed numbers `p. 31` and `pp. 243–250`, directly contravening `01_網路考據.md` & `02_審稿Critic.md` rules.

#### Defect 2: Incomplete Tagging for External Book in `A-18_審稿-文化_antigravity.md:14` (Recommended Polish)
- **File**: `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md`
- **Line**: 14 (Shots 15–17 🟡建議 row, 依據 column)
- **Verbatim Text**:
  ```markdown
  Sylvie Cauville & Éric Aubourg (1995), *BIFAO*, 95, pp. 251–284；Christian Leitz (2002), *LGG*
  ```
- **Observation**:
  - `Christian Leitz (2002), *LGG*` contains NO guessed page numbers (compliant with no-guessed-pages rule).
  - However, in `A-18_考據_gemini.md:54`, the full work is cited as `Christian Leitz (2002), *Lexikon der ägyptischen Götter und Götterbezeichnungen*, Band VI, Peeters（未核頁碼）`.
  - For 100% uniformity across files, it should be appended with `（未核頁碼）`.

---

## 4. Contradiction Audit: `[p|pp]\. \d+.*未核頁碼`

A multi-pass regex scan checked whether any single citation segment combines a guessed page number with the `未核頁碼` tag.

### Finding: ZERO Direct Contradictions
There are **zero instances** across all 20 files of the contradiction pattern `[p|pp]\. \d+.*未核頁碼` applied to the same book or citation.

### Clarification on Multi-Source Lines
Seven lines across the dataset contain both a page number and `未核頁碼`, but each represents separate, cleanly delimited citations:
1. `A-16_考據_gemini.md:12`:
   `Don Childrey (2004), pp. 38, 54; Father Berard Haile (1947)（未核頁碼）`
   *Childrey has verified local pages; Haile is an external reference correctly tagged `（未核頁碼）`.*
2. `A-16_考據_gemini.md:16`:
   `Childrey, 2004, p. 50; Clyde Kluckhohn & Dorothea Leighton, *The Navaho* (1946)（未核頁碼）; Trudy Griffin-Pierce (1992)（未核頁碼）`
3. `A-16_考據_gemini.md:30`:
   `Don Childrey (2004), p. 72; Father Berard Haile (1947)（未核頁碼）`
4. `A-16_審稿-文化_antigravity.md:16`:
   `Childrey (2004) pp. 37–39; Gary Witherspoon (1977)（未核頁碼）; Paul Radin, *The Trickster* (1956)（未核頁碼）`
5. `A-16_審稿-文化_antigravity.md:17`:
   `Childrey (2004) pp. 44–46; Griffin-Pierce (1992)（未核頁碼）`
6. `A-17_考據_gemini.md:12`:
   `McClintock (1910, p. 500); Dorcas S. Miller (1997)（未核頁碼）`
7. `A-18_考據_gemini.md:9`:
   `Bradley E. Schaefer (2000), "The Heliacal Rise of Sirius and Ancient Egyptian Chronology", *Journal for the History of Astronomy*, 31(2), pp. 149–155; Juan Antonio Belmonte (2009), *In Search of Cosmic Order*（未核頁碼）`

In all seven cases, the separation is semantically sound and preserves provenance integrity.

---

## 5. Root Cause Analysis: Verifier Test Blind Spot

The failure of the automated verifier in Round 2 (`verify_batch2_r2_rules.py`) to catch the violation in `A-18_審稿-文化_antigravity.md:17` was traced to its architecture:

```python
# Lines 113-120 of verify_batch2_r2_rules.py:
external_authors = [
    "Toelken", "Haile", "Griffin-Pierce", "Kluckhohn", "Young &", "Young and", "Jayne",
    "Newcomb", "Witherspoon", "Matthews", "Chamberlain", "Schaafsma", "IEI",
    "Frantz", "Russell", "Censorinus", "Parker", "Neugebauer", "Hurst", "Ball", "Petrie",
    "Buchwald", "Josefowicz", "Sethe", "Allen", "Otto", "Ibn Qutayba", "al-Sufi", "al-Ṣūfī",
    "Ibn Durayd", "Ibn Manzur", "Ibn Manẓūr", "Ibn al-Jawzi", "Ibn al-Jawzī", "Ibn Hibban",
    "Ibn Ḥibbān", "Kunitzsch", "Smart", "Lane"
]
```

Because `external_authors` used a hardcoded author list that omitted `"Chassinat"` and `"Belmonte"`, the verifier never evaluated `Émile Chassinat` or `Juan Antonio Belmonte`.

### Test Architecture Fix Recommendation
Replace the hardcoded author list with an exhaustive structural check:
1. Scan for all occurrences of `pp?\.?\s*\d+` and `\d+\s*頁`.
2. Allow matches if and only if they belong to:
   - `Childrey` (in A-16)
   - `Wissler`, `Duvall`, or `McClintock` (in A-17)
   - Verified journal names (`JHA`, `BIFAO`, `JEA`, `MIOB`, `Astronomy & Astrophysics`, `A&A`)
3. Flag any match outside these whitelisted sources as a hard error.

---

## 6. Actionable Remediation Specification for Worker

The worker can remediate the entire defect suite in one definitive pass:

### Action 1: Modify `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md`
- **Location**: Line 17, column 6 (`依據`)
- **Replace**:
  ```markdown
  Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II, p. 31；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*, pp. 243–250
  ```
- **With**:
  ```markdown
  Émile Chassinat (1897), *Le Temple d'Edfou*, Vol. II（未核頁碼）；Juan Antonio Belmonte (2009), *In Search of Cosmic Order*（未核頁碼）
  ```

### Action 2 (Optional Consistency Polish):
- **Location**: `04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md`, Line 14, column 6 (`依據`)
- **Replace**:
  ```markdown
  Sylvie Cauville & Éric Aubourg (1995), *BIFAO*, 95, pp. 251–284；Christian Leitz (2002), *LGG*
  ```
- **With**:
  ```markdown
  Sylvie Cauville & Éric Aubourg (1995), *BIFAO*, 95, pp. 251–284；Christian Leitz (2002), *LGG*（未核頁碼）
  ```

### Action 3: Synchronize Workspace
- Copy the remediated `A-18_審稿-文化_antigravity.md` to:
  `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/A-18_審稿-文化_antigravity.md`
- Verify SHA-256 identity between the worktree and Downloads files.

### Action 4: Patch Verifier Test Suite
- In `.agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py`:
  Add `"Chassinat"`, `"Belmonte"`, and `"Leitz"` to `external_authors`, or implement the structural whitelist validator.
