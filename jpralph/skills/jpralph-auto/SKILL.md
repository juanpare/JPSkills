---
name: jpralph-auto
description: "Execute Ralph iterations in batches autonomously - implement up to 5 user stories automatically. Use for faster execution while maintaining context management. Triggers on: ralph auto, batch execute, autonomous ralph, run batch."
---

# Ralph Batched Autonomous Executor

Execute Ralph iterations in **batches** - implement up to 5 user stories automatically in a single chat, then stop.

This is the **batched autonomous mode** skill. Use this when you want:
- Faster execution (5 stories per chat)
- Autonomous operation within batch
- Balance between speed and context management

For maximum context cleanliness, use `jpralph-iterate` instead (one story per chat).

---

## Your Task

1. Read the PRD at `prd.json` (in project root)
2. Read the progress log at `progress.txt` (check Codebase Patterns section first)
3. Check you're on the correct branch from PRD `branchName`. If not, check it out or create from main.
4. **Loop through incomplete stories (up to batch limit)**:
   - Pick highest priority story where `passes: false`
   - Implement that story completely
   - Run quality checks (typecheck, lint, test)
   - Update AGENTS.md if you discover reusable patterns
   - If checks pass, commit with message: `feat: [Story ID] - [Story Title]`
   - Update PRD to set `passes: true` for completed story
   - Append progress to `progress.txt`
   - Continue to next story (up to batch limit)
5. Output completion signal based on status

---

## Batch Configuration

- **Default batch size:** 5 stories
- **Maximum batch size:** 10 stories
- **User can specify:** "Execute batch of 3 stories" or "Run 7 stories"
- **Purpose:** Prevents context overflow by limiting iterations per chat

---

## Progress Report Format

For EACH story in the batch, APPEND to progress.txt:

```
## [Date/Time] - [Story ID]
Chat: [Current chat ID] - Batch iteration [N of batch_size]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered
  - Gotchas encountered
  - Useful context
---
```

---

## Consolidate Patterns

Same as jpralph-iterate - add reusable patterns to `## Codebase Patterns` section at top of progress.txt.

---

## Update AGENTS.md Files

Same as jpralph-iterate - update AGENTS.md files with genuinely reusable knowledge discovered during implementation.

---

## Quality Requirements

- ALL commits must pass quality checks (typecheck, lint, test)
- Do NOT commit broken code
- Keep changes focused and minimal per story
- Follow existing code patterns

---

## Browser Testing

For any story that changes UI, verify in browser using Antigravity's browser tools.

---

## Stop Conditions

### Batch Complete (more stories remain)
If you've completed the batch limit BUT there are still stories with `passes: false`:

```
<promise>BATCH_COMPLETE</promise>

Batch complete! ✅

Completed in this batch:
- US-001: [title]
- US-002: [title]
- US-003: [title]
- US-004: [title]
- US-005: [title]

Remaining stories: [count]
Next story: US-006 - [title]

To continue:
1. Create a NEW CHAT (for fresh context)
2. Load the jpralph-auto skill
3. Execute next batch of 5 stories
```

### All Complete
If ALL stories have `passes: true`:

```
<promise>COMPLETE</promise>

All user stories complete! 🎉

Total stories completed: [count]
Branch: [branchName]

Next steps:
1. Review all changes
2. Run final quality checks
3. Merge branch to main
```

---

## Error Handling

If a story fails quality checks after 3 attempts:
1. Mark story with notes in prd.json explaining the issue
2. Skip to next story in batch
3. Report all failures at end of batch

Example notes:
```json
{
  "id": "US-003",
  "passes": false,
  "notes": "Failed after 3 attempts. Typecheck error: Property 'foo' does not exist on type 'Bar'. Needs manual review."
}
```

---

## Loop Control

- **Maximum attempts per story:** 3
- **Stop if:** Critical error (e.g., git conflicts, missing dependencies)
- **Continue if:** Individual story fails (mark and skip)
- **Report:** All failures and successes at end

---

## Progress Tracking During Batch

Provide status updates as you work:

```
Starting batch execution...
Batch size: 5 stories

[1/5] Implementing US-001: Add priority field to database
✅ US-001 complete

[2/5] Implementing US-002: Display priority indicator
✅ US-002 complete

[3/5] Implementing US-003: Add priority selector
✅ US-003 complete

[4/5] Implementing US-004: Filter tasks by priority
✅ US-004 complete

[5/5] Implementing US-005: Sort by priority
✅ US-005 complete

Batch complete! All 5 stories passed.
```

---

## Important

- Work through stories in priority order
- Commit after each story (not at end of batch)
- Keep CI green throughout
- Read Codebase Patterns section before starting
- Provide clear continuation guidance when batch completes

---

## Batch Size Recommendation

- **Small PRDs (3-5 stories):** Use full batch size
- **Medium PRDs (6-15 stories):** Use batch size of 5 (default)
- **Large PRDs (16+ stories):** Use batch size of 3-5, split into multiple batches

This keeps context manageable and allows for fresh chats between batches.
