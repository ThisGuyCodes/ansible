#!/bin/bash
set -euo pipefail

declare -r SCRIPT_DIR=$( cd -- "$(dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
cd "$SCRIPT_DIR"

# exec ansible localhost -m include_role -a name=workstation "$@"
exec pipenv run ansible-playbook ./play.yml "$@"
