"""Re-export base classes from set-project-base.

All base classes and dataclasses are defined in set-project-base.
This module re-exports them for backward compatibility.
"""

from set_project_base.base import (
    OrchestrationDirective,
    ProjectType,
    ProjectTypeInfo,
    TemplateInfo,
    VerificationRule,
)

__all__ = [
    "OrchestrationDirective",
    "ProjectType",
    "ProjectTypeInfo",
    "TemplateInfo",
    "VerificationRule",
]
