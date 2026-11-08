# Handoff Report: NTNU Astronomy Club SOP & Rubric Specification Mining

## 1. Observation

Direct observations from the authoritative repository documents:

### 1.1 Scope & Context (`ORIGINAL_REQUEST.md`)
- **Target Episodes (9 scripts)**:
  - Early episodes: `04_腳本庫/A-01-中國四象青龍-逐字稿-v1.md`, `04_腳本庫/A-02-三垣天上的紫禁城-逐字稿-v1.md`, `04_腳本庫/A-03-玄武馱著洛書上天的龜蛇-逐字稿-v1.md`, `04_腳本庫/A-04-韓國印在鈔票上的星圖-逐字稿-v1.md`, `04_腳本庫/A-06-中秋特輯二十八宿月亮的28間驛站-逐字稿-v1.md`, `04_腳本庫/H-七夕-牛郎織女-逐字稿-v1.md`.
  - Recent completed episodes: `04_腳本庫/A-13-阿拉伯半島Thurayya與沙漠的雨季-逐字稿-v1.md`, `04_腳本庫/A-14-因紐特極夜裡的星鐘-逐字稿-v1.md`, `04_腳本庫/A-15-北歐Yule之夜的狼與神駒-逐字稿-v1.md`.
- **Target Working Directories**:
  - Primary repo worktree: `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost`
  - Target sync directory: `/Users/kimjoo/Downloads/NTNU Insta`
- **Integrity Rule**: "嚴禁直接修改 `04_腳本庫/` 下任何現有原始逐字稿檔案。" (`ORIGINAL_REQUEST.md`:45)

---

### 1.2 R1 (01 網路考據) Specifications
- **Source**: `02_製作流程SOP/外包任務書/01_網路考據.md` (lines 1–34) & `02_製作流程SOP/外包任務書/README.md` (lines 19–25)
- **Output File Pattern**: `04_腳本庫/_審稿/{編號}_考據_gemini.md` (繁體中文)
  - Example: `A-01_考據_gemini.md`, `A-13_考據_gemini.md`, `H-七夕_考據_gemini.md`
- **Scope of Audit**:
  - Primary focus: Check the "⚠ 待查核清單" in the script's "考據備忘".
  - Full-text audit: Comprehensive scan of voice-over (旁白), text cards (字卡), Instagram caption (Caption), first comment (首留言), and alliance post copy (聯盟版文案) for:
    > "任何帶數字、年代、人名、書名、引文、外文拼寫、「最早／最大／唯一」的句子都查一次。" (`01_網路考據.md`:9)
