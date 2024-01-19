project_dir := .

lint:
	@black --check --diff $(project_dir)
	@ruff $(project_dir)
	@mypy --strict $(project_dir)

reformat:
	@black $(project_dir)
	@ruff --fix $(project_dir)


.PHONY: lint, reformat