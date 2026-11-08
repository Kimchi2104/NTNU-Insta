# Project: Batch 2 NTNU Insta World Sky Cultures (萬國星空)

## Architecture
- Fact-Checking Reports: `04_腳本庫/_審稿/{編號}_考據_gemini.md` (A-16, A-17, A-18, A-19)
- Critique Reports: `04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md` where 角色 ∈ {天文, 文化, 敘事, 語言} (16 files)
- Reference SOPs: `02_製作流程SOP/外包任務書/01_網路考據.md`, `02_製作流程SOP/外包任務書/02_審稿Critic.md`
- Target Scripts: `04_腳本庫/A-16*.md`, `A-17*.md`, `A-18*.md`, `A-19*.md`
- Astronomical Tools: `08_python_script/` (Skyfield, PyEphem, `de421.bsp`)

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Survey Scripts & SOPs | Check A-16~A-19 scripts, SOP specs, astronomical scripts | M1 | SOP & Request |
| 2 | A-16 Fact-Checking | 納瓦荷只在冬天說的星星故事 考據報告 (4 sections, 6-col table) | M2 | SOP 01 |
| 3 | A-16 4-Role Critique | 天文, 文化, 敘事, 語言 獨立審稿 (3-line summary, 6-col table) | M2 | SOP 02 |
| 4 | A-17 Fact-Checking | 黑腳族留在天上的六個孩子 考據報告 | M3 | SOP 01 |
| 5 | A-17 4-Role Critique | 天文, 文化, 敘事, 語言 獨立審稿 | M3 | SOP 02 |
| 6 | A-18 Fact-Checking | 古埃及叫醒尼羅河的天狼星 考據報告 | M4 | SOP 01 |
| 7 | A-18 4-Role Critique | 天文, 文化, 敘事, 語言 獨立審稿 | M4 | SOP 02 |
| 8 | A-19 Fact-Checking | 古阿拉伯兩隻鴕鳥與擋路的老人星 考據報告 | M5 | SOP 01 |
| 9 | A-19 4-Role Critique | 天文, 文化, 敘事, 語言 獨立審稿 | M5 | SOP 02 |
| 10 | Quality & Sync Check | Format checks, 0 script edits, SHA-256 dual sync | M6 | Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Survey | Verify files, scripts, SOP rules, python env | None | DONE |
| 2 | Episode A-16 | A-16 fact checking + 4 critiques | M1 | DONE |
| 3 | Episode A-17 | A-17 fact checking + 4 critiques | M1 | DONE |
| 4 | Episode A-18 | A-18 fact checking + 4 critiques | M1 | DONE |
| 5 | Episode A-19 | A-19 fact checking + 4 critiques | M1 | DONE |
| 6 | Verification & Dual Sync | Audit, SHA-256 sync between worktrees | M2, M3, M4, M5 | DONE |

## Code Layout
- Worktree root: `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost`
- Target outputs: `04_腳本庫/_審稿/`
- Dual destination: `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`
- Script sources (READ ONLY): `04_腳本庫/`
- Reference datasets: `07_資料來源/`
- Python astronomical scripts: `08_python_script/`