- **Five Verification Standards**:
  1. *引文* (Quotations): Must find the primary text in original sources (Chinese classics: ctext.org, Wikisource; foreign: original book, academic edition, author's original paper). Collate word-for-word, recording book title, chapter/section, edition, and page number (`01_網路考據.md`:11–12).
  2. *民族誌資料* (Ethnography): Must trace to original recorder and year (e.g. anthropologist's field report in year X); never cite only secondary websites or Stellarium descriptions (`01_網路考據.md`:13).
  3. *天文數字* (Astronomical figures): Give calculation basis or authoritative sources (SIMBAD, Hipparcos/Gaia, IAU WGSN, Central Weather Administration, IMO, PyEphem/Skyfield ephemeris) (`01_網路考據.md`:14).
  4. *無法證實之處理* (Unverifiable claims): Claims lacking reliable provenance must be marked as "？ 無法證實" and recommended to be hedged ("有人認為", "一說") or deleted (`01_網路考據.md`:15).
  5. *批判性審視* (Critical stance): Do not trust the script itself, nor judge an item correct merely because multiple websites repeat it — trace to the earliest source (`01_網路考據.md`:16).
- **Required Report Structure & Table Schema**:
  ```markdown
  # {編號} 網路考據

  ## 一、待查核清單逐條結果
  | # | 原主張 | 判定（✓ 證實／✗ 錯誤／⚠ 部分正確或需限定／？ 無法證實） | 查到的正確說法 | 出處（網址或書目＋頁碼） | 建議改寫（旁白要口語、短句） |

  ## 二、清單以外發現的問題
  （同上表格式，只列 ✗、⚠、？）

  ## 三、可以加進影片的好材料（選填）
  （查證過程中發現、有出處、對台灣觀眾有吸引力的事實；每條附出處）

  ## 四、參考資料總表
  ```

---

### 1.3 R2 (02 四角色平行審稿) Specifications
- **Source**: `02_製作流程SOP/外包任務書/02_審稿Critic.md` (lines 1–59)
- **Execution Architecture**: Four independent agents running in parallel, one role per agent, without cross-referencing:
  > "四個角色平行審，互不參考，避免意見互相同化。" (`02_審稿Critic.md`:3)
- **Output File Pattern**: `04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`
  - Where `{角色}` ∈ {`天文`, `文化`, `敘事`, `語言`}.
  - Total output files: 9 episodes × 4 roles = 36 files.
- **Top 3-Line Summary Requirement**:
  > "檔案開頭用三行寫：整體評價、最重要的三個問題、你沒把握的地方。" (`02_審稿Critic.md`:21)
- **Review Opinion Table Schema**:
  ```markdown
  | 嚴重度（🔴必改／🟡建議／⚪可選） | 位置（鏡號或段落） | 原文 | 問題 | 建議改法 | 依據 |
  ```
  - `嚴重度`: 🔴 必改 (factual errors, severe rule violations), 🟡 建議 (improvements, pacing, hedging), ⚪ 可選 (minor phrasing or polish).
  - `依據`: URL, book citation with page, or marked as `（推論）` (`README.md`:24).
- **Universal Constraints for Suggested Rewrites**:
  - Voice-over speed limit: `旁白每格 ≤ 4.5 字/秒` (`02_審稿Critic.md`:13)
  - On-screen text card: `字卡每張 ≤ 14 字` (`02_審稿Critic.md`:13)
  - Opening formula: First line must follow `「同一片星空，◯◯看見——◯◯。」` (`02_審稿Critic.md`:13)
  - Closing requirement: Last shot previews the next episode (`02_審稿Critic.md`:13)
  - Language: Taiwan Traditional Chinese phrasing (台灣繁體中文用語, e.g., avoid 視頻, 質量, 信息) (`02_審稿Critic.md`:13, 55)
  - Target video duration: `≤ 240 秒，理想 180 秒內` (`02_審稿Critic.md`:47)
- **Specific Role Rubrics**:
  1. **天文** (Astronomer & Night Sky Tour Guide, lines 25–32):
     - Star name and constellation mapping (HIP, Bayer designation, IAU constellation, cultural line consistency).
     - Night sky clocking ("星空對時"): Date, time, azimuth, elevation, rise/set times verified for Taipei (25.03°N, 121.56°E, UTC+8) using PyEphem/Skyfield recalculation.
     - Physical metrics: Distance, magnitude, angular separation, periods, precession ("古今天空不同", ~25,800-year cycle).
     - Southern target visibility from Taiwan (e.g. Canopus at ~12°–14° elevation).
     - Stargazing practicality: "今晚抬頭看" feasibility against light pollution, altitude, and moonlight.
  2. **文化與原典** (Cultural Astronomy / Archaeoastronomy Researcher, lines 34–42):
     - Provenance of cultural claims: Primary record (who, when, where) vs. secondary retelling / Stellarium assumption.
     - Verbatim citation accuracy, correct chapter/section; detecting vernacular paraphrases passed as direct quotes.
     - Checking dogmatism: Detecting single-scholar hypotheses presented as settled fact, or unverifiable claims ("A earlier than B", "world's first/most").
     - Indigenous cultural sovereignty & taboos: Seasonal restrictions (e.g., Navajo stories told only in winter), restricted/sacred knowledge, stereotyping.
     - Transliteration & diacritics: ʻokina, macron, IAST, Arabic transliteration, Korean RR, Japanese kana.
  3. **敘事與節奏** (Short Video Screenwriter, lines 44–51):
     - First 3 seconds hook; opening sentence retention.
     - One core message per shot; cognitive load; trimming fat (target ≤ 240s, ideal ≤ 180s).
     - Text cards ≤ 14 chars; voice-over rate ≤ 4.5 chars/sec.
     - Next episode teaser attraction and consistency with upcoming titles.
     - Social platform adaptability: Caption opening hook, hashtags, and "聯盟版文案" (FB amateur astronomy group: first line focuses on the night sky, no club self-promotion, no IG influencer jargon).
  4. **語言與可讀性** (Taiwanese Mandarin Editor, lines 53–59):
     - Typos, tautologies, clumsy grammar, Mainland vocabulary (視頻, 質量, 信息, 軟件, etc.).
     - Spoken naturalness: Can voice actor comfortably breathe and read it aloud? Homophone confusion check (期中 vs. 其中, 必需 vs. 必須).
     - Punctuation, numbers, units, fullwidth vs. halfwidth consistency.
     - Pronunciation guides (zhuyin/furigana) for foreign/obscure names in 配音提示.
     - Pause alignment with visual shot transitions; card vs. voice-over redundancy.

---

### 1.4 R3 (03 英文版改寫) Specifications
- **Source**: `02_製作流程SOP/外包任務書/03_英文版改寫.md` (lines 1–24) & `02_製作流程SOP/英文版評估.md` §七 (lines 60–67)
- **Core Philosophy**:
  > "Adapt, don't translate word-for-word." (`03_英文版改寫.md`:9)
  > "英文稿要比中文刪 15–30%，才能壓進 180 秒。" (`英文版評估.md`:44)
- **Output File Pattern**: `04_腳本庫/_英文版/{編號}-EN-script-draft.md`
- **Master Glossary File**: `06_發布月曆/英文譯名表.csv`
- **Quantitative Hard Thresholds**:
  1. Total duration: **≤ 180 seconds** (`03_英文版改寫.md`:10, `英文版評估.md`:28)
  2. Speech rate: **≤ 2.6 words per second** per shot (`03_英文版改寫.md`:10)
  3. Text cards: **≤ 6 English words** each (`03_英文版改寫.md`:16)
- **Formula & Structural Standards**:
  - Opening sentence: *"One sky. The [people] saw — [X]."* (`03_英文版改寫.md`:12, `英文版評估.md`:62)
  - Unit conventions: Distances in *light-years*, angles in *°*, times in *24-hour clock* labeled *"Taiwan time (UTC+8)"* (`03_英文版改寫.md`:14, `英文版評估.md`:65).
  - Factuality: Do not introduce claims not present in the Chinese script; preserve epistemic hedging ("Some believe", "One account suggests") (`03_英文版改寫.md`:15).
  - Animation reuse: Preserve shot-by-shot row structure so existing Canva/animation assets can be aligned (`03_英文版改寫.md`:11).
- **Romanization & Proper Noun Rules** (`03_英文版改寫.md`:13, `英文版評估.md`:62–67):
  - **Chinese asterisms**: Pinyin + English meaning on first mention (*Xin, "the Heart"*). Must translate Chinese 星官 as ***asterisms***, NEVER *constellations* (to avoid confusion with the 88 IAU constellations). Standards: Sun & Kistemaker《The Chinese Sky during the Han》and Stellarium chinese culture. Add tone marks in subtitles/text, plain letters in VO.
  - **Korean names**: Revised Romanization (RR), e.g., *Cheonsang Yeolcha Bunya Ji Do*, *Jingnyeo* (직녀), *Hago* (하고), *Cheonjin* (천진).
  - **Japanese names**: Modified Hepburn (e.g., *Subaru*, *Kitora*).
  - **Sanskrit names**: IAST with full diacritics (e.g., *Kṛttikā*, *Nakṣatra*, *Abhijit*).
  - **Arabic & Indigenous names**: Retain exact original spelling and diacritics from authoritative sources / script's 星名表:
    - Polynesian: ʻokina (glottal stop) and macron (kahakō: ā, ē, ī, ō, ū).
    - Arabic: ʿayn (ʿ), hamza (ʾ), macrons (ā, ī, ū) (e.g., *al-Thurayyā*, *al-Twaibiʿ*, *al-Iklīl*, *al-Wasm*, *al-Murabbaʿāniyya*, *Suhail*).
    - Inuit: Roman orthography per John MacDonald / Nunavut standards (*Aagjuuk*, *Tukturjuit*, *Quturjuuk*, *Ullaktut*, *Nanurjuk*, *Nuutuittuq*).
    - Norse: Old Norse orthography (*Úlfs kjaptr*, *Fiskikarlar*, *Karlvagn*, *Leiðarstjarna*, *Sköll*, *Hati*).
- **Required Sections in `{編號}-EN-script-draft.md`**:
  1. Shot table: `| Shot | Sec | Voice-over | On-screen text | Words/sec |`
  2. Summary metrics: Total seconds, Total words, Average words/sec.
  3. Glossary table: `| Chinese | English used | Notes |`
  4. Social platform metadata:
     - YouTube title (≤ 60 characters)
     - YouTube description (3–5 lines + cited sources)
     - Facebook caption
  5. Cut & semantic adjustment log: List of cuts or semantic changes with reasoning for reviewer auditing.

---

## 2. Logic Chain

The requirements in `ORIGINAL_REQUEST.md` derive directly from the SOP architecture as follows:

1. **Origin of the R1, R2, R3 Pipeline**:
   - `02_製作流程SOP/外包任務書/README.md` defines the standard outsourcing workflow:
     Draft v0 → 01 網路考據 (Gemini) + 02 審稿Critic (Antigravity 4 roles) → Deliver to `04_腳本庫/_審稿/` → Merge into v1 → 03 英文版改寫 → Deliver to `04_腳本庫/_英文版/`.
   - The 9 assigned target scripts represent the core canon: early cornerstone scripts (`A-01` to `A-04`, `A-06`, `H-七夕`) that need retrofitting to full SOP rigor, and the latest complex scripts (`A-13`, `A-14`, `A-15`) which need their review and English adaptation cycles finalized.

2. **Deduction of File Naming & Organization**:
   - For R1: `{編號}_考據_gemini.md` in `04_腳本庫/_審稿/` ensures the merging editor can deterministically find research notes.
   - For R2: `{編號}_審稿-{角色}_antigravity.md` in `04_腳本庫/_審稿/` allows automated or side-by-side parsing of the 4 independent perspectives without collision.
   - For R3: `{編號}-EN-script-draft.md` in `04_腳本庫/_英文版/` isolates adapted English assets while maintaining a 1:1 pairing with Chinese originals.
   - All term pairs must be recorded in `06_發布月曆/英文譯名表.csv` to ensure cross-episode terminology consistency ("一詞一譯").

3. **Deduction of Rigor in Astronomical & Ephemeris Calculations**:
   - The series targets both public viewers on Instagram and the 60,000-member "臺灣業餘天文聯盟" FB community.
   - Any assertion regarding star visibility, coordinates, lunar phases, or rise/set times will be scrutinized.
   - Therefore, ephemeris calculations must be tied to Taipei coordinates (25.03°N, 121.56°E, UTC+8) with atmospheric refraction accounted for, and stellar identities must resolve to HIP / Bayer designations in SIMBAD, Gaia/Hipparcos, or IAU WGSN.

4. **Deduction of the 180s and 2.6 words/sec Limits for English**:
   - Instagram and YouTube Shorts have strict audience retention drop-offs beyond 3 minutes (180 seconds).
   - In English speech, conversational clarity for educational content caps at 130–155 words per minute (≈ 2.2–2.6 words per second). Exceeding 2.6 words/sec causes garbled speech and cognitive overload.
   - Chinese scripts often run 240–288 seconds (`A-13` is 283s, `A-14` is 288s). Translating directly yields > 600 words. Thus, an explicit 15–30% editorial trim is a mathematical necessity to hit ≤ 180s.

---

## 3. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | R1 網路考據 | Output Destination & Naming | Sourced fact-check report saved to standardized path | Script `{編號}` | `04_腳本庫/_審稿/{編號}_考據_gemini.md` | Non-standard name breaks merge pipeline | `README.md`:21, `01_網路考據.md`:18 |
| 2 | R1 網路考據 | Four-Section Structure | Mandatory 4-section report layout | Script text + research data | Sections 一 (待查核清單), 二 (清單外發現), 三 (好材料), 四 (參考資料) | Missing section fails programmatic rubric check | `01_網路考據.md`:20-33, `ORIGINAL_REQUEST.md`:57 |
| 3 | R1 網路考據 | Verification Table Schema | 6-column standardized verification table | Claims from script | `| # | 原主張 | 判定 | 查到的正確說法 | 出處 | 建議改寫 |` | Missing columns reject review | `01_網路考據.md`:24 |
| 4 | R1 網路考據 | 4-Tier Judgement Taxonomy | Standardized evaluation symbols | Evaluated claim | `✓ 證實`, `✗ 錯誤`, `⚠ 部分正確或需限定`, `？ 無法證實` | Ambiguous/unclassified verdict | `01_網路考據.md`:24 |
| 5 | R1 網路考據 | Classical Quotation Verification | Primary text collation with chapter, section, and edition | Ancient text quote | Verbatim match, book/chapter/page | Vernacular paraphrase flagged as ⚠ | `01_網路考據.md`:12 |
| 6 | R1 網路考據 | Ethnographic Provenance Audit | Tracing Indigenous star lore to original field recorder | Folklore/ethnographic claim | Anthropologist name, year, field report | Second-hand web/Stellarium cited flagged as ⚠ | `01_網路考據.md`:13 |
| 7 | R1 網路考據 | Celestial Mechanics Verification | Ephemeris & database cross-check for Taipei coordinates | Star data, dates, rise/set | SIMBAD/Gaia/PyEphem calculations for 25.03°N, 121.56°E | Unverified data flagged as ？ | `01_網路考據.md`:14, `ORIGINAL_REQUEST.md`:32 |
| 8 | R2 四角色審稿 | Quad-Role Separation | 4 independent critic personas running in parallel | Script file | 4 distinct critic files (`天文`, `文化`, `敘事`, `語言`) | Merged/homogenized reviews violate independence | `02_審稿Critic.md`:3, 25-59 |
| 9 | R2 四角色審稿 | Top 3-Line Summary | 3-line synthesis header at top of report | Review findings | 3 lines: (1) 整體評價, (2) 最重要的三個問題, (3) 沒把握的地方 | Omission violates rubric | `02_審稿Critic.md`:21 |
| 10 | R2 四角色審稿 | 6-Column Critic Table Schema | Standardized review opinion table | Issues identified | `| 嚴重度 | 位置 | 原文 | 問題 | 建議改法 | 依據 |` | Malformed table breaks parsing | `02_審稿Critic.md`:18 |
| 11 | R2 四角色審稿 | 3-Level Severity Taxonomy | Prioritizing fixes by urgency | Discovered issue | `🔴 必改`, `🟡 建議`, `⚪ 可選` | Unrated opinions hinder editor triage | `02_審稿Critic.md`:18 |
| 12 | R2 四角色審稿 | Voice-over Speed Limit | Spoken character rate upper bound | Voice-over text & shot seconds | Rate ≤ 4.5 chars/sec | Over 4.5 chars/sec triggers 🔴 必改 | `02_審稿Critic.md`:13, 48 |
| 13 | R2 四角色審稿 | Text Card Length Limit | On-screen graphic text upper bound | Text card string | Card ≤ 14 characters | Over 14 characters triggers 🔴/🟡 | `02_審稿Critic.md`:13, 48 |
| 14 | R2 四角色審稿 | Taiwan Mandarin Phrasing | Enforcing Taiwanese linguistic idioms | Script wording | Taiwan traditional Chinese phrasing | Mainland terms (視頻, 質量, etc.) flagged | `02_審稿Critic.md`:13, 55 |
| 15 | R2 四角色審稿 | Fixed Opening Sentence | Universal series opening pattern | Opening voice-over | Pattern: 「同一片星空，◯◯看見——◯◯。」 | Deviations flagged unless justified by special edition | `02_審稿Critic.md`:13 |
| 16 | R2 四角色審稿 | Closing Episode Teaser | Previews the next upcoming episode | Last shot voice-over/card | Teaser matching next episode title | Missing teaser flagged | `02_審稿Critic.md`:13, 49 |
| 17 | R2 四角色審稿 | Celestial Ephemeris for Taipei | Exact sky clocking calculation | Date, time, location | Azimuth, elevation, rise/set at (25.03°N, 121.56°E, UTC+8) | Fabricated sky timing flagged 🔴 | `02_審稿Critic.md`:29, `ORIGINAL_REQUEST.md`:58 |
| 18 | R2 四角色審稿 | Precession & Epoch Tracking | Accounting for 25,800-year precession cycle | Historic star alignments | Pole star shift, coordinate precession | Treating ancient sky as identical to today flagged | `02_審稿Critic.md`:30 |
| 19 | R2 四角色審稿 | Cultural Sovereignty & Taboos | Respecting sacred knowledge and seasonal restrictions | Indigenous star lore | Verification of storytelling rules (e.g. Navajo winter-only) | Violations flagged 🔴 必改 | `02_審稿Critic.md`:40, `英文版評估.md`:72 |
| 20 | R2 四角色審稿 | Platform Copy Alignment | Customizing captions for IG vs Alliance FB | Social copy | IG caption with hooks/hashtags; Alliance copy focusing on sky, not club | IG promo in Alliance copy flagged | `02_審稿Critic.md`:50 |
| 21 | R3 英文版改寫 | English Adaptation Destination | Output path for adapted English drafts | Chinese script v1 | `04_腳本庫/_英文版/{編號}-EN-script-draft.md` | Non-standard path | `03_英文版改寫.md`:18 |
| 22 | R3 英文版改寫 | Total Video Duration Cap | Hard duration upper bound for Shorts/Reels | Shot table seconds | Total seconds ≤ 180s | Over 180s fails check | `03_英文版改寫.md`:10, `英文版評估.md`:28 |
| 23 | R3 英文版改寫 | Shot Speech Rate Cap | Maximum English voiceover pace | Shot text & seconds | Words/sec ≤ 2.6 for every shot | Over 2.6 words/sec fails check | `03_英文版改寫.md`:10 |
| 24 | R3 英文版改寫 | English Card Word Limit | Maximum word count on graphic cards | Card text | On-screen text ≤ 6 English words | Over 6 words fails check | `03_英文版改寫.md`:16 |
| 25 | R3 英文版改寫 | English Opening Formula | Standard English opening hook | First shot voice-over | Pattern: *"One sky. The [people] saw — [X]."* | Non-standard opening | `03_英文版改寫.md`:12, `英文版評估.md`:62 |
| 26 | R3 英文版改寫 | Shot Table Schema | Standardized English分鏡 table | Adapted shots | `| Shot | Sec | Voice-over | On-screen text | Words/sec |` | Malformed table fails validation | `03_英文版改寫.md`:19 |
| 27 | R3 英文版改寫 | English Adaptation Sections | Mandatory 5-part structure of draft file | Adapted script | (1) Shot table, (2) Totals, (3) Glossary, (4) Social copy, (5) Cut list | Missing section fails acceptance check | `03_英文版改寫.md`:18-23 |
| 28 | R3 英文版改寫 | Master Glossary Maintenance | Central glossary tracking all translated terms | Proper nouns in episode | `06_發布月曆/英文譯名表.csv` | Duplicate/inconsistent terms across episodes | `英文版評估.md`:66, `ORIGINAL_REQUEST.md`:53 |
| 29 | R3 英文版改寫 | Chinese Asterism Translation | Disambiguating Chinese asterisms from IAU constellations | Chinese star/asterism names | Pinyin + English meaning (*Xin, "the Heart"*); call *asterisms* | Calling them *constellations* violates rule | `03_英文版改寫.md`:13, `英文版評估.md`:63 |
| 30 | R3 英文版改寫 | Multi-Lingual Romanization | Standardized orthography across language families | Non-English proper names | RR (Korean), Hepburn (Japanese), IAST (Sanskrit), exact diacritics (Arabic/Polynesian/Inuit/Norse) | Missing diacritics or non-standard romanization | `03_英文版改寫.md`:13, `英文版評估.md`:64 |
| 31 | R3 英文版改寫 | YouTube Metadata Constraints | YouTube title and description specifications | YouTube copy | Title ≤ 60 chars; description 3–5 lines + sources cited | Title > 60 chars fails validation | `03_英文版改寫.md`:22 |
| 32 | R3 英文版改寫 | Cut & Semantic Adjustment Log | Audit trail of editorial trims | Chinese vs English script | Section 5 table/list of trimmed scenes and hedged meanings | Undocumented factual divergence fails check | `03_英文版改寫.md`:23 |
| 33 | R4 原稿保護 | Script Immutability | Existing Chinese scripts must remain unmodified | Git worktree | Zero git modifications in `04_腳本庫/*.md` (excluding new subdirs) | Modifying original script violates hard constraint | `README.md`:23, `ORIGINAL_REQUEST.md`:45 |
| 34 | R4 原稿保護 | Dual-Workspace Synchronization | Deliverables mirrored to both environments | Generated files | Identical files in both worktree and `/Users/kimjoo/Downloads/NTNU Insta` | Missing files in either directory fails acceptance | `ORIGINAL_REQUEST.md`:46 |

---

## 4. Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | R1 網路考據 | Early scripts (`A-01`, `A-02`, `A-03`, `A-04`, `A-06`, `H-七夕`) lacking `⚠ 待查核清單` | The early scripts do not contain a formal `⚠ 待查核清單` section (they only contain "首留言考據" or "考據備忘"). The fact-checker must record Section 一 as "原稿無待查核清單", and migrate all audited statements into Section 二 ("清單以外發現的問題"). |
| 2 | R1 網路考據 | Claims from club lecture PPTs (`中國星座（師大天文社）.pptx`) | Several early scripts (`A-01`, `A-02`, `A-03`) cite internal club lecture slides as primary sources (e.g. "東夷—青龍", "樓人"). Fact-checker must recognize these as secondary or tertiary club hypotheses, evaluate them critically, and reclassify them as "一說" or "？ 無法證實" unless ancient epigraphic/classical sources (e.g. 濮陽西水坡 M45 蚌塑龍虎, 尚書) confirm them. |
| 3 | R1 網路考據 | Ancient vs Modern Coordinates (Precession) | `A-01` claims Spring Equinox sunset "龍抬頭" (Horn mansion rises in the East). 3,000 years ago, precession placed the vernal equinox near Taurus/Aries, and the dragon's head rose at dusk in early spring; today, due to 2,500+ years of precession, the rising time has shifted by over a month. Fact-checker must note the discrepancy between ancient astronomical reality and modern sky alignment. |
| 4 | R2 審稿Critic | Ultra-short episode `H-七夕` | `H-七夕` is only 42 seconds long (~170 words), designed as an introductory hook. Screenplay and pacing critics must evaluate it under short-hook criteria rather than full 3–4 minute criteria, while still enforcing speed ≤ 4.5 chars/sec and card limits. |
| 5 | R2 審稿Critic | Late deep episodes exceeding 240 seconds (`A-13`: 283s, `A-14`: 288s, `A-15`: 246s) | These episodes were expanded to deep-dive length. The Screenplay/Pacing critic (`敘事`) must flag the excess length against the ideal 180s/240s threshold, noting where fat can be trimmed or chapters condensed. |
| 6 | R2 審稿Critic | Korean Romanization in `A-04` | `A-04` script writes "JikNyeo, HaGo, CheonJin". Under Korean Revised Romanization (RR), 직녀 undergoes nasal assimilation (ㄱ + ㄴ -> ㅇ + ㄴ) and is transcribed phonetically as *Jingnyeo*, not *JikNyeo*. Language and Cultural critics must flag this error. |
| 7 | R3 英文版改寫 | Severe Length Discrepancy in Late Episodes | `A-13` (283s, 1,077 chars) and `A-14` (288s, 1,138 chars) exceed the 180s English cap by over 55%. Translating directly would produce ~700 English words (requiring ~270s). The English adapter must aggressively condense shots, merge background explanations, and cut 35–40% of non-essential anecdotes to achieve ≤ 180s and ≤ 2.6 words/sec. |
| 8 | R3 英文版改寫 | Non-existent Directories & Glossary File | `04_腳本庫/_審稿/`, `04_腳本庫/_英文版/`, and `06_發布月曆/英文譯名表.csv` do not exist in the repository prior to pipeline execution. Tools must automatically create parent directories before writing. |
| 9 | R3 英文版改寫 | Complex Diacritical Fonts & Arabic Right-to-Left (RTL) | Arabic names (*al-Thurayyā*, *al-Wasm*, *al-Murabbaʿāniyya*) and Inuktitut/Norse orthography require strict UTF-8 preservation. On Canva and subtitles, Arabic diacritics must not be stripped, and English scripts must provide phonetic approximations for spoken VO. |
| 10 | R3 英文版改寫 | Astronomical Separation in 3D Space (`H-七夕`) | `H-七夕` asserts Vega (25 ly) and Altair (17 ly) are separated by 16 light-years. Calculating distance between two stars in 3D Cartesian space: with angular separation θ ≈ 34.2° and distances $d_1 = 25.04$ ly, $d_2 = 16.73$ ly, the law of cosines gives $D = \sqrt{d_1^2 + d_2^2 - 2 d_1 d_2 \cos \theta} \approx \sqrt{627 + 280 - 2(25.04)(16.73)(0.827)} \approx \sqrt{907 - 693} = \sqrt{214} \approx 14.6$–15.2 ly (often cited as 15–16 ly). The English adapter and astronomical fact-checker must verify this figure. |

---

## 5. Caveats

1. **Absence of Pre-existing `_審稿/` and `_英文版/` folders**:
   - The directory listing confirms that `04_腳本庫/_審稿/` and `04_腳本庫/_英文版/` do not currently exist. All downstream agents must ensure their file writing routines create parent directories (`mkdir -p`).
2. **`英文譯名表.csv` Creation Timing**:
   - `06_發布月曆/英文譯名表.csv` does not exist yet. As noted in `英文版評估.md`:66, it is created during the first adaptation and incrementally updated.
3. **Primary Source Availability**:
   - For early Chinese scripts citing the club's internal PPT (`中國星座（師大天文社）.pptx`), primary texts must be traced back to classical canons (e.g. 《史記・天官書》, 《漢書・天文志》, 《步天歌》, 《石氏星經》) rather than treating the slide deck as authoritative.
4. **Different Ephemeris Precision across Coordinates**:
   - Taipei coordinates are specified as 25.03°N, 121.56°E (with 25.033°N, 121.565°E used in late scripts). Both refer to central Taipei. Astronomical tools should accept either precision.

---

## 6. Conclusion

The SOP documents in `02_製作流程SOP/外包任務書/` and `02_製作流程SOP/英文版評估.md` provide a complete, mathematically constrained, and highly rigorous specification:
1. **R1 (網路考據)** requires exhaustive vetting of 9 scripts into `04_腳本庫/_審稿/{編號}_考據_gemini.md`, enforcing primary source attribution, 4-tier judgements, and PyEphem ephemeris verification for Taipei.
2. **R2 (四角色審稿)** requires 36 independent review reports (`04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`), strictly formatted with a 3-line header and a 6-column review table across 天文, 文化, 敘事, and 語言, strictly validating VO speech rate (≤ 4.5 chars/sec), card length (≤ 14 chars), and Taipei sky clocking.
3. **R3 (英文版改寫)** mandates 9 adapted English scripts (`04_腳本庫/_英文版/{編號}-EN-script-draft.md`) adhering to duration ≤ 180s, speech rate ≤ 2.6 words/sec, card length ≤ 6 words, the *"One sky. The [people] saw — [X]."* formula, multi-lingual romanization standards, and central logging in `06_發布月曆/英文譯名表.csv`.
4. **R4 (保護與同步)** strictly forbids in-place modifications to existing scripts and requires dual-worktree synchronization.

This specification mining report is immediately actionable for all downstream execution subagents.

---

## 7. Verification Method

To independently verify the facts, schemas, and numbers in this report:

1. **Verify File Existence & Paths**:
   ```bash
   cd "/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost"
   ls -la 02_製作流程SOP/外包任務書/
   ls -la 02_製作流程SOP/英文版評估.md
   ```
2. **Verify Output Paths and Rule Constraints**:
   - Check R1 schemas: `grep -n "交件格式" 02_製作流程SOP/外包任務書/01_網路考據.md`
   - Check R2 roles & limits: `grep -n -E "字/秒|字卡|檔名角色|三行" 02_製作流程SOP/外包任務書/02_審稿Critic.md`
   - Check R3 thresholds: `grep -n -E "words per second|180 seconds|One sky" 02_製作流程SOP/外包任務書/03_英文版改寫.md`
   - Check Romanization rules: `sed -n '60,68p' 02_製作流程SOP/英文版評估.md`
3. **Verify Script Target List**:
   - Check existence of all 9 scripts:
     ```bash
     for ep in A-01 A-02 A-03 A-04 A-06 H-七夕 A-13 A-14 A-15; do
       ls 04_腳本庫/${ep}*.md
     done
     ```
