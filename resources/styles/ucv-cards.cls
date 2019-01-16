\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ultracv}[2014/08/16 Example LaTeX class]

\LoadClass{article}


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


% \rmfamily,\sffamily

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

\newcommand{\vcenteredinclude}[1]{\begingroup
\setbox0=\hbox{\includegraphics[width=12pt]{#1}}%
\parbox{\wd0}{\box0}\endgroup}


\RequirePackage{pgfplots}

\newcommand{\projectlink}[2]{\textbf{#2}}

\RequirePackage{lipsum}

\RequirePackage{parcolumns}

\RequirePackage[absolute,showboxes]{textpos}
\setlength{\TPHorizModule}{1pt}
\setlength{\TPVertModule}{\TPHorizModule}
\textblockorigin{0pt}{0pt}

\RequirePackage{wrapfig}

\RequirePackage{graphicx}

% Styles for main column
\newcommand{\cvhead}[1]{
  {
  \sffamily
  \fontsize{14}{14}
  \bfseries
  #1
  \par
  }
  \vspace{4pt}
}

\newcommand{\cvsubhead}[1]{
  {
  \sffamily
  \fontsize{12}{12}
  \bfseries
  #1
  \par
  }
}

\newcommand{\cvsubsubhead}[1]{
  {
  \sffamily
  \fontsize{12}{12}
  \selectfont
  % \bfseries
  #1
  \par
  }
}

\newcommand{\cvsubsubheadg}[1]{
  {
  \rmfamily
  \fontsize{12}{12}
  \color{gray}
  \selectfont
  \bfseries
  #1
  \par
  }
}

\newcommand{\cvirrelevant}[1]{
  {
  \rmfamily
  \fontsize{10}{10}
  \color{gray}
  \bfseries
  #1
  \par
  }
}

\newcommand{\cvyear}[1]{
{\rmfamily\fontsize{12}{12}\selectfont#1\par}
}

\newcommand{\cvnormal}{
  \rmfamily
  % \fontsize{10}{10}
  % \color{black}
  % \selectfont
  % \mdseries
}

\newcommand{\colsectionspace}{\vspace{6pt}}


\RequirePackage[absolute,showboxes]{textpos}
\setlength{\TPHorizModule}{1pt}
\setlength{\TPVertModule}{\TPHorizModule}
\textblockorigin{0pt}{0pt}
\setlength{\parindent}{0pt}


\RequirePackage{paracol}
