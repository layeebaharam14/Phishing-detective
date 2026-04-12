# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
My Env V4 Environment Implementation.

A simple test environment that echoes back messages sent to it.
Perfect for testing HTTP server infrastructure.
"""

import random
from typing import TypedDict, Literal

try:
    from ..models import Difficulty, EmailSample, MyEnvV4Action, MyEnvV4Observation
except ImportError:
    from models import Difficulty, EmailSample, MyEnvV4Action, MyEnvV4Observation


EmailLabel = Literal["phishing", "safe"]


class EmailInternal(TypedDict):
    subject: str
    sender: str
    message: str
    has_link: bool
    is_urgent: bool
    difficulty: Difficulty
    label: EmailLabel


class MyEnvV4Environment:
    """Simple single-session environment for the Phishing Detective demo."""

    def __init__(self):
        self._round = 0
        self._total_score = 0.0
        self._current: EmailInternal | None = None

    def reset(self):
        self._round += 1
        emails: list[EmailInternal] = [
            {
                "sender": "fake@scam.com",
                "subject": "Immediate Action Required",
                "message": "URGENT! Your account is hacked. Click now to secure it.",
                "has_link": True,
                "is_urgent": True,
                "difficulty": "easy",
                "label": "phishing"
            },
            {
                "sender": "security@yourbank.com",
                "subject": "Unusual sign-in activity",
                "message": "We noticed an unusual sign-in attempt. Please review your recent activity to keep your account secure.",
                "has_link": True,
                "is_urgent": False,
                "difficulty": "medium",
                "label": "phishing"
            },
            {
                "sender": "noreply@yourbank.com",
                "subject": "Bank Statement",
                "message": "Your monthly bank statement is ready. Log in to your banking app to view it.",
                "has_link": False,
                "is_urgent": False,
                "difficulty": "hard",
                "label": "safe"
            },
            {
                "sender": "it-support@company.com",
                "subject": "Password Expiration Reminder",
                "message": "Hi! Your password will expire in 3 days. Please update it via the internal portal.",
                "has_link": False,
                "is_urgent": False,
                "difficulty": "hard",
                "label": "safe"
            },
            {
                "sender": "billing@streaming-support.com",
                "subject": "Payment Failed — Update Required",
                "message": "Your last payment failed. Update your card details to avoid service interruption.",
                "has_link": True,
                "is_urgent": True,
                "difficulty": "easy",
                "label": "phishing"
            },
            {
                "sender": "support@paypaI.com",
                "subject": "Invoice available",
                "message": "Your invoice is ready. View the details to confirm this activity.",
                "has_link": True,
                "is_urgent": False,
                "difficulty": "medium",
                "label": "phishing"
            },
        ]

        self._current = random.choice(emails)
        email = EmailSample(
            subject=self._current["subject"],
            sender=self._current["sender"],
            message=self._current["message"],
            has_link=self._current["has_link"],
            is_urgent=self._current["is_urgent"],
            difficulty=self._current["difficulty"],
        )

        # OpenEnv-style: reset returns an observation only.
        return {"email": email.model_dump()}

    def step(self, action: MyEnvV4Action):
        """
        OpenEnv-style step().

        Returns:
            observation, reward, done, info
        """
        if self._current is None:
            # If someone calls /step before /reset, just start a round.
            obs = self.reset()
            return obs, 0.0, False, {"correct": False}

        prediction: EmailLabel = action.action.strip().lower()  # type: ignore[assignment]
        correct: EmailLabel = self._current["label"]
        is_correct = prediction == correct
        if is_correct:
            reward = 1.0 
        elif prediction in ["phishing", "safe"]:
            reward = 0.5
        else:
            reward = 0.0

        self._total_score += reward

        email = EmailSample(
            subject=self._current["subject"],
            sender=self._current["sender"],
            message=self._current["message"],
            has_link=self._current["has_link"],
            is_urgent=self._current["is_urgent"],
            difficulty=self._current["difficulty"],
        )

        observation = {"email": email.model_dump()}
        done = True
        info = {"correct": is_correct}
        return observation, float(reward), done, info
            

    @property
    def total_score(self) -> float:
        return self._total_score

    def state(self):
        return {"round": self._round, "total_score": self._total_score}
