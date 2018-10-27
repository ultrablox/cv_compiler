# cv_generator

## Aims

This is automatic generator of typical Software Engineer CV.

You are tired of constant updating your CV? Every time you get better idea how to do it and you have to recall all your past experience?

Forget about that. Just add your new experience into JSON, and generator will highlight the most relevant and decrease attention absolete records.

## Prerequistes

You need to have following software in your environment:


```

latex (xelatex)
svg2pdf
python3.5+

```

You might also need to install additional latex packages:

```
tlmgr install 

paracol
sectsty
enumitem

```

## Usage

Create directory with following structure:

data.json - your information and history
publications.bib - your scientific publications
lead.tex - your CV headline
img/ - your custom images

Refer for sample_input as an example.

Call 

```

./generate sample_input/

```

After that you will find main.pdf with compiled CV.

## For developers

If you want to improve it, create pull request with appropriate description - I will approve it. 