#!/bin/bash

############################################################################
# Create a venv and install workspace dependencies.
# Usage: ./scripts/install.sh
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname $CURR_DIR)"
VENV_DIR="${REPO_ROOT}/.venv"
source ${CURR_DIR}/_utils.sh

print_heading "Development setup..."

print_heading "Removing virtual env"
print_info "rm -rf ${VENV_DIR}"
rm -rf ${VENV_DIR}

print_heading "Creating virtual env"
print_info "VIRTUAL_ENV=${VENV_DIR} uv venv --python 3.12"
VIRTUAL_ENV=${VENV_DIR} uv venv --python 3.12

print_heading "Installing requirements"
print_info "VIRTUAL_ENV=${VENV_DIR} uv pip install -r ${REPO_ROOT}/requirements.txt"
VIRTUAL_ENV=${VENV_DIR} uv pip install -r ${REPO_ROOT}/requirements.txt

print_heading "Installing workspace in editable mode with dev dependencies"
print_info "VIRTUAL_ENV=${VENV_DIR} uv pip install -e ${REPO_ROOT}"
VIRTUAL_ENV=${VENV_DIR} uv pip install -e ${REPO_ROOT}

print_heading "Development setup complete"
print_heading "Activate venv using: source .venv/bin/activate"

