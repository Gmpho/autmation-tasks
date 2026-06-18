#!/usr/bin/env python3
"""
Secure Mock API Server for Instagram Automation Testing
FastAPI + LiteLLM + Ollama — unified AI with fallback support
"""

import os
import json
import re
import html
import random
import logging
import asyncio
from datetime import datetime
from typing import Any, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from mcp_integration import MCPManager

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------

class SecurityValidator:
    DANGEROUS_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"vbscript:",
        r"onload\s*=",
        r"onerror\s*=",
        r"onclick\s*=",
        r"[;&|`$(){}[\]\\]",
        r"\b(cat|ls|pwd|whoami|id|uname|ps|netstat|wget|curl|nc|telnet|ssh)\b",
        r"(\.\.\/|\.\.\\)",
        r"(%2e%2e%2f|%2e%2e%5c)",
    ]

    @staticmethod
    def sanitize_input(data):
        if isinstance(data, str):
            data = html.escape(data)
            data = data.replace('\x00', '')
            if len(data) > 10000:
                data = data[:10000]
        elif isinstance(data, dict):
            return {k: SecurityValidator.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [SecurityValidator.sanitize_input(item) for item in data]
        return data

    @staticmethod
    def validate_value(value: str) -> bool:
        if not isinstance(value, str):
            return True
        value_lower = value.lower()
        for pattern in SecurityValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, value_lower, re.IGNORECASE):
                logger.warning(f"Dangerous pattern detected: {pattern}")
                return False
        return True

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class APIResponse(BaseModel):
    status: str = "success"
    message: str = "Success"
    data: Any = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    cost: str = "$0.00 (Mock)"

class ContentRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    power_words: str = Field(..., min_length=1)
    emotion: str = Field(..., min_length=1)
    cta: str = Field(..., min_length=1)
    niche: str = Field(..., min_length=1)

class StoriesRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    style: str = "casual"

class InstagramPostRequest(BaseModel):
    content: str = Field(..., min_length=1)
    hashtags: list[str] = Field(..., min_length=1)

# ---------------------------------------------------------------------------
# Mock database
# ---------------------------------------------------------------------------

mock_database = {
    "generated_content": [],
    "instagram_posts": [],
    "analytics": {
        "total_requests": 0,
        "ai_generations": 0,
        "instagram_posts": 0
    }
}

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(title="Mock API Server", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5678",
        "http://127.0.0.1:5678",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

mcp_manager = MCPManager()

# ---------------------------------------------------------------------------
# Security middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")

    mock_database["analytics"]["total_requests"] += 1

    if request.method == "POST":
        body = await request.body()
        if body:
            try:
                data = json.loads(body)
                sanitized = SecurityValidator.sanitize_input(data)
                ok = True
                for v in (sanitized.values() if isinstance(sanitized, dict) else [sanitized]):
                    if isinstance(v, str) and not SecurityValidator.validate_value(v):
                        ok = False
                        break
                if not ok:
                    logger.warning(f"Malicious input detected from {request.client.host}")
                    return JSONResponse(
                        {"status": "error", "message": "Invalid input detected",
                         "timestamp": datetime.now().isoformat()},
                        status_code=400
                    )
            except json.JSONDecodeError:
                pass

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# ---------------------------------------------------------------------------
# LiteLLM helpers
# ---------------------------------------------------------------------------

PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "claude-sonnet-4-20250514")
FALLBACK_MODELS = os.getenv("FALLBACK_MODELS", "")

async def generate_ai_content(prompt: str, model: str | None = None) -> tuple[str, str]:
    from litellm import acompletion

    chosen = model or PRIMARY_MODEL
    kwargs = {
        "model": chosen,
        "messages": [{"role": "user", "content": prompt}],
        "num_retries": 2,
    }

    fallbacks = FALLBACK_MODELS.split(",") if FALLBACK_MODELS else []
    if fallbacks:
        kwargs["fallbacks"] = fallbacks

    response = await acompletion(**kwargs)
    content = response.choices[0].message.content or ""

    cost = "$0.00 (Mock)"
    try:
        raw = response._hidden_params.get("response_cost")
        if raw is not None:
            cost = f"${float(raw):.4f}"
    except Exception:
        pass

    return content, cost

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return APIResponse(
        data={
            "service": "Mock API Server",
            "status": "healthy",
            "uptime": "Running",
            "endpoints": [
                "/ai/generate", "/ai/compare", "/ai/stories",
                "/instagram/post", "/analytics"
            ]
        }
    )


