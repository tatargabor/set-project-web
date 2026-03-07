## 1. ProjectTypeResolver core

- [ ] 1.1 Create `wt_project_base/resolver.py` with `ProjectTypeResolver` class — constructor takes `ProjectType` instance and `overlay_path: Path`
- [ ] 1.2 Implement `_load_overlay()` — parse YAML, extract custom_rules, disabled_rules, rule_overrides, custom_directives, disabled_directives (all optional, default empty)
- [ ] 1.3 Implement `resolve_rules()` — package rules + custom_rules, filter disabled_rules by id, apply rule_overrides (merge config dicts), warn on unknown disabled ids
- [ ] 1.4 Implement `resolve_directives()` — package directives + custom_directives, filter disabled_directives by id
- [ ] 1.5 Implement `summary()` — return dict with counts: total, from_package, custom, disabled, overridden for both rules and directives

## 2. Local overrides layer

- [ ] 2.1 Extend resolver to check for `.local-overrides.yaml` in same directory as overlay — apply as final layer after project-type.yaml
- [ ] 2.2 Add `.local-overrides.yaml` to default .gitignore template in wt-project-base

## 3. Feedback system

- [ ] 3.1 Create `wt_project_base/feedback.py` with `FeedbackLesson` dataclass — fields: rule_id, issue (enum), context, suggested_fix (type + value), timestamp
- [ ] 3.2 Define issue enum: false_positive, too_aggressive, missing_exclude, missing_rule, config_improvement
- [ ] 3.3 Implement `FeedbackStore` — load/append/save lessons from `wt/knowledge/lessons/rule-feedback.yaml`
- [ ] 3.4 Implement `validate_lesson()` — check required fields, validate issue enum, warn if context contains path-like strings
- [ ] 3.5 Implement `export_lessons()` — read all lessons, validate, output clean YAML with header comment, warn on potentially identifying content

## 4. CLI extensions

- [ ] 4.1 Add `resolve` subcommand to `wt_project_base/cli.py` — accepts `--project-dir`, loads project type from `wt/plugins/project-type.yaml` type field via entry points, runs resolver, prints annotated rules and directives
- [ ] 4.2 Add `feedback record` subcommand — non-interactive mode with `--rule-id`, `--issue`, `--context`, `--fix-type`, `--fix-value` flags
- [ ] 4.3 Add `feedback export` subcommand — reads lessons, validates, prints anonymized YAML

## 5. YAML schema update

- [ ] 5.1 Update `_save_project_type()` in wt-tools `bin/wt-project` to generate extended YAML with commented-out custom sections as documentation
- [ ] 5.2 Add YAML format documentation as comments in the generated file

## 6. Testing with wt-project-web

- [ ] 6.1 Create a test overlay YAML in wt-project-web's `wt/plugins/project-type.yaml` with custom_rules, disabled_rules, and rule_overrides
- [ ] 6.2 Run `wt-project-base resolve --project-dir /home/tg/code2/wt-project-web` and verify merged output
- [ ] 6.3 Record a test feedback lesson and verify export format
- [ ] 6.4 Verify backward compat — run resolver on sales-raketa's existing project-type.yaml (no custom sections)
