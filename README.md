# JPSkills

> A collection of powerful Antigravity skills for autonomous AI coding

JPSkills is a curated collection of skills designed to enhance your Antigravity development workflow. Each skill is self-contained and can be installed independently in any Antigravity project.

## Available Skills

### 🚀 JPRalph - Autonomous PRD-Driven Development

JPRalph brings the powerful Ralph autonomous coding methodology to Antigravity. Break down features into small user stories and let AI implement them autonomously with quality checks and fresh context per iteration.

**Features:**
- 📝 PRD Generator - Create detailed product requirements documents
- 🔄 PRD to JSON Converter - Convert PRDs to executable format
- ⚡ Autonomous Executors - Implement stories automatically (single or batch mode)
- 🎯 Workflow Orchestrator - Step-by-step guidance through the process

[Learn more about JPRalph →](jpralph/README.md)

## Quick Install - JPRalph

Copy and paste this prompt into an Antigravity chat to install all JPRalph skills:

```
Please help me install the JPRalph skills from GitHub: https://github.com/juanpare/JPSkills

To install, execute these commands:
1. Clone the repo: git clone https://github.com/juanpare/JPSkills.git
2. Create skills dir: mkdir -p .agent/skills
3. Copy skills: cp -r JPSkills/jpralph/skills/* .agent/skills/
4. Clean up: rm -rf JPSkills

After installation, verify by loading:
view_file .agent/skills/jpralph-orchestrator/SKILL.md
```

For detailed installation instructions, see [jpralph/INSTALLATION.md](jpralph/INSTALLATION.md)

## Getting Started with JPRalph

Once installed, start with the orchestrator for guided workflow:

```
view_file .agent/skills/jpralph-orchestrator/SKILL.md
```

Or jump directly to creating a PRD:

```
view_file .agent/skills/jpralph-prd/SKILL.md
```

## Repository Structure

```
JPSkills/
├── jpralph/                    # Ralph methodology for Antigravity
│   ├── skills/                 # 5 self-contained skills
│   │   ├── jpralph-prd/
│   │   ├── jpralph-convert/
│   │   ├── jpralph-iterate/
│   │   ├── jpralph-auto/
│   │   └── jpralph-orchestrator/
│   ├── INSTALLATION.md         # Detailed installation guide
│   ├── README.md               # JPRalph documentation
│   └── AGENTS.md               # Project context for agents
└── README.md                   # This file
```

## Future Skills

More skills coming soon! This repository will grow to include additional Antigravity skills for various development workflows.

## Contributing

Contributions are welcome! If you have a skill you'd like to add to JPSkills:

1. Fork the repository
2. Create your skill following the atomic structure pattern (see jpralph/skills/ for examples)
3. Include a SKILL.md and resources/ directory
4. Submit a pull request

## License

MIT

## Credits

- **JPRalph** is based on the [Ralph methodology](https://github.com/ghuntley/how-to-ralph-wiggum) by Geoffrey Huntley
- Adapted for Antigravity by Juan Pare

---

**Ready to get started?** Install JPRalph using the prompt above and start building with autonomous AI coding! 🚀
