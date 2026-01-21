# JPRalph

> Ralph methodology for Antigravity - Autonomous AI coding with PRD-driven development

JPRalph brings the powerful Ralph autonomous coding methodology to Antigravity, adapted to work within Antigravity's chat-based workflow.

## What is Ralph?

Ralph is an autonomous coding methodology where:
- Features are broken down into small, focused user stories
- Each story is implemented in a fresh context (clean slate)
- State persists via files on disk (`prd.json`, `progress.txt`)
- Completion signals (`<promise>DONE</promise>`) indicate task completion
- Quality checks (typecheck, lint, test) act as guardrails

## What is JPRalph?

JPRalph adapts Ralph for Antigravity with three execution modes:

### Mode 1: Manual Iteration
- **One story per chat** (maximum context cleanliness)
- User creates new chat for each iteration
- Full review between stories
- Best for: Learning, complex projects

### Mode 2: Batched Autonomous ⭐ RECOMMENDED
- **5 stories per chat** (configurable batch size)
- Autonomous within batch
- User creates new chat between batches
- Best for: Speed + context management balance

### Mode 3: Workflow-Guided
- Step-by-step guidance through the process
- Copy-paste commands for each step
- Uses batched mode underneath
- Best for: First-time users

## Quick Start

### 1. Create a PRD

```
Load jpralph-prd skill and create a PRD for [your feature]
```

The skill will ask clarifying questions and generate a structured PRD in `tasks/prd-[feature-name].md`.

### 2. Convert to JSON

```
Load jpralph-convert skill and convert tasks/prd-[feature-name].md to prd.json
```

This creates `prd.json` in your project root with user stories structured for autonomous execution.

### 3. Execute (Choose Your Mode)

**Option A: Manual Mode**
```
Create NEW CHAT
Load jpralph-iterate skill
Agent implements one story → <promise>DONE</promise>
Create NEW CHAT for next story
```

**Option B: Batched Autonomous** (Recommended)
```
Load jpralph-auto skill
Agent implements up to 5 stories → <promise>BATCH_COMPLETE</promise>
Create NEW CHAT for next batch
```

**Option C: Workflow-Guided**
```
Load jpralph-orchestrator skill
Follow step-by-step guidance
```

## Installation

JPRalph skills are designed to be self-contained and easy to install in any Antigravity project.

**Quick Install:**

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions with copy-paste prompts.

**TL;DR:**
```
Copy the jpralph/skills/ directory to your project's .agent/skills/ directory.
Each skill includes its own resources (templates, examples) and works independently.
```

**Verify installation:**
```bash
ls -la .agent/skills/jpralph-*/
```

## Available Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `jpralph-prd` | Generate PRDs | Starting a new feature |
| `jpralph-convert` | Convert PRD to JSON | After PRD is created |
| `jpralph-iterate` | Execute one story | Manual mode, max control |
| `jpralph-auto` | Execute batch of stories | Autonomous mode, faster |
| `jpralph-orchestrator` | Workflow guidance | Need help with next steps |

## File Structure

```
your-project/
├── .agent/
│   └── skills/              # Installed JPRalph skills
│       ├── jpralph-prd/
│       │   ├── SKILL.md
│       │   └── resources/
│       ├── jpralph-convert/
│       │   ├── SKILL.md
│       │   └── resources/
│       ├── jpralph-iterate/
│       │   ├── SKILL.md
│       │   └── resources/
│       ├── jpralph-auto/
│       │   ├── SKILL.md
│       │   └── resources/
│       └── jpralph-orchestrator/
│           ├── SKILL.md
│           └── resources/
├── tasks/
│   └── prd-[feature-name].md    # Generated PRD
├── prd.json                      # Ralph execution format
├── progress.txt                  # Iteration log and learnings
└── archive/                      # Previous runs (auto-created)
    └── YYYY-MM-DD-feature-name/
        ├── prd.json
        └── progress.txt
```

## Key Concepts

### Story Sizing

Each story must be completable in ONE iteration (one context window):

✅ **Right-sized:**
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic

❌ **Too big (split these):**
- "Build the entire dashboard"
- "Add authentication"
- "Refactor the API"

### Completion Signals

- `<promise>DONE</promise>` - One story complete, more remain
- `<promise>BATCH_COMPLETE</promise>` - Batch complete, more stories remain
- `<promise>COMPLETE</promise>` - All stories complete!

### State Management

State persists between iterations via files:
- **prd.json** - User stories with `passes` status
- **progress.txt** - Learnings and patterns for future iterations
- **AGENTS.md** - Reusable patterns discovered during implementation

## Workflow Example

```
Chat 1: Create PRD
  → Load jpralph-prd
  → Answer questions
  → PRD saved to tasks/prd-user-profile.md

Chat 2: Convert to JSON
  → Load jpralph-convert
  → prd.json created with 12 user stories

Chat 3: Batch 1 (Stories 1-5)
  → Load jpralph-auto
  → Agent implements 5 stories
  → <promise>BATCH_COMPLETE</promise>

Chat 4: Batch 2 (Stories 6-10)
  → Load jpralph-auto
  → Agent implements 5 stories
  → <promise>BATCH_COMPLETE</promise>

Chat 5: Batch 3 (Stories 11-12)
  → Load jpralph-auto
  → Agent implements 2 stories
  → <promise>COMPLETE</promise>

Review and merge!
```

## Why Fresh Chats?

**Context Accumulation Problem:**
- Long sessions accumulate context
- Performance degrades over time
- Agent may "forget" earlier decisions

**Fresh Chat Solution:**
- Each chat starts with clean context
- Agent reads state from files (prd.json, progress.txt)
- Consistent performance across all iterations

**Batched Compromise:**
- 5 stories per chat balances speed and context
- Still requires new chat between batches
- Prevents context overflow

## Antigravity Limitation

Antigravity does NOT provide an API to programmatically create new chats. This is why:
- Manual mode requires user to create new chats
- Batched mode limits stories per chat (5 default)
- Workflow mode provides clear guidance for chat creation

This is a fundamental platform limitation, not a JPRalph limitation.

## Best Practices

1. **Start with small PRDs** (3-5 stories) to learn the workflow
2. **Use batched mode** for most projects (good speed/context balance)
3. **Review between batches** to catch issues early
4. **Keep stories small** (2-3 sentence description max)
5. **Read progress.txt** before each iteration to learn from previous work

## Troubleshooting

**Q: Agent seems confused or makes mistakes**
- Create a new chat (fresh context)
- Check progress.txt for patterns and gotchas
- Ensure story is small enough (one iteration)

**Q: Quality checks failing**
- Review the specific error
- May need to split story smaller
- Check AGENTS.md for project-specific patterns

**Q: How do I know which mode to use?**
- Learning/complex: Manual mode
- Most projects: Batched mode (default 5)
- First time: Workflow-guided mode

## Examples

See the `examples/` directory for:
- Example PRD (`prd-example.md`)
- Example JSON format (`prd.json.example`)
- Example progress log (`progress.txt.example`)

## Credits

JPRalph is based on:
- [Geoffrey Huntley's Ralph methodology](https://github.com/ghuntley/how-to-ralph-wiggum)
- [Ralph by Ryan Carson](https://github.com/snarktank/ralph)
- [Ralph Wiggum by fstandhartinger](https://github.com/fstandhartinger/ralph-wiggum)

Adapted for Antigravity by Juan Pare.

## License

MIT
