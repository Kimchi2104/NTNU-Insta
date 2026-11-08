# Task Assignment: SOP & Rubric Specification Mining

## Target
Investigate all SOP documents under `02_製作流程SOP/外包任務書/` and `02_製作流程SOP/英文版評估.md`.

## Deliverable
Write your comprehensive report to `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/survey_spec_miner/handoff.md`.
## 2026-10-28T09:08:56Z
You are the SOP Specification Miner for the NTNU Astronomy Club "World Sky Cultures" video series workflow.
Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/survey_spec_miner`
Your assignment file is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/survey_spec_miner/DISPATCH.md`

MANDATORY FIRST STEP: Read the authoritative user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`

Your task:
Examine the authoritative SOP specifications in the repository:
- `02_製作流程SOP/外包任務書/README.md`
- `02_製作流程SOP/外包任務書/01_網路考據.md`
- `02_製作流程SOP/外包任務書/02_審稿Critic.md`
- `02_製作流程SOP/外包任務書/03_英文版改寫.md`
- `02_製作流程SOP/英文版評估.md`

Extract and document every requirement, rule, and rubric:
1. For R1 (01 網路考據):
   - Output filename pattern (`04_腳本庫/_審稿/{編號}_考據_gemini.md`)
   - Four required sections: (1) 待查核清單逐條結果, (2) 清單以外發現的問題, (3) 可以加進影片的好材料, (4) 參考資料總表
   - Required table schemas, citation rules, astronomical verification rules (coordinates, databases like SIMBAD, Gaia/Hipparcos, IAU WGSN, ephemeris tools).
2. For R2 (02 四角色審稿):
   - Output filename pattern (`04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`)
   - The four independent roles: 天文, 文化, 敘事, 語言
   - Three-line summary schema (整體評價、最重要的三個問題、沒把握的地方)
   - Review opinion table schema (`| 嚴重度（🔴必改／🟡建議／⚪可選） | 位置（鏡號或段落） | 原文 | 問題 | 建議改法 | 依據 |`)
   - Voice-over speed limits (<= 4.5 chars/sec), on-screen text limits (<= 14 chars), Taiwan traditional Chinese phrasing, and astronomical verification calculations for Taipei (25.03°N, 121.56°E, UTC+8).
3. For R3 (03 英文版改寫):
   - Output filename pattern (`04_腳本庫/_英文版/{編號}-EN-script-draft.md`)
   - Glossary file: `06_發布月曆/英文譯名表.csv`
   - Quantitative thresholds: total seconds <= 180s, each shot <= 2.6 words/sec, on-screen text <= 6 English words
   - Opening formula: "One sky. The [people] saw — [X]."
   - Required sections in the English draft: shot table, total seconds/words, glossary table, YouTube title (<= 60 chars) + description + Facebook caption, cut/adjustment list.
   - Romanization and proper noun rules (Pinyin + asterism, Revised Romanization, Modified Hepburn, IAST, Arabic/Indigenous diacritics).
