# JPRalph - Ralph Methodology for Antigravity

This directory contains the JPRalph skill system, which brings the Ralph autonomous coding methodology to Antigravity.

## For AI Agents

When working with JPRalph:

1. **Load skills via view_file**, not by reading this directory
2. **Skills are self-contained** - each SKILL.md has complete instructions
3. **Follow the workflow** - PRD → Convert → Execute
4. **Respect completion signals** - `<promise>DONE</promise>`, `<promise>BATCH_COMPLETE</promise>`, `<promise>COMPLETE</promise>`

## Available Skills

- **jpralph-prd**: Generate Product Requirements Documents
- **jpralph-convert**: Convert PRDs to prd.json format
- **jpralph-iterate**: Execute one user story (manual mode)
- **jpralph-auto**: Execute batch of user stories (autonomous mode)
- **jpralph-orchestrator**: Guide users through workflow

## Execution Modes

### Manual Mode (jpralph-iterate)
- One story per chat
- Maximum context cleanliness
- Full control

### Batched Autonomous (jpralph-auto)
- 5 stories per chat (configurable)
- Balance of speed and context management
- **Recommended for most projects**

### Workflow-Guided (jpralph-orchestrator)
- Step-by-step guidance
- Best for first-time users

## Key Files

- **prd.json**: User stories with execution status (in project root)
- **progress.txt**: Iteration log and learnings (in project root)
- **tasks/prd-*.md**: Generated PRDs

## Important Patterns

1. **Story Sizing**: Each story must fit in one iteration
2. **Fresh Context**: New chat per iteration (manual) or per batch (auto)
3. **State on Disk**: prd.json and progress.txt persist between chats
4. **Quality Checks**: Always run typecheck/lint/test before committing

## For Developers

See [README.md](README.md) for complete documentation.

## Project Structure

```
jpralph/
├── skills/              # Skill definitions
│   ├── jpralph-prd/
│   ├── jpralph-convert/
│   ├── jpralph-iterate/
│   ├── jpralph-auto/
│   └── jpralph-orchestrator/
├── examples/            # Example files
├── templates/           # Templates for new projects
├── README.md            # Main documentation
└── AGENTS.md            # This file
```
