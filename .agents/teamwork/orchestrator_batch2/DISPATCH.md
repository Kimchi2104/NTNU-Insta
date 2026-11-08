## 2026-10-31T20:12:29Z

You are the Project Orchestrator for Batch 2 of the NTNU Astronomy Club "World Sky Cultures" (萬國星空) short video series.

Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator_batch2`

Please read the user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md` (specifically section `## 2026-10-31T20:10:42Z`).

### Task Scope
Execute:
1. `02_製作流程SOP/外包任務書/01_網路考據.md` for episodes `A-16`, `A-17`, `A-18`, `A-19`
2. `02_製作流程SOP/外包任務書/02_審稿Critic.md` (4 independent roles: 天文, 文化與原典, 敘事與節奏, 語言與可讀性) for `A-16`, `A-17`, `A-18`, `A-19`

Target Scripts:
- `04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md`
- `04_腳本庫/A-17-黑腳族留在天上的六個孩子-逐字稿-v0.md`
- `04_腳本庫/A-18-古埃及叫醒尼羅河的天狼星-逐字稿-v0.md`
- `04_腳本庫/A-19-古阿拉伯兩隻鴕鳥與擋路的老人星-逐字稿-v0.md`
(If any script is not present in the current worktree, check `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/` or git `origin/main`).

Deliverables (20 files total):
- 4 Fact-Checking Reports:
  - `04_腳本庫/_審稿/A-16_考據_gemini.md`
  - `04_腳本庫/_審稿/A-17_考據_gemini.md`
  - `04_腳本庫/_審稿/A-18_考據_gemini.md`
  - `04_腳本庫/_審稿/A-19_考據_gemini.md`
- 16 Critique Reports:
  - `04_腳本庫/_審稿/{編號}_審稿-{天文|文化|敘事|語言}_antigravity.md` (for A-16, A-17, A-18, A-19)

### Key Rules & Constraints
1. **Never modify original script files** in `04_腳本庫/` (0 modifications).
2. **Strict anti-hallucination**: Never invent page numbers or citations. If a primary page number is unverified, honestly mark "未核頁碼".
3. **No hallucinated asterisms/myths**: Every assertion must have real verifiable primary/scholarly sources.
4. **Astronomical calculations**: The "天文" role must verify Taipei (25.03°N, 121.56°E, UTC+8) celestial alignments, azimuth, altitude, and rise/set times using Skyfield/PyEphem (check `de421.bsp` or scripts in `08_python_script/`).
5. **Format requirements**:
   - Fact checking: 4 sections, 6-column table, judgment marks only `✓`, `✗`, `⚠`, `？`.
   - Critique: 3-line header summary, 6-column table with `🔴` / `🟡` / `⚪`, voiceover ≤ 4.5 chars/sec, text card ≤ 14 chars, Traditional Chinese (Taiwan).
6. **Dual-workspace synchronization**: All 20 files must exist and be byte-for-byte SHA-256 identical in both:
   - `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/04_腳本庫/_審稿/`
   - `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`

### Subagent Orchestration & Tracking
- Decompose the work and dispatch to specialized worker subagents (e.g. per episode or per role).
- Maintain your `progress.md` and `BRIEFING.md` in `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator_batch2/`.
- Keep `progress.md` updated with timestamps and completion status.
- Once all 20 deliverables are generated, validated, and synchronized, send a completion message with victory claim and handoff report back to Sentinel.
