# AGENTS.md

Operating manual for contributors and AI agents touching this repo. Read it before opening a PR.

The repo is a curriculum, not a SaaS app. The lessons are the product. Every rule below keeps 503 lessons coherent over time.

---

## Philosophy

503 lessons. 20 phases. Every algorithm built from raw math before a single framework gets imported. You write backprop, the tokenizer, the attention mechanism, and the agent loop by hand in Python, TypeScript, Rust, or Julia. Then you run the same operation through the production library so the framework stops being a black box. The "Build It / Use It" split is the spine. Each lesson ships a reusable artifact you can plug into your daily workflow.

---

## Repo layout

```
phases/
  NN-phase-slug/
    NN-lesson-slug/
      docs/en.md              # lesson explainer
      code/                   # implementation + tests
      quiz.json               # 6 questions
      outputs/                # reusable artifact (skill / prompt / agent / MCP server)
README.md                     # public face; lesson counts auto-synced
ROADMAP.md                    # phase/lesson status
glossary/terms.md             # canonical term definitions
site/
  build.js                    # parses README + ROADMAP + glossary -> data.js
  data.js                     # generated; rebuilt by CI on main push
certifications/claude/
  program.json                # program metadata, source policy, official links
  tracks/*.json               # exam blueprint, ordered route, study plans
  lessons/NN-slug/            # shared certification lesson contract
  assessments/<exam-code>/    # original diagnostics and full mocks
scripts/                      # automation (audits, catalog, book, i18n, scaffolders)
skills/                       # canonical curriculum skills (learn, course-guide, claude-certification, ...)
.claude/skills/               # MUST mirror skills/ exactly — CI diffs them and blocks on divergence
i18n/                         # per-language translated READMEs (committed); lesson translations live on the `translations` branch
docs/i18n.md                  # the i18n pipeline reference
.github/workflows/
  curriculum.yml              # invariant + auto-sync workflow
  translate.yml               # machine-translates lessons (NLLB-200) to a separate `translations` branch
  build-book.yml              # assembles lesson markdown into EPUB/PDF via pandoc
```

---

## Hard rules

1. **One commit per lesson directory.** Never batch multiple lessons into one commit. A 10-lesson PR has 10 commits.
2. **Conventional commit subjects** ≤72 chars: `feat(phase-NN/MM): <slug>`. Body explains why, not what.
3. **Mermaid or SVG only** for diagrams. No ASCII / Unicode box-drawing.
4. **Every fenced code block needs a language tag.** Use `text`, `json`, `python`, `typescript`, `rust`, `julia`, `bash`, `console`, `mermaid`, `yaml` as appropriate.
5. **Original implementations only.** Don't cite external curriculum repos in docs, code comments, or commit text. Cite RFCs, official specs, and academic papers when they are the canonical source.
6. **Dependency allowlist** (see `Dependencies` below). Stdlib-first.
7. **Never commit generated files**: `catalog.json` is gitignored, `site/data.js` is rebuilt by CI, `package-lock.json` is never tracked.
8. **`skills/` is canonical; `.claude/skills/` is a byte-for-byte mirror.** CI runs `diff -r skills .claude/skills` and blocks on any divergence. Editing a skill means updating both trees in the same commit. `scripts/install_skills.py` copies `outputs/` artifacts (skills/prompts/agents) into targets — it does not own the skills mirror.

---

## Dependencies

| Language   | Allowed                                                                  |
|------------|--------------------------------------------------------------------------|
| Python     | `numpy`, `torch`, `h5py`, `zstandard`, `safetensors`, stdlib              |
| TypeScript | `hono`, `zod`, `ws` (only when WebSockets needed), `@hono/node-server`, Node 20+ stdlib |
| Rust       | stdlib only (single-file `rustc --edition 2021`)                          |
| Julia      | `Random`, `Statistics`, `LinearAlgebra`, `Printf` (Julia stdlib)          |

