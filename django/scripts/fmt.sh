#!/bin/sh
set -x
path=${1:-.}

isort -rc ${path}

black ${path}
