# Migration Plan: Flask → FastAPI + LiteLLM

## Overview

Migrate `mock_api_server.py` from Flask to FastAPI, replace dual AI SDKs (Anthropic + OpenAI) with LiteLLM, and introduce Ollama as a zero-cost local fallback. Every endpoint keeps its existing URL path and response shape — **n8n workflows change: zero lines**.

---

## Target Architecture

```
┌─────────────────────────────────────────────────┐
│                  FastAPI                         │
│  (uvicorn, async, Pydantic, auto-docs)           │
│                                                  │
│  ┌─────────────────────┐  ┌──────────────────┐  │
│  │ AI Layer (LiteLLM)  │  │ MCP Tools (async) │  │
│  │                     │  │                  │  │
│  │ claude-sonnet-4     │  │ file_manager     │  │
│  │   ↕ fallback ↕      │  │ content_research │  │
│  │ gpt-4o              │  │ image_generator  │  │
│  │   ↕ fallback ↕      │  │ calendar_mgr     │  │
│  │ ollama/llama3.2     │  │ analytics        │  │
│  └─────────────────────┘  └──────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐    │
│  │ Security: middleware + Pydantic validators│    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Fallback Chain

```
Client → FastAPI → LiteLLM ──┬── claude-sonnet-4 (primary)
                              ├── gpt-4o (fallback on 429/error)
                              └── ollama/llama3.2 (fallback if cloud down)
```

Env-configurable via:
```python
model = os.getenv("PRIMARY_MODEL", "claude-sonnet-4-20250514")
fallbacks = os.getenv("FALLBACK_MODELS", "gpt-4o,ollama/llama3.2").split(",")
```

No `MOCK_MODE` flag. Dev = set `PRIMARY_MODEL=ollama/llama3.2`, prod = set to Claude.

---

## File Inventory

### Files to DELETE (7 files — dead code)

| File | Lines | Reason |
|------|-------|--------|
| `mock_ai_generator.py` | 111 | Replaced by LiteLLM + Ollama |
| `test_claude.py` | 39 | LiteLLM replaces Anthropic SDK |
| `test_openai.py` | 40 | LiteLLM replaces OpenAI SDK |
| `test-security-hardening.py` | — | Orphaned, no references |
| `test-zero-vulnerabilities.py` | — | Orphaned, no references |
| `validate-docker-security.py` | — | Standalone, not integrated |
| `validate-requirements.py` | — | Standalone, not integrated |

### Files to CONSOLIDATE (2 → 1)

| From | To | Why |
|------|----|-----|
| `templates/claude_prompt.py` | `templates/prompts.py` | Both prompt builders — same AIDA structure, only formatting differs. Merge into one file with a generic `build_instagram_prompt()` |

### Files to REWRITE (4 files)

| File | What Changes |
|------|-------------|
| `mock_api_server.py` | Flask → FastAPI, Pydantic models, LiteLLM, async, security middleware rewrite |
| `ai_content_generator.py` | Dual SDK → LiteLLM Router + async; or merge logic into `mock_api_server.py` |
| `mcp_integration.py` | Remove `run_mcp_tool()` sync wrapper at L332-336 |
| `start_mock_server.py` | Change `from mock_api_server import app` + `app.run()` → `uvicorn.run()` |

### Files to UPDATE (7 files)

| File | What Changes |
|------|-------------|
| `requirements.txt` | Remove `flask`, `flask-cors`, `anthropic`, `openai`; add `litellm`, `fastapi[standard]`, `uvicorn` |
| `Dockerfile.mock-api` | Remove `mock_ai_generator.py` COPY line; change `FLASK_APP` → `FASTAPI_APP` env var |
| `setup_free_development.py` | Replace mock AI test with Ollama install check; update dependency install |
| `.env.example` | Add `PRIMARY_MODEL`, `FALLBACK_MODELS`, `OLLAMA_BASE_URL` vars |
| `test_mock_api.py` | Update import paths + startup instructions (minor) |
| `test_mcp_integration.py` | Update import paths (minor) |
| `README.md` | Update project tree, model versions, architecture diagram |

### Files UNCHANGED (16 files)

`docker-compose.yml`, `docker-compose.cloud.yml`, `deploy-cloud.py`, `start-cloud.sh`, `keep_ngrok_alive.*`, `keep_n8n_and_ngrok_alive.*`, `test_env.py`, `post-commit-security-check.py`, `production-security.py`, `security-hardening.py`, `security-monitor.py`, `security-best-practices-audit.py`, `CLOUD_DEPLOYMENT_GUIDE.md`, `MCP_INTEGRATION_GUIDE.md`, `N8N_MOCK_INTEGRATION.md`, `DOCKER_SECURITY_GUIDE.md`, `FREE_DEVELOPMENT_GUIDE.md`, `COMMIT_SECURITY_CHECKLIST.md`, `CODE_OF_CONDUCT.md`, `LICENSE`, `.dockerignore`, `.gitignore`

---

## Before/After: Key Patterns

### Pattern 1: Route Definition

**Before (Flask):**
```python
@app.route('/ai/claude/generate', methods=['POST'])
@security_middleware
def claude_generate():
    try:
        data = request.get_json()
        required_fields = ['topic', 'power_words', 'emotion', 'cta', 'niche']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}")
        ...