If a finding suggests a banned dep, skip it with the reason "stays stdlib-first for educational clarity."

The root `requirements.txt` is **authoring tooling** (jupyter, matplotlib, transformers, SDKs) for running lessons locally — it is not the lesson dependency allowlist above. Lesson code still must not import anything outside its language row.

---

## Lesson contract

### docs/en.md frontmatter

```markdown
# <Title>

> <One-line hook>

**Type:** <Learn | Build | Reference>
**Languages:** <comma-list matching the main.* files in code/>
**Prerequisites:** <comma-list of upstream lessons, or "None">
**Time:** ~<estimate in minutes>

## Learning Objectives
- <4-6 bullet points starting with a verb>
```

The `**Languages:**` field must match the languages with a `main.*` file in `code/`.

### quiz.json schema

```json
{
  "lesson": "<dir-slug>",
  "title": "<Lesson Title>",
  "questions": [
    {"stage": "pre",   "question": "...", "options": ["a","b","c","d"], "correct": 0, "explanation": ""},
    {"stage": "check", "question": "...", "options": ["a","b","c","d"], "correct": 1, "explanation": ""},
    {"stage": "check", "question": "...", "options": ["a","b","c","d"], "correct": 2, "explanation": ""},
    {"stage": "check", "question": "...", "options": ["a","b","c","d"], "correct": 1, "explanation": ""},
    {"stage": "post",  "question": "...", "options": ["a","b","c","d"], "correct": 3, "explanation": ""},
    {"stage": "post",  "question": "...", "options": ["a","b","c","d"], "correct": 0, "explanation": ""}
  ]
}
```

Exactly 6 questions: 1 pre + 3 check + 2 post. `correct` is zero-indexed. The site renderer only understands this shape — legacy `q/choices/answer` schemas crash silently.

### Claude certification contract

Certification lessons under `certifications/claude/lessons/` follow the same
documentation, quiz, diagram, dependency, and one-commit-per-lesson rules as
phase lessons. Every certification lesson needs a runnable main file and at
least five deterministic tests. Tracks reference stable lesson paths so one
lesson can serve several credentials without duplication. Conceptual lessons
still need practical work: use a scenario runner, policy scorer, artifact
validator, approval simulator, threat-model checker, or evidence grader instead
of artificial provider API code. A track may also reference an existing
`phases/` lesson as an optional deep dive.

Full-parity certification lessons use the same explain, manipulate, build,
ship, and verify loop as the strongest phase lessons. Every certification
lesson must include the exact sections `Interactive Lab`, `Practice Lab`,
`Shipped Artifact`, `Verify It`, and `Capstone Connection`; embed a registered
`figure` mechanism; ship at least one file under `outputs/`; and provide a
runnable scenario, simulator, scorer, or artifact validator with tests. Code in
a conceptual lesson must exercise the lesson's judgment. Do not add a fake API
integration merely to satisfy the runnable surface. Governance lessons can use
mock incidents, policy scorers, threat-model checks, ADR validation, approval
workflows, or evidence-bundle graders.

`program.json` owns the independent-course disclaimer, verification date, and
official links. `prerequisites.json` owns the machine-readable certification
lesson dependency graph. Every required track route must contain those internal
prerequisites before the lesson that consumes them. Each file in `tracks/` owns
one public exam blueprint, its exact domain weights, ordered lesson route,
assessment declarations, and study plans.
Exam facts must come from the current official guide. Product and model details
must be dated and checked against current official documentation.

Diagnostics and mocks use a separate assessment schema because they support
multiple-response questions:

```json
{
  "id": "claude-ccar-f-diagnostic",
  "version": 1,
  "track": "claude-ccar-f",
  "kind": "diagnostic",
  "title": "Architect Foundations Diagnostic",
  "timeLimitMinutes": 30,
  "questions": [
    {
      "id": "ccar-f-agent-001",
      "domain": "agentic-architecture-orchestration",
      "objective": "choose-an-orchestration-pattern",
      "type": "single",
      "prompt": "A self-contained original scenario...",
      "options": ["a", "b", "c", "d"],
      "correct": [1],
      "explanation": "Why the decision fits and the alternatives do not.",
      "references": ["certifications/claude/lessons/16-multi-agent-orchestration-and-delegation"]
    }
  ]
}
```

