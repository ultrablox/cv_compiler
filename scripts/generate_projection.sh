#!/usr/bin/env bash

INPUT_DIR=../../my_cv/data
./analyse.py ../test_data/vacancy_1.txt $INPUT_DIR
cp -R $INPUT_DIR/img ./profile.analysed/
NEW_CMD="INPUT_DIR=./profile.analysed ./generate.sh"
echo "Running compiler with: $NEW_CMD"
echo "(rerun after changes)"
eval $NEW_CMD
