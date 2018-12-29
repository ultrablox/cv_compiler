#!/bin/bash
# set -x

SCRIPTPATH=${BASH_SOURCE%/*}
ROOT_DIR=$(realpath $SCRIPTPATH/../)
DOCKER_USER="$(id -u):$(id -g)"
# TMP_DIR=tmp
LOCAL_DIR=$(realpath tmp_local)
CACHE_DIR=$(realpath tmp_cache)
TMP_DIR=$(realpath tmp_tmp)
DOCKER_IMAGE="ultrablox/latex-python3.6"

OUT_DIR=$(realpath $ROOT_DIR/out)

if [ -z $INPUT_DIR] ;
then
    INPUT_DIR=$(realpath $ROOT_DIR/sample_input)
else
    INPUT_DIR=$(realpath $INPUT_DIR)
fi

mkdir -p $LOCAL_DIR
mkdir -p $CACHE_DIR
mkdir -p $TMP_DIR
mkdir -p $OUT_DIR

build_docker_image () {
  docker build -t $DOCKER_IMAGE ../docker
}

docker pull $DOCKER_IMAGE || build_docker_image

docker run -u $DOCKER_USER --rm -v $ROOT_DIR:/repo -v $LOCAL_DIR:/.local -v $CACHE_DIR:/.cache -v $TMP_DIR:/.tmp -v $INPUT_DIR:/input -v $OUT_DIR:/out -w /repo $DOCKER_IMAGE bash -c "\
    pip3 install --user -r requirements.txt ;
    cd scripts;
    ./compile.py --tmp_dir=/.tmp --input_dir=/input --out_dir=/out
    "
    
rm -rf $LOCAL_DIR
rm -rf $CACHE_DIR
rm -rf $TMP_DIR

