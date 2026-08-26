#!/usr/bin/env bash
set -Eeuo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_root="${SCENICOPS_VENV:-${HOME}/.virtualenvs/scenicops}"
python="${venv_root}/bin/python"

if [[ ! -x "${python}" ]]; then
    echo "Virtual environment not found. Run: bash scripts/bootstrap.sh" >&2
    exit 1
fi

cd "${project_root}"
"${python}" -m ruff check .
"${python}" -m ruff format --check .
"${python}" -m mypy src
"${python}" -m pytest

