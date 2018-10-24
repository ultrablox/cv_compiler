#!/bin/bash

rm -rf test/ bundle.zip input
ln -s $1 input
zip -q -r bundle.zip img styles input
cd src && zip -r -q ../bundle.zip ./* && cd ..
cd styles && zip -r -q ../bundle.zip ./* && cd ..
mkdir test && unzip -q -d test/ bundle.zip
cd test
./main.py || exit
xelatex main.tex
rm -f input