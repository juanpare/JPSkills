# JPSkills

> Antigravity-compatible skills for autonomous development and server automation.

A curated collection of self-contained skill packages for [Antigravity](https://antigravity.sh). Each skill includes its own `SKILL.md`, supporting resources, and workflow-specific scripts—just copy what you need into your project.

## Collections

| Collection | Focus | Skills |
|------------|-------|--------|
| [`jpralph`](jpralph/README.md) | PRD-driven autonomous coding | 5 skills |
| [`openclaw`](openclaw/README.md) | Server-side CLI automation | 1 skill |

### jpralph — Ralph Methodology for Antigravity

PRD-driven autonomous development with fresh-context execution.

| Skill | Purpose |
|-------|---------|
| `jpralph-prd` | Generate a structured feature PRD |
| `jpralph-convert` | Convert PRD → `prd.json` for execution |
| `jpralph-iterate` | Execute one story (manual mode) |
| `jpralph-auto` | Execute up to 5 stories (batch mode) |
| `jpralph-orchestrator` | Guide the overall Ralph workflow |

→ Full docs: [`jpralph/README.md`](jpralph/README.md) · Install guide: [`jpralph/INSTALLATION.md`](jpralph/INSTALLATION.md)

### openclaw — Server Automation Skills

Deterministic CLI workflows for VPS/server environments.

| Skill | Purpose |
|-------|---------|
| `openclaw-url-to-kindle` | URL → markdown → EPUB → Kindle delivery pipeline |

→ Full docs: [`openclaw/README.md`](openclaw/README.md)

## Quick Install

Copy the skills you need into your project's `.agent/skills/` directory:

```bash
# From this repo's root
mkdir -p /path/to/your-project/.agent/skills

# Install a jpralph skill
cp -r jpralph/skills/jpralph-auto /path/to/your-project/.agent/skills/

# Install an openclaw skill
cp -r openclaw/skills/openclaw-url-to-kindle /path/to/your-project/.agent/skills/
```

Load the installed skill in Antigravity:

```
view_file .agent/skills/jpralph-auto/SKILL.md
```

## Repository Structure

```
skills/
├── jpralph/
│   ├── skills/           # 5 Ralph execution skills
│   ├── examples/         # Sample PRD, prd.json, progress.txt
│   ├── templates/        # Project scaffolding templates
│   ├── INSTALLATION.md   # Detailed install instructions
│   ├── README.md         # Full jpralph documentation
│   └── AGENTS.md         # AI agent conventions
├── openclaw/
│   ├── skills/           # Server automation skills
│   ├── README.md         # OpenClaw documentation
│   └── AGENTS.md         # AI agent conventions
└── README.md             # This file
```

## Conventions

- **Self-contained skills** — Each skill has its own `SKILL.md` with complete instructions.
- **Colocated assets** — Supporting files (`resources/`, `scripts/`, `templates/`) live next to the skill.
- **Collection-level docs** — Each collection has a `README.md` explaining workflow and assumptions.
- **AGENTS.md** — Machine-readable conventions for AI agents working in that collection.

## Requirements by Collection

| Collection | Dependencies |
|------------|--------------|
| `jpralph` | None (pure skill definitions) |
| `openclaw` | Python + `gog` CLI (skill-specific) |

See individual skill documentation for detailed prerequisites.

## License

MIT
