# Changelog

All notable changes to this profile repository are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [4.1.0] — 2026-08-07

Follow-up to 4.0.0, narrowing what the profile shows while the products behind
it are still private.

### Hidden

- **The `CreatorOS` and `Planix` cards**, wrapped in a single HTML comment
  inside `Featured Projects`. The rest of the section renders: PDFily,
  KidzoRides, and the two verified repository cards.

  Consequence worth recording: CreatorOS was the card carrying the AI
  positioning that the banner and `Currently Building` both lead with. With it
  hidden, PDFily is the only card on the page that mentions AI at all, and it
  is not public either. The `Currently Building` TODO records this.

- **`Recent Activity`**, the subsection of `Open Source` written daily by
  `activity.yml`, to be added back later. This one was **removed rather than
  commented out**: its content sat between two marker comments, and since HTML
  comments do not nest, an outer wrapper would have closed at the first
  marker’s delimiter and leaked the rest onto the live profile. A comment in
  its place records where it belonged and how to restore it, pinned to commit
  `4471f5b`, which is on `main` and holds the markers verbatim.

### Changed

- **`activity.yml` schedule disabled.** The action fails by design when the
  README markers are absent, so with the section hidden its daily run would
  have failed every morning. The `schedule:` trigger is commented out and
  `workflow_dispatch` kept, so nothing runs and nothing fails while the section
  is away. The section and the schedule must be restored together — the
  section without the workflow is a heading that never updates, and the
  workflow without the section is a daily red cross.

## [4.0.0] — 2026-08-07

Fifth pass, and the one that turns the page from a well-formatted README into
a developer brand. The positioning moves from a job title to a named identity —
**AI Engineer · React &amp; Next.js Architect · SaaS Builder · Open Source
Developer** — and the two sections that were hidden pending correction are
restored with real content instead of scaffolding.

### Changed

- **Both banner SVGs redrawn** at 1200×320. They now carry a layered gradient
  field, a glassmorphic content panel with a gradient edge, a faint grid, a
  three-layer neural-network motif standing in for the AI reference, and a
  gradient-filled name. Light and dark are separate documents rather than one
  file with a filter, so each palette is tuned on its own.
- **Hero rewritten** around the four-part identity line. The emoji focus row
  was dropped — the banner already carries the same claim, and repeating it
  immediately underneath weakened both.
- **`Current Focus` republished as `Currently Building`**, rewritten as a
  table of what is actively under construction (AI applications, MCP servers,
  React 19 &amp; Next.js, AI developer tools, full stack SaaS, Ever Gauzy)
  rather than a list of things being learned.
- **`Featured Projects` republished** with the four product cards — CreatorOS,
  Planix, PDFily, KidzoRides — carrying their descriptions. Stack and status
  read *private, not yet documented publicly* rather than inventing
  technologies for repositories that are not public. The two verified cards
  (`rahul-rocket.github.io`, `nestjs-multi-orm`) follow them.
- **`Tech Stack` renamed to `Technical Expertise`**; `GitHub Metrics` to
  `GitHub Activity`; `Open Source Contributions` to `Open Source`, which also
  gained a row for `nestjs-multi-orm` as author.
- **Sections reordered** to Banner → About Me → Currently Building → Featured
  Projects → Open Source → Technical Expertise → GitHub Activity → Latest
  Gists → How I Build → Get in Touch, so identity, proof and impact lead and
  decoration follows.
- **Footer replaced with a call to action** — a question, a line on the kind
  of work being sought, and a direct mail link — in place of the previous
  single closing sentence.

### Added

- **A `How I Build` section**: a short statement of approach plus three
  principles (ship inspectable work, type the boundaries, budget for the
  reader).
- **Archive snapshot `archive/2026-08-07-v3.0.0/`**, holding the v3.0.0 README
  and both v3.0.0 banner SVGs byte-identical to what was live, so this rebuild
  can be reverted without reading git history. The banners are included because
  the rebuild overwrote them in place — restoring the README alone would leave
  a banner that no longer matches its text. Snapshot naming gained a version
  suffix, since this is the second snapshot taken on 2026-08-07 and dates alone
  collide.

