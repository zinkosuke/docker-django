#!/bin/sh
path=${1:-.}
set -x
isort ${path}
black ${path}
