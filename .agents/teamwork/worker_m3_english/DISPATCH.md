# Task Assignment: Milestone 3 (R3 英文版改寫與譯名表) + 3項關鍵勘誤修訂

## Target
1. Produce 9 English adaptation script drafts:
   `04_腳本庫/_英文版/{編號}-EN-script-draft.md` for `A-01`, `A-02`, `A-03`, `A-04`, `A-06`, `H-七夕`, `A-13`, `A-14`, `A-15`.
2. Produce Master Glossary CSV:
   `06_發布月曆/英文譯名表.csv`
3. Mirror all 10 files to `/Users/kimjoo/Downloads/NTNU Insta/`.
4. Apply the 3 critical errata from DeepInvestigator to `04_腳本庫/_審稿/` and mirror them:
   - `A-02_考據_gemini.md` & `A-02_審稿-天文_antigravity.md`: 太微右垣西上將為室女/獅子座腰部（σ Leo, HIP 55434），非后髮座；太微左垣末端東上將才接后髮座；五帝座一為太微垣內中央。
   - `A-03_考據_gemini.md` & `A-03_審稿-天文_antigravity.md`: 2026/09/04 台北室宿一 17:33:40 CST 升起，20:00 Alt = +32.08°, Az = 92.22°；壁宿一 18:42:02 CST 升起，20:00 Alt = +16.65°, Az = 86.78°。
   - `A-06_考據_gemini.md` & `A-06_審稿-文化_antigravity.md`: al-Thurayya「只取兩顆」改判為 `✗ 錯誤`（或 `⚠ 需限定`），因原典為整團昴宿星團（6-7星），腳本誤讀了 Stellarium 兩個自連錨點。

## Deliverables
Write your handoff report to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_m3_english/handoff.md`.


## 2026-10-28T09:57:49Z
You are the R3 English Script Adapter & Glossary Master for the NTNU Astronomy Club "World Sky Cultures" video series workflow.
Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_m3_english`
Your assignment file is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_m3_english/DISPATCH.md`

MANDATORY FIRST STEP: Read the authoritative user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Also read:
- `PROJECT.md` at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator/PROJECT.md`
- SOPs `02_製作流程SOP/外包任務書/03_英文版改寫.md` and `02_製作流程SOP/英文版評估.md`
- All fact-checking reports in `04_腳本庫/_審稿/{編號}_考據_gemini.md` and critic reports in `04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`.

Your tasks:
Part 1: Produce all 9 adapted English scripts in `04_腳本庫/_英文版/{編號}-EN-script-draft.md` for:
`A-01`, `A-02`, `A-03`, `A-04`, `A-06`, `H-七夕`, `A-13`, `A-14`, `A-15`.
And mirror each to `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_英文版/{編號}-EN-script-draft.md`.

Every English script MUST strictly satisfy:
1. Adaptation philosophy: Trim 15–30% of explanatory fat from the Chinese originals to ensure concise, natural English delivery.
2. Hard quantitative thresholds:
   - Total duration: <= 180 seconds
   - Speech pace: <= 2.6 words/sec per shot
   - Graphic card: <= 6 English words per on-screen text card
   - YouTube title: <= 60 characters
3. Fixed opening formula:
   First line starts with: *"One sky. The [people] saw — [X]."*
4. Mandatory 5-section structure in each draft:
   - Section 1: Shot table (`| Shot | Sec | Voice-over | On-screen text | Words/sec |`)
   - Section 2: Summary metrics (Total seconds, Total words, Average words/sec)
   - Section 3: Glossary table (`| Chinese | English used | Notes |`)
   - Section 4: Social platform copy:
     - YouTube title (<= 60 chars)
     - YouTube description (3–5 lines + sources cited)
     - Facebook caption
   - Section 5: Cut & semantic adjustment log (explaining trims and adaptations)
5. Multi-lingual Romanization & Terminology:
   - Chinese asterisms: Pinyin + English meaning (*Xin, "the Heart"*). Call them *asterisms*, NEVER *constellations*.
   - Korean: Revised Romanization (RR), e.g. *Jingnyeo*, *Hago*, *Cheonjin*, *Cheonsang Yeolcha Bunya Ji Do*.
   - Japanese: Modified Hepburn (*Subaru*, *Kitora*).
   - Sanskrit: IAST with diacritics (*Kṛttikā*, *Nakṣatra*, *Abhijit*).
   - Arabic & Indigenous: Exact diacritics (*al-Thurayyā*, *al-Twaibiʿ*, *al-Iklīl*, *Aagjuuk*, *Tukturjuit*, *Úlfs kjaptr*, *Fiskikarlar*).

Part 2: Create Master Glossary CSV at `06_發布月曆/英文譯名表.csv`
And mirror to `/Users/kimjoo/Downloads/NTNU Insta/06_發布月曆/英文譯名表.csv`.
Columns: `Chinese,English,Category,Episode,Notes`
Compile all proper nouns, star names, asterisms, cultural terms, and book titles from all 9 episodes.

Part 3: Apply the 3 critical errata from DeepInvestigator and mirror to `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`:
1. `A-02_考據_gemini.md` & `A-02_審稿-天文_antigravity.md`:
   Correct the description of 太微右垣（西牆）: 由南至北五星為右執法（HIP 57757, β Vir）→ 西上將（HIP 55434, σ Leo）→ 西次將（HIP 55642, ι Leo）→ 西次相（HIP 54879, θ Leo Chertan）→ 西上相（HIP 54872, δ Leo Zosma），位於室女與獅子座腰部；接后髮座（α Com）的是東牆太微左垣最北端的「東上將」；五帝座一為太微垣內中央。
2. `A-03_考據_gemini.md` & `A-03_審稿-天文_antigravity.md`:
   Correct 2026/09/04 台北室宿一與壁宿一升起數據：
   - 室宿一（Markab, α Peg, HIP 113963）：17:33:40 CST 升起，20:00 CST Alt = +32.08°, Az = 92.22°（21:00 達 +45.65°）。
   - 壁宿一（Algenib, γ Peg, HIP 1067）：18:42:02 CST 升起，20:00 CST Alt = +16.65°, Az = 86.78°（21:00 達 +30.25°）。
3. `A-06_考據_gemini.md` & `A-06_審稿-文化_antigravity.md`:
   Correct al-Thurayya「只取兩顆星」claim: 改判為 `✗ 錯誤`（或 `⚠ 需限定`），因 Stellarium JSON lines 是兩個長度為零的自連標記錨點（HIP 17608 Merope 與 HIP 18163 背景暗星），原典實為整團昴宿星團（Pleiades cluster, 6–7星），腳本誤讀了數據格式。

Part 4: Run the verification harness to validate all 55 deliverables:
Command: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_all.py"`
Ensure all suites pass (Ephemeris, Immutability, Schemas, Sync).

Part 5: Write your handoff report to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_m3_english/handoff.md`.
Communicate back with send_message when done.