@app.post("/ai/generate")
async def ai_generate(data: ContentRequest):
    from templates.prompts import build_instagram_prompt

    await asyncio.sleep(random.uniform(0.5, 2.0))

    prompt = build_instagram_prompt(
        data.topic, data.power_words, data.emotion, data.cta, data.niche
    )
    content, cost = await generate_ai_content(prompt)

    result = {
        "id": len(mock_database["generated_content"]) + 1,
        "provider": PRIMARY_MODEL,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    }
    mock_database["generated_content"].append(result)
    mock_database["analytics"]["ai_generations"] += 1

    return APIResponse(data=result, message="Content generated successfully", cost=cost)


@app.post("/ai/claude/generate")
async def claude_generate_redirect(data: ContentRequest):
    logger.warning("/ai/claude/generate is deprecated — use /ai/generate with PRIMARY_MODEL")
    import copy
    req = copy.copy(data)
    return await ai_generate(req)


@app.post("/ai/openai/generate")
async def openai_generate_redirect(data: ContentRequest):
    logger.warning("/ai/openai/generate is deprecated — use /ai/generate with PRIMARY_MODEL")
    import copy
    req = copy.copy(data)
    return await ai_generate(req)


@app.post("/ai/compare")
async def ai_compare(data: ContentRequest):
    from litellm import acompletion
    from templates.prompts import build_instagram_prompt

    await asyncio.sleep(random.uniform(1.0, 3.0))

    models = ["claude-sonnet-4-20250514", "gpt-4o"]
    prompt = build_instagram_prompt(
        data.topic, data.power_words, data.emotion, data.cta, data.niche
    )

    async def call_model(model: str):
        try:
            resp = await acompletion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                num_retries=1,
            )
            c = resp.choices[0].message.content or ""
            cost_raw = None
            try:
                cost_raw = resp._hidden_params.get("response_cost")
            except Exception:
                pass
            return {"provider": model, "content": c, "cost": cost_raw}
        except Exception as e:
            return {"provider": model, "error": str(e)}

    results = await asyncio.gather(call_model(models[0]), call_model(models[1]))

    total_cost = 0.0
    for r in results:
        if r.get("cost") is not None:
            total_cost += float(r["cost"])
        r.pop("cost", None)

    comparison_result = {
        "comparison_id": len(mock_database["generated_content"]) + 1,
        "timestamp": datetime.now().isoformat(),
        "providers": {r["provider"].split("-")[0]: r for r in results},
        "recommendation": "Both providers generated quality content. Choose based on your preference.",
        "total_cost": f"${total_cost:.4f}" if total_cost else "$0.00 (Mock)",
    }

    mock_database["generated_content"].append(comparison_result)
    mock_database["analytics"]["ai_generations"] += 2

    return APIResponse(
        data=comparison_result,
        message="AI comparison completed successfully",
        cost=comparison_result["total_cost"],
    )


@app.post("/ai/stories")
async def generate_stories(data: StoriesRequest):
    from templates.prompts import build_story_prompt

    await asyncio.sleep(random.uniform(0.5, 1.5))

    prompt = build_story_prompt(data.topic, data.style)
    content, cost = await generate_ai_content(prompt)

    result = {
        "id": len(mock_database["generated_content"]) + 1,
        "provider": PRIMARY_MODEL,
        "content": content,
        "type": "stories",
        "timestamp": datetime.now().isoformat(),
    }
    mock_database["generated_content"].append(result)

    return APIResponse(data=result, message="Instagram Stories generated successfully", cost=cost)


@app.post("/instagram/post")
async def instagram_post(data: InstagramPostRequest):
    await asyncio.sleep(random.uniform(1.0, 3.0))

    post_result = {
        "post_id": f"mock_post_{random.randint(1000, 9999)}",
        "status": "published",
        "content": data.content,
        "hashtags": data.hashtags,
        "timestamp": datetime.now().isoformat(),
        "engagement": {
            "likes": random.randint(10, 100),
            "comments": random.randint(1, 20),
            "shares": random.randint(0, 10)
        },
        "reach": random.randint(100, 1000),
        "url": f"https://instagram.com/p/mock_post_{random.randint(1000, 9999)}"
    }

    mock_database["instagram_posts"].append(post_result)
    mock_database["analytics"]["instagram_posts"] += 1

    return APIResponse(data=post_result, message="Instagram post published successfully")


