# Archive

Nothing in this profile is deleted — it is moved here first. Every snapshot
directory is named for the date the content was replaced, and holds the files
exactly as they were on that day.

```
archive/
└── 2026-08-07/          Profile as it stood before the 2026 redesign
    ├── README.md            previous profile README
    └── workflows/
        └── snake.yml        previous snake workflow
```

- **[notes.md](notes.md)** — what was archived, and why, item by item.

## Restoring something

Copy the file back out of the snapshot:

```bash
cp archive/2026-08-07/README.md README.md
cp archive/2026-08-07/workflows/snake.yml .github/workflows/snake.yml
```

Or recover any earlier state straight from git history, which is untouched:

```bash
git log --oneline -- README.md
git show <commit>:README.md
```

## Adding a snapshot

Before a future redesign, create `archive/<YYYY-MM-DD>/`, copy the files being
replaced into it preserving their relative paths, and add a section to
`notes.md` explaining the reasoning. Keep the entries factual — the point of the
archive is that a decision made today can still be understood, and reversed, a
year from now.
