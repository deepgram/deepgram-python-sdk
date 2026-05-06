# Pull Request Interface & Contract Review

You are reviewing a pull request to assess its impact on the project's **public interface and contracts**. Your goal is to produce a per-interface review that classifies every signature change by breaking-change risk, identifies what backwards-compatibility measures were taken, and calls out gaps that remain.

This review is **strictly about the public surface** — types, classes, function signatures, request/response schemas, exported symbols, wire formats, and CLI/config flags. It is *not* a general code review.

---

## Step 1 — Gather the change set

1. Fetch the PR metadata, file list, and diffs. Don't stop at the first page — paginate until you have every changed file.
2. Identify the **public-surface files**. Heuristics:
   - Anything re-exported from `__init__.py`, `index.ts`, `mod.rs`, `lib.rs`, package entry points, or barrel files.
   - Files under `types/`, `models/`, `schemas/`, `requests/`, `responses/`, `dto/`, `api/`, `proto/`, `openapi/`, `*.d.ts`.
   - Generated SDK files (Fern, OpenAPI Generator, protoc, etc.) — these are public surface even when auto-generated.
   - Any file whose path or name suggests it defines a contract (`*_request.py`, `*Params`, `*Response`, `I*.ts`, `*.proto`).
3. **Ignore** lockfiles, vendored code, fixtures, internal helpers, and tests — except note when a test was *deleted* (see Step 5).
4. If the repo has compat-tracking docs (e.g. `AGENTS.md`, `CHANGELOG.md`, `MIGRATION.md`, `BREAKING.md`, `.fernignore`, codeowner files for "frozen" generated files), read them. They tell you what the maintainers consider stable, what shims already exist, and what's deliberately frozen.

## Step 2 — Extract every interface change

For each public-surface file, enumerate every change at the **method, class, type-alias, enum, exported-constant, or schema-field** level. For each one, record:

- **Identifier** (fully qualified — `module.Class.method`, `package::Type`, etc.).
- **Kind**: class, function, method, type alias, enum, TypedDict / interface / Pydantic model field, exported symbol, route handler, message schema.
- **Before** signature/shape (from the `-` side of the diff or the base ref).
- **After** signature/shape (from the `+` side).
- **Direction of change**: addition, removal, rename, type widening, type narrowing, field add (required vs optional), field remove, default change, reshape (nesting), constructor → alias collapse.

If a change is a rename, **trace where the old name went** — is it gone, aliased, re-exported under both names, or replaced by a wrapper?

## Step 3 — Classify each change

Assign each interface change to one of these tiers. Be strict; when in doubt, escalate.

| Tier | Name | Definition |
|---|---|---|
| 🚨 **1** | **Breaking, no compat** | Old call sites will fail to compile, fail at import, fail at runtime, or silently produce wrong wire payloads. No shim, alias, validator, or wrapper exists. |
| ⚠️ **2** | **Reshape with partial compat** | Schema/shape changed but maintainers added a validator, adapter, default, or alias that catches *most* legacy callers. Some patterns still slip through. |
| ✅ **3** | **Pure rename with full alias** | Identifier renamed, but the old name is preserved as an alias/re-export with identity preserved (`old is new` holds, or runtime type identity is preserved). |
| 🔍 **4** | **Type tightening / silent risk** | A type was narrowed (e.g. `str` → enum), a default removed, a docstring contract changed, or behavior subtly shifted. Compiles fine; may surprise users. |
| ➕ **5** | **Purely additive** | New optional field, new optional parameter with default, new method, new exported type. No existing caller can break. |
| 🆕 **6** | **Brand-new public type** | Entirely new type/class/symbol with no predecessor. Only breaks callers who happened to define a same-named local symbol. |

## Step 4 — For each change, document compat & gaps

Use this template per interface:

```
### N. <FullyQualifiedName>
**File:** `path/to/file.ext`
**Tier:** <emoji + number>

| Aspect | Before | After |
|---|---|---|
| <signature/fields/etc.> | ... | ... |

**Compat attempted:** <None | description of validator / alias / wrapper / default / re-export>. Reference any test that proves it works.

**Gaps:**
- <Specific caller pattern that still breaks, with a concrete example>
- <Static-typing vs runtime mismatches>
- <Read-side vs write-side asymmetries>
- <isinstance / identity / subclassing concerns>

**Recommendation:** <Concrete fix — wrapper class, extended validator, restored field, deprecation property, changelog note>
```

