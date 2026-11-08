# TEST_READY.md: E2E Verification Suite Release Manifest

**Date**: 2026-10-28T09:30:00Z  
**Author**: E2E Test Suite Developer (`e2e_test_writer`)  
**Status**: READY FOR WORKFLOW EXECUTION  
**Target Project**: NTNU Astronomy Club "World Sky Cultures" Video Series (9 Target Episodes)  

---

## 1. Test Suite Entry Point & Execution Commands

### Master Test Runner
The primary entry point executes all 4 verification suites, outputs a colorized terminal report, and exits with code 0 on 100% pass, or code 1 on any violation:

```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_all.py"
```

### Self-Check Regression Suite (Harness Integrity Check)
Runs 17 comprehensive unit tests verifying tokenizers, boundary cases, validators, and ephemeris formulas against synthetic fixtures:

```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
  "02_製作流程SOP/verification_harness/verify_all.py" --self-test
```

### Individual Verification Commands
- **Astronomical Ephemeris Verification**:
  ```bash
  /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
    "02_製作流程SOP/verification_harness/verify_ephemeris.py" -v
  ```
- **Markdown Schemas & Thresholds (All deliverables)**:
  ```bash
  /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
    "02_製作流程SOP/verification_harness/verify_schemas.py" --repo .
  ```
- **Markdown Schemas & Thresholds (Single file)**:
  ```bash
  /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
    "02_製作流程SOP/verification_harness/verify_schemas.py" --file "04_腳本庫/_審稿/A-01_考據_gemini.md"
  ```
- **Dual-Workspace Synchronization & Script Immutability**:
  ```bash
  /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
    "02_製作流程SOP/verification_harness/verify_sync.py" -v
  ```

---

## 2. Verification Harness Components

All modules are located under `02_製作流程SOP/verification_harness/`:

| File | Purpose | Key Checks & Hard Constraints |
|---|---|---|
| `verify_all.py` | Master Test Runner | Coordinates all 4 suites, formats ANSI color status matrix, manages exit codes (0 = pass, 1 = fail). |
| `verify_ephemeris.py` | Astronomical Engine | Skyfield 1.54 + local `de421.bsp`. Verifies Alt/Az, rise, set, culmination, separation, and 3D distance for Taipei (25.03°N, 121.56°E, UTC+8). |
| `verify_schemas.py` | Schema & Constraint Validator | - 9 Research files: 4 mandatory sections, 6-col table, 4-tier verdicts (`✓`, `✗`, `⚠`, `？`).<br>- 36 Critic files: 3-line summary header, 6-col table with `🔴/🟡/⚪`, Taipei sky clocking in 天文 role.<br>- 9 English drafts: 5 mandatory sections, duration $\le 180$s, speech rate $\le 2.6$ words/sec, cards $\le 6$ words, *"One sky."* formula, YouTube title $\le 60$ chars.<br>- Master Glossary CSV: valid CSV format with required bilingual columns. |
| `verify_sync.py` | Sync & Immutability | SHA-256 hash match for all 55 deliverables between worktree and `/Users/kimjoo/Downloads/NTNU Insta`; `git status 04_腳本庫/*.md` confirms 0 modifications. |
| `test_harness_self_check.py` | Unit & Regression Suite | 17 unit test cases testing boundary values, Unicode diacritics, and adversarial malformations. |

---

## 3. Test Coverage Matrix

- **Target Episodes Covered (9)**: `A-01`, `A-02`, `A-03`, `A-04`, `A-06`, `H-七夕`, `A-13`, `A-14`, `A-15`
- **Total Deliverable Files Inspected (55)**:
  - 9 Research Reports (`04_腳本庫/_審稿/{編號}_考據_gemini.md`)
  - 36 Quad-Role Critic Reports (`04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md`)
  - 9 English Adaptation Drafts (`04_腳本庫/_英文版/{編號}-EN-script-draft.md`)
  - 1 Central Glossary Table (`06_發布月曆/英文譯名表.csv`)
- **Total Test Cases Specified in `TEST_INFRA.md`**: > 310 cases (5+ Tier 1 and 5+ Tier 2 cases across all 31 features in `PROJECT.md`, plus Tier 3 integration, Tier 4 real-world, and Tier 5 adversarial tests).
- **Self-Test Regression Results**:
  - `Ran 17 tests in 0.021s`
  - `OK (17 passed, 0 failures, 0 errors)`

---

## 4. Current Execution Status

Running `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 "02_製作流程SOP/verification_harness/verify_all.py"` on the current repository yields:

- **Suite 1: Astronomical Ephemeris**: `PASS` (9/9 target episode astronomical baselines verified)
- **Suite 2: Original Script Immutability**: `PASS` (0 modified files in `04_腳本庫/*.md`)
- **Suite 3: Markdown Schemas & Constraints**: `PENDING` (Progressively validating as downstream implementation milestones M1–M3 deliver files; existing delivered research files pass 100%)
- **Suite 4: Dual-Workspace Sync**: `PENDING` (Will turn `PASS` upon Milestone 4 dual-workspace mirror completion)

The verification harness is fully tested, operational, and immediately ready to gate all downstream milestones and final victory audit.
