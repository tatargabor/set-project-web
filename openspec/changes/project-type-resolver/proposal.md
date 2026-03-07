## Why

Project type plugins (wt-project-base, wt-project-web) provide verification rules and orchestration directives, but there's no way for companies or projects to customize them without forking the package. Companies need to add their own rules, disable irrelevant ones, and override configs — all without their specifics leaking into the public repos. Additionally, lessons learned from running rules in production (false positives, missing excludes) need a structured, anonymized way to feed back into the upstream packages.

## What Changes

- **ProjectTypeResolver** in wt-project-base: merges package-provided rules/directives with a local YAML overlay (`wt/plugins/project-type.yaml`), supporting `custom_rules`, `disabled_rules`, `rule_overrides`, `custom_directives`, `disabled_directives`
- **Extended YAML schema** for `wt/plugins/project-type.yaml`: adds customization sections below the managed header
- **Feedback system** in wt-project-base: structured lesson format (rule_id-based, anonymized) with `feedback export` CLI command that produces shareable, company-name-free YAML
- **CLI extensions**: `wt-project-base resolve` to show merged final ruleset, `wt-project-base feedback export` to generate anonymized feedback
- **wt-tools integration**: consumers (opsx:verify, sentinel) call resolver instead of reading package rules directly

## Capabilities

### New Capabilities
- `rule-resolver`: YAML overlay engine that merges package rules with local customizations (custom, disabled, overrides)
- `feedback-loop`: Structured anonymized lesson collection and export for feeding improvements back to upstream packages

### Modified Capabilities

## Impact

- **wt-project-base**: new modules `resolver.py`, `feedback.py`; CLI additions
- **wt-project-web**: test project — validates resolver with WebProjectType + overlay
- **wt-tools**: `wt-project init` generates extended YAML; future: opsx:verify and sentinel use resolver
- **wt/plugins/project-type.yaml**: format extends with customization sections (backward compatible — existing files work unchanged)
