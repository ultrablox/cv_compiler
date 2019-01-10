\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ultracv}[2014/08/16 Example LaTeX class]

\LoadClass{article}

% \newcommand{\headlinecolor}{\normalcolor}

% \RequirePackage{xcolor}
% \definecolor{slcolor}{HTML}{882B21}


% \DeclareOption{onecolumn}{\OptionNotUsed}
% \DeclareOption{green}{\renewcommand{\headlinecolor}{\color{green}}}
% \DeclareOption{red}{\renewcommand{\headlinecolor}{\color{slcolor}}}
% \DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
% \ProcessOptions\relax

% \renewcommand{\maketitle}{%
%     \twocolumn[%
%         \fontsize{50}{60}\fontfamily{phv}\fontseries{b}%
%         \fontshape{sl}\selectfont\headlinecolor
%         \@title
%         \medskip
%         ]%
% }

% \renewcommand{\section}{%
%     \@startsection
%     {section}{1}{0pt}{-1.5ex plus -1ex minus -.2ex}%
%     {1ex plus .2ex}{\large\sffamily\slshape\headlinecolor}%
% }

% \renewcommand{\normalsize}{\fontsize{9}{10}\selectfont}
% \setlength{\textwidth}{17.5cm}
% \setlength{\textheight}{22cm}
% \setcounter{secnumdepth}{0}


% Two paired fonts for body and headings
% https://mirror.hmc.edu/ctan/macros/xetex/latex/fontspec/fontspec.pdf

\RequirePackage{mathspec,fontspec}

\setmathfont[version=normal,
  Extension = .ttf,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  ItalicFont = *-Italic
]{ArchivoNarrow}

\setmainfont[Extension = .ttf,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  ItalicFont = *-Italic
]{ArchivoNarrow}

\setsansfont[Extension = .ttf,
  UprightFont = *-Regular,
  BoldFont = *-Bold,
  ItalicFont = *-Italic
]{OpenSans}

% Don't use ALL CAPS to highlight
\newcommand{\sectionhead}[1]{\sffamily\fontsize{12}{12}\selectfont\bfseries \raggedleft #1}
\newcommand{\regulartext}{\rmfamily\fontsize{10}{6}\selectfont}

% \rmfamily,\sffamily

% Two column style
\RequirePackage{paracol}
\columnratio{0.18}

% Layout
\newlength\sectionspace
\setlength{\sectionspace}{2mm}

% COLORATION
% https://uxmovement.com/content/how-color-saturation-affects-user-efficiency/
% Dark, desaturated colors to express professional and serious

% URLs are smaller
\RequirePackage{hyperref}
% \RequirePackage[hyphens]{url}

\RequirePackage{xcolor}
\hypersetup{
    colorlinks,
    linkcolor={red!30!black},
    citecolor={black!50!black},
    urlcolor={black!80!black}
}

\newcommand{\httplink}[2]{{\href{#1}{\rmfamily\color{gray}\fontsize{9}{9}\selectfont#2}}}



% Compact itemization
% \RequirePackage{enumitem}

\RequirePackage{enumitem,amssymb,pifont}
\newcommand{\cmark}{\ding{51}}%
\newcommand{\done}{\rlap{$\square$}{\raisebox{2pt}{\large\hspace{1pt}\cmark}}\hspace{-2.5pt}}%

\newenvironment{itemize-cv}
{
  \begin{itemize}[noitemsep,nolistsep,leftmargin=12pt]
    % \renewcommand\labelitemi{\includegraphics[height=12pt]{img/correct.pdf}}
    \setlength{\itemsep}{0pt}
    \setlength{\parskip}{0pt}
    \setlength{\parsep}{0pt}}
{\end{itemize}}

\newenvironment{itemize-achievments}
{
  \begin{itemize}[noitemsep,nolistsep,label=$\star$,leftmargin=2pt]
    % \setlength\itemindent{0pt}
    % \setlength{\leftmargini}{0pt}
    \setlength{\itemsep}{0pt}
    \setlength{\parskip}{0pt}
    \setlength{\parsep}{0pt}}
{\end{itemize}}

