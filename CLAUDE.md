# Working in this repository

## Always open a pull request

Every change ships as a pull request. After making changes, without being asked:

1. Commit on the designated feature branch, using
   [Conventional Commits](https://www.conventionalcommits.org/).
2. `git push -u origin <branch>`.
3. **Open the PR immediately**, describing what changed, why, and how it was
   verified.

A pushed branch with no PR is an unfinished change. Never commit directly to
`main`.

If the branch's previous PR has already been merged, that PR is finished and
cannot carry new work: restart the branch from the latest `main`
(`git fetch origin main && git checkout -B <branch> origin/main`) and open a new
PR, rather than stacking commits on merged history.

Two reasons this is not optional here:

- `main` is protected, so a direct push is rejected anyway.
- This repository renders as the public profile at
  [github.com/rahul-rocket](https://github.com/rahul-rocket). The PR is the only
  review step between a change and something every visitor sees.

Before opening the PR, run `npx markdownlint-cli2 "**/*.md"` — the same check
runs in CI on every pull request.
