# Claude Code plugin

NiceTryGPT is available in two compatible forms in this repository:

- `nice-try-gpt/` — the standalone Agent Skill source and ZIP-packaging source;
- `skills/nice-try-gpt/` — the Claude Code plugin copy discovered automatically from the repository root.

The plugin manifest lives at `.claude-plugin/plugin.json`.

## Local test

Clone the repository and start Claude Code with the repository as a plugin directory:

```bash
claude --plugin-dir /path/to/NiceTryGPT
```

Then ask Claude to review an authorized CTF challenge with NiceTryGPT, or invoke the skill directly if your Claude Code version exposes installed skills as slash commands.

## Keep the two skill layouts synchronized

The standalone and plugin layouts intentionally contain the same skill so existing standalone users are not broken while the repository becomes plugin-ready.

After changing the canonical standalone skill, run:

```bash
python scripts/sync_plugin_skill.py
python tests/test_release.py
```

CI checks that every file in `nice-try-gpt/` has an identical counterpart in `skills/nice-try-gpt/`.

## Distribution status

The repository is structurally ready to be tested as a Claude Code plugin and submitted to a Claude plugin directory. Inclusion in an Anthropic-managed marketplace is a separate review process and is not claimed until accepted.

The plugin intentionally contains no hooks, MCP servers, background services, or additional executable dependencies. Its behavior comes from the NiceTryGPT skill instructions and the tools already available in the user's authorized Claude Code environment.
