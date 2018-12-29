---
layout: default
---

# About

## Do you need it?

You are tired of constant updating your CV? Every time you get better idea how to do it and you have to recall all your past experience?

Forget about that. Just add your new experience into JSON, and generator will highlight the most relevant and decrease attention to obsolete records.

## Origin

The structure is based on my own experience (PhD in AI, Computer Science, 10+ years in industial software development) and also influenced by collegues, friends and other people among software engineers, HRs and technical directors.

## Employer profile

This project is primarilly aimed for 'worker' roles, for the men who really does the development job. That's why there is additional emphasis for technology and languages related skills.

# Structure

## Audience

CV structure is developed and refined for applying to western companies. Basing on the western mentality, this structure must highlight your achievements for the company. So you instead of cold-hearted description of what you did, you should find something unique, that spared lots of money to your employer.

This approach will not work for Asian mentality, and might work for Russia.

## Vacancy adaptation

It is true, that you can't have universal CV for all the vacancies, you need to highlight specific things basing on potential employer requests. I have ideas how to do that, but it is not implemented yet.

## Breif overview

The CV contains of a few sections:

1. Personal and Contact
1. Objective Summary
1. Education
1. Professional Skills
1. Projects
1. Employment History
1. Professional Activities
1. Interests and Personal Traits

The order is refined basing on two principles:
* Personal and Contacts
* If HR read to the Nth section, he will not reject you because of N-1th section.

## Section Details

### Personal and Contacts

This is classical basis - where you are and how can you be contacted. If company does not work with immigrants and you are outside the country - your CV is not interesting. If you do not speak team language - your CV is not interested.

### Objective and Summary

Simly tell what role are you looking for. But tell it as a inspiring unique little story. I believe it can replace cover-letter in most cases. If you skip it completely - HR will not guess if you want a role of developer or a DBMS administrator.

![Summary]({{ site.baseurl }}/assets/img/section_summary.png)

### Education

Netherless rumors that top IT companies say that education is not crucial now, I do not believe it. My creative abilites were inherent, but ability to think and structure were acquired during attaining university technical education.

![Education]({{ site.baseurl }}/assets/img/section_education.png)

### Skills

This section is designed in the way to help HR to filter as quick as possible if you are the right candidate. It is generated completely automated basing on your projects. Vacancies use 'years' gradation - I use the same - let's make life easier for both sides.

![Skills]({{ site.baseurl }}/assets/img/section_skills.png)

Except the last part, where there are 'special skills' that are not software engineering skills, but you still want to highlight it.

I also don't want to have proposals about vacancies where C# is primary language because I hate this language - that's why I also add attidude grades.

### Projects

This is the main atomic block of your experience. Don't write that you 'created bugfixes' for your employer. List projects that you did for this employer and give a project proper description. And emphasize your professional and profit achievement. Also list skills you developed here and team size - show if you are teamplayer or not.

![Projects]({{ site.baseurl }}/assets/img/section_projects.png)

I also put my hobby projects here if they are big enough to highlight my skills, if I have any valuable achievements here.

### Employment History

Somebody would not hire a person who changes companies too frequently. And it is good to show how easy you can change environment with relations to project and small description of the company domain.

![History]({{ site.baseurl }}/assets/img/section_history.png)

### Professional Activities

I am a man of science, that's why I have lots of conference presentations, scientific publications, popular IT-related publications which I want to show here. This is optional section that shows that I don't simply work for money, but it is my passion.

![Activities]({{ site.baseurl }}/assets/img/section_activities.png)

### Interests and Traits

I believe this is useless section, but standards and advises from other sources tell the opposite. So let it stay here.

# Appearence

## Styling

Fonts, colors and layout is based on modern western practices and handbooks. Font is Arial Narrow, that allows to compress text.

## Density

Everything obvious or something that can be guessed by reader is evaded. Limit is 3-4 pages, let's stay in 3. Publications are compressed to tail automatically, I think about doing the same for projects and employment history.

## Decorations

There are special decoration images which replaces long word description. I never got reject because my CV look bad, only complements how original and cool is it. Because, again, it enhances information density. 

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
