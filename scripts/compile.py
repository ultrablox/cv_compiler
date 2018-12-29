#!/usr/bin/env python3

from skill_attitude import *
import json
import datetime

import urllib.parse
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
import sys, os
import argparse
from check import *
from skill_matrix import *
from basic_entities import *
import glob
import shutil
from tex_printer import *

MAX_SCI_PUBS = 5
MAX_NON_SCI_PUBS = 3
MAX_CONFERENCES = 5

DEBUG_LATEX = False

LATEX_OUTPUT = '' if DEBUG_LATEX else '1>/dev/null'
LATEX_PARAMS = [] if DEBUG_LATEX else ['-halt-on-error', '--interaction=batchmode']


class EmployerProfile:
    def __init__(self):
        self.projects = []
        self.employments = []
        self.publicationStats = {}
    
    def deserialize(self, json_node):
        self.contacts = json_node['contacts']
        self.personal = json_node['personal']
        self.education = json_node['education']
        self.traits = json_node['traits']
    
        self.specialSkillGroups = json_node['special_skills']
        
        self.skills = {}

        for skill in json_node['skills']:
            new_skill = Skill(skill)
            sd = json_node['skills'][skill]
            if 'attitude' in sd:
                switcher = {
                    'favourite' : SkillAttitude.FAVOURITE,
                    'neutral' : SkillAttitude.NEUTRAL,
                    'negative' : SkillAttitude.NEGATIVE
                }
                new_skill.attitude = switcher.get(sd['attitude'], lambda: None)
            self.skills[skill] = new_skill

        for prj in json_node['projects']:
            new_prj = Project(prj)
            self.projects += [new_prj]
            
            if 'skills' in prj:
                for prj_skill in prj['skills']:
                    self.add_period_for_skill(prj_skill, new_prj.period)

            if 'secondary_skills' in prj:
                for sec_skill in prj['secondary_skills']:
                    self.add_period_for_skill(sec_skill['name'], TimePeriod(sec_skill['period']))
        
        # Remove empty skills
        empty_skills = []
        for skill_name, skill_data in self.skills.items():
            if skill_data.total_size() == 0.0:
                empty_skills += [skill_name]

        for empty_name in empty_skills:
            del self.skills[empty_name]

        for employment_node in json_node['employments']:
            self.employments += [Employment(employment_node, self)]
        
        # non_sci_pubs = []
        

        self.popularPublications = json_node['pop_publications'][0:MAX_NON_SCI_PUBS]

        self.conferences = json_node['conferences'][0:MAX_CONFERENCES]

    def deserialize_publications(self, pubs_path):
      scopus_pubs = []
      other_pubs = []
      
      with open(pubs_path, encoding='utf-8') as bibtex_file:
        parser = BibTexParser()
        parser.customization = homogenize_latex_encoding
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

        sorted_pubs = sorted(bib_database.entries, key=lambda pub: int(pub['year']), reverse=True)
        for publication in sorted_pubs:
          skip = False
          skip = skip or (('language' in publication) and (publication['language'] == 'russian'))
          skip = skip or (publication['ENTRYTYPE'] != 'article')

          if not skip:
              if ('source' in publication) and (publication['source'] == 'Scopus'):
                  scopus_pubs += [publication]
              else:
                  other_pubs += [publication]
        
        self.publicationStats['sci_total'] = len(bib_database.entries)
        self.publicationStats['scopus'] = len(scopus_pubs)

        if len(scopus_pubs) > MAX_SCI_PUBS:
          self.scientificPublications = scopus_pubs[0:MAX_SCI_PUBS]
        else:
          raise Exception('Not implemented')

    
    def skills_totals(self):
        res = []
        for key, data in self.skills.items():
            res += [{'name' : key, 'size' : data.total_size()}]
        return sorted(res, key=lambda rec: rec['size'], reverse=True)

    def add_period_for_skill(self, skill, period):
        if not skill in self.skills:
            new_skill = Skill(skill)
            self.skills[skill] = new_skill
        cur_skill = self.skills[skill]
        cur_skill.add_period(period)
    
    def best_skill(self):
        skills = self.skills_totals()
        return skills[0]['size']

    def generate_employments(self, path):
        with open(path, "w") as file:
            for employment in self.employments:
                file.write("\job{%s}{%s}{%s}{%s}{%s}{%s}{\n" % (employment.period.startDate.strftime('%b %Y'), 'Present' if employment.period.isOpen else employment.period.endDate.strftime('%b %Y'), employment.name, employment.web, employment.role, employment.description))
                file.write("\t\\begin{itemize-noindent}\n")
                
                prj_names = []
                for prj in employment.projects:
                    prj_names += ['\projectlink{%s:project}{%s}' % ('xx', latex_escape(prj.name))]

                notes_arr = ['\t\t\item{ worked in %s project%s}' % (', '.join(prj_names), 's' if len(prj_names) > 1 else '')]

                for note in employment.notes:
                    notes_arr += ['\t\t\item{%s}' % note]

                file.write("\n".join(notes_arr))
                file.write("\n")
                file.write("\t\end{itemize-noindent}\n")
                file.write("}\n")

    def generate_publications(self, path):
        with open(path, "w") as file:
            file.write('(%d total, incl. %d Scopus)\n' % (self.publicationStats['sci_total'], self.publicationStats['scopus']))
            file.write('\\begin{itemize-noindent}\n')
            for publication in self.scientificPublications:
                file.write('\item %d --- %s // %s' % (int(publication['year']), publication['title'], publication['journal']))
                if ('source' in publication) and (publication['source'] == 'Scopus'):
                    file.write(' \scopus')
                file.write('\n')

            file.write('\end{itemize-noindent}\n')

    def generate_popular_publications(self, path):
        with open(path, "w+") as file:
            
            file.write('\\begin{itemize-noindent}\n')
            for publication in self.popularPublications:
                file.write('\item \ppublication{%d}{%s}{%s}{%s}' % (publication['year'], publication['name'], publication['source'], latex_escape(publication['url'])))
            file.write('\end{itemize-noindent}\n')
        
    
    def generate_conferences(self, path):
        with open(path, "w") as file:
            conf_strs = []
            for conf in self.conferences:
                conf_strs += ['%s (%s, %d)' % (conf['name'], conf['location'], conf['year'])]
            file.write("%s, etc.\n" % ' '.join(conf_strs))

    def generate_educations(self, path):
        with open(path, "w") as file:
            for edu in self.education:
                tp = TimePeriod(edu['period'])
                file.write('\education{%s}{%d-%d}{%s}{%s}{' % (edu['place'], tp.startDate.year, tp.endDate.year, edu['name'], latex_escape(edu['gpa'])))
                if ('notes' in edu) and (len(edu['notes']) > 0):
                    file.write('\\begin{itemize-noindent}')
                    notes_arr = []
                    for note in edu['notes']:
                        notes_arr += ['\item %s' % note]
                    file.write('\n'.join(notes_arr))
                    file.write('\end{itemize-noindent}')
                file.write('}')
    
    def generate_skills(self, path):
        totals = self.skills_totals()
        totals = totals[VISUAL_SKILL_COUNT:]

        skill_groups = {}
        #0, <1yr, 1-2yr, 2-5, 5-7, 7-10, 10+
        barriers = [0, 1, 2, 5, 7, 10, 1000]
        cur_gr_idx = 0
        with open(path, "w") as file:
            for skill in totals:
                gr_val = 0
                for idx in range(0, len(barriers)):
                    if (barriers[idx] <= skill['size']) and (skill['size'] < barriers[idx+1]):
                        gr_val = barriers[idx]
                        break

                if gr_val in skill_groups:
                    skill_groups[gr_val] += [skill]
                else:
                    skill_groups[gr_val] = [skill]

            first_non_empty = True
            for barrier in reversed(barriers):
                if barrier in skill_groups:
                    barrier_idx = barriers.index(barrier)

                    skills = []
                    max_size = 0
                    for sk in skill_groups[barrier]:
                        skills += [latex_escape(sk['name'])]
                        max_size = max(max_size, sk['size'])

                    max_val_name = str(barriers[barrier_idx+1])
                    if first_non_empty:
                        max_val_name = '%.1f' % max_size
                        first_non_empty = False
                    
                    group_name = '<%s year' % max_val_name if barrier_idx == 0 else '%d-%s years' % (barriers[barrier_idx], max_val_name)
                    
                    
                    file.write('\\textbf{%s:} %s\n\n' % (group_name, ', '.join(skills)))

            for sgr in self.specialSkillGroups:
                file.write('\skillgroup{%s:}{%s}{\n' % (sgr['name'], sgr['details']))
                for adv in sgr['advantages']:
                    file.write('\item %s\n' % adv)
                file.write('}\n')

    
    def generate_traits(self, path):
        with open(path, "w") as file:
            for trait in self.traits:
                file.write('\item \\textbf{%s:} %s\n' % (trait['name'], trait['details']))

