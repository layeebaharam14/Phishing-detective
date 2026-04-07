# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
FastAPI application for the My Env V4 Environment.

This module creates an HTTP server that exposes the MyEnvV4Environment
over HTTP and WebSocket endpoints, compatible with EnvClient.

Endpoints:
    - POST /reset: Start a new round (get a random email)
    - POST /step: Submit classification (phishing/safe) and get reward

Usage:
    # Development (with auto-reload):
    uvicorn server.app:app --reload --host 0.0.0.0 --port 8000

    # Production:
    uvicorn server.app:app --host 0.0.0.0 --port 8000 --workers 4

    # Or run directly:
    python -m server.app
"""

try:
    # openenv is optional for this hackathon demo backend.
    pass
except Exception:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import MyEnvV4Action, ResetResponse, StepResponse
from server.my_env_v4_environment import MyEnvV4Environment

app = FastAPI(title="Phishing Detective API", version="1.0.0")

env = MyEnvV4Environment()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/reset", response_model=ResetResponse)
async def reset():
    obs = env.reset()  # observation only
    return {
        "email": obs["email"],
        "reward": 0.0,
        "correct": False,
        "done": False,
    }


@app.post("/step", response_model=StepResponse)
async def step(action: MyEnvV4Action):
    observation, reward, done, info = env.step(action)
    return {
        "email": observation["email"],
        "reward": float(reward),
        "correct": bool(info.get("correct", False)),
        "done": bool(done),
    }


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/state")
async def state():
    return env.state()
def main(host: str = "0.0.0.0", port: int = 8000):
    """
    Entry point for direct execution via uv run or python -m.

    This function enables running the server without Docker:
        uv run --project . server
        uv run --project . server --port 8001
        python -m my_env_v4.server.app

    Args:
        host: Host address to bind to (default: "0.0.0.0")
        port: Port number to listen on (default: 8000)

    For production deployments, consider using uvicorn directly with
    multiple workers:
        uvicorn my_env_v4.server.app:app --workers 4
    """
    import uvicorn

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