### Not added

- **An achievements block.** Requested, and deliberately left as a comment in
  the source rather than published. The `profile-details` card immediately
  above prints real commit, PR and contribution totals; a hand-written
  "1000+ commits" next to a live figure only creates a chance to be caught
  disagreeing with it. The comment records what to publish once each claim
  points at something a reader can open.

## [3.0.0] — 2026-08-07

Fourth pass, and a repositioning rather than a tidy-up. The previous three
passes made the profile readable; this one makes it say something specific.
The profile now leads with **AI applications, React &amp; Next.js SaaS, and
developer tools** instead of a general full-stack summary, and the section
order was rebuilt so a reader meets the positioning, the proof, and the stack
in that order.

### Changed

- **New hero and banner.** Both banner SVGs were redrawn around the name and a
  single positioning line, with the technology strip changed from
  `TYPESCRIPT · ANGULAR · NESTJS · NODE.JS` to
  `TYPESCRIPT · REACT · NEXT.JS · NODE.JS · NESTJS · AI`. The README hero
  carries the same claim in text, plus a one-line focus row.
- **Sections reordered** to Banner → Hero → About Me → Current Focus →
  Featured Projects → Tech Stack → GitHub Metrics → Open Source Contributions →
  Latest Gists → Get in Touch → Footer. Tech Stack moved above the widgets and
  Open Source Contributions below them, so the page reads claim → evidence →
  activity instead of interleaving them.
- **`Skills` renamed to `Tech Stack`**, with React and Next.js promoted to the
  front of the Frontend row. `Currently` renamed to `Current Focus`.
- **`Recent Activity` is now a subsection of Open Source Contributions**
  rather than a peer heading, which is what it actually describes.
- **`Get in Touch` gained Email and X rows**, both restored from handles that
  the pre-redesign README carried commented out, plus a location/timezone row.
  Each row is prefixed with the channel's icon.

### Added

- **A `Latest Gists` section**, written between markers by a new `gists.yml`
  workflow. It runs `.github/scripts/update_gists.py` — a standard-library
  script against the public gists API — rather than a third-party action,
  because none exists for gists and the script keeps the job off the supply
  chain. The script is idempotent, so a quiet day produces no commit, and it
  renders "No public gists yet." rather than an empty section.

### Removed

- **The streak-stats card.** Current streak, longest streak and total
  contributions restate the same contribution history that the stats card and
  the two graphs already show. It was the widget most likely to read as padding
  rather than evidence, and it was the one card the redesign brief did not ask
  to keep.
- **"Cloud Architect" from the hero.** It was asserted with nothing public
  behind it. The same applies to the AI positioning, which is kept because it
  is the stated direction — but the README now says so in the open rather than
  implying a track record, and carries a TODO naming the missing artifact.

### Notes

Four product cards — CreatorOS, Planix, PDFily and KidzoRides — remain
commented-out scaffolds. None of them is public, so there is nothing factual to
write from; the layout is finished and waiting on four blanks each. The
Featured Projects comment now also shows where a screenshot goes, since the
brief asked for screenshots over bare links.

## [2.3.0] — 2026-08-07

### Fixed

- **The two GitHub statistics cards were rendering broken and are replaced.**
  `github-readme-stats.vercel.app` had stopped serving: GitHub's camo proxy
  returned `502 Error Fetching Resource` for that host on every attempt across
  repeated checks, including with all query parameters stripped, so the failure
  was the host itself rather than the URLs. The public instance of that project
  shares a single free-tier quota across every profile that embeds it, which
  makes this a recurring failure mode, not a one-off outage.

  Replaced with `github-profile-summary-cards`: `profile-details` for the
  headline numbers, and `repos-per-language` plus `most-commit-language` in
  place of the single top-languages card. Each replacement was verified to
  resolve **through camo** before being committed — a URL that loads in a
  browser can still 502 for GitHub, so browser-level checking is not
  sufficient.

  The activity graph and the snake were checked at the same time and were
  serving normally throughout; they are unchanged.

### Changed

