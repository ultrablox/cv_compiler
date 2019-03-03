#!/usr/bin/env python3

# Copyright: (c) 2018, Yury Blokhin ultrablox@gmail.com
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)


from utils import *


def main():
  #call_system('cd ..; copyright-header --add-path scripts/ --output-dir ./ --license-file copyright_header.txt --guess-extension')
  call_system('./generate.sh --paper_size=a5 ')
  call_system('convert -density 300 -background white -alpha remove -bordercolor black -border 2x2 ../out/bruce_wayne_CV.pdf ../docs/assets/img/cv_preview_%d.png')

if __name__ == "__main__":
    main()
