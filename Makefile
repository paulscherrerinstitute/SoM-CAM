ENVNAME := SoM-CAM

.ONESHELL:
ENV_PREFIX=$(conda info | grep -i ${ENVNAME} | awk '{print $5}')
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@if [ "$(USING_POETRY)" ]; then poetry env info && exit; fi
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort som_cam/
	$(ENV_PREFIX)black -l 79 som_cam/
	$(ENV_PREFIX)black -l 79 tests/

.PHONY: lint
lint:			## Run pep8, black, mypy linters.
	$(ENV_PREFIX)python -m pip install types-paramiko
	$(ENV_PREFIX)flake8 som_cam/
	$(ENV_PREFIX)black -l 79 --check som_cam/
	$(ENV_PREFIX)black -l 79 --check tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports som_cam/
	$(ENV_PREFIX)mypy --install-type

.PHONY: pretty
pretty: 
	$(ENV_PREFIX)black .

.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=som_cam -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

check-condaenv-inactive:
	( \
		echo "checking for conda environment $(ENVNAME) ... " && \
		[[ "${CONDA_DEFAULT_ENV}" != "$(ENVNAME)" ]] && \
		echo "conda environment $(ENVNAME) is NOT active (OK)" && \
		exit 0 \
	) || ( \
		echo "conda environment $(ENVNAME) is ACTIVE (FAIL)\ntry: conda deactivate" >&2 && \
		exit 1 \
	)


check-condaenv-active:
	( \
		echo "checking for conda environment $(ENVNAME) ... " && \
		[[ "${CONDA_DEFAULT_ENV}" == "$(ENVNAME)" ]] && \
		echo "conda environment $(ENVNAME) is ACTIVE (OK)" && \
		exit 0 \
	) || ( \
		echo "conda environment $(ENVNAME) is NOT active (FAIL)\ntry: conda activate $(ENVNAME)" >&2 && \
		exit 1 \
	)

.PHONY: condapackage # Create the conda package
condapackage: 
	conda build \
		--no-anaconda-upload \
		./conda-recipe 

.PHONY: release
release:          ## Create a new tag for release.
	@echo "WARNING: This operation will create s version tag and push to github"
	@read -p "Version? (provide the next x.y.z semver) : " TAG
	@echo "$${TAG}" > som_cam/VERSION
	@$(ENV_PREFIX)gitchangelog > HISTORY.md
	@git add som_cam/VERSION HISTORY.md
	@git commit -m "release: version $${TAG} 🚀"
	@echo "creating git tag : $${TAG}"
	@git tag $${TAG}
	@git push -u origin HEAD --tags
	@echo "Github Actions will detect the new tag and release the new version."

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL



.PHONY: install
install:          ## Install the project in dev mode.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "Don't forget to run 'make virtualenv' if you got errors."
	$(ENV_PREFIX)pip install -e .[test]