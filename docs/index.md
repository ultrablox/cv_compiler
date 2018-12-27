---
layout: default
---

# What is it

You are tired of constant updating your CV? Every time you get better idea how to do it and you have to recall all your past experience?

Forget about that. Just add your new experience into JSON, and generator will highlight the most relevant and decrease attention to obsolete records.

# How to use

## Input

You need to create a directory with following structure:

```
input_dir
│-- data.json
│-- lead.txt
│-- publications.bib
│
└───img
│   │-- icon1.png
│   │-- icon2.svg
│   │-- ...
```

For more information look to the example (/sample_input).

## Compiling

Compilation is performed with use of docker virtualisation. First you need to clone the source repo:

```
git clone https://github.com/ultrablox/cv_generator.git
cd cv_generator
```

Then create data directory and run the compiler:

```
export INPUT_DIR=~/my_cv/
cd scripts
./generate.sh
```

You will find comopiled CV in cv_generator/out/.
