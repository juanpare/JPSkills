---
name: jpralph-iterate
description: "Execute a single Ralph iteration - implement one user story autonomously. Use for manual mode where you want maximum control and fresh context per story. Triggers on: ralph iterate, execute one story, run single iteration, manual ralph."
---

# Ralph Single Iteration Executor

Execute ONE Ralph iteration - implement a single user story completely, then stop.

This is the **manual mode** skill. Use this when you want:
- Maximum context cleanliness (new chat per story)
- Full control and review between stories
- To work through complex projects carefully

For faster execution with batches, use `jpralph-auto` instead.

---

## Your Task

1. Read the PRD at `prd.json` (in project root)
2. Read the progress log at `progress.txt` (check Codebase Patterns section first)
3. Check you're on the correct branch from PRD `branchName`. If not, check it out or create from main.
4. Pick the **highest priority** user story where `passes: false`
5. Implement that single user story completely
6. Run quality checks (e.g., typecheck, lint, test - use whatever your project requires)
7. Update AGENTS.md files if you discover reusable patterns (see below)
8. If checks pass, commit ALL changes with message: `feat: [Story ID] - [Story Title]`
9. Update the PRD to set `passes: true` for the completed story
10. Append your progress to `progress.txt`

---

## Progress Report Format

APPEND to progress.txt (never replace, always append):
```
## [Date/Time] - [Story ID]
Chat: [Current chat ID or description]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered (e.g., "this codebase uses X for Y")
  - Gotchas encountered (e.g., "don't forget to update Z when changing W")
  - Useful context (e.g., "the evaluation panel is in component X")
---
```

The learnings section is critical - it helps future iterations avoid repeating mistakes and understand the codebase better.

---

## Consolidate Patterns

If you discover a **reusable pattern** that future iterations should know, add it to the `## Codebase Patterns` section at the TOP of progress.txt (create it if it doesn't exist). This section should consolidate the most important learnings:

```
## Codebase Patterns
- Example: Use `sql<number>` template for aggregations
- Example: Always use `IF NOT EXISTS` for migrations
- Example: Export types from actions.ts for UI components
```

Only add patterns that are **general and reusable**, not story-specific details.

---

## Update AGENTS.md Files

Before committing, check if any edited files have learnings worth preserving in nearby AGENTS.md files:

1. **Identify directories with edited files** - Look at which directories you modified
2. **Check for existing AGENTS.md** - Look for AGENTS.md in those directories or parent directories
3. **Add valuable learnings** - If you discovered something future developers/agents should know:
   - API patterns or conventions specific to that module
   - Gotchas or non-obvious requirements
   - Dependencies between files
   - Testing approaches for that area
   - Configuration or environment requirements

**Examples of good AGENTS.md additions:**
- "When modifying X, also update Y to keep them in sync"
- "This module uses pattern Z for all API calls"
- "Tests require the dev server running on PORT 3000"
- "Field names must match the template exactly"

**Do NOT add:**
- Story-specific implementation details
- Temporary debugging notes
- Information already in progress.txt

Only update AGENTS.md if you have **genuinely reusable knowledge** that would help future work in that directory.

---

## Quality Requirements

- ALL commits must pass your project's quality checks (typecheck, lint, test)
- Do NOT commit broken code
- Keep changes focused and minimal
- Follow existing code patterns

---

## Browser Testing (Required for Frontend Stories)

For any story that changes UI, you MUST verify it works in the browser:

1. Use Antigravity's browser tools to navigate to the relevant page
2. Verify the UI changes work as expected
3. Take a screenshot if helpful for the progress log

A frontend story is NOT complete until browser verification passes.

---

## Stop Condition

After completing a user story, check if ALL stories have `passes: true`.

If ALL stories are complete and passing, reply with:
<promise>COMPLETE</promise>

If there are still stories with `passes: false`, end your response with:
<promise>DONE</promise>

This signals that this iteration is complete, but more work remains. The user should create a NEW CHAT for the next iteration.

---

## Important

- Work on ONE story per iteration
- Commit when quality checks pass
- Keep CI green
- Read the Codebase Patterns section in progress.txt before starting
- **End with `<promise>DONE</promise>` when this story is complete**
- **End with `<promise>COMPLETE</promise>` only if ALL stories are done**

---

## Next Steps Guidance

When you output `<promise>DONE</promise>`, also provide clear guidance:

```
Story US-XXX complete! ✅

Remaining stories: [count]
Next story: US-YYY - [title]

To continue:
1. Create a NEW CHAT (for fresh context)
2. Load the jpralph-iterate skill
3. The agent will pick up the next story automatically
```

This helps the user know exactly what to do next.
