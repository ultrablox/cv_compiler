# [<img src="docs/assets/img/logo.png?raw=true" height="64"/>]() cv_compiler

![Price](https://img.shields.io/badge/price-FREE-0098f7.svg)
![suitable](https://img.shields.io/badge/CV-software_engineer-green.svg)
![suitable](https://img.shields.io/badge/CV-software_developer-green.svg)

## Table of contents

- [Demo](#demo)
- [Quick start](#quick-start)
- [Writing Custom Journal](#writing-custom-journal)
- [Technologies](#technologies)

## Demo

[<img src="docs/assets/img/cv_preview_0.png?raw=true" width="384" />](out/bruce_wayne_CV.pdf)
[<img src="docs/assets/img/cv_preview_1.png?raw=true" width="384" />](out/bruce_wayne_CV.pdf)

## Quick Start

1. **Install** [GIT LFS](https://help.github.com/articles/installing-git-large-file-storage/) or make sure it is already installed.

2. **Clone** current repository.

```bash
git clone https://github.com/ultrablox/cv_compiler.git
```

3. **Install docker** according to [official instruction](https://docs.docker.com/install) and make sure service is running.

4. **Compile Sample CV**, which journal is in *cv_compiler/sample_input*.

```bash
cd cv_compiler/scripts
./generate.sh
```
5. **Find** compiled CV in pdf at:
```bash
> ls cv_compiler/out
bruce_wayne_CV.pdf
```

## Writing Custom Journal

**Write Exprience Journal** with following structure: 

```
journal_dir
│-- data.json
│-- lead.txt
│-- sci_publications.bib
│-- pop_publications.bib
│
└───img
│   │-- project_logo1.png
│   │-- company_logo2.svg
│   │-- ...
```

For the reference look to the [default example](sample_input).

**Compile Sample CV**, providing it path to the *journal_dir* folder:

```bash
cd cv_compiler/scripts
INPUT_DIR=$HOME/Documents/journal_dir ./generate.sh
```

## Technologies

[<img src="docs/assets/img/latex.png?raw=true" height="64" />](https://www.latex-project.org)
[<img src="docs/assets/img/python.png?raw=true" height="64" />](https://www.python.org)
[<img src="docs/assets/img/docker.png?raw=true" height="64" />](https://www.docker.com)

## Aims

This is automatic generator of typical Software Engineer CV. Read more at pages.

## Prerequistes

Install docker, compilation is performed inside the container.

## Usage

Create directory with like in example (sample_input).


After that you will find compiled CV at out/your_name_cv.pdf.

## For developers

If you want to improve it, create pull request with appropriate description - I will approve it. 