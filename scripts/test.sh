#!/usr/bin/env bash

DOCKER_IMAGE="ultrablox/latex-python3.6"
DOCKER_USER="$(id -u):$(id -g)"
SCRIPTPATH=${BASH_SOURCE%/*}
ROOT_DIR=$(realpath $SCRIPTPATH/../)

mkdir -p .local .cache

docker run -u $DOCKER_USER --rm -v $ROOT_DIR:/repo -v $(realpath .local):/.local -v $(realpath .cache):/.cache -w /repo $DOCKER_IMAGE bash -c "\
    pip3 install --user -r requirements.txt ;
    cd src ;
    python3 -m unittest discover
    "
