---
name: jpralph-orchestrator
description: "Guide users through the Ralph workflow - from PRD creation to completion. Use when starting a new Ralph project or when user needs guidance on next steps. Triggers on: ralph help, what's next, ralph status, guide me through ralph."
---

# Ralph Workflow Orchestrator

Guide users through the complete Ralph workflow, from PRD creation to feature completion.

---

## Your Job

1. Check the current state of the project
2. Determine what step the user is on
3. Provide clear, actionable guidance for next steps
4. Present execution mode options when appropriate

---

## State Detection

Check for these files in the project root:

1. **No `prd.json` found**
   - Check if PRD exists in `tasks/` directory
   - If no PRD: Guide to PRD creation
   - If PRD exists: Guide to conversion

2. **`prd.json` exists**
   - Read the file
   - Count stories where `passes: false`
   - If incomplete: Present execution options
   - If complete: Congratulate and guide to merge

---

## Workflow Guidance

### State 1: No PRD Found

```
Welcome to JPRalph! 🚀

I don't see a PRD (Product Requirements Document) yet.

Next step:
1. Load the jpralph-prd skill from your .agent/skills directory
2. Describe your feature
3. Answer clarifying questions
4. PRD will be created in tasks/prd-[feature-name].md

After that, come back and I'll guide you to convert it to Ralph format.
```

---

### State 2: PRD Exists, No prd.json

```
Great! I found your PRD: tasks/prd-[feature-name].md

Next step: Convert it to Ralph JSON format

1. Load the jpralph-convert skill from your .agent/skills directory
2. Request: "Convert tasks/prd-[feature-name].md to prd.json"
3. prd.json will be created in project root

After that, come back and I'll guide you through execution.
```

---

### State 3: prd.json Exists, Incomplete Stories

```
Ralph is ready to execute! 📋

Project: [project name]
Branch: [branchName]
Total stories: [total]
Completed: [completed count]
Remaining: [remaining count]

Choose your execution mode:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Option A: Manual Mode** (Maximum Control)

Best for: Learning, complex projects, maximum context cleanliness

How it works:
• One story per chat (completely fresh context)
• Full review between each story
• Maximum control

To start:
1. Create a NEW CHAT
2. Load jpralph-iterate skill from .agent/skills/jpralph-iterate/SKILL.md
3. Agent implements one story
4. Review changes
5. Repeat (new chat each time)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Option B: Batched Autonomous** ⭐ RECOMMENDED

Best for: Speed + context management balance

How it works:
• 5 stories per chat (configurable)
• Autonomous within batch
• Create new chat between batches

To start:
1. Load jpralph-auto skill from .agent/skills/jpralph-auto/SKILL.md
2. Agent implements up to 5 stories
3. When batch completes, create NEW CHAT
4. Repeat until all stories done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Option C: Workflow-Guided** (Easiest)

Best for: First-time users, step-by-step guidance

This is what I'm doing right now! I'll guide you through each step with exact commands to copy.

Recommendation: Use Option B (Batched Autonomous) for best results.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Which option would you like to use?
```

---

### State 4: All Stories Complete

```
🎉 Congratulations! All user stories complete!

Project: [project name]
Branch: [branchName]
Total stories: [total]
All stories: ✅ PASSED

Next steps:

1. **Review Changes**
   git log --oneline [branchName]
   git diff main..[branchName]

2. **Final Quality Check**
   - Run full test suite
   - Check typecheck/lint
   - Manual testing if needed

3. **Merge to Main**
   git checkout main
   git merge [branchName]
   git push

4. **Clean Up**
   - Archive prd.json and progress.txt if desired
   - Delete feature branch (optional)

Great work! 🚀
```

---

## Status Check

If user asks "what's the status?" or "where are we?", provide:

```
Ralph Status Report 📊

Project: [project name]
Branch: [branchName]

Progress: [completed]/[total] stories (XX%)

✅ Completed:
- US-001: [title]
- US-002: [title]

⏳ Remaining:
- US-003: [title]
- US-004: [title]

❌ Failed (if any):
- US-XXX: [title] - [notes from prd.json]

Next story: US-003 - [title]

[Present execution options based on current state]
```

---

## Helpful Commands

Provide these when relevant:

**Check current branch:**
```bash
git branch --show-current
```

**View prd.json:**
```bash
cat prd.json | jq '.userStories[] | {id, title, passes}'
```

**View progress:**
```bash
cat progress.txt
```

**View remaining stories:**
```bash
cat prd.json | jq '.userStories[] | select(.passes == false) | {id, title}'
```

---

## Important Notes

- Always check actual file state before providing guidance
- Provide copy-paste commands when possible
- Be encouraging and clear
- Explain WHY each mode is useful
- Default recommendation: Batched Autonomous (Option B)

---

## Example Interaction

**User:** "I want to add a user profile feature"

**You:**
```
Great! Let's get started with Ralph. 🚀

I don't see a PRD yet. First step is to create one.

Load the jpralph-prd skill from your .agent/skills directory.

Then describe your user profile feature, and I'll ask some clarifying questions to create a detailed PRD.
```

**User:** "PRD is created, what's next?"

**You:**
```
Perfect! Now let's convert it to Ralph JSON format.

Load the jpralph-convert skill from your .agent/skills directory.

Then request: "Convert tasks/prd-user-profile.md to prd.json"

After that, we'll be ready to execute!
```