### Specific patterns to look for

When evaluating compat, actively check for these failure modes:

1. **Class → type alias collapse.** A class that becomes `T = Union[...]` or `T = OtherClass` breaks `T(...)` constructor calls and `isinstance(x, T)` checks even when fields appear preserved elsewhere. **Always flag this.**
2. **Field migration across nesting boundaries.** If fields moved from `Outer` into `Outer.inner`, check whether validators on **both** levels intercept legacy flat payloads, or only one.
3. **Read-side vs write-side compat.** A `model_validator(mode="before")` rescues *construction* but not attribute access. After construction, `obj.old_field` raises `AttributeError`. Check whether a `@property` or `__getattr__` shim was added.
4. **TypedDict / interface keys can't run validators.** Renamed/moved keys in TypedDicts, TS interfaces, or Go structs have no runtime safety net — only static-typing breakage. Flag whether the runtime parent (Pydantic model, JSON deserializer) catches the legacy shape.
5. **Type narrowing with `Any` escape hatches.** `Union[Literal[...], Any]` looks like a tightening but accepts anything at runtime. Flag the IDE/UX impact even when runtime is safe.
6. **Default-value changes.** A field going from `default=X` to `default=None` (or vice versa) is a wire-format break even if the type is unchanged.
7. **Required ↔ optional flips.** Making a previously-optional field required is breaking; the reverse is usually safe but check serialization (does it now emit `null` where it used to omit?).
8. **Enum widening vs narrowing.** Adding members is safe for producers, breaking for exhaustive consumers (Rust `match`, TS `switch` with `never` checks). Removing members is always breaking.
9. **Re-export surface changes.** A symbol dropped from `__init__.py` / `index.ts` is breaking even if the underlying file is unchanged. Check `__all__`, `__dir__`, and barrel re-exports.
10. **Generic / type-parameter changes.** Adding a type param, changing variance, or changing bounds breaks downstream type annotations.
11. **Exception types.** A function that used to raise `FooError` now raising `BarError` breaks `except` clauses. Check raise sites.
12. **Async ↔ sync flips.** Returning a coroutine where a value was returned (or vice versa) is breaking even with the same name.
13. **Wire-format vs library-API split.** A change can be library-breaking but wire-compatible (or vice versa). Call out which axis breaks.

## Step 5 — Audit the test changes

- List every test **added** that exercises a compat shim or migration. These prove which patterns are covered.
- List every test **deleted** or **modified to remove a case**. A deleted compat test is a red flag — the shim it proved may still exist but is now unverified, or the shim is gone and the deletion was the silent break.
- Note any compat shim that has **no test**. Recommend adding one.

## Step 6 — Produce the final review

Structure your output exactly like this:

1. **One-line headline assessment**: `Mostly backwards-compatible with N breaking edges` or `M breaking changes, no compat measures` etc.
2. **What's well-handled** — bullet list of compat wins, with file links.
3. **Per-interface review** — one block per changed interface, ordered by tier (🚨 first, then ⚠️, then 🔍, with ✅/➕/🆕 collapsed into a summary table at the end).
4. **Test-coverage observations** — added/removed/missing tests for compat behavior.
5. **Summary table** — every interface, its tier, compat status (✅/⚠️/❌), and the gap to fix.
6. **Recommendations before merging** — prioritized, concrete, actionable items. Each should map to a specific interface.

## Output rules

- Use file blocks with `name=` and `url=` (with `#L` line anchors when quoting) for every code reference.
- Don't summarize — enumerate. If there are 30 interface changes, produce 30 entries.
- If the PR is large, paginate the file fetch and don't stop until you've seen every file. Acknowledge if you had to truncate.
- Don't editorialize on style, naming choices, or architecture unless they directly cause a contract break.
- Distinguish **runtime breakage** from **static-typing breakage** explicitly — they have different audiences and different fixes.
- When recommending a fix, prefer the least invasive option that preserves both runtime and type compat (alias > wrapper class > validator > deprecation property > changelog-only).

## When to skip this review

This prompt is overkill for:
- Docs-only PRs.
- Test-only PRs (unless tests are deleted — then still run Step 5).
- Internal refactors that touch zero public-surface files (verify this — don't take the PR description's word).
- Dependency bumps (unless they change a re-exported type from the dependency).

If the PR qualifies for skipping, say so in one sentence and stop.