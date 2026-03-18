# OpenClaw Skills

OpenClaw skills in this repository target small, automation-friendly server workflows.

## Available Skills

### `openclaw-url-to-kindle`

Pipeline:

```text
URL -> markdown -> EPUB -> Kindle delivery command
```

The skill uses a lightweight URL-to-markdown fetch step and a local Python EPUB generator adapted from `smerchek/claude-epub-skill`.

## Structure

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

## Notes

- The EPUB conversion is local Python code.
- The Kindle send step is intentionally command-template based because delivery CLIs vary by server.
- In this environment, `gog` was not installed on `PATH`, so send-to-Kindle could not be end-to-end verified here.
