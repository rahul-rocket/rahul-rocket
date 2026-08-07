# Archive notes

## Snapshot `2026-08-07-v3.0.0` — brand rebuild

Preserves the profile as it stood at **v3.0.0**, immediately before the rebuild
that repositioned it from a job title to a named identity. Everything in the
snapshot was taken from `origin/main` at commit `f3f1a03` and is byte-identical
to what was live.

### `README.md`

Archived at `archive/2026-08-07-v3.0.0/README.md`. This is the version whose
hero read *Senior Full Stack Engineer*, and in which the `Current Focus` and
`Featured Projects` sections were wrapped in HTML comments and therefore did
not render.

It is worth keeping for one reason beyond reversibility: it carries the
scaffolding and TODO comments written while those two sections were hidden,
including the four-blank card template for the product entries. If a future
pass needs that template again, it is here rather than several commits back.

### `banner/`

Both banner SVGs are archived because the rebuild **overwrote them in place**
rather than adding new files — restoring the v3.0.0 README without them would
produce a page whose banner does not match its text. These are the 1200×260
versions: flat white or dark background, a ruled grid, a solid accent bar, and
a four-line text block ending in the strip
`TYPESCRIPT · REACT · NEXT.JS · NODE.JS · NESTJS · AI`.

The replacements are 1200×320 and differ in kind, not degree: gradient field,
glassmorphic panel, neural-network motif. If the new banner ever proves too
heavy for the page, the v3.0.0 pair is the lighter design to fall back to.

### Naming

The earlier snapshot in this file is named for its date alone. This one was
taken on the same date, so it carries `-v3.0.0` as well. Future snapshots
should follow `<YYYY-MM-DD>-v<version>`; the original directory is left under
its bare date rather than renamed, because `archive/README.md` and this file
both already refer to it by that name.

### What was not archived

No workflow, script or configuration file was modified by the rebuild, so
`.github/` needed no snapshot. `CHANGELOG.md` and `archive/` are append-only
records rather than replaced content, and archiving a record of the archive
would be circular.

## Snapshot `2026-08-07` — profile modernization

The repository contained exactly two files before this change: `README.md` and
`.github/workflows/snake.yml`. Both are preserved verbatim in
`archive/2026-08-07/`.

There were **no** `assets/`, `images/`, or `widgets/` directories, and no other
workflows, so nothing else existed to archive. All imagery in the old README was
loaded from third-party services at render time rather than stored in the repo.

### `README.md`

Archived at `archive/2026-08-07/README.md`. Replaced by a restructured README.
Every factual claim in the old file — skills, open-source contributions, contact
links, including the five links that were commented out — was carried across to
the new one or preserved as a comment in it. What changed and why:

| Old element | Disposition | Reason |
| --- | --- | --- |
| Intro paragraph | Rewritten | Kept the substance; reorganized into a hero block plus an `About` section so the first screen reads as an introduction rather than a wall of prose. |
| Visitor badge (`visitor-badge.laobi.icu`) | Removed | A hit counter is a vanity metric, not a hiring signal. It also sent every visitor's request to a third-party host on every page view. |
| `🏆 GitHub Awards` trophy panel | Removed | `github-profile-trophy` renders a row of decorative trophies derived from the same numbers the stats card already shows. Redundant, and the main source of badge-spam feel. |
| Streak stats card | Kept, host corrected | The URL pointed at `github-readme-streak-stats.herokuapp.com`. The project's documented default host is now `streak-stats.demolab.com`; the Heroku deployment is a self-hosted option that costs money to keep running. |
| GitHub stats card | Kept, restyled | Switched from the `radical` theme to a theme pair selected by `prefers-color-scheme`, so the card matches whichever GitHub theme the reader uses. |
| Snake animation | Kept, **URLs fixed** | The three `srcset`/`src` URLs used `github.com/rahul-rocket/rahul-rocket/blob/output/…`. That path returns an HTML page (`Content-Type: text/html`), not an image, so all three rendered as broken images. Now pointed at `raw.githubusercontent.com/…/output/…`, which returns `image/svg+xml`. |
| `📫 Get in Touch` badges | Kept, converted to text links | Six of the eight were commented-out `img.shields.io` badges. Plain text links carry the same information, cost no external requests, and are readable by screen readers without relying on badge alt text. The commented-out destinations are preserved as a comment in the new README so they can be re-enabled. |
| Skills bullet list | Kept, regrouped | Same technologies, reorganized into a labelled table. `CodeIgnitor` corrected to `CodeIgniter`. |
| Open-source contributions | Kept | Unchanged in substance; moved into a table alongside the role held on each project. |

### `.github/workflows/snake.yml`

Archived at `archive/2026-08-07/workflows/snake.yml`. Rewritten in place rather
than replaced — it still generates the animation with `Platane/snk@v3` and
publishes to the `output` branch, so the existing branch and its consumers keep
working. Changes:

- `actions/checkout@v3` **removed**. Neither `snk` nor the publish step reads the
  repository working tree, so the checkout was doing nothing but adding runtime.
  (v3 also runs on a deprecated Node runtime.)
- `actions/upload-artifact@v4` step **removed**. It uploaded a copy of output
  that is already committed to the `output` branch, where it expires after 90
  days and is never downloaded.
- The `github-contribution-grid-snake.gif` output **removed**. Nothing references
  it; the two SVGs are what the README uses.
- `peaceiris/actions-gh-pages` bumped **v3 → v4**.
- Added an explicit least-privilege `permissions: contents: write` block, a
  `concurrency` group so overlapping runs cannot race, and a `push` trigger
  scoped to the workflow file itself so edits are verified immediately.
- Commit message changed to the Conventional Commits form.

Nothing about the `output` branch or its contents was touched, so the currently
published SVGs remain live until the next scheduled run overwrites them.

### Follow-up: hero banner rewording (same day)

The banner SVGs added in the redesign originally carried the GitHub profile bio
— *Web Artisan · Open-Source Enthusiast / Full Stack Developer · Problem Solver*
— and were rewritten hours later to carry the requested positioning: *Senior
Full Stack Engineer · AI Engineer / SaaS Builder · Cloud Architect*. No snapshot
directory was created for this: both versions are assets authored in this
repository on the same day, and the earlier wording is one `git show` away.

```bash
git log --oneline -- assets/banner/
git show <commit>:assets/banner/profile-banner-dark.svg
```

### Other branches

`master`, `gh-pages`, and `output` all still exist on the remote and were not
modified by this change. `gh-pages` holds an old copy of the README and
workflow, and `master` is a stale duplicate of an early `main`; both are
independent historical records and are best left alone unless you decide to
clean them up deliberately.
