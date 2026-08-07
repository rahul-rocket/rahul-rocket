# Gist Knowledge Base

Production-ready, reusable reference material on AI engineering, React, Next.js,
TypeScript, and modern backend work. Each file here is a self-contained
technical article, written to be published as a standalone GitHub Gist and to
stand on its own when read in this repository.

## Standard structure

Every gist follows the same shape, so a reader who has read one knows where to
look in the next:

1. Clear title
2. Short introduction
3. Why this matters
4. Complete example
5. Explanation
6. Best practices
7. Common mistakes
8. Performance considerations
9. Security considerations (where applicable)
10. Related resources

## Published

### AI Engineering

| Gist | Suggested Gist filename | What it covers |
| --- | --- | --- |
| [MCP Server Starter](ai-engineering/mcp-server-starter.md) | `mcp-server-starter.md` | A typed, testable Model Context Protocol server in TypeScript — tools, resources, validation, error handling, transports, and the security boundary |

## Planned

Categories to be filled in, one complete gist at a time:

- **AI Engineering** — Claude Code best practices, prompt engineering,
  Anthropic and OpenAI API integration, streaming responses, AI code review
- **React** — folder structure, custom hooks, performance, React Query,
  Suspense, error boundaries, forms, authentication
- **Next.js** — App Router, server actions, route handlers, metadata and SEO,
  middleware, caching, image optimization, deployment
- **Node.js & NestJS** — clean architecture, DI, authn/authz, JWT, logging,
  validation, uploads, API versioning, background jobs
- **Databases** — Prisma, Drizzle, PostgreSQL, transactions, indexing,
  migrations
- **Cloud & DevOps** — Docker, GitHub Actions, CI/CD, Vercel, environment
  variables, monitoring
- **Testing** — Vitest, Playwright, Testing Library, mocking, integration and
  end-to-end
- **Developer productivity** — Git, pnpm, Turborepo, ESLint, Prettier
- **TypeScript** — utility types, generics, type guards, conditional and mapped
  types
- **Career & engineering** — code review checklists, SOLID, API design,
  monorepos

## Publishing

Every Markdown file in this directory except this index is published to
<https://gist.github.com/rahul-rocket> as a public gist by the
[Publish Gists workflow](../.github/workflows/publish-gists.yml). The repository
stays the source of truth; the gists are copies, republished from here.

### One-time setup

1. **Create a token.** Go to
   <https://github.com/settings/tokens> → **Generate new token (classic)**.
   Tick **only** the `gist` scope, and nothing else. A fine-grained token will
   not work — fine-grained tokens cannot access gists at all, because gists are
   account-level rather than repository-level.
2. **Store it.** Repository → **Settings → Secrets and variables → Actions →
   New repository secret**. Name it exactly `GIST_TOKEN` and paste the token.
   The built-in `GITHUB_TOKEN` cannot be used here for the same reason: it is
   scoped to this repository.
3. **Allow the push.** The workflow commits `gists/published.json` back to
   `main`, which is protected, so `github-actions[bot]` needs the bypass already
   described at the top of `.github/workflows/activity.yml`.

### Publishing a gist

1. Merge the gist file to `main`.
2. Repository → **Actions → Publish Gists → Run workflow**.
3. Leave **dry run** checked for the first run. The job logs exactly which
   files it would create or update and calls no API. Read the log.
4. Run it again with **dry run** unchecked. The run summary prints a table of
   source paths and the resulting gist URLs.

### How republishing works

`gists/published.json` maps each source path to the gist ID it created, and the
workflow commits it back after every real run. On later runs a file with a
recorded ID is **updated in place**, so the gist URL is stable and its revision
history accumulates — the same file is never published twice as two gists.

Two consequences worth knowing:

- **Renaming a source file creates a second gist.** The registry is keyed by
  path, so the old entry is orphaned and the old gist is left live. Delete the
  stale gist by hand and drop its line from `published.json`.
- **Deleting a gist on gist.github.com is recoverable.** The next run notices
  the ID is gone, recreates the gist, and records the new ID rather than
  failing.

The workflow is manual-only, with no schedule. Publishing to a public URL under
your own name is not something to leave on a nightly timer.
