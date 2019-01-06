#!/usr/bin/env bash
#
# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)
#

DOCKER_IMAGE="ultrablox/latex-python3.6"
docker pull $DOCKER_IMAGE || docker build -t $DOCKER_IMAGE ../docker

mkdir -p .local .cache

SCRIPTPATH=${BASH_SOURCE%/*}
ROOT_DIR=$(realpath $SCRIPTPATH/../)

if [ -z $INPUT_DIR ] ;
then
    INPUT_DIR=$ROOT_DIR/sample_input
fi

DOCKER_USER="$(id -u):$(id -g)"
docker run -u $DOCKER_USER --rm -v $ROOT_DIR:/repo -v $(realpath .local):/.local -v $(realpath .cache):/.cache -v $(realpath $INPUT_DIR):/input -w /repo $DOCKER_IMAGE bash -c "\
    pip3 install --user -r requirements.txt ;
    cd scripts;
    ./compile.py --input_dir=/input ${@:1}
    "
