#!/bin/bash
set -euo pipefail

list="$(brew list)"
readonly list

if ! grep pipenv <<<"$list"; then
    brew install pipenv
fi

if ! grep pyenv <<<"$list"; then
    brew install pyenv
fi

declare -r SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"

pipenv sync
pipenv clean

# exec ansible localhost -m include_role -a name=workstation "$@"
exec pipenv run ansible-playbook ./play.yml "$@"
