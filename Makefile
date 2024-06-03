# keep in sync with: https://github.com/kitconcept/buildout/edit/master/Makefile
# update by running 'make update'
SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

.all: ## Make
	build-plone-6

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Remove old virtualenv and creates a new one
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	rm -rf bin include lib lib64

bin/python bin/pip:
	python3 -m venv .
	bin/pip install --upgrade pip

.PHONY: build-plone-5.2
build-plone-5.2: bin/pip  ## Build Plone 5.2
	bin/pip install Plone Paste -c https://dist.plone.org/release/5.2.7/constraints.txt
	bin/pip install -e ".[test]"

.PHONY: build-plone-6
build-plone-6: bin/pip  ## Build Plone 6
	bin/pip install Plone -c https://dist.plone.org/release/6.0.9/constraints.txt
	bin/pip install plone.app.robotframework==2.1.3
	bin/pip install robotframework==4.1.3
	bin/pip install -e ".[test]"

bin/mkwsgiinstance: build-plone-6
	bin/mkwsgiinstance -d .

.PHONY: instance
instance etc/zope.ini: bin/mkwsgiinstance  ## Create instance
	bin/mkwsgiinstance -d . -u admin:admin

.PHONY: start
start: instance  ## Start instance
	bin/runwsgi -v etc/zope.ini

.PHONY: test
test: bin/zope-testrunner ## Run tests
	bin/zope-testrunner --auto-color --auto-progress --test-path src

.PHONY: black
black:  ## Black
	bin/black src/ setup.py

.PHONY: isort
isort:  ## iSort
	bin/isort src/ setup.py

.PHONY: format
format:  black isort ## Format codebase

.PHONY: Test Release
test-release:  ## Run Pyroma and Check Manifest
	bin/pyroma -n 10 -d .

.PHONY: Release
release:  ## Release
	bin/fullrelease
