# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read AGENTS.md first

`AGENTS.md` at the repo root is the full operating manual for this repo (hard rules, dependency allowlist, lesson contract, quiz schema, CI gates, conflict resolution, new-lesson onboarding). It applies to Claude Code exactly as written — read it before making any change to `phases/`, `certifications/`, `README.md`, `ROADMAP.md`, or `site/`. This file only adds Claude-Code-specific pointers and is not a substitute.

## What this repo is

A curriculum, not an app: 435 lessons across 20 phases teaching AI engineering by building every algorithm from raw math before using the production library ("Build It / Use It"). The lessons themselves are the product being shipped — most "code changes" here are new or edited lesson directories, not application features.

```
phases/NN-phase-slug/MM-lesson-slug/
  docs/en.md      # lesson explainer (frontmatter: Type, Languages, Prerequisites, Time)
  code/           # implementation + code/tests/ (5+ unit tests)
  quiz.json       # exactly 6 questions: 1 pre + 3 check + 2 post
  outputs/        # reusable artifact (skill / prompt / agent / MCP server)
certifications/claude/   # independent Claude certification tracks (own contract, see AGENTS.md)
site/             # static site; build.js parses README/ROADMAP/glossary -> data.js (generated, CI-owned)
scripts/          # audit/build/translate automation (see below)
skills/           # curriculum-facing Claude Code skills (learn, course-guide, claude-certification, ...)
i18n/             # translated lesson trees, one dir per language
```

## Commands

Per-PR validation (run before pushing, per AGENTS.md):

```bash
python3 scripts/audit_lessons.py
python3 scripts/audit_certifications.py
python3 scripts/check_readme_counts.py        # advisory — CI fixes on merge

# For each touched lesson, run its canonical command, e.g.:
cd phases/NN-phase/MM-lesson/code
python3 main.py && python3 -m unittest discover tests -v
# TypeScript: npx tsx --test ; Rust: rustc --edition 2021 main.rs && ./main ; Julia: inline tests
```

Other scripts of note (`scripts/`): `build_catalog.py` (rebuilds gitignored `catalog.json`), `build_book.py`, `readme_translations.py` / `translate_lessons.py` (i18n pipeline), `scaffold-lesson.sh` / `scaffold_workbench.py` (new-lesson skeleton), `link_check.py`, `debias_quizzes.py` / `debias_certification_questions.py`.

Site: `node site/build.js` regenerates `site/data.js` from README/ROADMAP/glossary — never hand-edit `site/data.js`, it's rebuilt by CI on push to main.

## Hard rules (full list in AGENTS.md)

- One commit per lesson directory; conventional commit subjects `feat(phase-NN/MM): <slug>`.
- Diagrams: Mermaid or SVG only, no ASCII art.
- Every fenced code block needs a language tag.
- Original implementations only — no citing external curriculum repos.
- Dependency allowlist is stdlib-first: Python (`numpy`, `torch`, `h5py`, `zstandard`, `safetensors` + stdlib), TypeScript (`hono`, `zod`, `ws`, `@hono/node-server` + Node stdlib), Rust (stdlib only), Julia (`Random`, `Statistics`, `LinearAlgebra`, `Printf`).
- Never commit generated files: `catalog.json` (gitignored), `site/data.js` (CI-rebuilt), `package-lock.json`.
- `README.md` lesson-link rows and `ROADMAP.md` status must use the `[Title](phases/NN-phase/MM-lesson/)` markdown link form — plain text rows break `site/build.js`'s URL derivation.

## Learning harness

`.harness/` tracks Chethan's own day-by-day progress through this curriculum (separate from the curriculum content itself — this is his personal learning log, not a lesson artifact). Structure and full protocol are documented in `.harness/README.md`.

**When Chethan says "update harness"**, do this for today's date:
1. Write/update `.harness/tracker/tracker-<DATE>.md` (from `_TEMPLATE.md`) — lessons covered, time spent, concepts learned, artifacts produced, stuck points, tomorrow's plan. Pull this from what actually happened in the session, don't invent it.
2. Write/update `.harness/linkedin/post-<DATE>.md` (from `_TEMPLATE.md`) — draft or refine a short LinkedIn post about the day's learning. If told the post is already live, fill in `Posted URL` under Status — never check the "Posted" box without a URL.
3. Write/update `.harness/summaries/summary-<DATE>.md` (from `_TEMPLATE.md`) — a short revision-focused recap (5-10 bullets) for skimming later.
4. Add/update today's line in `.harness/INDEX.md` (newest first).
5. Set `.harness/CURRENT.md` to today's date.

This harness is independent of the curriculum's own `README.md`/`ROADMAP.md`/lesson tracking above — don't conflate the two.

## Certification learner mode

If asked to choose, start, resume, study, or assess a Claude certification track, follow `skills/claude-certification/SKILL.md` (Claude Code discovers it under `.claude/skills/`) rather than teaching ad hoc. Certification lessons under `certifications/claude/lessons/` follow the same contract as phase lessons plus additional required sections (`Interactive Lab`, `Practice Lab`, `Shipped Artifact`, `Verify It`, `Capstone Connection`) — see AGENTS.md for the full contract before editing them.
