#!/usr/bin/env bash
set -Eeuo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_command="${SCENICOPS_PYTHON:-python3.13}"
venv_root="${SCENICOPS_VENV:-${HOME}/.virtualenvs/scenicops}"
venv_python="${venv_root}/bin/python"

if ! command -v "${python_command}" >/dev/null 2>&1; then
    echo "Python 3.13 was not found. Install the Python.org macOS Universal2 package first." >&2
    exit 1
fi

if [[ ! -x "${venv_python}" ]]; then
    mkdir -p "$(dirname "${venv_root}")"
    "${python_command}" -m venv "${venv_root}"
fi

"${venv_python}" -m pip install --upgrade pip
"${venv_python}" -m pip install -e "${project_root}[dev]"

echo "ScenicOps development environment is ready at ${venv_root}."
echo "Run: bash scripts/check.sh"

