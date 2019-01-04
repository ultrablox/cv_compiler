#!/usr/bin/env python3

from utils import *


def main():
    # call_system('./generate.sh')
    call_system('convert -density 300 -background white -alpha remove ../out/bruce_wayne_CV.pdf ../docs/assets/img/cv_preview_%d.png')

if __name__ == "__main__":
    main()
