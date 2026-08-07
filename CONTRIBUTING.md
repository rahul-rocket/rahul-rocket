# Contributing

This is a personal profile repository — the README it contains is what renders
at [github.com/rahul-rocket](https://github.com/rahul-rocket). It isn't a
library, so there's no feature roadmap to contribute to. Small corrections are
genuinely welcome though.

## Worth opening an issue or PR for

- A broken link, a dead badge, or a widget that stopped rendering.
- A typo or grammatical slip.
- An accessibility problem — missing alt text, a heading level skipped, contrast
  that fails at the default GitHub themes.
- A workflow that has started failing, or an action pinned to a version that has
  since been deprecated.

Please don't send PRs that rewrite the wording, restyle the layout, or add
widgets — those are personal-taste calls and will be closed.

## Working on it locally

```bash
git clone https://github.com/rahul-rocket/rahul-rocket.git
cd rahul-rocket
```

There is no build step. Preview your change by pasting the README into any
GitHub Markdown preview, or by pushing to a branch and viewing the file on
GitHub — that is the only renderer that matters here, since GitHub sanitizes
HTML and resolves the `<picture>` elements itself.

### Check the Markdown

```bash
npx markdownlint-cli2 "**/*.md"
```

The same command runs in CI on every push and pull request. Configuration lives
in [`.markdownlint-cli2.jsonc`](.markdownlint-cli2.jsonc); inline HTML and long
table rows are deliberately allowed, because GitHub-flavoured profile READMEs
need both.

### Check the workflows

All four workflows can be run by hand from the Actions tab — each declares
`workflow_dispatch`. `metrics.yml` will skip every step and pass as a no-op
unless a `METRICS_TOKEN` secret exists; that is expected, not a failure.

Two things to know before changing them:

- **Every `uses:` is pinned to a release tag.** Never `@master` or `@latest` —
  an unpinned reference lets an unreviewed upstream change run against this
  repository's write token. Bump a pin deliberately, in its own commit.
- **`activity.yml` and `metrics.yml` push to `main`, which is protected.** Their
  pushes only land if `github-actions[bot]` is allowed to bypass the branch
  rule; see the comment at the top of `activity.yml`. `snake.yml` is unaffected
  — it publishes to the unprotected `output` branch.

## Conventions

- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/):
  `feat:`, `fix:`, `docs:`, `ci:`, `chore:`, with an optional scope such as
  `feat(readme):`.
- **Markdown** wraps prose at 80 characters. Tables and URLs are exempt.
- **Images** need descriptive `alt` text, and any image that carries meaning in
  colour needs both a dark and a light variant — see
  [`assets/README.md`](assets/README.md).
- **Nothing gets deleted outright.** Content being replaced is copied into
  `archive/<date>/` first, with a note in [`archive/notes.md`](archive/notes.md)
  explaining why. See [`archive/README.md`](archive/README.md).
- **Notable changes** are recorded in [`CHANGELOG.md`](CHANGELOG.md).

## Unverified claims

The README deliberately carries `TODO (Rahul)` comments where a fact could not
be verified from a public source — project descriptions, and specific tools in
the Cloud, DevOps, AI and Testing categories. Please leave those in place rather
than filling them with a plausible guess; an unfilled TODO is the honest state,
and only the profile's owner can resolve it.
