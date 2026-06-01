# Agent Orchestration Rules

## Model Selection

| Task | Model | Reason |
|---|---|---|
| Exploration / file search | Haiku | Fast, cheap, sufficient |
| Single-file edits | Haiku | Clear scope |
| Writing docs | Haiku | Simple structure |
| Multi-file implementation | Sonnet | Best balance for coding |
| PR reviews | Sonnet | Understands context |
| Architecture decisions | Opus | Deep reasoning needed |
| Security analysis | Opus | Cannot afford to miss vulnerabilities |
| Debugging complex bugs | Opus | Must hold entire system in mind |

Default to **Sonnet** for 90% of coding tasks. Upgrade to Opus when: first attempt failed, task spans 5+ files, architectural decisions required, or security-critical code.

## Orchestration Phases

Follow these phases in order. Each phase has one clear input and one clear output.

1. **Research** — Use Explore agent. Output: `research-summary.md`
2. **Plan** — Use Plan agent. Input: research-summary.md. Output: `plan.md`
3. **Implement** — Use tdd-guide agent. Input: plan.md. Output: code changes
4. **Review** — Use code-reviewer agent. Input: diff. Output: `review-comments.md`
5. **Verify** — Run tests; use build-error-resolver if needed. Output: green tests or loop back

Never skip phases. Use `/clear` between agents to prevent context bleed.

## Context Discipline

- Store intermediate outputs in `.claude/sessions/YYYYMMDD.tmp` for cross-session continuity.
- Disable auto-compact for complex sessions; compact manually at logical phase boundaries.
- Pass objective context (the WHY), not just the query, when briefing a subagent.