- Card themes are now `github_dark` / `github`, confirmed to be a genuine
  dark/light pair (`#0d1117` vs `#ffffff` backgrounds). `light` is not a real
  theme name for this service — it silently falls back to `default` — so it is
  not used.
- Layout note rewritten for the new intrinsic sizes: `profile-details` is 700px
  and takes its own row, the two language cards are 340px each and pair inside
  the ~880px content column.

### Notes

The section is still built from render-time third-party services, and one has
now failed once. The durable fix is the `lowlighter/metrics` panel already wired
up in `metrics.yml`: a workflow that generates an SVG and commits it has no
render-time dependency and cannot break this way. The snake graph already works
like that, which is why it kept rendering while the stats cards did not. This is
recorded in the README next to the metrics TODO.

## [2.2.0] — 2026-08-07

Third pass. The structure from 2.0.0 held up, so this is a correctness and
density pass rather than another redesign: supply-chain pins on the workflows,
a documented failure mode, and the removal of the last duplicated content.

### Fixed

- **Both unpinned actions are now pinned to release tags.**
  `jamesgeorge007/github-activity-readme@master` → `@v0.4.5` and
  `lowlighter/metrics@latest` → `@v3.34`. Both previously resolved to a moving
  pointer, so an unreviewed upstream change could have run against this
  repository's `contents: write` token without any commit here. Every `uses:`
  in the repository is now pinned; all five tags were confirmed to exist.
- **`Recent Activity` no longer renders as a bare heading.** The section had
  nothing between its markers, so the live profile showed a heading with empty
  space under it. A placeholder line now sits there and is overwritten by the
  workflow's first successful run.
- **Documented why `activity.yml` and `metrics.yml` may fail.** Both commit to
  `main`, which is a protected branch; unless `github-actions[bot]` is allowed
  to bypass the rule, every run fails at the push step. This is a repository
  setting only the owner can change, so it is recorded in the workflow header
  and in `CONTRIBUTING.md` rather than worked around in YAML. `snake.yml` is
  unaffected — it publishes to the unprotected `output` branch.

### Changed

- **Stats and Top Languages now sit side by side**, recovering roughly a screen
  of scroll. `card_width` dropped 450 → 400: inside the centred `<div>` GitHub
  renders every card as an inline sibling sharing one wrapping line box, so
  width alone decides the layout. At 450 the pair totalled 900px against a
  ~880px content column and always wrapped; at 400 they fit, and still stack on
  a phone. Verified against the live rendered HTML on both branches — the blank
  lines between the cards turned out to have no effect either way, and the note
  in the README says so, so the next edit does not preserve a rule that was
  never real.
- **The `📫 Get in Touch` section is no longer a verbatim repeat of the hero
  link row.** Same four destinations, now a table stating what each channel is
  actually for. The section and its heading are kept, as previously requested.
- **Hero tightened** — the six-role positioning is unchanged but rebalanced onto
  two even lines, and the value proposition is one sentence instead of two.
- **Closing line replaced.** "Let's collaborate and create something amazing
  together!" was the one line on the page that read like a template.

### Verified, not changed

Checked this pass and found correct, so recorded here to save the next audit:

- The banner's `<picture>` relative `srcset` paths are rewritten correctly by
  GitHub's renderer (to `/rahul-rocket/rahul-rocket/raw/main/…`) — confirmed
  against the live rendered HTML, not assumed.
- The snake's dark and light SVGs are genuinely different palettes
  (`--c0:#161b22` vs `#ebedf0`); the `?palette=github-dark` output works.
- `markdownlint-cli2` reports 0 issues across all 4 linted files.
- The four third-party widget URLs are served through GitHub's camo proxy, so
  they cost the reader no direct third-party request. Their upstream
  availability could not be checked from the build sandbox, whose network policy
  blocks those hosts.

### Open TODOs

Unchanged from 2.1.0 and still blocked on information only the owner has — the
product cards, the Cloud/DevOps/AI/Testing skill rows, and the AI/cloud evidence
bullets in `About`. See the 2.1.0 notes below for what each needs.

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
