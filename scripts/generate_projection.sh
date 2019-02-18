#!/usr/bin/env bash

set -e
set -x

# VACANCY=../test_data/vacancy.9.txt
VACANCY=$1
INPUT_DIR=../../my_cv/data
# INPUT_DIR=../sample_input
OUT_DIR=../out


SKILLS_CORRECT_FILE=$VACANCY.skills

if [ ! -f "$SKILLS_CORRECT_FILE" ]; then
  SKILLS_FILE=$OUT_DIR/skills.txt
  ./extract_skills.py $VACANCY > $SKILLS_FILE
else
   SKILLS_FILE=$SKILLS_CORRECT_FILE
fi

./analyse.py $INPUT_DIR $SKILLS_FILE
cp -R $INPUT_DIR/img ./profile.analysed/
NEW_CMD="INPUT_DIR=./profile.analysed ./generate.sh"
echo "Running compiler with: $NEW_CMD"
echo "(rerun after changes)"
eval $NEW_CMD
