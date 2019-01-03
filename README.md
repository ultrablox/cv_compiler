# [<img src="docs/assets/img/logo.png?raw=true" height="64"/>]() cv_generator

![Price](https://img.shields.io/badge/price-FREE-0098f7.svg)
![suitable](https://img.shields.io/badge/CV-software_engineer-green.svg)
![suitable](https://img.shields.io/badge/CV-software_developer-green.svg)

## Table of contents

<!-- <details>
<summary>Click to expand</summary> -->

- [Quick start](#quick-start)
- [Technologies](#technologies)

<!-- </details> -->

## Demo

[![](out/bruce_wayne_CV.pdf?raw=true)](out/bruce_wayne_CV.pdf?raw=true)

## Quick Start

1. **Clone** current repository.

```bash
git clone https://github.com/ultrablox/cv_compiler.git
```

2. **Write Exprience Journal** with following structure: 

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

3. **Install docker** according to [official instruction](https://docs.docker.com/install) and make sure service is running.

4. **Compile CV**, providing it path to the *journal_dir* folder.

```bash
cd cv_compiler/scripts
INPUT_DIR=$HOME/Documents/journal_dir ./generate.sh
```

5. **Find** compiled CV in pdf at:
```bash
ls cv_compiler/out
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