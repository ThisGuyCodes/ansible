#!/bin/bash
set -euo pipefail

if ! brew list | grep pipenv; then
    brew install pipenv pyenv
fi

declare -r SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"

pipenv sync
pipenv clean

# exec ansible localhost -m include_role -a name=workstation "$@"
exec pipenv run ansible-playbook ./play.yml "$@"
