# Commenting Guidelines

These guidelines govern the **content and semantics** of code comments and docstrings across Python, JavaScript, CSS, and Django templates. Syntactic rules (which comment delimiter to use, formatting, etc.) live in [Coding Standards](coding-standards.md).

The audience for these guidelines is the cleanup pass that runs before a PR opens, but the same rules apply any time a comment is being judged on its merits.

## The Reader Frame

Every comment is judged from the perspective of a **future developer reading the code cold**, with no knowledge of:
- The conversation, ticket, or PR that produced the change.
- What the code used to do.
- The bug that motivated the current shape.
- Which session, phase, or work stream the change belonged to.

If a comment only makes sense with that missing context, it does not belong in the code. That context belongs in the commit message or PR description.

## The Default Is No Comment

Start from zero. A comment must earn its place. Before writing one, try in order:

1. **Rename.** If a better variable, method, or class name would convey the same information, rename instead of commenting.
2. **Restructure.** If extracting a helper, splitting a function, or reorganizing the code would make the intent obvious, do that instead.
3. **Delete.** If the comment restates what the code already says, do not write it.

Only when none of the above work does a comment become the right tool.

## When a Comment Earns Its Place

A comment is justified when a future cold reader would be misled, confused, or surprised by the code without it. The legitimate categories are narrow:

- **Non-obvious *why* behind a design decision.** Why this approach was chosen over an alternative that would seem equally reasonable on inspection.
- **Hidden constraints or invariants.** Assumptions the code depends on that are not visible at the call site.
- **External system quirks and workarounds.** Library bugs, API rate limits, protocol oddities, third-party behavior the reader cannot infer from the code.
- **Cross-file coordination.** A value here must match a value there; changing one without the other breaks something.
- **Surprising behavior.** The code does something correct but counterintuitive that a reader would otherwise "fix" and regress.
- **Genuinely complex domain or algorithmic logic.** Business rules or math that cannot be made obvious through naming and structure alone.
- **Bug-fix invariants that prevent regression.** Only when the comment documents the *invariant the code now maintains*, not the story of the bug.

A useful comment in any of these categories is short, points at the non-obvious thing, and would still make sense to a reader who has never heard of the original problem.

## When a Comment Does Not Belong

Remove comments that fall into any of these categories. These are the patterns observed most often.

### Restating what the code already conveys
- Comments that paraphrase a well-named method, variable, or class.
- Docstrings that restate the method name and parameter types in prose.
- Inline comments that describe *what* the next line does when the line itself says it.
- Comments on conditionals, loops, or assignments that add no information beyond the expression.

### Information a reader can trivially discover
- Argument types and return types already in the signature.
- Class purpose already obvious from the class name and module location.
- Default values, exception types, or call sites that are one search away.

### Archeology and historical narrative
- "This used to do X, now does Y."
- "Previously we Z, but we changed it because…"
- "This fixes the bug where…" (the fix is the code; the bug story is the commit).
- "Mirrors how X does it" / "Same pattern as Y."
- "Without this, Z happens" / "We use A rather than B because of bug C."

These narrate the path to the current code. The reader only needs the current code.

### Session, PR, or work-stream context
- "Phase 3 / Phase 4" references.
- "Added in this PR / removed in this PR."
- Comments explaining why other code was deleted, moved, or refactored.
- Anything that reads like a debugging conversation, status update, or progress note.

These have a half-life measured in days. They become noise immediately after merge.

### Re-explaining the same architectural fact in every touched location
When a change spans many files, there is a temptation to drop a paragraph about the new architecture into every file that participates. Resist this. The architectural explanation belongs in **one** place — usually the module, class, or docstring that owns the concept. Other call sites should be self-explanatory through naming, not re-explanation.

### Comments that describe the caller, not the callee
A method's comment should describe what the method does and the contract it offers, not how a specific caller happens to use it. Caller-specific context lives at the call site (or, better, in the call-site code itself).

