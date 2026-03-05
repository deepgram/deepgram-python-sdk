# Review Fern SDK Regeneration

Triggers: review regen, review regeneration, diff regen, compare regen, post regen review

## Steps

Read AGENTS.md for full context on the regeneration workflow and freeze classification rules.

1. Find all `.bak` files in the repo — these are our pre-regen manually-patched versions (protected by `.fernignore`).
2. For each `.bak` file, diff it against the corresponding newly generated file to show what changed.
3. Identify which manual patches are still needed (the `.bak` has changes the generator doesn't produce).
4. Present a summary of findings to the user, grouped by category:
   - Patches no longer needed (generator now handles it)
   - Patches still needed (must be re-applied)
   - New changes from the generator worth noting
5. Wait for user direction on which patches to re-apply.
6. Re-apply confirmed patches to the generated files.
7. In `.fernignore`, replace each `.bak` path back to the original path for files that still need patches.
8. Remove `.fernignore` entries entirely for files where patches are no longer needed.
9. Delete all `.bak` files.
10. Run `ruff check --fix`, `mypy --ignore-missing-imports src/deepgram/`, and `pytest` to verify.
11. Commit as `chore: re-apply manual patches after regen` and push.
