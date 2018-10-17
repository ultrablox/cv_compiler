#!/bin/bash

rm -rf test/
zip -q -r data.zip *
mkdir test && unzip -q -d test/ data.zip
cd test
./main.py || exit
xelatex main.tex