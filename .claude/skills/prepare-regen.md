# Prepare Repo for Fern SDK Regeneration

Triggers: prepare regen, prepare for regeneration, prep for fern, new sdk gen, prepare sdk gen

## Steps

Read AGENTS.md for full context on the regeneration workflow.

1. Fetch latest `main` and create a new branch: `lo/sdk-gen-<YYYY-MM-DD>` (use today's date).
2. Push the branch to origin.
3. Create an empty commit (`chore: initialize SDK regeneration branch`) if needed, then create a PR titled `chore: SDK regeneration <YYYY-MM-DD>` with body `## Summary\n- Fern SDK regeneration`.
4. Read `.fernignore` and identify all frozen generated files (Client & Socket Clients, Type Fixes, Redact type, Listen Clients, Tests & WireMock). Do NOT unfreeze the "always frozen" files listed in AGENTS.md.
5. Back up each identified file as `<filename>.bak` alongside the original.
6. Remove their entries and associated comments from `.fernignore`.
7. Stage the updated `.fernignore` and all `.bak` files.
8. Commit as `chore: unfreeze files pending regen` and push.
9. Report the PR URL and confirm the branch is ready for generator output.
