## 1. Package Data

- [x] 1.1 Update set-project-web pyproject.toml to include templates/, directives/, and verification-rules/ directories in the wheel (hatch build config)
- [x] 1.2 Verify WebProjectType.get_template_dir("nextjs") returns a valid path with the expected files after editable install (fixed get_template_dir to use subclass module path via inspect.getfile)

## 2. Python Deploy Logic (set-project-base)

- [x] 2.1 Add `deploy_templates()` function in set-project-base that takes a ProjectType, template_id, target_dir, force flag, and dry_run flag — copies template files to target with additive-only logic
- [x] 2.2 Map template paths to target locations: `project-knowledge.yaml` → `wt/knowledge/project-knowledge.yaml` (or project root if wt/knowledge/ doesn't exist), `rules/*.md` → `.claude/rules/*.md`
- [x] 2.3 Add `deploy-templates` subcommand to set-project-base CLI with --project-dir, --type, --template, --force, --dry-run flags
- [x] 2.4 Handle single-template auto-selection and multi-template error with variant listing

## 3. Bash Init Integration (wt-project)

- [x] 3.1 Add `--template` flag parsing to `cmd_init` in wt-project bash script
- [x] 3.2 Add `_deploy_project_templates()` bash function that calls `set-project-base deploy-templates`
- [x] 3.3 Call `_deploy_project_templates` from `cmd_init` after `_save_project_type` when --project-type is specified
- [x] 3.4 When project type has multiple templates and --template not specified, print available variants and skip deploy (handled by Python CLI error message)

## 4. init-knowledge Type Awareness

- [x] 4.1 Update `cmd_init_knowledge` to read `set/plugins/project-type.yaml` and resolve the configured project type
- [x] 4.2 When a project type is found, delegate to `_deploy_project_templates` for the project-knowledge.yaml instead of copying the generic template
- [x] 4.3 Preserve fallback to generic template when no project type is configured

## 5. Verification

- [x] 5.1 Test end-to-end: `wt-project init --project-type web --template nextjs` in a fresh git repo deploys all expected files
- [x] 5.2 Test additive safety: re-run init with same flags, verify no files are overwritten
- [x] 5.3 Test init-knowledge with and without project type configured
