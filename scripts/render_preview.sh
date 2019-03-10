#!/usr/bin/env bash

set -e
set -x

#copyright-header --add-path scripts/ --output-dir ./ --license-file copyright_header.txt --guess-extension
scripts/generate.sh
convert -density 300 -background white -alpha remove -bordercolor black -border 2x2 out/bruce_wayne_CV.pdf docs/assets/img/cv_preview_%d.png

src/visualize_skills.py
convert -density 300 -background white -alpha remove -bordercolor black -border 2x2 skills.pdf docs/assets/img/skills_onthology.png