```

**After (FastAPI):**
```python
class ContentRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    power_words: str = Field(..., min_length=1)
    emotion: str = Field(..., min_length=1)
    cta: str = Field(..., min_length=1)
    niche: str = Field(..., min_length=1)

@app.post("/ai/generate", response_model=APIResponse)
async def ai_generate(data: ContentRequest):
    ...
```

- **Validation is automatic** — missing fields return 422 with no manual checks
- **Async** — `await asyncio.sleep()` instead of `time.sleep()`
- **Single route** — LiteLLM handles provider switching via the model parameter

### Pattern 2: AI Generation

**Before (Flask + dual SDKs):**
```python
# Claude
message = self.claude_client.messages.create(
    model="claude-3-sonnet-20240229", ...
)
return message.content[0].text

# OpenAI
response = self.openai_client.chat.completions.create(
    model="gpt-3.5-turbo", ...
)
return response.choices[0].message.content
```

**After (FastAPI + LiteLLM):**
```python
from litellm import acompletion

response = await acompletion(
    model=requested_model,           # "claude-sonnet-4-20250514" | "gpt-4o" | "ollama/llama3.2"
    messages=[{"role": "user", "content": prompt}],
    fallbacks=fallback_list,         # auto-chain on failure
    num_retries=2
)
content = response.choices[0].message.content  # always this shape
```

### Pattern 3: Security Middleware

**Before (Flask decorator):**
```python
def security_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            data = request.get_json()
            data = SecurityValidator.sanitize_input(data)
            if not SecurityValidator.validate_input(data):
                abort(400)
        response = f(*args, **kwargs)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        ...
```

**After (FastAPI middleware):**
```python
class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        if body:
            data = json.loads(body)
            if not SecurityValidator.validate_input(data):
                return PlainTextResponse("Invalid input", status_code=400)

        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        ...
```

- `SecurityValidator` class **stays identical** (same regex patterns, same logic)
- No more `request._cached_json` hack
- `bleach`, `validators`, `html` imports preserved

### Pattern 4: MCP Integration

**Before (Flask — sync wrapper):**
```python
# mcp_integration.py L332-336 — problem line
def run_mcp_tool(tool_name, parameters):
    manager = MCPManager()
    return asyncio.run(manager.call_tool(tool_name, parameters))

# mock_api_server.py L430 — called from sync route
result = run_mcp_tool(tool_name, data)
```

**After (FastAPI — native async, no wrapper):**
```python
# mcp_integration.py — delete run_mcp_tool(), just keep MCPManager
# mock_api_server.py — direct await
result = await mcp_manager.call_tool(tool_name, data)
```

### Pattern 5: Response Shape (PRESERVED)

**Exact contract n8n expects — unchanged:**
```python
class APIResponse(BaseModel):
    status: str = "success"
    message: str = "Success"
    data: Any = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    cost: str = "$0.00 (Mock)"  # LiteLLM provides real cost in prod
```

### Pattern 6: Dashboard

**Before (Flask):**
```python
return render_template_string(dashboard_html, analytics=mock_database["analytics"])
```

**After (FastAPI):**
```python
from jinja2 import Template

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(Template(DASHBOARD_HTML).render(analytics=mock_database["analytics"]))
```

Same HTML template, same variable injection — just swap the renderer.

---

## Dependencies

### requirements.txt Before (47 lines)
```
anthropic==0.52.1
openai==1.82.0
flask==3.1.1
flask-cors==6.0.0
httpx==0.28.1
gunicorn==23.0.0
cryptography==45.0.3
certifi==2025.4.26
urllib3==2.5.0
requests==2.32.4
bleach==6.2.0
validators==0.35.0
flask-limiter==3.12
flask-talisman==1.1.0
structlog==25.3.0
werkzeug==3.1.3
itsdangerous==2.2.0
click==8.1.8
markupsafe==3.0.2
bandit==1.8.0
safety==4.0.1
```

### requirements.txt After (~20 lines)
```
# AI — unified provider interface with fallback support
litellm>=1.61.2

