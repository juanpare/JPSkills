# JPSkills

> A curated repo of Antigravity-compatible skills, organized by workflow.

JPSkills contains self-contained skill packages that can be copied into an Antigravity project's `.agent/skills/` directory. Each skill lives with its own `SKILL.md`, supporting resources, and any workflow-specific scripts.

## Collections

### `jpralph`

PRD-driven autonomous development for Ralph-style execution inside Antigravity.

| Skill | Purpose |
| --- | --- |
| `jpralph-prd` | Generate a feature PRD |
| `jpralph-convert` | Convert a PRD into `prd.json` |
| `jpralph-iterate` | Execute one story in manual mode |
| `jpralph-auto` | Execute up to 5 stories in batch mode |
| `jpralph-orchestrator` | Guide the overall Ralph workflow |

Docs: [`jpralph/README.md`](jpralph/README.md)

### `openclaw`

Server-oriented automation skills for deterministic CLI workflows.

| Skill | Purpose |
| --- | --- |
| `openclaw-url-to-kindle` | Fetch a public URL, normalize it to markdown, sync it to Google Drive as a Doc, build an EPUB, and hand it off to Kindle delivery via `gog` |

Docs: [`openclaw/README.md`](openclaw/README.md)

## Install a Skill

Copy only the skill directories you need into your target project's `.agent/skills/` folder.

```bash
mkdir -p .agent/skills
cp -r JPSkills/jpralph/skills/jpralph-orchestrator .agent/skills/
cp -r JPSkills/openclaw/skills/openclaw-url-to-kindle .agent/skills/
```

Then load the installed skill directly, for example:

```text
view_file .agent/skills/jpralph-orchestrator/SKILL.md
view_file .agent/skills/openclaw-url-to-kindle/SKILL.md
```

## Repository Layout

```text
JPSkills/
|- jpralph/
|  |- skills/
|  |- examples/
|  |- templates/
|  |- INSTALLATION.md
|  |- README.md
|  `- AGENTS.md
|- openclaw/
|  |- skills/
|  |- README.md
|  `- AGENTS.md
`- README.md
```

## Conventions

- Skills are self-contained and documented through their local `SKILL.md` files.
- Supporting assets stay next to the skill in `resources/`, `scripts/`, or similar folders.
- Collection-level `README.md` files explain the workflow and assumptions for that area.

## Notes

- `jpralph` includes the most complete workflow documentation and installation guidance in [`jpralph/INSTALLATION.md`](jpralph/INSTALLATION.md).
- `openclaw-url-to-kindle` depends on the external `gog` CLI and local Python dependencies; see its skill doc for prerequisites.

## License

MIT
