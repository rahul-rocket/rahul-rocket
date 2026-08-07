# Changelog

All notable changes to this profile repository are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.1.0] — 2026-08-07

Second pass: repositioning, repository scaffolding, and two more workflows.

### Added

- **Positioning in the hero** — Senior Full Stack Engineer, AI Engineer, Open
  Source Developer, SaaS Builder, Developer Tools Enthusiast, Cloud Architect —
  plus a one-line value proposition and the current role.
- **`LICENSE`** (MIT). <!-- TODO (Rahul): the copyright line reads "Rahul Rocket"; swap in your legal name if you would rather it be enforceable under that. -->
- **`CONTRIBUTING.md`** — what is worth an issue or PR on a profile repository,
  how to lint locally, and the archive-before-delete rule.
- **`.markdownlint-cli2.jsonc`** and a **`Lint` workflow** running
  `markdownlint-cli2` on every push and pull request. The repository now lints
  clean.
- **`Recent Activity` workflow** (`activity.yml`) writing the five most recent
  public events into the README between marker comments.
- **Four product cards** for CreatorOS, Planix, PDFily and KidzoRides — see
  *Open TODOs* below.
- **Cloud, DevOps, AI and Testing skill rows**, drafted with candidate
  technologies — see *Open TODOs* below.

### Changed

- Hero banner rewritten to carry the new positioning. Both SVG variants were
  regenerated; the previous wording is in git history and noted in
  `archive/notes.md`.
- `About` reframed around business platforms rather than a generic full-stack
  summary.
- Project cards gained a consistent **Stack / Status / Links** triple, so every
  card exposes the same fields.
- Prose rewrapped at 80 columns. `MD013` is deliberately off in the lint config:
  a widget's `<source srcset="…">` is one unbreakable URL well past 80 columns,
  so enforcing it would mean an inline disable comment on nearly every image.

### Open TODOs

Two additions are committed **inside HTML comments** so the live profile never
renders half-empty cards or blank table cells. Each is a complete block that
becomes visible the moment it is filled in and uncommented:

- **CreatorOS, Planix, PDFily, KidzoRides** — none is public. They do not appear
  under `github.com/rahul-rocket` (all 18 repositories were enumerated), nor
  anywhere in the `rahul-rocket.github.io` repository. Each card has the layout
  in place and four blanks: description, stack, status, links.
- **Cloud / DevOps / AI / Testing skills** — drafted with candidate
  technologies to trim rather than a guess at what is actually in use.
- **AI engineering and cloud architecture bullets** in `About` — the hero states
  the positioning; these two bullets are the evidence behind it and need the
  real product and capability named.

## [2.0.0] — 2026-08-07

Full redesign of the profile README, plus a rebuild of the automation behind it.
Nothing was deleted: the previous README and workflow are preserved verbatim
under [`archive/2026-08-07/`](archive/2026-08-07/), with per-item reasoning in
[`archive/notes.md`](archive/notes.md).

### Added

- Hero banner as a local SVG in two colour schemes
  (`assets/banner/profile-banner-{dark,light}.svg`), selected with `<picture>`
  and `prefers-color-scheme`. Hand-written, ~1 KB each, no external request.
- `About`, `Currently`, and `Featured Projects` sections — the profile
  previously had no project showcase at all.
- Project cards for `rahul-rocket.github.io` and `nestjs-multi-orm`, each with
  stack, status, and a live link where one exists.
- `assets/` directory structure (`banner/`, `icons/`, `images/`, `metrics/`)
  with [conventions documented](assets/README.md).
- `archive/` directory with a restore procedure and a rationale for every
  archived item.
- Opt-in **GitHub Metrics** workflow (`.github/workflows/metrics.yml`). It skips
  cleanly — a passing no-op run, not a failure — until a `METRICS_TOKEN` secret
  is configured.
- Activity graph widget, giving a view of contribution volume over time that the
  stats card does not provide.
- This changelog.

### Fixed

- **The snake animation was not rendering.** All three of its URLs pointed at
  `github.com/…/blob/output/…`, which serves an HTML page rather than an image.
  They now use `raw.githubusercontent.com`, which returns `image/svg+xml`.
- Streak stats pointed at `github-readme-streak-stats.herokuapp.com`. Repointed
  at `streak-stats.demolab.com`, the host the project currently documents.
- `CodeIgnitor` → `CodeIgniter`.

### Changed

- Widgets are now theme-aware. Each card ships a dark and a light variant chosen
  by `prefers-color-scheme` instead of a single fixed theme (`radical`) that
  clashed with light-mode GitHub.
- Contact links converted from `img.shields.io` badges to text links: same
  information, four fewer image requests, and readable without relying on badge
  alt text. The `📫 Get in Touch` section keeps its heading, its closing
  invitation, and the five commented-out destinations, and is now mirrored by a
  compact link row in the hero.
- `🐍 Contribution Snake Graph` keeps its own heading, now nested as an `h3`
  under `GitHub` alongside the other cards.
- Skills regrouped from a flat emoji-prefixed bullet list into a labelled table
  (Languages, Frontend, Backend, Databases, APIs, Tooling).
- Open-source contributions moved into a table that names the role held on each
  project.
- Heading hierarchy made semantic — a single `h1` (the name, as real text rather
  than baked into an image) followed by `h2` sections and `h3` project titles,
  with no level skipped.
- Every image carries descriptive `alt` text; both banner SVGs carry `<title>`
  and `<desc>`.
- Snake workflow: dropped the unused `actions/checkout@v3` and
  `upload-artifact@v4` steps and the unreferenced GIF output; bumped
  `peaceiris/actions-gh-pages` v3 → v4; added least-privilege `permissions`, a
  `concurrency` group, and a path-scoped `push` trigger.

### Removed

- Visitor-count badge — a vanity metric that sent a third-party request on every
  page view.
- `github-profile-trophy` panel — decorative, and derived from numbers the stats
  card already reports.
- Unused snake GIF generation and the artifact upload that duplicated content
  already committed to the `output` branch.

All removals are recoverable from `archive/2026-08-07/` and from git history.

### Open TODOs

Marked as HTML comments in `README.md`, at the point where each belongs:

- **AI Engineering, Cloud, DevOps, Testing.** The brief asked for these to be
  highlighted. Nothing in the public repositories or profile evidences them, so
  they were left out rather than invented. Add them once there is public work to
  point at.
- **`gpt-chatbot`.** No repository description, and its README is a single
  heading — there was no factual basis for a project card.
- **Metrics panel embed.** Add the `assets/metrics/metrics.svg` image to the
  README after the first successful metrics run.

### Future ideas

- Pin the featured repositories on the GitHub profile so they match this README.
- Add repository descriptions and topics to `rahul-rocket.github.io`,
  `nestjs-multi-orm`, and `gpt-chatbot` — they surface in search and on the
  profile, and all three are currently blank.
- Add a `LICENSE` to `nestjs-multi-orm`; an unlicensed repository is not
  reusable, which limits adoption of a library.
- Replace the third-party stats cards with self-hosted SVGs generated by a
  workflow, removing the last of the render-time external dependencies.
- Decide the fate of the stale `master` and `gh-pages` branches.
- A "latest blog posts" or "recent activity" section, once there is a feed to
  pull from.

## [1.x] — 2022-03-11 … 2026

The original profile: an introduction, a skills list, open-source
contributions, a trophy panel, streak and stats cards, the snake graph, and a
row of contact badges — plus the daily workflow that generated the snake
animation. Preserved in [`archive/2026-08-07/`](archive/2026-08-07/) and in git
history.
