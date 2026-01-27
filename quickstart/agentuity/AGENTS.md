# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- **Dev**: `bun run dev` (starts dev server at http://localhost:3500)
- **Build**: `bun run build` (compiles to .agentuity/)
- **Typecheck**: `bun run typecheck` (TypeScript type checking)
- **Deploy**: `bun run deploy` (deploys to Agentuity cloud)

Test endpoints locally:
```bash
curl -X POST http://localhost:3500/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "toLanguage": "Spanish"}'
```

## Architecture

This is an Agentuity project using Bun runtime and TypeScript with two main layers:

### Agents (`src/agent/`)
AI-powered handlers defined with `createAgent()`. Each agent folder contains `agent.ts`. Agents have:
- Input/output schemas using `@agentuity/schema` (the `s` object)
- Handler function receiving `(ctx, input)` where ctx provides logger, kv, vector, thread state
- Optional setup/shutdown lifecycle hooks

### API Routes (`src/api/`)
REST endpoints using Hono router via `createRouter()`. Routes access services through `c.var.*`. Call agents by importing: `await agent.run(data)`.

### Generated Files (`src/generated/`)
Auto-generated on build. Never edit.

## Key Patterns

- **Schema validation**: Use `@agentuity/schema` for schemas. Use `agent.validator()` middleware for automatic validation.
- **State**: `ctx.thread.state` for persistent conversation state. `ctx.state` for request-scoped state.
- **Agent calls**: Import directly: `import agent from '../other/agent'` then `await agent.run(input)`
- **Logging**: Use `ctx.logger` (agents) or `c.var.logger` (routes), not console.log

## Agent-Friendly CLI

The Agentuity CLI supports `--json` for machine-readable output, `--explain` to preview commands, and `--dry-run` for safe testing.

See [CLI AGENTS.md](./node_modules/@agentuity/cli/AGENTS.md) for detailed CLI usage.

## Learn More

- [Agentuity Documentation](https://agentuity.dev)
- [Bun Documentation](https://bun.sh/docs)
- [Hono Documentation](https://hono.dev/)
- [Zod Documentation](https://zod.dev/)
