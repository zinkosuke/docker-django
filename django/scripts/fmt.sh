#!/bin/sh
path=${1:-.}
set -x
isort -rc ${path}
black ${path}