# Web framework — async-native, Pydantic validation, auto-docs
fastapi[standard]>=0.115.0
uvicorn[standard]>=0.34.0

# HTTP client (for MCP tools)
httpx>=0.28.1

# Security
bleach>=6.2.0
validators>=0.35.0

# Production infra
gunicorn>=23.0.0

# Dev/audit
bandit>=1.8.0
safety>=4.0.1
```

---

## Dockerfile.mock-api Changes

| Line | Before | After |
|------|--------|-------|
| 72 | `COPY mock_ai_generator.py .` | **Remove** (deleted file) |
| 95 | `ENV FLASK_APP=mock_api_server.py` | `ENV FASTAPI_APP=mock_api_server.py` |
| 123 | `CMD ["python3", "-u", "mock_api_server.py"]` | `CMD ["uvicorn", "mock_api_server:app", "--host", "0.0.0.0", "--port", "8000"]` |

---

## Implementation Order (sequential)

| Step | What | Files Changed | Expected Time |
|------|------|---------------|---------------|
| 1 | Delete dead files | 7 files removed | 2 min |
| 2 | Consolidate templates | `claude_prompt.py` + `openai_prompt.py` → `prompts.py` | 5 min |
| 3 | Rewrite `mock_api_server.py` | Flask → FastAPI, LiteLLM, Pydantic, async, security middleware | 30 min |
| 4 | Rewrite `ai_content_generator.py` | Dual SDK → LiteLLM Router | 10 min |
| 5 | Clean `mcp_integration.py` | Remove `run_mcp_tool()` sync wrapper | 2 min |
| 6 | Update `start_mock_server.py` | Flask import → FastAPI/uvicorn import | 3 min |
| 7 | Update `requirements.txt` | Remove old deps, add `litellm fastapi uvicorn` | 2 min |
| 8 | Update `Dockerfile.mock-api` | Remove deleted file COPY, update CMD | 2 min |
| 9 | Update `setup_free_development.py` | Replace mock AI test with Ollama check, new deps | 5 min |
| 10 | Update `.env.example` | Add model config vars | 2 min |
| 11 | Update test files | `test_mock_api.py`, `test_mcp_integration.py` | 5 min |
| 12 | Update `README.md` | Project tree, model versions, architecture | 10 min |
| 13 | Test everything | Run test suite, verify n8n contract | 10 min |

**Total: ~90 min of code work**

---

## n8n Contract Verification

All existing n8n workflows will continue to work because:

| n8n Expects | Status |
|-------------|--------|
| `POST /health` | ✅ Same URL, same response shape |
| `POST /ai/claude/generate` | ✅ **Deprecated** — use `POST /ai/generate` with `model="claude-sonnet-4"` |
| `POST /ai/openai/generate` | ✅ **Deprecated** — use `POST /ai/generate` with `model="gpt-4o"` |
| `POST /ai/compare` | ✅ Same URL, same response (A/B comparison preserved) |
| `POST /ai/stories` | ✅ Same URL, same response |
| `POST /instagram/post` | ✅ Same URL, same response |
| `GET /analytics` | ✅ Same URL, same response |
| `GET /` (dashboard) | ✅ Same URL, same HTML |
| `POST /mcp/<tool>` | ✅ All 6 MCP routes unchanged |
| `GET /mcp/tools` | ✅ Same URL, same response |

Old `/ai/claude/generate` and `/ai/openai/generate` endpoints return a 301 redirect to `/ai/generate` with a deprecation warning in the response — n8n workflows using them continue working without changes, but can be updated at leisure.

---

## Quickstart (after migration)

```bash
# Development with Ollama (free, local, no API keys)
pip install -r requirements.txt
ollama pull llama3.2
PRIMARY_MODEL=ollama/llama3.2 uvicorn mock_api_server:app --port 8000

# Production with Cloud AI + Ollama fallback
PRIMARY_MODEL=claude-sonnet-4-20250514 \
FALLBACK_MODELS=gpt-4o,ollama/llama3.2 \
uvicorn mock_api_server:app --host 0.0.0.0 --port 8000
```
