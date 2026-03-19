## 1. Manifest Format & Template Updates

- [x] 1.1 Create `manifest.yaml` for the nextjs template — categorize existing rules as core, move `data-privacy.md` and `integrations.md` to optional modules
- [x] 1.2 Create `manifest.yaml` for the spa template (all files as core, no optional modules yet)
- [x] 1.3 Create `manifest.yaml` for the base/default template — `data-privacy.md` as optional module

## 2. Deploy Logic Updates (set-project-base)

- [x] 2.1 Update `deploy_templates()` to detect and parse `manifest.yaml` — if present, build file list from core + selected modules; if absent, walk all files (backward compat)
- [x] 2.2 Add `modules` parameter to `deploy_templates()` function signature
- [x] 2.3 Add `--modules` flag to `deploy-templates` CLI subcommand
- [x] 2.4 When manifest exists and no modules specified, deploy only core and print available optional modules
- [x] 2.5 Validate manifest references — warn on files listed in manifest but missing from template directory

## 3. Bash Init Integration

- [x] 3.1 Add `--modules` flag parsing to `cmd_init` in wt-project bash script
- [x] 3.2 Pass `--modules` to `_deploy_project_templates()` when specified
- [x] 3.3 Interactive module selection: when modules not specified and optional modules exist, prompt user with available modules and accept comma-separated input
- [x] 3.4 Save selected modules to `set/plugins/project-type.yaml` under `modules` key
- [x] 3.5 On re-init, read tracked modules from `project-type.yaml` and pass to deploy (skip prompt)
- [x] 3.6 Update `_save_project_type()` to include `template` and `modules` fields

## 4. Harvest Skill

- [x] 4.1 Create `/wt:harvest` skill definition in set-core (`skills/wt/harvest/SKILL.md`)
- [x] 4.2 Skill logic: read source project `.claude/rules/*.md`, diff against template manifest (core + modules), identify new/richer candidates
- [x] 4.3 Skill logic: for each candidate, classify as base/web/skip based on content analysis
- [x] 4.4 Skill logic: generalize candidates — strip project-specific paths, entity names, API references
- [x] 4.5 Skill logic: show summary with original vs generalized, prompt user to approve/edit/skip each
- [x] 4.6 Skill logic: write approved files to template directory and update manifest.yaml with new optional module
- [x] 4.7 Divergence detection — identify template rules that are a subset of source project rules, offer to merge back

## 5. Verification

- [x] 5.1 Test: init with manifest — only core files deployed when no modules specified
- [x] 5.2 Test: init with --modules — core + selected modules deployed
- [x] 5.3 Test: re-init reads tracked modules from project-type.yaml
- [x] 5.4 Test: backward compat — template without manifest deploys all files
- [x] 5.5 Test: harvest skill end-to-end with a mock source project
