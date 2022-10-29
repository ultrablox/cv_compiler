import copy
import logging


class ProfileFilter:
  def create_relevant_projection(self, src_profile, compress_publications=True):
    profile = copy.deepcopy(src_profile)
    if compress_publications:
      profile.compress_scientific()

    profile.skillRecords.sort(key=lambda x: x.relevance, reverse=True)

    logging.info('Skill in relevance order:')
    for skill in profile.skillRecords:
      logging.info('::: %s->%f' % (skill.skill.name, skill.relevance))

    irrelevant_skills = []
    for rec in profile.skillRecords:
      if not rec.keep:
        irrelevant_skills += [rec.skill]

    for iskill in irrelevant_skills:
      logging.info('Skill "%s" is non-relevant and removed' % iskill.name)
      profile.remove_skill(iskill)

    # Remove non-relevant projects
    non_relevant_projects = []
    for i in range(len(profile.projects), 0, -1):
      proj = profile.projects[i - 1]
      if not proj.keep:
        logging.info('Project "%s" is non-relevant and removed' % proj)
        del profile.projects[i - 1]

    profile.projects.sort(key=lambda x: x.relevance, reverse=True)

    # Remove non-relevant tasks from projects
    for proj in profile.projects:
      for i in range(len(proj.tasks), 0, -1):
        task = proj.tasks[i - 1]
        if not task.keep:
          logging.info('Task "%s" is non-relevant and removed' % task)
          del proj.tasks[i - 1]
      proj.tasks.sort(key=lambda x: x.relevance, reverse=True)

    # Remove non-relevant part-time employments
    for i in range(len(profile.employments), 0, -1):
      emp = profile.employments[i - 1]
      if emp.is_part_time() and (not emp.keep):
        logging.info('Part-time employment "%s" is non-relevant and removed' % emp.name)
        del profile.employments[i - 1]

    # Convert references to non-relevant projects into notes
    for employment in profile.employments:
      for i in range(len(employment.projects), 0, -1):
        if not employment.projects[i - 1].keep:
          del employment.projects[i - 1]

    return profile
