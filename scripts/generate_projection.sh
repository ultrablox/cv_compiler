#!/usr/bin/env bash

set -e
set -x

SCRIPT=`realpath $0`
DIRECTORY=`dirname $SCRIPT`
DIRECTORY=$DIRECTORY/..

# VACANCY=../test_data/vacancy.9.txt
VACANCY=$1
INPUT_DIR=$DIRECTORY/../my_cv/data
# INPUT_DIR=../sample_input
OUT_DIR=$DIRECTORY/out


SKILLS_CORRECT_FILE=$VACANCY.skills

if [ ! -f "$SKILLS_CORRECT_FILE" ]; then
  SKILLS_FILE=$OUT_DIR/skills.txt
  $DIRECTORY/src/extract_skills.py $VACANCY > $SKILLS_FILE
else
   SKILLS_FILE=$SKILLS_CORRECT_FILE
fi

$DIRECTORY/src/analyse.py $INPUT_DIR $SKILLS_FILE --min_relevance=0.07
cp -R $INPUT_DIR/img ./profile.analysed/
NEW_CMD="INPUT_DIR=./profile.analysed $DIRECTORY/scripts/generate.sh"
echo "Running compiler with: $NEW_CMD"
echo "(rerun after changes)"
eval $NEW_CMD
