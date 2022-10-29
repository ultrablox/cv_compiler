from tex_printer import *
from skill_matrix import *
from project_printer import *
from employment_printer import *
from cv.time import *
from cv.skill_experience import *
from tex.elements import *
from tex.cv_project import *
from tex.cv_employment import *
from tex.cv_headcolumn import *


PT_IN_MM = 2.83465

# In pt
GRID_V_SPACING = 15
GRID_H_SPACING = 12
PAGE_H_MARGIN = 10*PT_IN_MM



# A4 =  210 mm x  297 mm =  595 pt x  842 pt
class TexCardsPrinter(TexPrinter):

  V_SPACING = 15
  # CARD_WIDTH = (595 - 4 * V_SPACING)/3
  # CARD_HEIGHT = 206
  CARD_WIDTH = (595 - 2 * PAGE_H_MARGIN - 2* GRID_H_SPACING) / 3
  CARDS_IN_ROW = 3
  HEADER_HEIGHT = 24
  HOR_SPACING = 4

  def __init__(self, out_fname):
    self._pdfName = out_fname

  def __enter__(self):
    self._tmpDir = tempfile.TemporaryDirectory()
    self.tmpDirName = self._tmpDir.name # #os.path.abspath('tmp')#
    self._texName = os.path.join(self.tmpDirName, 'main.tex')
    self._texFile = open(self._texName, 'w+')
    self.file = self._texFile
    self.rootDir = self.tmpDirName
    return self

  def __exit__(self, type, value, tb):
    print(self.tmpDirName)
    self._texFile.close()
    call_system('cd {} && xelatex {} main.tex'.format(self.tmpDirName, ' '.join(self.TEX_ARGS)))
    shutil.copy(os.path.join(self.tmpDirName, 'main.pdf'), self._pdfName)

  
  def print_scientific_pubs(self, pubs, scopus_count):
    summary_str = '%d total' % len(pubs)
    if scopus_count:
      summary_str += ', incl. %d Scopus' % scopus_count
    self.write([r'\itemhead{\textbf{Scientific Publications}}',
      r'',
      r'\itemsubhead{%s}' % summary_str,
      r''])
    
    with Itemize(self) as itemize:
      for pub in pubs:
        if pub['visible']:
          is_scopus = '\scopus' if (('source' in pub) and (pub['source'] == 'Scopus')) else ''
          itemize.item(r'\rmfamily %d --- %s // %s %s' % (int(pub['year']), latex_escape(pub['title']), pub['journal'] if 'journal' in pub else 'Unknown', is_scopus))


  def print_popoular_pubs(self, pubs):    
    years = int(pubs[0]['year']) - int(pubs[-1]['year']) + 1
    summary_str = '%d total, avg. %.1f publicatons / year' % (len(pubs), float(len(pubs))/years)
    self.write([r'\itemhead{\textbf{Popular Publications}}',
      r'',
      r'\itemsubhead{%s}' % summary_str,
      r''])
  
    with Itemize(self) as itemize:
      for pub in pubs:
        if pub['visible']:
          itemize.item(r'\rmfamily %d --- %s // %s \href{%s}{[link]}' % (int(pub['year']), pub['title'], pub['source'], pub['url']))

  def print_conferences(self, conferences):
    years = int(conferences[0]['year']) - int(conferences[-1]['year']) + 1
    summary_str = '%d total, avg. %.1f presentations / year' % (len(conferences), float(len(conferences))/years)
    conf_strs = []
    

    self.write([r'\itemhead{\textbf{Conference Presentations}}',
      r'',
      r'\itemsubhead{%s}' % summary_str,
      r''
    ])

    with Itemize(self) as itemize:
      for conf in conferences:
        itemize.item('%s (%s, %d)' % (conf['name'], conf['location'], conf['year']))


  def print_profile(self, profile, cfg):
    EMPLOYMENT_CARD_HEIGHT = 100
   
    out_dir = self.rootDir
    with Document(self, 10):
      self.write([
        r'\setlength\multicolsep{0pt}',
        r'\setlength{\parindent}{0pt}',
        r'\setlength{\columnsep}{%dpt}' % GRID_H_SPACING
      ])
      
      with TextBlock(self, self.CARD_WIDTH, 0, 0, PAGE_H_MARGIN, PT_IN_MM*10):
        with MinipageElement(self, r'%dpt' % (self.CARD_WIDTH - 2), r'[t][\textheight]'):
          HeadColumn(self, profile, cfg)

        self.write([
          r'\hspace{1pt}\textcolor{color1}{\vrule width 1.5pt}',
          r''
        ])

      header_hoffset = self.CARD_WIDTH + GRID_H_SPACING - 6
      SectionHeading(self, 'Relevant Projects', 'In order of relevance', header_hoffset)
      
      with SectionElement(self):
        for project in profile.projects:
          with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
            with VSpaceGuard(self, GRID_V_SPACING):
              ProjectElement(self, project)   

      SectionHeading(self, 'Employment History', 'Total %.1f years in industrial development' % profile.total_employment().years(), header_hoffset)
      with SectionElement(self):
        for employment in profile.fulltime_employments():
          with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
            with VSpaceGuard(self, GRID_V_SPACING):
              EmploymentBlock(self, employment)
      
      part_employments = profile.parttime_employments()
      if part_employments:
        SectionHeading(self, 'Part-Time Employments', 'Only relevant included', header_hoffset)
        with SectionElement(self):
          for employment in part_employments:
            with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
              with VSpaceGuard(self, GRID_V_SPACING):
                EmploymentBlock(self, employment)
      
      SectionHeading(self, 'Activities and Personal', 'Only recent is presented', header_hoffset)
      with SectionElement(self):
        if profile.scientificPubs:
          with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
            with VSpaceGuard(self, GRID_V_SPACING):
              self.print_scientific_pubs(profile.scientificPubs, profile.scopus_publication_count())
      
        if profile.popularPubs:
          with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
            with VSpaceGuard(self, GRID_V_SPACING):
              self.print_popoular_pubs(profile.popularPubs)

        if profile.conferences:
          with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
            with VSpaceGuard(self, GRID_V_SPACING):
              self.print_conferences(profile.conferences)

        if profile.traits:
          with MinipageElement(self, '{}pt'.format(self.CARD_WIDTH)):
            with VSpaceGuard(self, GRID_V_SPACING):
              self.write([r'\itemhead{\textbf{Personal}}',
                r''])

              with Itemize(self) as itemize:
                for trait in profile.traits:
                  itemize.item(r'\textbf{%s:} %s' % (trait['name'], trait['details']))

              
