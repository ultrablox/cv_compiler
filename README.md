# [<img src="docs/assets/img/logo.png?raw=true" height="64"/>]() cv_compiler

![Price](https://img.shields.io/badge/code-opensource-green.svg)
![Price](https://img.shields.io/badge/price-FREE-0098f7.svg)
![suitable](https://img.shields.io/badge/CV-software_engineer-green.svg)
![suitable](https://img.shields.io/badge/CV-software_developer-green.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Table of contents

- [Aims](#aims)
- [Demo](#demo)
- [Quick start](#quick-start)
- [Writing Your Journal](#writing-your-journal)
  - [Directory Structure](#directory-Structure)
  - [Structure](#structure)
  - [Compiling](#compiling)
- [Technologies](#technologies)
- [Feedback](#feedback)
- [Credit the Author](#credit-the-author)

## Aims

This is automatic compiler of your **working experience journal** into standardized CV for Software Engineer and related positions. 

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

## Writing Your Journal

### Directory Structure

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

### Structure

Journal (*journal_dir/data.json'*) is written in JSON with a few sections:

```json
{
  "personal" : {
      "..."
  },
  "contacts" : {
      "..."
  },
  "education" : [
      "..."
  ],
  "skills" : {
    "..."
  },
  "special_skills" : [
      "..."
  ],
  "projects" : [
    "..."
  ],
  "employments" :[
      "..."
  ],
  "conferences" : [
      "..."
  ],
  "traits" : [
      "..."
  ]   
}
```

#### Contacts

```json
{
  "email" : "bruce@gmail.com",
  "skype" : "bruce",
  "phone" : "06-12345678",
  "residence" : "Endhoven, Netherlands",
  "linkedin" : "https://www.linkedin.com/in/yuri-blokhin-01688a78/",
  "languages" : [
      "English (advanced)",
      "Chineese (native)",
      "German (basic)"
  ]
}
```


#### Skills

Here you can add special data about referencing further skills - it's full name and your attitude (when you like mentioned technology, or don't want to use it anymore). 

```json
"ML" : {
    "attitude" : "negative",
    "full_name" : "Machine Learning"
}
```

#### Projects

This is basic unit of your experience. State here the projects you weere involved in, skills that you gained and tasks with your achievments. Show that you really did something.

```json
{
  "name" : "Photoshop",
  "icon" : "photoshop_project.png",
  "period" : "01.09.2015-30.08.2016",
  "description" : "Raster graphics editor",
  "team-size" : "9",
  "web" : "https://www.adobe.com/products/photoshop.html",
  "tasks" : [
    "..."
  ]
}
```

I strongly recomment to include project logo into each project. Tasks that you did within the project must contain period, skills and achievments.

```json
{
  "description" : "Development of text-recognition filter from raw image",
  "period" : "01.09.2015-28.02.2016",
  "skills" : ["CI", "C++", "ML"],
  "achievements" : [
    "achievied recognition accuracy up to 85%"
  ]
}
```

#### Employments

This is a list of your work history. If you worked in well-reccognised company - I strongly recomment to include company logo into the records.

```json
{
    "name" : "Google Inc",
    "logo" : "img/logo_google.png",
    "description" : "search engine",
    "role" : "Software Engineer",
    "location" : "Zurich, SZ",
    "period" : "01.09.2016-30.08.2017",
    "web" : "https://www.google.com",
    "projects" : ["Google Drive"]
}
```

Make also references to the projects that you worked on in this company.

### Compiling

**Compile Sample CV**, providing it path to the *journal_dir* folder:

```bash
cd cv_compiler/scripts
INPUT_DIR=$HOME/Documents/journal_dir ./generate.sh
```

## Projecting (experimental)

In order to create CV projection for exact vacncy:

```bash
cd cv_compiler/scripts
INPUT_DIR=../sample_input ./generate_projection.sh test_data/vacancy_1.txt
```

## Technologies

[<img src="docs/assets/img/latex.png?raw=true" height="64" />](https://www.latex-project.org)
[<img src="docs/assets/img/python.png?raw=true" height="64" />](https://www.python.org)
[<img src="docs/assets/img/docker.png?raw=true" height="64" />](https://www.docker.com)

## Feedback

I appreciate any form of feedback, that helps me improve the project. You can do it in form of **Pull Requests** or **Issues**.

## Credit the Author

If you like the project, and want to credit the author - leave the QR with link to this page in your CV - so more people can know about it. If for some reasons you want to get rid of the QR, use *--no-watermark* parameter:

```bash
./generate.sh --no-watermark
```