def main():
  parser = argparse.ArgumentParser(description='Compile CV into PDF file.')
  parser.add_argument('--input_dir', type=str, default='/input', help='Input directory')
  parser.add_argument('--tmp_dir', type=str, default='/tmp', help='Temporary directory')
  parser.add_argument('--out_dir', type=str, default='/out', help='Output directory')
  args = parser.parse_args()

  # Check necessary paths exist 
  check_always(os.path.exists(args.input_dir), 'Input directory "%s" does not exist' % args.input_dir)
  check_always(os.path.exists(args.tmp_dir), 'Temp directory "%s" does not exist' % args.tmp_dir)
  check_always(os.path.exists(args.out_dir), 'Output directory "%s" does not exist' % args.out_dir)

  # Check input structure
  data_path = os.path.join(args.input_dir, 'data.json')
  check_always(os.path.exists(data_path), 'Primary input "%s" does not exist' % data_path)

  lead_path = os.path.join(args.input_dir, 'lead.txt')
  check_always(os.path.exists(lead_path), 'Lead text "%s" does not exist' % lead_path)

  publications_path = os.path.join(args.input_dir, 'publications.bib')
  enable_pubs = os.path.exists(publications_path)

  # Load input data
  
  profile = EmployerProfile()
  with open(data_path, 'r') as json_data:
      data = json.load(json_data)
      profile.deserialize(data)

  if enable_pubs:
    profile.deserialize_publications(publications_path)
  
  # for sk in profile.skills:
  #     sk_ref = profile.skills[sk]
  #     print('%s: %s (%0.1f years)\n' % (sk, sk_ref.periods, sk_ref.total_size()))


  # Run along the projects and look for the minmal and maximum date
  min_date = None
  max_date = None
  for new_prj in profile.projects:

      if min_date:
          min_date = min(min_date, new_prj.period.startDate)
      else:
          min_date = min(new_prj.period.startDate, new_prj.period.endDate)

      if max_date:
          max_date = max(max_date, new_prj.period.endDate)
      else:
          max_date = max(new_prj.period.startDate, new_prj.period.endDate)
  
  # Generate skill matrix
  skill_matrix_path = os.path.join(args.tmp_dir, 'skill_matrix.pdf')
  skill_matrix = SkillMatrix(profile)
  skill_matrix.compile(skill_matrix_path)
  
  # Generate tex files
  rc_dirs = [os.path.join('..', 'resources'), os.path.join(args.input_dir)]
  
  styles_printer = StylesPrinter(args.tmp_dir, rc_dirs)
  styles_printer.print(None, 'generated_styles.tex')
  


  projects_printer = ProjectsPrinter(args.tmp_dir, rc_dirs)
  projects_printer.print(profile, 'generated_projects.tex')

  employments_path = os.path.join(args.tmp_dir, "generated_employments.tex")
  profile.generate_employments(employments_path)

  publications_path = os.path.join(args.tmp_dir, "generated_scientific_publications.tex")
  profile.generate_publications(publications_path)

  conferences_path = os.path.join(args.tmp_dir, "generated_conferences.tex")
  profile.generate_conferences(conferences_path)

  popular_publications_path = os.path.join(args.tmp_dir, "generated_popular_publications.tex")
  profile.generate_popular_publications(popular_publications_path)

  educations_path = os.path.join(args.tmp_dir, "generated_educations.tex")
  profile.generate_educations(educations_path)

  skills_path = os.path.join(args.tmp_dir, "generated_skills.tex")
  profile.generate_skills(skills_path)

  
  contacts_printer = ContactsPrinter(args.tmp_dir, rc_dirs)
  contacts_printer.print(profile, 'personal_contacts.tex')

  traits_path = os.path.join(args.tmp_dir, "generated_traits.tex")
  profile.generate_traits(traits_path)

  # Copy static resources
  for file in glob.glob(r'../resources/styles/*.*') + glob.glob(r'../resources/fonts/*.*'):
    shutil.copy(file, args.tmp_dir)
  shutil.copy(lead_path, os.path.join(args.tmp_dir, 'lead.tex'))

  # Compile PDF

  call_system('cd %s && xelatex %s main.tex %s' % (args.tmp_dir, ' '.join(LATEX_PARAMS), LATEX_OUTPUT))

  # Move result to output

  shutil.copy(os.path.join(args.tmp_dir, 'main.pdf'), os.path.join(args.out_dir, '%s_CV.pdf' % to_file_name(profile.personal['name'])))

if __name__ == "__main__":
    main()
