# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Data models for the My Env V4 Environment.

The my_env_v4 environment is a simple test environment that echoes back messages.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


EmailLabel = Literal["phishing", "safe"]
Difficulty = Literal["easy", "medium", "hard"]


class EmailSample(BaseModel):
    subject: str
    sender: str
    message: str
    has_link: bool = Field(description="Whether the email contains a link")
    is_urgent: bool = Field(description="Whether the email sounds urgent")
    difficulty: Difficulty


class MyEnvV4Action(BaseModel):
    """Action for the Phishing Detective environment."""

    action: EmailLabel = Field(..., description="User classification action")


class MyEnvV4Observation(BaseModel):
    """Observation (email only)."""

    email: EmailSample


class ResetResponse(BaseModel):
    email: EmailSample
    reward: float
    correct: bool
    done: bool


class StepResponse(BaseModel):
    email: EmailSample
    reward: float
    correct: bool
    done: bool
