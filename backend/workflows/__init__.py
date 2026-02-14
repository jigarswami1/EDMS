"""Workflow orchestration package."""

from .state_machine import ALLOWED_TRANSITIONS, assert_transition_allowed

__all__ = ["ALLOWED_TRANSITIONS", "assert_transition_allowed"]
