#!/usr/bin/env bash

set -e
set -x

VACANCY=../test_data/vacancy.7.txt
INPUT_DIR=../../my_cv/data
# INPUT_DIR=../sample_input
OUT_DIR=../out


./extract_skills.py $VACANCY > $OUT_DIR/skills.txt
./analyse.py $INPUT_DIR $OUT_DIR/skills.txt
cp -R $INPUT_DIR/img ./profile.analysed/
NEW_CMD="INPUT_DIR=./profile.analysed ./generate.sh"
echo "Running compiler with: $NEW_CMD"
echo "(rerun after changes)"
eval $NEW_CMD
