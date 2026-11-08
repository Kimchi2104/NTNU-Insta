# Scope: Batch 2 R2 Remediation (A-16, A-17, A-18, A-19)

## Architecture & Code Layout
- Target files:
  - Worktree:
    - `04_腳本庫/_審稿/A-16_考據_gemini.md`
    - `04_腳本庫/_審稿/A-16_審稿-{天文,文化,敘事,語言}_antigravity.md`
    - `04_腳本庫/_審稿/A-17_考據_gemini.md`
    - `04_腳本庫/_審稿/A-17_審稿-{天文,文化,敘事,語言}_antigravity.md`
    - `04_腳本庫/_審稿/A-18_考據_gemini.md`
    - `04_腳本庫/_審稿/A-18_審稿-{天文,文化,敘事,語言}_antigravity.md`
    - `04_腳本庫/_審稿/A-19_考據_gemini.md`
    - `04_腳本庫/_審稿/A-19_審稿-{天文,文化,敘事,語言}_antigravity.md`
    - `04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md`
  - Downloads directory:
    - `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/` (all 20 files must match worktree byte-for-byte via SHA-256)
    - `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md` (source to copy to worktree)

## Feature Inventory & Remediation Items

| # | Item | Description | Milestone | Status |
|---|------|-------------|-----------|--------|
| 1 | Anti-Hallucination & Provenance | In A-16 考據 & 文化, remove fake book title/pages Barre Toelken (1987) *The Anguish of Arrival*; replace with *The Anguish of Snails* (2003) (未核頁碼) or Toelken & Scott (1969) (未核頁碼). Keep verified pages from local 07_資料來源/: Don Childrey 2004 for A-16 (pp. 18, 29-39, 42-73, 99-103; note p. 54 typo); Wissler & Duvall 1908 (pp. 5-7, 40-44, 58-65, 68-72) & McClintock 1910 (pp. 26-35, 217-218, 488-501, 521-524) for A-17. For all other external books/papers not in 07_資料來源/, remove guessed pages and mark "（未核頁碼）". | M1 | DONE |
| 2 | Section 2 Format | In all 4 考據 files, Section 2 (## 二、清單以外發現的問題) must ONLY contain ✗, ⚠, ？. Remove all ✓ rows (or merge into Section 1). Do not treat deleted scenes from header changelog as problems. | M1 | DONE |
| 3 | A-16 Specifics | Shot 16 Canopus color: F0 Ib/A9 II yellowish-white supergiant, appears red due to horizon extinction (alt < 2° at Window Rock) or Haile 1947 Antares alternate. Do NOT suggest altering 01 fixed opening sentence; do NOT suggest deleting 05 hooghan definition. | M1 | DONE |
| 4 | A-17 Specifics | Shot 18 Jupiter (Poïa): do NOT suggest deleting Jupiter in shot 18; it corresponds to shot 12 morning star family (2027/01/22 Taipei 19:30 alt 7°, 20:00 alt 14°). Four-Tail Lodge is on p. 42 of Wissler & Duvall 1908. | M1 | DONE |
| 5 | A-18 Specifics | Taipei 2027/01/25 Sirius timing: 16:52 rise -> 21:00 alt 43.7° -> 22:21 culmination -> 03:51 set (8 min shift from Jan 23). Add to A-18 考據 (Section 2 ⚠) & 審稿-天文. Do NOT suggest inserting text before 01 opening sentence. | M1 | DONE |
| 6 | A-19 Specifics | Shot 18 Canopus refraction timing: 18:11 rise -> 21:44 culmination -> 01:17 set is correct with refraction. Change critique to ⚪可選 note. Do NOT suggest deleting "人" from opening sentence. | M1 | DONE |
| 7 | A-16 v0 Sync | Copy A-16 v0 from Downloads/NTNU Insta/04_腳本庫/ to worktree 04_腳本庫/ (0 modifications). | M1 | DONE |
| 8 | Dual-Workspace Sync | Ensure all 20 files in `04_腳本庫/_審稿/` match byte-for-byte (identical SHA-256) between worktree and `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`. | M1 | DONE |
| 9 | Verification Scripts | Run `verify_schemas.py` and `verify_batch2_ephemeris.py` to ensure 100% compliance. | M1 | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Batch 2 R2 Remediation | All 9 remediation items above across A-16, A-17, A-18, A-19 | none | DONE |
