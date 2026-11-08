## 2026-10-31T21:03:58Z
You are the Project Orchestrator for Batch 2 R2 Remediation of the NTNU Astronomy Club "World Sky Cultures" (萬國星空) short video series.

Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator_batch2_r2`

Please read the user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md` (specifically section `## 2026-10-31T21:03:02Z`).

### Scope of Remediation
Address all items specified in `## 2026-10-31T21:03:02Z`:
1. Strict Anti-Hallucination & Provenance:
   - In `A-16_考據_gemini.md` & `A-16_審稿-文化_antigravity.md`: remove fake book title/pages `Barre Toelken, The Anguish of Arrival (1987), pp. 129–130` (correct: *The Anguish of Snails*, 2003, 未核頁碼; or Toelken & Scott 1969, 未核頁碼).
   - Only keep verified page numbers from local `07_資料來源/`:
     - `A-16`: Don Childrey 2004 *Star Trails: Navajo* (pp. 18, 29–39, 42–73, 99–103; note p. 54 summer/winter Hai/Shi typo).
     - `A-17`: Wissler & Duvall 1908 (pp. 5–7, 40–44 [point out Four-Tail Lodge on p. 42], 58–65, 68–72) & McClintock 1910 (pp. 26–35, 217–218, 488–501, 521–524).
   - For all other external books/papers not in `07_資料來源/`: remove guessed page numbers and directly mark "（未核頁碼）" (do NOT contradict by writing guessed page numbers and then "未核頁碼").
2. Section 2 Format (`## 二、清單以外發現的問題`):
   - Per `01_網路考據.md` line 30, Section 2 must ONLY contain `✗`, `⚠`, `？`! Remove all `✓ 證實` rows from Section 2 (or merge into Section 1 if extending the checklist).
   - Do not treat deleted scenes from header changelog as problems.
3. Specific Factual/Astronomical Corrections:
   - `A-16`: Canopus color in shot 16 (yellowish-white supergiant F0 Ib/A9 II, appears red due to horizon atmospheric extinction at Window Rock, alt < 2°; or Haile 1947 Antares alternate). Do NOT suggest altering 01 fixed opening sentence; do NOT suggest deleting 05 `hooghan` definition.
   - `A-17`: Do NOT suggest deleting Jupiter (Poïa) in shot 18 (corresponds to shot 12 morning star family; 2027/01/22 Taipei 19:30 alt 7°, 20:00 alt 14°).
   - `A-18`: Taipei 2027/01/25 Sirius timing has 8-minute shift from Jan 23: 16:52 rise -> 21:00 alt 43.7° -> 22:21 culmination -> 03:51 set. Add to `A-18_考據_gemini.md` (Section 2 `⚠`) and `A-18_審稿-天文_antigravity.md`. Do NOT suggest inserting text before 01 opening sentence.
   - `A-19`: Canopus refraction timing 18:11 rise -> 21:44 culmination -> 01:17 set is correct with refraction. Change critique to `⚪可選` note. Do NOT suggest deleting "人" from opening sentence.
   - Copy `04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md` from `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/` to worktree `04_腳本庫/` (0 modifications).
4. Synchronization:
   - Ensure all 20 files in `04_腳本庫/_審稿/` match byte-for-byte (identical SHA-256) between the worktree and `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`.
5. Validation:
   - Run verification harness scripts (`verify_schemas.py`, `verify_batch2_ephemeris.py`).
   - Maintain `progress.md` and `BRIEFING.md`.
   - Dispatch workers/reviewers as appropriate, verify everything, and notify Sentinel when finished with a victory claim.
