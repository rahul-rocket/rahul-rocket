# Archive

Nothing in this profile is deleted — it is moved here first. Every snapshot
directory holds the files exactly as they stood at the moment they were
replaced, so any version of the profile can be restored without reading git
history.

```
archive/
├── 2026-08-07/              Profile as it stood before the 2026 redesign
│   ├── README.md                original profile README
│   └── workflows/
│       └── snake.yml            original snake workflow
├── 2026-08-07-v3.0.0/       Profile at v3.0.0, before the brand rebuild
│   ├── README.md                v3.0.0 profile README
│   └── banner/
│       ├── profile-banner-dark.svg    v3.0.0 banner, dark
│       └── profile-banner-light.svg   v3.0.0 banner, light
└── 2026-08-07-v4.3.0/       Profile at v4.3.0, before Latest Gists was removed
    ├── README.md                v4.3.0 profile README
    ├── workflows/
    │   └── gists.yml            the Latest Gists workflow
    └── scripts/
        └── update_gists.py      the script that workflow ran
```

- **[notes.md](notes.md)** — what was archived, and why, item by item.

Two snapshots were taken on 2026-08-07, so the second carries the version it
preserves as a suffix. Name any future snapshot `<YYYY-MM-DD>-v<version>` —
dates alone collide, as these two nearly did. The third, `-v4.3.0`, follows that
rule; the bare `2026-08-07` directory predates it and is left as-is.

## Restoring something

Copy the file back out of the snapshot. To restore the profile as it stood at
v3.0.0, before the brand rebuild:

```bash
cp archive/2026-08-07-v3.0.0/README.md README.md
cp archive/2026-08-07-v3.0.0/banner/*.svg assets/banner/
```

To restore the `Latest Gists` section and the automation behind it:

```bash
cp archive/2026-08-07-v4.3.0/workflows/gists.yml .github/workflows/gists.yml
mkdir -p .github/scripts
cp archive/2026-08-07-v4.3.0/scripts/update_gists.py .github/scripts/
```

Then copy the `## Latest Gists` heading and its `START_SECTION`/`END_SECTION`
marker pair back into `README.md` — take them from
`archive/2026-08-07-v4.3.0/README.md`. The workflow exits non-zero when those
markers are absent, so restoring the two files without the markers turns a
removed section into a daily failing job.

To restore the original pre-redesign profile:

```bash
cp archive/2026-08-07/README.md README.md
cp archive/2026-08-07/workflows/snake.yml .github/workflows/snake.yml
```

Restoring a README is not by itself a complete revert — check what else the
version depended on. The v3.0.0 README references only `assets/banner/`, both
files of which are in its snapshot. The pre-redesign README referenced no
repository assets at all.

Or recover any earlier state straight from git history, which is untouched:

```bash
git log --oneline -- README.md
git show <commit>:README.md
```

## Adding a snapshot

Before a future redesign, create `archive/<YYYY-MM-DD>-v<version>/`, copy the
files being replaced into it preserving their relative paths, and add a section
to `notes.md` explaining the reasoning. Copy every file the change overwrites,
not just the README — assets referenced by a README are part of that version.
Keep the entries factual: the point of the archive is that a decision made today
can still be understood, and reversed, a year from now.
