# Task Assignment: Forensic Integrity Audit

## Role
Forensic Integrity Auditor

## Target
Execute full forensic integrity audit on all 55 deliverable files and the verification test suite. Verify that implementations are authentic, non-cheating, non-dummy, and free of hardcoded fake test results.

Deliver your forensic audit report to `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/auditor_1/handoff.md` with explicit verdict: CLEAN or INTEGRITY VIOLATION.


## 2026-10-28T10:17:34Z
You are auditor_1 (Forensic Integrity Auditor) for the NTNU Astronomy Club "World Sky Cultures" video series workflow.
Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/auditor_1`
Your assignment file is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/auditor_1/DISPATCH.md`

MANDATORY FIRST STEP: Read the authoritative user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`

Also read:
- `PROJECT.md` at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator/PROJECT.md`
- `TEST_READY.md`

Your task:
Execute forensic integrity verification across all 55 deliverables and test suite scripts:
1. Verify that all implementations and reports are authentic and genuine:
   - Check for hardcoded test results, fake pass flags, or dummy/facade implementations.
   - Verify that quotes from classical texts (《史記》《漢書》《左傳》《說文》《古蘭經》《Edda》) are real historical texts, not fabricated.
   - Verify that astronomical calculations are calculated by genuine physics models (Skyfield / DE421), not synthetic mocked constants.
   - Verify that the test runner `verify_all.py` actually parses and asserts all files and conditions rather than returning an unverified mock exit code 0.
   - Verify that original Chinese scripts in `04_腳本庫/` are untouched.
2. Deliver your forensic audit report to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/auditor_1/handoff.md`.
Your report MUST explicitly state your verdict: `CLEAN` or `INTEGRITY VIOLATION`.
Communicate back with send_message when done.

## 2026-10-31T20:34:54Z
You are Forensic Auditor (teamwork_preview_auditor) for Batch 2 (A-16, A-17, A-18, A-19).

Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/auditor_1`

Read:
- `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`
- Integrity Forensics rules

MANDATORY BINARY VETO AUDIT:
Your job is independent, forensic verification of integrity.
Check:
1. **0 Modifications to Original Scripts**:
   - Check `04_腳本庫/A-16-納瓦荷只在冬天說的星星故事-逐字稿-v0.md`
   - Check `04_腳本庫/A-17-黑腳族留在天上的六個孩子-逐字稿-v0.md`
   - Check `04_腳本庫/A-18-古埃及叫醒尼羅河的天狼星-逐字稿-v0.md`
   - Check `04_腳本庫/A-19-古阿拉伯兩隻鴕鳥與擋路的老人星-逐字稿-v0.md`
   - Verify `git status` in worktree and Downloads shows 0 modifications to any original script files.
2. **Dual-Workspace Synchronization**:
   - Verify that all 20 deliverables exist in both:
     `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/04_腳本庫/_審稿/`
     `/Users/kimjoo/Downloads/NTNU Insta/04_腳本庫/_審稿/`
   - Calculate SHA-256 for all 20 files in both locations and verify that hashes match 100% bit-for-bit.
3. **Anti-Hallucination & Honest Citations**:
   - Check fact-checking reports: are citations authentic? Are page numbers verified or honestly marked "未核頁碼"?
   - Verify that no fake asterisms or fabricated myths were invented.
4. **Harness & Schema Validation**:
   - Run `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_schemas.py"` across all 20 files and confirm 100% PASS with 0 errors.

Write your complete audit report and explicit verdict (`CLEAN` or `INTEGRITY VIOLATION`) to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/auditor_1/handoff.md`
and send a completion message with your verdict to the orchestrator.
