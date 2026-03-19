## Why

Project type plugins (set-project-base, set-project-web) provide verification rules and orchestration directives, but there's no way for companies or projects to customize them without forking the package. Companies need to add their own rules, disable irrelevant ones, and override configs — all without their specifics leaking into the public repos. Additionally, lessons learned from running rules in production (false positives, missing excludes) need a structured, anonymized way to feed back into the upstream packages.

## What Changes

- **ProjectTypeResolver** in set-project-base: merges package-provided rules/directives with a local YAML overlay (`set/plugins/project-type.yaml`), supporting `custom_rules`, `disabled_rules`, `rule_overrides`, `custom_directives`, `disabled_directives`
- **Extended YAML schema** for `set/plugins/project-type.yaml`: adds customization sections below the managed header
- **Feedback system** in set-project-base: structured lesson format (rule_id-based, anonymized) with `feedback export` CLI command that produces shareable, company-name-free YAML
- **CLI extensions**: `set-project-base resolve` to show merged final ruleset, `set-project-base feedback export` to generate anonymized feedback
- **set-core integration**: consumers (opsx:verify, sentinel) call resolver instead of reading package rules directly

## Capabilities

### New Capabilities
- `rule-resolver`: YAML overlay engine that merges package rules with local customizations (custom, disabled, overrides)
- `feedback-loop`: Structured anonymized lesson collection and export for feeding improvements back to upstream packages

### Modified Capabilities

## Impact

- **set-project-base**: new modules `resolver.py`, `feedback.py`; CLI additions
- **set-project-web**: test project — validates resolver with WebProjectType + overlay
- **set-core**: `wt-project init` generates extended YAML; future: opsx:verify and sentinel use resolver
- **set/plugins/project-type.yaml**: format extends with customization sections (backward compatible — existing files work unchanged)
