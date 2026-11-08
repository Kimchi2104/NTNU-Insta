# Task Assignment: Gate Review - Workflow & Schema Reviewer

## Role
Workflow & Schema Reviewer

## Target
Inspect all 55 deliverable files and run the master verification test runner:
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_all.py"`

Deliver your review report to `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/reviewer_1/handoff.md` with explicit verdict: APPROVE or REQUEST_CHANGES.

## 2026-10-28T10:17:33Z
You are reviewer_1 (Workflow & Schema Reviewer) for the NTNU Astronomy Club "World Sky Cultures" video series workflow.
Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/reviewer_1`
Your assignment file is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/reviewer_1/DISPATCH.md`

MANDATORY FIRST STEP: Read the authoritative user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`

Also read:
- `PROJECT.md` at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator/PROJECT.md`
- `TEST_READY.md` at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/TEST_READY.md`
- `TEST_INFRA.md` at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/TEST_INFRA.md`

Your task:
1. Execute the master test runner and review the output:
   `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_all.py"`
2. Inspect the 55 deliverable files:
   - 9 Research files (`04_腳本庫/_審稿/{編號}_考據_gemini.md`)
   - 36 Critic files (`04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`)
   - 9 English adaptation drafts (`04_腳本庫/_英文版/{編號}-EN-script-draft.md`)
   - Master Glossary CSV (`06_發布月曆/英文譯名表.csv`)
3. Verify that:
   - All required sections, table schemas, severity tiers, and 3-line summaries are present and correctly structured.
   - All English drafts adhere to duration <= 180s, speech rate <= 2.6 words/sec, cards <= 6 words, opening formula, and YouTube title <= 60 chars.
4. Deliver your review report to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/reviewer_1/handoff.md`.
Your report MUST explicitly state your verdict: `APPROVE` or `REQUEST_CHANGES`.
Communicate back with send_message when done.
## 2026-10-31T20:34:54Z
You are Reviewer 1 (teamwork_preview_reviewer) for Batch 2 (A-16, A-17, A-18, A-19).

Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/reviewer_1`

Read:
- `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`
- `02_製作流程SOP/外包任務書/01_網路考據.md`
- `02_製作流程SOP/外包任務書/02_審稿Critic.md`

Your tasks:
1. Inspect all 4 Fact-Checking reports:
   - `04_腳本庫/_審稿/A-16_考據_gemini.md`
   - `04_腳本庫/_審稿/A-17_考據_gemini.md`
   - `04_腳本庫/_審稿/A-18_考據_gemini.md`
   - `04_腳本庫/_審稿/A-19_考據_gemini.md`
   Verify: 4 mandatory sections, 6 columns, only `✓`/`✗`/`⚠`/`？` marks, honest "未核頁碼" labeling where primary page numbers are unverified.
2. Inspect the 4 `審稿-文化` files and 4 `審稿-語言` files:
   - Verify cultural fidelity (Navajo winter taboo & sacred sandpainting ethics, Blackfoot 6/7 boys & painted lodge origins, Egyptian Sothic cycle & Decans/KV9 inscriptions, Arabic Bedouin folklore vs fabricated hadiths).
   - Verify language fidelity (Taiwan Traditional Chinese, pronunciation guides, no homophone confusion).
3. Execute automated schema validation:
   Run `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_schemas.py" --file ...` for all target files.
4. Record your review and explicit verdict (`APPROVE` or `REQUEST_CHANGES`) in:
   `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/reviewer_1/handoff.md`
   and send a completion message with verdict to the orchestrator.
