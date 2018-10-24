#!/bin/bash
set -x

rm -rf test/ bundle.zip input
ln -s $1 input
zip -q -r bundle.zip img styles input
cd src && zip -r -q ../bundle.zip ./* && cd ..
cd styles && zip -r -q ../bundle.zip ./* && cd ..
rm -f input
mkdir test && unzip -q -d test/ bundle.zip
cd test
./main.py || exit
mkdir svg_img 
svgs=$(ls img/*.svg)

for fn in $(ls img/*.svg); do
    fname=$(basename $fn)
    fbname=${fname%.*}
    svg2pdf $fn svg_img/$fbname.pdf
done

# exit 1
 # 
xelatex main.tex 
cp main.pdf ../
