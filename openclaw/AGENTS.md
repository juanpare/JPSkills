# OpenClaw Skills

This directory contains OpenClaw-oriented skills intended to run on a VPS or server environment.

## For AI Agents

When working with OpenClaw skills:

1. Load the target `SKILL.md` directly
2. Keep skills self-contained with their own scripts and resources
3. Prefer deterministic CLI steps over interactive flows
4. Document environment assumptions explicitly

## Available Skills

- `openclaw-url-to-kindle`: Fetch a public URL, convert it to markdown, build an EPUB, and hand it off to a Kindle delivery command

## Project Structure

```
openclaw/
├── skills/
│   └── openclaw-url-to-kindle/
│       ├── SKILL.md
│       ├── requirements.txt
│       ├── scripts/
│       └── resources/
├── README.md
└── AGENTS.md
```