### Implementation details that belong somewhere else
- Details about a collaborator's internals showing up at a usage point.
- Details about a caller's flow showing up inside the callee.
- Cross-cutting design rationale buried in a leaf function instead of stated once at the owning abstraction.

### Maintenance liabilities
- File paths, line numbers, class names, or method names quoted in comments. These rot the moment the referenced thing moves or renames.
- Counts, lists, or enumerations that must be kept in sync with code elsewhere.
- "See also" pointers to specific lines.

If a cross-reference is genuinely load-bearing, prefer a stable signal: a shared constant, an explicit import, or a name match enforced by the code itself.

### Commented-out code
Delete it. Version control retains the history. Commented blocks create ambiguity about whether the code should be active and tend to drift out of compilability.

### Speculative TODOs
Vague intentions ("TODO: clean this up later", "TODO: maybe refactor") have a very high bar. If the work is worth doing, it is worth an issue. A TODO is acceptable only when it is specific, actionable, and there is a real reason it cannot be done now.

## Archeology Smells — Phrasings That Signal a Delete

Treat the following phrasings as strong signals that the comment is narrating history rather than helping a future reader. When found, default to deletion unless the substance is clearly load-bearing:

- "Used to…" / "Previously…" / "We changed this because…"
- "Now does…" / "Now we…" / "We no longer…"
- "This fixes…" / "Fixes the bug where…"
- "Mirrors…" / "Same pattern as…" / "Like in X…"
- "Without this, …" / "Otherwise …" (when describing the bug it would cause, not the invariant it maintains)
- "Phase N" / "Step N of the migration" / "TODO from issue #…"
- "Added for X" / "Per the discussion in…" / "Per request from…"

## Docstrings

The same content rules apply to docstrings as to inline comments. In particular:

- A docstring that restates the method name and parameter types should be removed.
- Public API methods may warrant docstrings even when the name is clear, when they document contract, side effects, or invariants a caller cannot see.
- Private and internal methods rarely need docstrings; their names and bodies should suffice.
- A long docstring that recounts the design history of the class is archeology. The part of it that describes the current contract may be worth keeping; the rest should go.

## The Cleanup Pass — Decision Rules

When reviewing comments on a branch or in a directory, decide per comment:

### Keep
- Falls into one of the earned-place categories above.
- Would be missed by a cold reader if removed.
- Is concise and focused on the non-obvious *why*.

### Rewrite
- The substance is load-bearing but the framing is archeological (narrates the change rather than stating the invariant). Rewrite to state the invariant directly, without reference to what came before.
- The comment is correct but verbose or scattered across multiple lines that could be one.
- The comment mixes a useful note with debugging narrative — keep the note, drop the narrative.

### Remove
- Restates the code, the name, or the type.
- Narrates history, the session, or the work stream.
- Re-explains an architectural fact already stated elsewhere.
- Is a stale maintenance liability (file:line refs, name quotes, counts).
- Is commented-out code or a vague TODO.

### When Unsure — Keep and Flag

Removing a *bad* comment is free. Removing a *load-bearing* comment is expensive and easy to miss in review. When in doubt:

- Keep the comment.
- Flag it for human review with the specific reason for uncertainty.

A cleanup pass that errs toward keeping ambiguous comments is correct. A cleanup pass that silently deletes load-bearing context is a regression.

## What Is Out of Scope for the Cleanup Pass

The cleanup pass is about **content and semantics**. The following are syntactic concerns that belong to general code review and to [Coding Standards](coding-standards.md):

- Which comment delimiter to use (`#` vs docstring, `//` vs JSDoc, `{# #}` vs `<!-- -->`).
- Comment formatting, indentation, and line length.
- Where in a file comments are placed.

The cleanup pass should not rewrite a comment purely for syntactic reasons. If a comment's *content* earns its place, leave its form alone.
