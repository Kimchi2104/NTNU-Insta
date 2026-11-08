## 2026-10-31T20:21:01Z

You are Worker A-19 (teamwork_preview_worker) responsible for executing Episode A-19 of Batch 2:
`A-19-古阿拉伯兩隻鴕鳥與擋路的老人星`

Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_a19`

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY READING:
Read `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md` (specifically `## 2026-10-31T20:10:42Z` and `## 2026-10-28T09:54:46Z`).
Read `02_製作流程SOP/外包任務書/01_網路考據.md`
Read `02_製作流程SOP/外包任務書/02_審稿Critic.md`
Read reference examples: `04_腳本庫/_審稿/A-13_考據_gemini.md`, `04_腳本庫/_審稿/A-13_審稿-天文_antigravity.md`, etc.

TARGET SCRIPT:
- `04_腳本庫/A-19-古阿拉伯兩隻鴕鳥與擋路的老人星-逐字稿-v0.md` (Read from `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-19-古阿拉伯兩隻鴕鳥與擋路的老人星-逐字稿-v0.md` or git `origin/main`).
- NEVER MODIFY THE ORIGINAL SCRIPT (0 modifications).

PRIMARY SOURCES TO CONSULT:
- `07_資料來源/Arabic Ancient/arabic_ancient_star_chart.rtf`
- `07_資料來源/Stellarium/stellarium-skycultures-master/arabic_ancient/`
- `07_資料來源/Stellarium/stellarium-skycultures-master/arabic_arabian_peninsula/`
- `07_資料來源/_整理CSV/Arabic Ancient.csv`
- `07_資料來源/_整理CSV/Arabic Arabian Peninsula.csv`
- `07_資料來源/_整理CSV/Arabic Lunar Stations.csv`
- Classical Arabic astronomical sources: al-Ṣūfī (Book of Fixed Stars / Kitāb Ṣuwar al-Kawākib), Ibn Qutayba (Kitāb al-Anwāʼ), Khalid al-Ajaji, Paul Kunitzsch.

ASTRONOMICAL VERIFICATION:
- Use `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` with Skyfield 1.54 and `de421.bsp` (at worktree root).
- Compute exact celestial coordinates, azimuth, altitude, rise/transit/set for Taipei (25.03°N, 121.56°E, UTC+8) for Canopus (Suhail, α Car, HIP 30438 - note max altitude in Taipei is ~12.3° above southern horizon!), Two Male Ostriches (al-Ẓalīmān: Achernar α Eri HIP 7588 & Fomalhaut α PsA HIP 113368), Ostrich Nest (al-Udḥiyy / Azha in Eridanus), Sirius (al-Shiʼrā al-Yamāniya) & Procyon (al-Shiʼrā al-Shāmiya).

DELIVERABLES (5 files, written to `04_腳本庫/_審稿/`):
1. `04_腳本庫/_審稿/A-19_考據_gemini.md` (4 sections: 一、待查核清單逐條結果, 二、清單以外發現的問題, 三、可以加進影片的好材料, 四、參考資料總表. 6-col table. Marks `✓`, `✗`, `⚠`, `？`. If page unverified from primary source, mark "未核頁碼").
2. `04_腳本庫/_審稿/A-19_審稿-天文_antigravity.md` (3-line summary: 整體評價, 最重要的三個問題, 沒把握的地方. 6-col table: 嚴重度 `🔴`/`🟡`/`⚪`, 位置, 原文, 問題, 建議改法, 依據. Appendix: 台北星空對時報告與星名交叉對照表).
3. `04_腳本庫/_審稿/A-19_審稿-文化_antigravity.md` (Cultural/mythological critic: Bedouin desert navigation, Suhail / Canopus murder myth and fleeing south, two sisters mourning Sirius & weeping Procyon, Ostriches crossing Milky Way River).
4. `04_腳本庫/_審稿/A-19_審稿-敘事_antigravity.md` (Pacing/narrative critic: hook, rhythm, voiceover ≤ 4.5 chars/s, text card ≤ 14 chars, opening format "同一片星空，古阿拉伯看見——", next episode teaser).
5. `04_腳本庫/_審稿/A-19_審稿-語言_antigravity.md` (Linguistic critic: Taiwan Traditional Chinese terminology, Arabic transliteration with macrons/diacritics, subtitle reading comfort, clarity).

VALIDATION:
Run `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_schemas.py" --file "04_腳本庫/_審稿/A-19_..."` for all 5 files. Fix any validation issues until 100% PASS.

Write your completion report in `.agents/teamwork/worker_a19/handoff.md` and message the orchestrator.