`correct` is always an array. A `single` item has exactly one index; a
`multiple` item has at least two. Questions must be original, map to a public
objective, include a substantive explanation, and never reproduce or attempt
to reconstruct confidential exam content. Practice percentages are raw scores,
not Anthropic scaled scores, and the curriculum never guarantees a pass.
Public certification pages and lesson context must also state that this is an
independent community curriculum that is not affiliated with, endorsed by,
sponsored by, or authorized by Anthropic.

### AI-native certification learner mode

When a user asks to choose, start, resume, study, practice, or assess a Claude
certification, read and follow `skills/claude-certification/SKILL.md` before
teaching. This applies to Codex and any other harness that reads `AGENTS.md`;
Claude Code also discovers the matching wrapper under `.claude/skills/`.

Treat the repository as an interactive tutor in learner mode. Read the selected
track manifest, teach one route lesson at a time, run its real scenario and
tests, require a learner-owned artifact under `learning-artifacts/`, grade the
stored quiz or assessment, and preserve progress in
`CLAUDE-CERTIFICATION.md`. Do not modify checked-in reference artifacts as
learner work. The certification curriculum is delivered through GitHub and the
website and is intentionally outside the book-generation pipeline.
It remains English-only and is intentionally outside the machine-translation
pipeline as well.

### code/

- Runs end-to-end and exits 0 on the canonical command for the language.
- Self-terminating demo. No infinite stdin loops, no hangs on missing API keys.
- 4-6 line header comment citing the lesson's `docs/en.md` path and any spec or RFC sources.

### code/tests/

- 5+ unit tests minimum.
- Runs via the language's stdlib runner (`python3 -m unittest discover`, `npx tsx --test`, Rust/Julia inline).

---

## Per-PR validation

Run locally before pushing:

```bash
python3 scripts/audit_lessons.py
python3 scripts/audit_certifications.py
python3 scripts/backfill_certification_references.py --check
python3 scripts/debias_quizzes.py --check
python3 scripts/debias_certification_questions.py --check
python3 scripts/build_readme_i18n.py --check    # if you touched README.md
diff -r skills .claude/skills                    # if you touched skills/
python3 scripts/check_readme_counts.py           # advisory — CI fixes on merge

# For each lesson touched:
cd phases/NN-phase/MM-lesson/code
python3 main.py && python3 -m unittest discover tests -v   # or the lang equivalent
```

CI gates (`.github/workflows/curriculum.yml`):

| Job                              | Trigger      | Behavior                                              |
|----------------------------------|--------------|-------------------------------------------------------|
| `audit`                          | push + PR    | Blocking. Runs `audit_lessons.py`, `audit_certifications.py`, `backfill_certification_references.py --check`, certification `main.py`/tests, `debias_*.py --check`, `build_readme_i18n.py --check`, `test_translate_workflow.py`, `node site/build.js`, and `diff -r skills .claude/skills`. |
| `readme-counts-sync` (main only) | push to main | Rebuilds catalog, auto-fixes README counts, regenerates `i18n/*/README.md`. |
| `site-rebuild` (main only)       | push to main | Re-runs `node site/build.js`, commits `site/data.js`. |
| `readme-counts-drift`            | PR           | Advisory only — main self-heals on merge.             |
| `translate` (`.github/workflows/translate.yml`) | push to main | Machine-translates lessons (NLLB-200, no API key) to a separate `translations` branch. |
| `build-book` (`.github/workflows/build-book.yml`) | push to main | Builds EPUB volumes via `scripts/build_book.py`. |

