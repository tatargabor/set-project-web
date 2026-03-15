"""Web project type plugin for wt-tools."""

import json
import subprocess
from pathlib import Path
from typing import List, Optional

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
            version="0.2.0",
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
            VerificationRule(
                id="page-metadata",
                description="Public pages must export metadata or generateMetadata for SEO",
                check="file-mentions",
                severity="warning",
                config={
                    "source": {
                        "pattern": "src/app/**/page.tsx",
                        "exclude": [
                            "src/app/api/**",
                            "src/app/**/admin/**",
                            "src/app/**/account/**",
                        ],
                    },
                    "mentions": ["metadata", "generateMetadata"],
                },
            ),
            VerificationRule(
                id="image-alt-text",
                description="Images must have alt text for accessibility",
                check="pattern-absence",
                severity="warning",
                config={
                    "pattern": "src/**/*.tsx",
                    "forbidden": r'<(?:img|Image)\s+(?:(?!alt)[a-zA-Z]+=)[^>]*/>',
                },
            ),
            VerificationRule(
                id="env-example-sync",
                description="New env vars must be documented in .env.example",
                check="cross-reference",
                severity="warning",
                config={
                    "groups": [
                        {
                            "name": "env-vars",
                            "files": [
                                {"role": "usage", "pattern": "src/**/*.{ts,tsx}"},
                                {"role": "definition", "file": ".env.example"},
                            ],
                            "key_pattern": "process.env.",
                        }
                    ]
                },
            ),
            VerificationRule(
                id="error-boundary-exists",
                description="App must have root error.tsx, global-error.tsx, and not-found.tsx",
                check="file-mentions",
                severity="warning",
                config={
                    "required_files": [
                        "src/app/error.tsx",
                        "src/app/global-error.tsx",
                        "src/app/not-found.tsx",
                    ],
                },
            ),
            VerificationRule(
                id="no-public-secrets",
                description="NEXT_PUBLIC_ prefix must not be used for secret-like env vars",
                check="pattern-absence",
                severity="error",
                config={
                    "pattern": "src/**/*.{ts,tsx}",
                    "forbidden": r"NEXT_PUBLIC_(?:SECRET|KEY|PASSWORD|TOKEN|API_KEY|PRIVATE)",
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
            OrchestrationDirective(
                id="db-seed",
                description="Re-seed database after schema changes to keep test data current",
                trigger='change-modifies("prisma/schema.prisma")',
                action="post-merge",
                config={"command": "pnpm db:seed", "after": "db-generate"},
            ),
            OrchestrationDirective(
                id="env-example-review",
                description="Flag changes that add new env vars for .env.example review",
                trigger="change-modifies-any(cross_cutting_files.env_config)",
                action="flag-for-review",
            ),
        ]
        return base_directives + web_directives

    # --- Profile methods (engine integration) ---

    def planning_rules(self) -> str:
        rules_file = Path(__file__).parent / "planning_rules.txt"
        if rules_file.is_file():
            return rules_file.read_text()
        return ""

    def security_rules_paths(self, project_path: str) -> List[Path]:
        rules_dir = Path(project_path) / ".claude" / "rules"
        paths = []
        for pattern in ("security*.md", "auth*.md", "api-design*.md"):
            paths.extend(rules_dir.glob(pattern))
        if not paths:
            template_rules = Path(__file__).parent / "templates" / "nextjs" / "rules"
            for name in ("security.md", "auth-conventions.md"):
                p = template_rules / name
                if p.is_file():
                    paths.append(p)
        return paths

    def security_checklist(self) -> str:
        return (
            "- [ ] Data mutations by client-provided ID include ownership/authorization check\n"
            "- [ ] Protected resources enforce auth before the handler runs (middleware, not handler-level)\n"
            "- [ ] Public-facing inputs are validated at the boundary (type, range, size)\n"
            "- [ ] Multi-user queries are scoped by the owning entity\n"
            "- [ ] No `dangerouslySetInnerHTML` or `v-html` with user-supplied content"
        )

    def generated_file_patterns(self) -> List[str]:
        return [
            "tsconfig.tsbuildinfo", "*.tsbuildinfo",
            "next-env.d.ts",
            "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
            ".next/**", "dist/**", "build/**",
        ]

    def lockfile_pm_map(self) -> list:
        return [
            ("pnpm-lock.yaml", "pnpm"),
            ("yarn.lock", "yarn"),
            ("bun.lockb", "bun"),
            ("bun.lock", "bun"),
            ("package-lock.json", "npm"),
        ]

    def detect_test_command(self, project_path: str) -> Optional[str]:
        pkg_json = Path(project_path) / "package.json"
        if not pkg_json.is_file():
            return None
        pm = self.detect_package_manager(project_path) or "npm"
        try:
            data = json.loads(pkg_json.read_text())
            scripts = data.get("scripts", {})
            for candidate in ("test", "test:unit", "test:ci"):
                if scripts.get(candidate):
                    return f"{pm} run {candidate}"
        except (json.JSONDecodeError, OSError):
            pass
        return None

    def detect_build_command(self, project_path: str) -> Optional[str]:
        pkg_json = Path(project_path) / "package.json"
        if not pkg_json.is_file():
            return None
        pm = self.detect_package_manager(project_path) or "npm"
        try:
            data = json.loads(pkg_json.read_text())
            scripts = data.get("scripts", {})
            for candidate in ("build:ci", "build"):
                if scripts.get(candidate):
                    return f"{pm} run {candidate}"
        except (json.JSONDecodeError, OSError):
            pass
        return None

    def detect_dev_server(self, project_path: str) -> Optional[str]:
        pkg_json = Path(project_path) / "package.json"
        if not pkg_json.is_file():
            return None
        pm = self.detect_package_manager(project_path) or "npm"
        try:
            data = json.loads(pkg_json.read_text())
            if data.get("scripts", {}).get("dev"):
                return f"{pm} run dev"
        except (json.JSONDecodeError, OSError):
            pass
        return None

    def bootstrap_worktree(self, project_path: str, wt_path: str) -> bool:
        pkg_json = Path(wt_path) / "package.json"
        node_modules = Path(wt_path) / "node_modules"
        if not pkg_json.is_file() or node_modules.is_dir():
            return True
        pm = self.detect_package_manager(wt_path)
        if not pm:
            return True
        result = subprocess.run(
            [pm, "install", "--frozen-lockfile"],
            cwd=wt_path, capture_output=True, timeout=120,
        )
        if result.returncode != 0:
            subprocess.run(
                [pm, "install"],
                cwd=wt_path, capture_output=True, timeout=120,
            )
        return True

    def post_merge_install(self, project_path: str) -> bool:
        pm = self.detect_package_manager(project_path)
        if not pm:
            return True
        result = subprocess.run(
            [pm, "install"],
            cwd=project_path, capture_output=True, timeout=300,
        )
        return result.returncode == 0

    def ignore_patterns(self) -> List[str]:
        return ["node_modules", ".next", "dist", "build", ".turbo"]
