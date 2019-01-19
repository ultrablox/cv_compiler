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





% Compact itemization
% \RequirePackage{enumitem}

\RequirePackage{enumitem,amssymb,pifont}
\newcommand{\cmark}{\ding{51}}%
\newcommand{\done}{\rlap{$\square$}{\raisebox{2pt}{\large\hspace{1pt}\cmark}}\hspace{-2.5pt}}%

% \setlist[itemize]{labelindent=\parindent, leftmargin=*, align=left}
% \setlist[itemize]{leftmargin=0pt}


\newenvironment{itemize-tasks}
{
  \begin{enumerate}[
    leftmargin=0pt,itemindent=2pt,labelsep=4pt,labelwidth=0pt,align=left,label=\done,
    noitemsep,
    nolistsep,
    ]
    \setlength{\itemsep}{0pt}
    \setlength{\parskip}{0pt}
    \setlength{\parsep}{0pt}}
{\end{enumerate}}

\newenvironment{itemize-cv}
{
  \begin{enumerate}[
    leftmargin=0pt,itemindent=2pt,labelsep=4pt,labelwidth=0pt,align=left,label=\textbullet,
    noitemsep,
    nolistsep,
    % leftmargin=0pt,
    % itemindent=0pt,
    % labelwidth=20pt,
    % align=left
    ]
    \setlength{\itemsep}{0pt}
    \setlength{\parskip}{0pt}
    \setlength{\parsep}{0pt}}
{\end{enumerate}}

\newenvironment{itemize-achievments}
{
  \begin{itemize}[noitemsep,nolistsep,label=$\star$,leftmargin=10pt]
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

\newcommand{\projectlink}[2]{{\color{color1}\textbf{#2}}}

\RequirePackage{lipsum}

\RequirePackage{parcolumns}

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
  \rmfamily
  \fontsize{12}{12}
  \bfseries
  #1
  \par
  }
}

\newcommand{\cvsubsubhead}[1]{
  {
  \rmfamily
  \fontsize{12}{12}
  \selectfont
  \color{color2}
  % \bfseries
  #1
  \par
  }
}

\newcommand{\cvsubsubheadg}[1]{
  {
  \rmfamily
  \fontsize{12}{12}
  \color{color2}
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
  \color{color2}
  \bfseries
  #1
  \par
  }
}

\newcommand{\cvyear}[1]{
{\rmfamily\fontsize{12}{12}\selectfont#1\par}
}


\newcommand{\skills}[1]{
{
  \rmfamily
  \fontsize{10}{10}
  \selectfont
  \itshape
  \color{color1}
  #1
  \par
  }
}

\newcommand{\itemhead}[1]{
{
  \sffamily
  \fontsize{12}{12}
  \selectfont
  % \bfseries
  #1
  \par
  }
}

\newcommand{\itemsubhead}[1]{
{
  \rmfamily
  \fontsize{12}{12}
  \selectfont
  #1
  \par
  }
}

\newcommand{\itemsubsubhead}[1]{
{
  \rmfamily
  \fontsize{11}{11}
  \selectfont
  #1
  \par
  }
}


\newcommand{\httplink}[2]{{\href{#1}{\rmfamily\color{gray}\fontsize{10}{10}\selectfont\bfseries#2}}}


\newcommand{\cvnormal}{
  \rmfamily
  % \fontsize{10}{10}
  % \color{black}
  % \selectfont
  % \mdseries
}

\newcommand{\colsectionspace}{\vspace{6pt}}


\RequirePackage[absolute]{textpos}%,showboxes
\setlength{\TPHorizModule}{1pt}
\setlength{\TPVertModule}{\TPHorizModule}
\textblockorigin{0pt}{0pt}
\setlength{\parindent}{0pt}


\RequirePackage{paracol}


\RequirePackage{multicol}

\newcommand{\scopus}{\textcolor{color1}{[Scopus]}}

\newcommand{\photo}[2]{
\tikz\node[circle,draw,
      text=white,
      path picture={
          \node at (path picture bounding box.center){
              \includegraphics[width=#2]{#1}
          };
      }]{xxxxxxxxxxxxxxxxxxx};
}



\usepackage{xcolor}
% https://www.colorcombos.com/color-schemes/40/ColorCombo40.html
\definecolor{color1}{RGB}{51, 102, 153}
\definecolor{color2}{RGB}{102, 102, 102}
\definecolor{color3}{RGB}{153, 153, 153}


