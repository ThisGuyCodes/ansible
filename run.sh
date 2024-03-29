#!/bin/bash
set -euo pipefail

list="$(brew list)"
readonly list

if ! grep pipenv <<<"$list" &>/dev/null; then
    brew install pipenv pyenv
elif ! grep pyenv <<<"$list" &>/dev/null; then
    brew install pyenv
fi

declare -r SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"

pipenv sync
pipenv clean

# exec ansible localhost -m include_role -a name=workstation "$@"
exec caffeinate -i pipenv run ansible-playbook ./play.yml "$@"