Certification lessons also have their own lab gates in the audit job: every `certifications/claude/lessons/*/code/main.py` must run and every `code/tests/test_*.py` must pass.

---

## Automation contract

**CI handles automatically — do not touch in your PR:**

| Surface                       | Bot                            | When                |
|-------------------------------|--------------------------------|---------------------|
| `catalog.json`                | rebuilt on demand (gitignored) | every CI job        |
| `README.md` counts            | `readme-counts-sync`           | on push to main     |
| `site/data.js` + other site artifacts (`certification-data.js`, `sitemap.xml`, `llms.txt`, `build-meta.js`, `langs.js`) | `site-rebuild` / Vercel build | on push to main / deploy |
| translated lessons (`i18n/*/phases/`) | `translate` workflow | on push to main, to the `translations` branch — never `main` |

`site/build.js` also regenerates `site/langs.js` (gitignored) from `languages.json` — never hand-edit any of these; they are all derived.

**You handle:**

| Surface                       | When                                                             |
|-------------------------------|------------------------------------------------------------------|
| `README.md` lesson-link rows  | when adding a new lesson — link `[Title](phases/NN-phase/MM-lesson/)` |
| `ROADMAP.md` status           | when marking a lesson complete or WIP                            |
| `glossary/terms.md`           | when introducing a term used by more than one lesson             |

**Common bug**: if `grep -c 'tree/main/phases/NN-' site/data.js` is 0 after merge, the Phase NN README rows are plain text and missing the `[Title](phases/NN-...)` markdown link. `site/build.js` derives the URL from that link.

**i18n**: English lessons are canonical. Translated lesson markdown goes to the `translations` branch only — never commit anything under `i18n/*/phases/` or `i18n/*/.cache/` to `main` (they are gitignored). The per-language `i18n/<lang>/README.md` is hand-authored and committed to `main`; regenerate it with `python3 scripts/build_readme_i18n.py` after touching `README.md`. Adding a language means editing `languages.json` (the single registry). See `docs/i18n.md` for the full pipeline.

---

## Conflict resolution

```bash
git fetch origin main
git merge --no-edit origin/main

# Catalog conflict (legacy branches only — catalog.json is gitignored now):
git rm catalog.json
git commit --no-edit

# README count conflict:
git checkout --theirs README.md
python3 scripts/build_catalog.py
python3 scripts/check_readme_counts.py --fix
git add README.md && git commit --no-edit

# site/data.js conflict:
git checkout --theirs site/data.js
node site/build.js
git add site/data.js && git commit --no-edit

git push origin <your-branch>
```

Avoid `git push --force` to a branch with open review comments. Force-push detaches them.

---

## New-lesson onboarding

```bash
# Fastest start — scripts/scaffold-lesson.sh <phase-dir> <slug> [title] creates
# the skeleton (code/, notebook/, docs/, outputs/ + docs/en.md from LESSON_TEMPLATE.md).
mkdir -p phases/NN-phase-slug/MM-new-lesson/{docs,code/tests,outputs}

# 1. Write docs/en.md with the frontmatter above.
# 2. Write code/main.<lang> with the 4-6 line header.
# 3. Write code/tests/test_main.* with 5+ tests.
# 4. Write quiz.json with the schema above.
# 5. (Optional) Add outputs/skill-<slug>.md if the lesson ships a skill.

# 6. Add to README.md:
#    | MM | [Lesson Title](phases/NN-phase-slug/MM-new-lesson/) | Type | Lang |

# 7. Update ROADMAP.md status row.

# 8. Validate locally.

# 9. Atomic commit:
git add phases/NN-phase-slug/MM-new-lesson README.md ROADMAP.md
git commit -m "feat(phase-NN/MM): add <slug>"
git push -u origin <your-branch>
gh pr create --title "feat(phase-NN/MM): add <slug>" --body "<5-line summary>"
```

`site/data.js` regenerates on merge — leave it for CI.

---

Last reviewed: 2026-08-10.
