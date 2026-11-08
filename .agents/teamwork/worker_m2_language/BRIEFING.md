# BRIEFING — 2026-10-28T09:50:30Z

## Mission
Perform independent language and readability review (台灣繁體中文主編／配音修辭顧問) for 9 episodes of NTNU Astronomy Club "World Sky Cultures" video series.

## 🔒 My Identity
- Archetype: critic
- Roles: reviewer, critic, specialist
- Working directory: /Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/worker_m2_language
- Original parent: 99335e05-87c1-4071-bf18-9e62ab38c021
- Milestone: M2
- Instance: 1 of 1

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code or original scripts in 04_腳本庫/
- Exclusive write ownership: `04_腳本庫/_審稿/{編號}_審稿-語言_antigravity.md` for the 9 target episodes (`A-01`, `A-02`, `A-03`, `A-04`, `A-06`, `H-七夕`, `A-13`, `A-14`, `A-15`) and mirror to `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`
- Every report MUST begin with 3-line summary:
  `整體評價：...`
  `最重要的三個問題：...`
  `沒把握的地方：...`
- Every report MUST contain the 6-column review table:
  `| 嚴重度（🔴必改／🟡建議／⚪可選） | 位置（鏡號或段落） | 原文 | 問題 | 建議改法 | 依據 |`
- Role Rubric Focus (`語言`):
  - Taiwan Traditional Chinese terminology (台灣繁體中文用語; flag and fix mainland vocabulary: 視頻, 質量, 信息, 軟件, etc.)
  - Spoken readability: Can a voice actor breathe comfortably? Homophone confusion check (e.g. 必需 vs 必須, 唯 vs 惟)
  - Pronunciation guides (zhuyin/furigana) for foreign/ancient/obscure names in 配音提示
  - Punctuation, unit conventions, fullwidth vs halfwidth consistency
  - Suggested rewrites must strictly comply with voice-over <= 4.5 chars/sec, text card <= 14 chars

## Current Parent
- Conversation ID: 99335e05-87c1-4071-bf18-9e62ab38c021
- Updated: 2026-10-28T09:50:30Z

## Review Scope
- **Files to review**: 9 target scripts in `04_腳本庫/`: A-01, A-02, A-03, A-04, A-06, H-七夕, A-13, A-14, A-15
- **Fact check references**: `04_腳本庫/_審稿/{編號}_考據_gemini.md`
- **SOP**: `02_製作流程SOP/外包任務書/02_審稿Critic.md`
- **Review criteria**: Language, Taiwan Traditional Chinese phrasing, rhythm/breathing, homophones, phonetic guides, pacing constraints

## Key Decisions Made
- Fully completed all 9 independent language and readability reviews.
- Formatted all files with mandatory 3-line summary and 6-column review tables.
- Validated with `verify_schemas.py` — 100% pass, 0 errors, 0 warnings.
- Mirrored all 9 files to `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/` with verified SHA-256 matches.
- Confirmed zero modifications to original scripts via `verify_sync.py` (git immutability).

## Artifact Index
- `.agents/teamwork/worker_m2_language/progress.md` — Liveness & task progress
- `.agents/teamwork/worker_m2_language/handoff.md` — Final handoff report
- `04_腳本庫/_審稿/{編號}_審稿-語言_antigravity.md` — 9 deliverable review files
- `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/{編號}_審稿-語言_antigravity.md` — 9 mirrored deliverable review files

## Review Checklist
- **Items reviewed**: 9 / 9 episodes (A-01, A-02, A-03, A-04, A-06, H-七夕, A-13, A-14, A-15)
- **Verdict**: approve (all 9 language review deliverables complete and verified)
- **Unverified claims**: 0

## Attack Surface
- **Hypotheses tested**: Speech rate <= 4.5 chars/sec, card text <= 14 chars, homophone pitfalls, dialectal contamination, pronunciation ambiguities.
- **Vulnerabilities found**: "直녀" typo in A-04, card overflow > 14 chars in A-06/A-13/A-14/A-15, speech rate > 6.0 in H-七夕/A-01, "算雨" homophone with "酸雨" in A-13, mainland terms "一只" in A-01.
- **Untested angles**: None.

## Loaded Skills
- None
