"""Web project type plugin for wt-tools."""

from typing import List

from wt_project_base import BaseProjectType
from wt_project_base.base import (
    OrchestrationDirective,
    ProjectTypeInfo,
    TemplateInfo,
    VerificationRule,
)


class WebProjectType(BaseProjectType):
    """Web application project type.

    Extends BaseProjectType with web-specific verification rules and
    orchestration directives (i18n, routing, DB migrations, components).
    """

    @property
    def info(self) -> ProjectTypeInfo:
        return ProjectTypeInfo(
            name="web",
            version="0.1.0",
            description="Web application project knowledge (i18n, routing, DB, components)",
            parent="base",
        )

    def get_templates(self) -> List[TemplateInfo]:
        return [
            TemplateInfo(
                id="nextjs",
                description="Next.js App Router with Prisma, next-intl, shadcn/ui",
                template_dir="templates/nextjs",
            ),
            TemplateInfo(
                id="spa",
                description="Generic single-page application (minimal starting point)",
                template_dir="templates/spa",
            ),
        ]

    def get_verification_rules(self) -> List[VerificationRule]:
        # Base rules (file-size-limit, no-secrets, todo-tracking) inherited from BaseProjectType
        base_rules = super().get_verification_rules()
        web_rules = [
            VerificationRule(
                id="i18n-completeness",
                description="All UI strings must exist in all locale files",
                check="cross-file-key-parity",
                severity="error",
                config={"files": {"pattern": "messages/*.json"}},
            ),
            VerificationRule(
                id="route-registered",
                description="New page routes should be registered in navigation config",
                check="file-mentions",
                severity="warning",
                config={
                    "source": {
                        "pattern": "src/app/**/page.tsx",
                        "exclude": ["src/app/api/**", "src/app/login/**", "src/app/register/**"],
                    },
                    "target": "cross-cutting.sidebar",
                },
            ),
            VerificationRule(
                id="cross-cutting-consistency",
                description="Sidebar items, route labels, and i18n keys must be in sync",
                check="cross-reference",
                severity="warning",
                config={
                    "groups": [
                        {
                            "name": "navigation",
                            "files": [
                                {"role": "sidebar"},
                                {"role": "route_labels"},
                                {"role": "i18n"},
                            ],
                            "key_pattern": "route-segment",
                        }
                    ]
                },
            ),
            VerificationRule(
                id="migration-safety",
                description="Schema changes must have corresponding migrations",
                check="schema-migration-sync",
                severity="error",
                config={
                    "schema_file": "prisma/schema.prisma",
                    "migrations_dir": "prisma/migrations/",
                    "design_doc": "docs/design/data-model.md",
                },
            ),
            VerificationRule(
                id="ghost-button-text",
                description="Ghost buttons must be icon-only (no text content)",
                check="pattern-absence",
                severity="warning",
                config={
                    "pattern": "src/components/**/*.tsx",
                    "forbidden": r'variant="ghost".*>[^<]*<',
                },
            ),
            VerificationRule(
                id="functional-test-coverage",
                description="User-facing feature changes must include Playwright functional tests",
                check="file-mentions",
                severity="warning",
                config={
                    "source": {
                        "pattern": "src/app/**/page.tsx",
                        "exclude": ["src/app/api/**"],
                    },
                    "target": "tests/e2e/*.spec.ts",
                },
            ),
        ]
        return base_rules + web_rules

    def get_orchestration_directives(self) -> List[OrchestrationDirective]:
        # Base directives (install-deps, no-parallel-lockfile, config-review) inherited
        base_directives = super().get_orchestration_directives()
        web_directives = [
            OrchestrationDirective(
                id="no-parallel-i18n",
                description="Serialize changes that modify locale files to prevent merge conflicts",
                trigger='change-modifies("messages/*.json")',
                action="serialize",
                config={"with": 'changes-modifying("messages/*.json")'},
            ),
            OrchestrationDirective(
                id="consolidate-i18n",
                description="Warn when multiple changes each modify locale files",
                trigger='plan-has-multiple-changes-modifying("messages/*.json")',
                action="warn",
                config={
                    "message": "Multiple changes modify locale files — consider consolidating into a single i18n change"
                },
            ),
            OrchestrationDirective(
                id="db-generate",
                description="Regenerate Prisma client after schema changes",
                trigger='change-modifies("prisma/schema.prisma")',
                action="post-merge",
                config={"command": "pnpm db:generate"},
            ),
            OrchestrationDirective(
                id="cross-cutting-review",
                description="Flag changes to cross-cutting files for extra review",
                trigger="change-modifies-any(cross_cutting_files.sidebar, cross_cutting_files.i18n, cross_cutting_files.route_labels)",
                action="flag-for-review",
            ),
            OrchestrationDirective(
                id="playwright-setup",
                description="First change that creates Playwright tests must also set up playwright.config.ts and install browsers",
                trigger='change-creates("tests/e2e/*.spec.ts")',
                action="warn",
                config={
                    "message": "Playwright test files detected — ensure playwright.config.ts exists and @playwright/test is in devDependencies"
                },
            ),
        ]
        return base_directives + web_directives
