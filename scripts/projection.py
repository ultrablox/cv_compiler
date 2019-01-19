import copy
import logging


class Compressor:
  def create_relevant_projection(self, src_profile, minimal_relevance = 0.0):
    profile = copy.deepcopy(src_profile)
    profile.compress()

    profile.skillRecords.sort(key=lambda x: x.relevance, reverse=True)
    
    logging.info('Skill in relevance order:')
    for skill in profile.skillRecords:
      logging.info('::: %s->%f' % (skill.skill.name, skill.relevance))
    
    irrelevant_skills = []
    for rec in profile.skillRecords:
      if rec.relevance <= minimal_relevance:
        irrelevant_skills += [rec.skill]

    for iskill in irrelevant_skills:
      logging.info('Skill "%s" is non-relevant and removed' % iskill)
      profile.remove_skill(iskill)

    # Remove non-relevant projects
    non_relevant_projects = []
    for i in range(len(profile.projects), 0, -1):
      proj = profile.projects[i - 1]
      if proj.relevance <= minimal_relevance:
        logging.info('Project "%s" is non-relevant and removed' % proj)
        del profile.projects[i - 1]

    profile.projects.sort(key=lambda x: x.relevance, reverse=True)

    # Remove non-relevant tasks from projects
    for proj in profile.projects:
      for i in range(len(proj.tasks), 0, -1):
        task = proj.tasks[i - 1]
        if task.relevance <= minimal_relevance:
          logging.info('Task "%s" is non-relevant and removed' % task)
          del proj.tasks[i - 1]
      proj.tasks.sort(key=lambda x: x.relevance, reverse=True)

    # Convert references to non-relevant projects into notes
    for employments in profile.employments:
      for i in range(len(employments.projects), 0, -1):
        if employments.projects[i - 1].relevance <= minimal_relevance:
          del employments.projects[i - 1]

    return profile
