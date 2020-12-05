#!/bin/sh
path=${1:-.}
set -x
isort -rc --check-only ${path}
CODE=$((${CODE:-0} + ${?}))
black --check ${path}
CODE=$((${CODE:-0} + ${?}))
flake8 ${path}
CODE=$((${CODE:-0} + ${?}))
mypy ${path}
CODE=$((${CODE:-0} + ${?}))
exit ${CODE}
