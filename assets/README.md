# Assets

Static assets for the profile README. Everything here is committed to the
repository so the README does not depend on an external image host.

```text
assets/
├── banner/    Hero banner, one SVG per colour scheme
├── icons/     Small inline icons (currently empty)
├── images/    Screenshots and photos (currently empty)
└── metrics/   Generated output — see .github/workflows/metrics.yml
```

## Conventions

- **Prefer SVG.** The banners are hand-written SVG, a couple of kilobytes each,
  and stay sharp at any width. Use raster formats only for photographs.
- **Ship both colour schemes.** Files ending in `-dark` / `-light` are selected
  by a `<picture>` element in the README using `prefers-color-scheme`. The
  `<img>` fallback inside each `<picture>` must always point at the light
  variant, since that is what renderers without media-query support will show.
- **Describe every image.** Each SVG carries a `<title>` and `<desc>`, and every
  `<img>` in the README carries descriptive `alt` text.
- **Compress raster assets** before committing (for example with `oxipng` or
  `squoosh`), and keep individual files under roughly 200 KB.

## Generated files

`assets/metrics/` is written by the **GitHub Metrics** workflow. Do not edit it
by hand — the next scheduled run will overwrite it. The workflow only runs once
a `METRICS_TOKEN` secret exists; see the comments in
[`.github/workflows/metrics.yml`](../.github/workflows/metrics.yml).

The snake animation is *not* stored here: it is published to the orphan `output`
branch by [`.github/workflows/snake.yml`](../.github/workflows/snake.yml) and
referenced from the README over `raw.githubusercontent.com`, which keeps the
generated binaries out of the main branch's history.
