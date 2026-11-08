# Project: NTNU Astronomy Club "World Sky Cultures" Video Series Production & Verification

## Architecture
This project executes a dual-track production and automated verification workflow for 9 target episodes of the NTNU Astronomy Club "World Sky Cultures" (萬國星空) video series:
`A-01`, `A-02`, `A-03`, `A-04`, `A-06`, `H-七夕`, `A-13`, `A-14`, `A-15`.

```
Project Orchestrator
├── E2E Testing Track (Milestone MT) - DONE
│   ├── Test Harness: verify_all.py, verify_ephemeris.py, verify_schemas.py, verify_sync.py
│   ├── TEST_INFRA.md
│   └── TEST_READY.md
└── Implementation Track
    ├── Milestone 1 (M1): R1 網路考據 (9 files in 04_腳本庫/_審稿/{編號}_考據_gemini.md) - DONE
    ├── Milestone 2 (M2): R2 四角色獨立審稿 (36 files in 04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md) - DONE
    ├── Milestone 3 (M3): R3 英文版改寫與譯名表 (9 files in 04_腳本庫/_英文版/ + 06_發布月曆/英文譯名表.csv) - DONE
    ├── Milestone 4 (M4): R4 雙向同步與原稿保護 (Mirror to /Users/kimjoo/Downloads/NTNU Insta, git immutability) - DONE
    └── Final Milestone (M5): 100% E2E Test Suite Pass (Tiers 1-4) & Adversarial Hardening (Tier 5) + Forensic Audit - DONE
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | R1-DEST | Output path `04_腳本庫/_審稿/{編號}_考據_gemini.md` for 9 episodes | M1 | SOP 01 |
| 2 | R1-SECT | 4 mandatory sections in research reports | M1 | SOP 01 |
| 3 | R1-TABL | 6-column verification table schema with 4-tier verdicts (`✓`, `✗`, `⚠`, `？`) | M1 | SOP 01 |
| 4 | R1-COLL | Primary classical text collation with chapter, section, and edition | M1 | SOP 01 |
| 5 | R1-ETHN | Ethnographic provenance tracing to original field recorder and year | M1 | SOP 01 |
| 6 | R1-ASTR | Skyfield ephemeris & database cross-check for Taipei (25.03°N, 121.56°E, UTC+8) | M1 | SOP 01 |
| 7 | R2-QUAD | 4 independent critic roles (`天文`, `文化`, `敘事`, `語言`) across 9 episodes (36 files) | M2 | SOP 02 |
| 8 | R2-SUMM | 3-line summary header (整體評價、最重要的三個問題、沒把握的地方) | M2 | SOP 02 |
| 9 | R2-TABL | 6-column review table (`嚴重度|位置|原文|問題|建議改法|依據`) with `🔴`, `🟡`, `⚪` | M2 | SOP 02 |
| 10 | R2-VOSP | Voice-over pace limit ≤ 4.5 chars/sec in suggested rewrites | M2 | SOP 02 |
| 11 | R2-CARD | On-screen text card limit ≤ 14 chars in suggested rewrites | M2 | SOP 02 |
| 12 | R2-LANG | Taiwan traditional Chinese phrasing and terminology | M2 | SOP 02 |
| 13 | R2-FORM | Opening formula 「同一片星空，◯◯看見——◯◯。」 & closing next-episode teaser | M2 | SOP 02 |
| 14 | R2-TAIP | Empirical Taipei sky clocking verification in 天文 critic role | M2 | SOP 02 |
| 15 | R3-DEST | Output path `04_腳本庫/_英文版/{編號}-EN-script-draft.md` for 9 episodes | M3 | SOP 03 |
| 16 | R3-TIME | Total video duration cap ≤ 180 seconds | M3 | SOP 03 |
| 17 | R3-PACE | Shot speech rate cap ≤ 2.6 words/sec | M3 | SOP 03 |
| 18 | R3-CARD | Graphic text card limit ≤ 6 English words | M3 | SOP 03 |
| 19 | R3-FORM | Opening formula *"One sky. The [people] saw — [X]."* | M3 | SOP 03 |
| 20 | R3-TABL | Shot table schema `| Shot | Sec | Voice-over | On-screen text | Words/sec |` | M3 | SOP 03 |
| 21 | R3-SECT | 5 mandatory sections in English draft (Shot table, Totals, Glossary, Social copy, Cut log) | M3 | SOP 03 |
| 22 | R3-GLOS | Central glossary maintenance in `06_發布月曆/英文譯名表.csv` | M3 | SOP 03 |
| 23 | R3-ROMA | Multi-lingual romanization (Pinyin asterisms, Korean RR, Hepburn, IAST, Arabic/Indigenous diacritics) | M3 | SOP 03 |
| 24 | R3-METS | YouTube title ≤ 60 chars, description 3-5 lines with sources, Facebook caption | M3 | SOP 03 |
| 25 | R4-IMMU | Script immutability: zero modifications to existing `04_腳本庫/*.md` scripts | M4 | R4 |
| 26 | R4-SYNC | Dual-workspace synchronization: mirror all 55 files to `/Users/kimjoo/Downloads/NTNU Insta` | M4 | R4 |
| 27 | T-HARN | Programmatic test harness for automated verification of all 55 files | MT | E2E Track |
| 28 | T-EPHE | Skyfield automated astronomical verification script for Taipei coordinates | MT | E2E Track |
| 29 | T-SCHM | Markdown schema and quantitative threshold validator (seconds, words/sec, cards) | MT | E2E Track |
| 30 | T-SYNC | Dual-worktree SHA-256 equivalence and git porcelain immutability verifier | MT | E2E Track |
| 31 | V-GATE | 100% E2E test verification and adversarial hardening gate | M5 | Victory Audit |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| MT | E2E Testing Suite | Verification harness (`verify_all.py`, `verify_schemas.py`, `verify_ephemeris.py`, `verify_sync.py`), `TEST_INFRA.md`, `TEST_READY.md` | none | DONE |
| M1 | R1 網路考據 | 9 episodes research reports `04_腳本庫/_審稿/{編號}_考據_gemini.md` | none | DONE |
| M2 | R2 四角色審稿 | 36 critic review files `04_腳本庫/_審稿/{編號}_審稿-{角色}_antigravity.md` | M1 | DONE |
| M3 | R3 英文版改寫與譯名表 | 9 English scripts in `04_腳本庫/_英文版/` + `06_發布月曆/英文譯名表.csv` + 3項勘誤 | M1, M2 | DONE |
| M4 | R4 雙向同步與原稿保護 | Mirror all 55 files to `/Users/kimjoo/Downloads/NTNU Insta` & verify 0 git modifications | M1, M2, M3 | DONE |
| M5 | 驗收與終審 (Final Milestone) | Pass 100% E2E tests (Tiers 1-4) + Adversarial hardening (Tier 5) + Forensic Audit | MT, M1, M2, M3, M4 | DONE |

## Interface Contracts
### Verification Harness ↔ Deliverables
- Entry point: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 02_製作流程SOP/verification_harness/verify_all.py`
- Exit code: 0 on 100% pass, non-zero on any rubric or threshold violation.
- All 4 verification suites passed 100% with exit code 0.
- Auditor: CLEAN. Reviewers: APPROVE. Challengers: APPROVE.
