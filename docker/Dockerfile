FROM ubuntu:latest
RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends texlive-fonts-recommended texlive-latex-extra texlive-fonts-extra dvipng texlive-latex-recommended texlive-xetex librsvg2-bin lmodern inkscape zip python3
RUN apt-get install -yq python3-pip
RUN pip3 install --upgrade pip
RUN apt-get -y install libcairo2-dev apt-utils pkg-config
RUN DEBIAN_FRONTEND=noninteractive apt-get -yq install ttf-mscorefonts-installer
RUN fc-cache
RUN fc-match Narrow
RUN apt-cache search texlive-fonts-
#RUN tlmgr install paracol