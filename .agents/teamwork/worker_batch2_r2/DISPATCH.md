## 2026-10-31T21:16:41Z

You are the Batch 2 Remediation Worker.
Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_batch2_r2`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY FIRST STEP:
Read the following files before starting any work:
1. `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md` (especially sections `## 2026-10-31T21:03:02Z` and `## 2026-10-31T20:10:42Z`).
2. `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator_batch2_r2/SCOPE.md`.
3. `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/explorer_a16_a17/analysis.md` (contains complete line-by-line replacement chunks for A-16 and A-17 files).
4. `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/explorer_a18_a19/analysis.md` (contains complete line-by-line replacement chunks for A-18 and A-19 files).
5. `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/explorer_crosscut_sync/analysis.md` (contains runbook, test scripts, and sync protocols).

YOUR EXCLUSIVE WRITE OWNERSHIP:
- Worktree `04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md` (copy with 0 modifications)
- Worktree `04_腳本庫/_審稿/` 20 files:
  `A-16_考據_gemini.md`, `A-16_審稿-{天文,文化,敘事,語言}_antigravity.md`
  `A-17_考據_gemini.md`, `A-17_審稿-{天文,文化,敘事,語言}_antigravity.md`
  `A-18_考據_gemini.md`, `A-18_審稿-{天文,文化,敘事,語言}_antigravity.md`
  `A-19_考據_gemini.md`, `A-19_審稿-{天文,文化,敘事,語言}_antigravity.md`
- Synchronized mirror:
  `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/` (all 20 files must be copied after modification so SHA-256 matches 100%)

TASKS TO EXECUTE:
1. Copy `A-16` v0 script from Downloads to worktree `04_腳本庫/`:
   `cp -p "/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md" "04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md"`
   Verify that tracked original scripts in git are NOT modified (`python3 02_製作流程SOP/verification_harness/verify_sync.py --check-immutability-only`).
2. Apply the exact remediation changes for A-16 and A-17 per `explorer_a16_a17/analysis.md`:
   - Replace fake Barre Toelken (1987) title/pages with `The Anguish of Snails (2003)（未核頁碼）`.
   - Keep verified pages from local `07_資料來源/`: Don Childrey 2004 for A-16; Wissler & Duvall 1908 (noting Four-Tail Lodge on p. 42) & McClintock 1910 for A-17.
   - For all other external books not in local `07_資料來源/`: remove guessed page numbers and mark `（未核頁碼）`.
   - In `A-16_考據_gemini.md` Section 2, remove all 5 `✓ 證實` rows so Section 2 only has `✗`, `⚠`, `？`.
   - In `A-16_考據_gemini.md` & `A-16_審稿-天文_antigravity.md`: clarify Canopus color physics (F0 Ib/A9 II yellowish-white, appears red due to horizon extinction alt < 2° at Window Rock; or Haile 1947 Antares alternate).
   - In `A-16_審稿-敘事_antigravity.md`: ensure 01 opening sentence "同一片星空，納瓦荷人看見——" is preserved.
   - In `A-16_審稿-語言_antigravity.md`: ensure 05 `hooghan` definition is preserved.
   - In `A-17_審稿-天文_antigravity.md` & `A-17_審稿-敘事_antigravity.md`: ensure 18 Jupiter (Poïa) is preserved.
3. Apply the exact remediation changes for A-18 and A-19 per `explorer_a18_a19/analysis.md`:
   - For all external books not in `07_資料來源/` (Censorinus, Parker, Neugebauer, Hurst, Petrie, Buchwald, Ibn Qutayba, al-Sufi, Ibn Durayd, Ibn Manzur, Kunitzsch, Lane, etc.): remove guessed page numbers and mark `（未核頁碼）`. In A-19 考據, resolve contradictory "guessed page + 未核頁碼" to simply `（未核頁碼）`.
   - In `A-18_考據_gemini.md` Section 2 & `A-18_審稿-天文_antigravity.md`: add the 2027/01/25 Sirius timing (16:52 rise -> 21:00 alt 43.7° -> 22:21 culmination -> 03:51 set, 8 min shift).
   - In `A-18_審稿-敘事_antigravity.md`: do NOT suggest prepending text before 01 opening sentence.
   - In `A-19_審稿-天文_antigravity.md`: Canopus 18:11 rise / 01:17 set is correct with atmospheric refraction (-34'); change critique to `⚪可選` note confirming refraction.
   - In `A-19_審稿-敘事_antigravity.md`: preserve "人" in "同一片星空，古阿拉伯人看見——".
4. Run all verification scripts:
   - `python3 .agents/teamwork/explorer_crosscut_sync/verify_batch2_r2_rules.py`
   - `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 02_製作流程SOP/verification_harness/verify_batch2_ephemeris.py`
   - `python3 02_製作流程SOP/verification_harness/verify_sync.py --check-immutability-only`
   - `python3 02_製作流程SOP/verification_harness/verify_schemas.py --file 04_腳本庫/_審稿/<file> --type <research|critic>` for all 20 files!
5. Synchronize all 20 files to `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`:
   `cp -p 04_腳本庫/_審稿/A-1[6789]_*.md "/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/"`
   Verify identical SHA-256 between worktree and Downloads for all 20 files!

OUTPUT:
Write your changes log, test output evidence, and SHA-256 comparison table to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_batch2_r2/changes.md`
and write a comprehensive handoff report to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_batch2_r2/handoff.md`.
Send a completion message back to orchestrator when finished.
