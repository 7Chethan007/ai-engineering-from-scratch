# Learning Harness

Cross-session state for Chethan's "AI Engineering from Scratch" learning journey. One entry per learning day. Works with Claude Code or any agent that reads markdown.

---

## How to use this harness

### Start of session
```bash
cat .harness/CURRENT.md
cat .harness/tracker/$(cat .harness/CURRENT.md).md          # yesterday/today's tracker so far
cat .harness/summaries/$(cat .harness/CURRENT.md).md 2>/dev/null   # last summary, for a quick refresher
```

### "update harness" — what it means
When Chethan says **"update harness"**, do the following for today's date (`YYYY-MM-DD`):

1. **Tracker** — create/update `tracker/tracker-<DATE>.md` from `tracker/_TEMPLATE.md`. Fill it from the session: lessons/phases touched, time spent, concepts learned, artifacts produced, stuck points, tomorrow's plan. If a tracker for today already exists, append/update rather than overwrite.
2. **LinkedIn post** — create/update `linkedin/post-<DATE>.md` from `linkedin/_TEMPLATE.md`. Draft (or refine) a short post about what was learned today. If Chethan says he already posted it, ask for (or use the given) URL and fill in the `Posted URL` field — never mark a post as posted without a URL.
3. **Summary** — create/update `summaries/summary-<DATE>.md` from `summaries/_TEMPLATE.md`. A short, revision-focused recap (5-10 bullets) of the day's core ideas — written so a future skim refreshes the concept, not the play-by-play.
4. **Index** — add or update today's line in `INDEX.md` (newest first).
5. **CURRENT.md** — set it to today's date so the next session's start-of-session read picks it up.

Do not invent lesson content or claim work that wasn't actually done this session — pull from the actual conversation/phase progress.

---

## Directory structure

```
.harness/
├── README.md                 ← this file — update whenever the harness structure changes
├── CURRENT.md                ← 1 line: today's date (YYYY-MM-DD), points at the latest day's files
├── INDEX.md                  ← cumulative index, one line per day, newest first
├── tracker/
│   ├── _TEMPLATE.md
│   └── tracker-YYYY-MM-DD.md      ← what was learned/built today
├── linkedin/
│   ├── _TEMPLATE.md
│   └── post-YYYY-MM-DD.md         ← post draft; filled with the posted URL once it's live
└── summaries/
    ├── _TEMPLATE.md
    └── summary-YYYY-MM-DD.md      ← short revision recap of the day
```

---

## Updating this README

Update this file when the `.harness/` directory structure changes or the "update harness" protocol changes. See `CLAUDE.md` at the repo root for the trigger instructions given to Claude Code.
