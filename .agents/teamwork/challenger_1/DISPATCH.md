# Task Assignment: Gate Challenger - Empirical Constraint Challenger

## Role
Empirical Constraint Challenger

## Target
Perform adversarial stress testing of all quantitative thresholds, edge cases, duration bounds, speech rates, card word counts, and Unicode diacritical handling across all deliverables.

Deliver your challenge report to `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/challenger_1/handoff.md` with explicit verdict: APPROVE or REQUEST_CHANGES.


## 2026-10-28T10:17:33Z
You are challenger_1 (Empirical Constraint Challenger) for the NTNU Astronomy Club "World Sky Cultures" video series workflow.
Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/challenger_1`
Your assignment file is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/challenger_1/DISPATCH.md`

MANDATORY FIRST STEP: Read the authoritative user request at:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`

Also read:
- `PROJECT.md` at `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/orchestrator/PROJECT.md`
- `TEST_READY.md` and `TEST_INFRA.md`

Your task:
1. Conduct code-executing adversarial stress testing on all quantitative metrics and constraints across the 9 English drafts and 36 critic reports:
   - Write independent validation scripts or run edge-case tests.
   - Verify that NO shot in any English script exceeds 2.6 words/sec.
   - Verify that NO on-screen card in any English script exceeds 6 words.
   - Verify that NO English script exceeds 180 seconds.
   - Verify that NO YouTube title exceeds 60 characters.
   - Test Unicode boundary edge cases: contractions (e.g. *don't*, *it's*), hyphens (e.g. *sky-culture*), and diacritics/okina (*al-Thurayyā*, *Kṛttikā*, *Úlfs kjaptr*, *ʻokina*).
   - Verify voice-over <= 4.5 chars/sec and card <= 14 chars in critic suggested rewrites.
2. Deliver your challenge report to:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/challenger_1/handoff.md`.
Your report MUST explicitly state your verdict: `APPROVE` or `REQUEST_CHANGES`.
Communicate back with send_message when done.

## 2026-10-31T20:34:54Z
You are Challenger 1 (teamwork_preview_challenger) for Batch 2 (A-16, A-17, A-18, A-19).

Your working directory is:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/challenger_1`

Read:
- `/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/ORIGINAL_REQUEST.md`

Your task:
Perform empirical adversarial verification of the astronomical claims and Skyfield ephemeris reports across all 4 episodes:
- A-16: Canopus (老人星, HIP 30438) transit altitude in Taipei (25.033°N, 121.565°E, UTC+8) on 2027/01/08 (culmination ~12.3° Alt, transit time ~23:07 CST); Alkaid rising time (~22:16 CST); Polaris altitude (~25.5°).
- A-17: Pleiades (Bunched Stars / 昴宿) altitude in Taipei on 2027/01/15 (near zenith ~88.8° Alt); Big Dipper stars altitude/rise times; Browning Montana (48.56°N) invisibility period (May–June).
- A-18: Sirius (天狼星, HIP 32349) transit in Taipei on 2027/01/22 (~22:33 CST at ~48.2° Alt); Full Moon 20:17 CST; Giza / Cairo precession drift (38 days between 2500 BCE and 2027 CE).
- A-19: Canopus transit in Taipei on 2027/01/29 (~21:43 CST at ~12.3° Alt); Sirius vs Procyon vs Canopus galactic coordinates and brightness ratios (Sirius 5.45x brighter than Procyon; Canopus 309 ly, 36x farther than Sirius, 661x intrinsically brighter).

Write a standalone Python verification script using `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` and `de421.bsp`, execute it, and record exact output and your verdict (CONFIRMED or CHALLENGED) in:
`/Users/kimjoo/.gemini/antigravity/worktrees/NTNU Insta/browser_teamwork_preview_boost/.agents/teamwork/challenger_1/handoff.md`
and message the orchestrator.
