## 1. Parent Chain Resolution (set-project-base)

- [ ] 1.1 Add `resolve_parent_chain(project_type)` function to `deploy.py` — walks `parent` links via entry points, returns ordered list `[root_ancestor, ..., leaf_type]` with their resolved template dirs
- [ ] 1.2 Handle missing parent gracefully — warn and continue with just the requested type
- [ ] 1.3 Each ancestor auto-resolves its own template (single template → auto-select, multiple → use default)

## 2. Inherited Deploy Logic (set-project-base)

- [ ] 2.1 Add `deploy_with_inheritance()` function that iterates the parent chain and calls `deploy_templates()` for each ancestor in parent-first order
- [ ] 2.2 Child files override parent files — track deployed paths, skip parent file if child will deploy same path
- [ ] 2.3 Merge module availability across all ancestors — collect `{module_id: {source_type, description, files, template_dir}}` from each ancestor's manifest
- [ ] 2.4 Route module file deployment to the correct ancestor's template directory based on source
- [ ] 2.5 Add `--update` flag to `deploy-templates` CLI command — enables managed-file update mode

## 3. Managed-File Headers (set-project-base)

- [ ] 3.1 Add `_add_managed_header(content, rel_path, type_name, template_id)` — prepends `<!-- wt-managed: type/template -->` for `.md` files, `# wt-managed: type/template` for `.yaml`/`.yml` files
- [ ] 3.2 Add `_is_managed_file(target_path)` — checks if first line(s) contain `wt-managed` marker
- [ ] 3.3 Update `deploy_templates()` file copy logic — add managed header when deploying new files
- [ ] 3.4 Update `deploy_templates()` skip logic — when target exists: if managed → overwrite (update mode), if not managed → skip (user-owned)
- [ ] 3.5 On first init (no `--update`), deploy all with headers, skip existing (current behavior + headers)

## 4. Bash CLI Integration (set-core)

- [ ] 4.1 Update `_deploy_project_templates()` to pass `--update` flag on re-init (project already registered)
- [ ] 4.2 Update module prompt to show source type: `data-privacy (base) — description`
- [ ] 4.3 Update `_list_available_modules()` to return merged modules from full parent chain (call new Python API)

## 5. Verification

- [ ] 5.1 Test: init with web/nextjs deploys both base core + web core files
- [ ] 5.2 Test: project-knowledge.yaml from web/nextjs overrides base version (child wins)
- [ ] 5.3 Test: module prompt shows both base and web modules with source labels
- [ ] 5.4 Test: selecting base module `data-privacy` deploys from base template dir
- [ ] 5.5 Test: deployed files have `wt-managed` header
- [ ] 5.6 Test: re-init updates managed files, skips user-owned files
- [ ] 5.7 Test: removing managed header from file → re-init skips it
- [ ] 5.8 Test: base-only init (no parent) works as before (backward compat)
