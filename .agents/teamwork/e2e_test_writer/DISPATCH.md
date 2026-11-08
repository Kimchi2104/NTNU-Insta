# Task Assignment: E2E Test Suite & Verification Harness Development

## Target
Design and implement the automated verification harness in `02_製作流程SOP/verification_harness/` and publish `TEST_INFRA.md` and `TEST_READY.md`.

## Deliverable
Write your implementation, run the test harness self-check, and deliver your handoff report to `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/e2e_test_writer/handoff.md`.

## 2026-10-28T09:20:17Z
[Message] sender=99335e05-87c1-4071-bf18-9e62ab38c021 priority=MESSAGE_PRIORITY_HIGH
You are the E2E Test Suite Developer for the NTNU Astronomy Club "World Sky Cultures" video series workflow.
Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/e2e_test_writer`
Your assignment file is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/e2e_test_writer/DISPATCH.md`

MANDATORY FIRST STEP: Read the authoritative user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`

Also read:
- `PROJECT.md` at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator/PROJECT.md`
- Survey handoffs:
  - `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/survey_spec_miner/handoff.md`
  - `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/survey_tools_explorer/handoff.md`

Your task:
1. Build the programmatic verification harness under `02_製作流程SOP/verification_harness/`:
   - `verify_all.py`: Master test runner that runs all checks, produces a comprehensive colorized summary, and exits with code 0 if all tests pass, or non-zero if any test fails.
   - `verify_schemas.py`: Validates all required markdown schemas and quantitative constraints:
     - 9 research files (`04_腳本庫/_審稿/{編號}_考據_gemini.md`): 4 mandatory sections, 6-column table, 4-tier judgements.
     - 36 critic files (`04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`): 3-line summary header, 6-column review table with 🔴/🟡/⚪.
     - 9 English draft files (`04_腳本庫/_英文版/{編號}-EN-script-draft.md`): 5 mandatory sections, total seconds <= 180s, each shot <= 2.6 words/sec, on-screen text <= 6 English words, opening formula "One sky. The [people] saw — [X].", YouTube title <= 60 chars.
     - Glossary file `06_發布月曆/英文譯名表.csv`: valid CSV format, required columns (Chinese, English, Category/Notes, Episode).
   - `verify_ephemeris.py`: Standalone script utilizing Skyfield 1.54 (via `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` and local `de421.bsp`) to compute and verify celestial coordinates, altitude, azimuth, and rise/set times for Taipei (25.03°N, 121.56°E, UTC+8) across the target episodes.
   - `verify_sync.py`: Verifies that all 55 deliverable files exist identically in both the active worktree and `/Users/kimjoo/Downloads/NTNU Insta` (via SHA-256), and verifies that `git status --porcelain 04_腳本庫/*.md` confirms zero modifications to original scripts.
2. Create `TEST_INFRA.md` at the project root detailing the 4-tier testing architecture (Tier 1: Feature Coverage >= 5/feat, Tier 2: Boundary/Corner >= 5/feat, Tier 3: Cross-Feature Combinations, Tier 4: Real-World Scenarios).
3. Test your verification harness by running it (note: files not yet created will report expected pending/fail status).
4. Publish `TEST_READY.md` at the project root with the test runner command and coverage summary.
5. Write your complete handoff report to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/e2e_test_writer/handoff.md`.
Communicate back with send_message when done.
