# Prepare Repo for Fern SDK Regeneration

Triggers: prepare regen, prepare for regeneration, prep for fern, new sdk gen, prepare sdk gen

## Steps

Read AGENTS.md for full context on the regeneration workflow and freeze classification rules.

1. Fetch latest `main` and create a new branch: `lo/sdk-gen-<YYYY-MM-DD>` (use today's date).
2. Push the branch to origin.
3. Create an empty commit (`chore: initialize SDK regeneration branch`) if needed, then create a PR titled `chore: SDK regeneration <YYYY-MM-DD>`.
4. Read `.fernignore` and classify each entry using the rules in AGENTS.md:
   - **Permanently frozen**: entirely hand-written, no Fern equivalent. NEVER touch these.
   - **Temporarily frozen**: Fern-generated with manual patches. These get swapped.
5. For each **temporarily frozen** file only:
   - Copy the file to `<filename>.bak` alongside the original.
   - In `.fernignore`, replace the original path with the `.bak` path (protects our patch, lets Fern overwrite the original).
6. Stage the updated `.fernignore` and all `.bak` files.
7. Commit as `chore: unfreeze files pending regen` and push.
8. Report the PR URL and confirm the branch is ready for generator output.
