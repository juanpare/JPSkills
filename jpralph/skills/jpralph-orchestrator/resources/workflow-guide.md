# JPRalph Workflow Quick Reference

This guide provides a quick reference for the JPRalph workflow.

## Complete Workflow

```
1. Create PRD
   └─> Load jpralph-prd skill
   └─> Describe feature
   └─> Answer questions
   └─> PRD saved to tasks/prd-[feature].md

2. Convert to JSON
   └─> Load jpralph-convert skill
   └─> Convert PRD to prd.json
   └─> prd.json created in project root

3. Execute Stories
   
   Option A: Manual Mode
   └─> Create NEW CHAT per story
   └─> Load jpralph-iterate skill
   └─> One story implemented
   └─> Repeat
   
   Option B: Batched Mode (Recommended)
   └─> Load jpralph-auto skill
   └─> 5 stories implemented
   └─> Create NEW CHAT for next batch
   └─> Repeat

4. Review & Merge
   └─> All stories complete
   └─> Review changes
   └─> Merge to main
```

## File Structure

```
your-project/
├── tasks/
│   └── prd-[feature].md
├── prd.json
├── progress.txt
└── .agent/
    └── skills/
        ├── jpralph-prd/
        ├── jpralph-convert/
        ├── jpralph-iterate/
        ├── jpralph-auto/
        └── jpralph-orchestrator/
```

## Completion Signals

- `<promise>DONE</promise>` - One story complete, more remain
- `<promise>BATCH_COMPLETE</promise>` - Batch complete, more stories remain
- `<promise>COMPLETE</promise>` - All stories complete!

## Common Commands

**Check status:**
```bash
cat prd.json | jq '.userStories[] | {id, title, passes}'
```

**View progress:**
```bash
cat progress.txt
```

**View remaining:**
```bash
cat prd.json | jq '.userStories[] | select(.passes == false) | {id, title}'
```