@app.get("/analytics")
async def get_analytics():
    analytics = {
        **mock_database["analytics"],
        "recent_content": mock_database["generated_content"][-5:],
        "recent_posts": mock_database["instagram_posts"][-5:],
        "server_uptime": "Running",
        "total_cost": "$0.00 (All Mock)"
    }
    return APIResponse(data=analytics, message="Analytics retrieved successfully")


# ---------------------------------------------------------------------------
# MCP Endpoints
# ---------------------------------------------------------------------------

@app.get("/mcp/tools")
async def get_mcp_tools():
    try:
        tools = mcp_manager.get_available_tools()
        return APIResponse(data=tools, message="MCP tools retrieved successfully")
    except Exception as e:
        logger.error(f"Failed to get MCP tools: {e}", exc_info=True)
        return JSONResponse(
            {"status": "error", "message": "Failed to retrieve MCP tools",
             "timestamp": datetime.now().isoformat()},
            status_code=500
        )


class MCPCallRequest(BaseModel):
    parameters: dict[str, Any] = Field(default_factory=dict)


@app.post("/mcp/{tool_name}")
async def call_mcp_tool(tool_name: str, data: MCPCallRequest):
    try:
        result = await mcp_manager.call_tool(tool_name, data.parameters)

        result["id"] = len(mock_database["generated_content"]) + 1
        mock_database["generated_content"].append(result)

        return APIResponse(
            data=result,
            message=f"MCP tool '{tool_name}' executed successfully",
            cost=result.get("cost", "$0.00 (Mock)"),
        )
    except ValueError as e:
        logger.error(f"ValueError: {e}", exc_info=True)
        return JSONResponse(
            {"status": "error", "message": str(e),
             "timestamp": datetime.now().isoformat()},
            status_code=404
        )
    except Exception as e:
        logger.error(f"MCP tool execution failed: {e}", exc_info=True)
        return JSONResponse(
            {"status": "error", "message": "MCP tool execution failed",
             "timestamp": datetime.now().isoformat()},
            status_code=500
        )


@app.post("/mcp/filesystem")
async def mcp_filesystem(data: MCPCallRequest):
    return await call_mcp_tool("file_manager", data)


@app.post("/mcp/research")
async def mcp_research(data: MCPCallRequest):
    return await call_mcp_tool("content_research", data)


@app.post("/mcp/images")
async def mcp_images(data: MCPCallRequest):
    return await call_mcp_tool("image_generator", data)


@app.post("/mcp/calendar")
async def mcp_calendar(data: MCPCallRequest):
    return await call_mcp_tool("calendar_manager", data)


@app.post("/mcp/analytics")
async def mcp_analytics(data: MCPCallRequest):
    return await call_mcp_tool("analytics_tracker", data)


@app.post("/mcp/hashtags")
async def mcp_hashtags(data: MCPCallRequest):
    return await call_mcp_tool("hashtag_optimizer", data)


# ---------------------------------------------------------------------------
# Dashboard — serves frontend SPA if built, otherwise redirects to /docs
# ---------------------------------------------------------------------------

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "frontend", "dist")

@app.get("/", include_in_schema=False)
async def dashboard():
    index = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.isfile(index):
        return FileResponse(index)
    return JSONResponse({
        "message": "Frontend not built. Run `cd frontend && npm run build` or `npm run dev`.",
        "docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/health",
    })

if os.path.isdir(FRONTEND_DIST):
    from fastapi.staticfiles import StaticFiles
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")
    app.mount("/favicon.ico", StaticFiles(directory=FRONTEND_DIST), name="favicon")


# ---------------------------------------------------------------------------
# Entrypoint (for direct execution, otherwise use uvicorn)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    debug = os.getenv("FASTAPI_DEBUG", "false").lower() == "true"
    uvicorn.run("mock_api_server:app", host="localhost", port=8000, reload=debug)
