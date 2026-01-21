# JPRalph Installation Guide

This guide provides copy-paste prompts to install JPRalph skills in any Antigravity project.

## Quick Install - All Skills

Copy and paste this entire prompt into an Antigravity chat to install all JPRalph skills:

---

**Installation Prompt:**

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

---

## Individual Skill Installation

If you only need specific skills, use these individual prompts:

### Install jpralph-prd (PRD Generator)

```
Please install the jpralph-prd skill from https://github.com/juanpare/JPSkills/tree/main/jpralph/skills/jpralph-prd

Copy the entire directory including:
- SKILL.md
- resources/prd-template.md
- resources/prd-example.md

Place in: .agent/skills/jpralph-prd/

Verify: view_file .agent/skills/jpralph-prd/SKILL.md
```

### Install jpralph-convert (PRD to JSON Converter)

```
Please install the jpralph-convert skill from https://github.com/juanpare/JPSkills/tree/main/jpralph/skills/jpralph-convert

Copy the entire directory including:
- SKILL.md
- resources/prd-example.md
- resources/prd.json.example

Place in: .agent/skills/jpralph-convert/

Verify: view_file .agent/skills/jpralph-convert/SKILL.md
```

### Install jpralph-iterate (Single Story Executor)

```
Please install the jpralph-iterate skill from https://github.com/juanpare/JPSkills/tree/main/jpralph/skills/jpralph-iterate

Copy the entire directory including:
- SKILL.md
- resources/prd.json.example
- resources/progress.txt.example

Place in: .agent/skills/jpralph-iterate/

Verify: view_file .agent/skills/jpralph-iterate/SKILL.md
```

### Install jpralph-auto (Batch Story Executor)

```
Please install the jpralph-auto skill from https://github.com/juanpare/JPSkills/tree/main/jpralph/skills/jpralph-auto

Copy the entire directory including:
- SKILL.md
- resources/prd.json.example
- resources/progress.txt.example

Place in: .agent/skills/jpralph-auto/

Verify: view_file .agent/skills/jpralph-auto/SKILL.md
```

### Install jpralph-orchestrator (Workflow Guide)

```
Please install the jpralph-orchestrator skill from https://github.com/juanpare/JPSkills/tree/main/jpralph/skills/jpralph-orchestrator

Copy the entire directory including:
- SKILL.md
- resources/workflow-guide.md

Place in: .agent/skills/jpralph-orchestrator/

Verify: view_file .agent/skills/jpralph-orchestrator/SKILL.md
```

---

## Verification

After installation, verify all skills are accessible:

```bash
# List installed skills
ls -la .agent/skills/

# Verify each skill has resources
ls -la .agent/skills/jpralph-prd/resources/
ls -la .agent/skills/jpralph-convert/resources/
ls -la .agent/skills/jpralph-iterate/resources/
ls -la .agent/skills/jpralph-auto/resources/
ls -la .agent/skills/jpralph-orchestrator/resources/
```

## Getting Started

Once installed, start with the orchestrator to get guided through the workflow:

```
view_file .agent/skills/jpralph-orchestrator/SKILL.md
```

Or jump directly to creating a PRD:

```
view_file .agent/skills/jpralph-prd/SKILL.md
```

## Skill Dependencies

The skills work together in this workflow:

```
jpralph-prd → jpralph-convert → (jpralph-iterate OR jpralph-auto)
                                           ↑
                                  jpralph-orchestrator
                                  (guides the workflow)
```

**Recommended installation order:**
1. Install all skills at once (easiest)
2. Or install in workflow order: prd → convert → iterate/auto → orchestrator

## Troubleshooting

### Skills not found

If you get "file not found" errors:
- Verify the .agent/skills directory exists
- Check that skill directories are named correctly (lowercase, with hyphens)
- Ensure resources/ subdirectories are present

### Missing resources

If a skill references a missing template or example:
- Check that the resources/ directory was copied
- Verify all files in resources/ are present
- Re-run the installation prompt for that skill

### Path issues

All skills now use relative paths and generic instructions. If you see absolute paths like `/Users/...`:
- You may have an older version
- Pull the latest from GitHub
- Re-install the affected skill

## Manual Installation

If you prefer to install manually:

1. Clone the repository:
   ```bash
   git clone https://github.com/juanpare/JPSkills.git
   ```

2. Copy skills to your project:
   ```bash
   mkdir -p .agent/skills
   cp -r JPSkills/jpralph/skills/* .agent/skills/
   ```

3. Verify installation:
   ```bash
   ls -la .agent/skills/
   ```

## Updates

To update skills to the latest version:

1. Pull latest changes from GitHub
2. Re-run the installation prompt for all skills
3. Or manually copy updated skill directories

## Support

For issues or questions:
- GitHub: https://github.com/juanpare/JPSkills
- See README.md for detailed documentation
- Check AGENTS.md for project-specific guidance

---

## What's Next?

After installation:

1. **Learn the workflow**: Load jpralph-orchestrator for step-by-step guidance
2. **Create your first PRD**: Load jpralph-prd and describe a feature
3. **Execute autonomously**: Use jpralph-auto for batched execution
4. **Read the docs**: Check out the main README.md for best practices

Happy coding with JPRalph! 🚀
