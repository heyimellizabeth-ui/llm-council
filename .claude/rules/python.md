# Python Rules — LLM Council

## Module System

- Always use relative imports: `from .config import COUNCIL_MODELS` not `from config import COUNCIL_MODELS`.
- Always run the backend as `python -m backend.main` from the project root, never as `python backend/main.py`.

## Ports

- Backend: **8001** (not 8000).
- Frontend: **5173** (Vite default).
- If changing ports, update both `backend/main.py` CORS config and `frontend/src/api.js`.

## Async Patterns

- Use `asyncio.gather()` for parallel model queries; never use sequential `await` loops when parallelism is possible.
- Graceful degradation: a single model failure must never abort the full request. Return `None` for failed models and continue.

## Error Handling

- Log errors server-side; do not expose raw exceptions to the frontend.
- Only surface errors to the user when all models fail.

## Data Persistence

- Conversation metadata (label_to_model, aggregate_rankings) is ephemeral — returned via API but NOT persisted to `data/conversations/` JSON.
- Never persist API keys or model secrets to storage.

## Markdown Rendering (Frontend)

- All ReactMarkdown components must be wrapped in `<div className="markdown-content">` for correct spacing.
