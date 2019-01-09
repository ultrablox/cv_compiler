import copy
from log import *


class Compressor:
  def create_relevant_projection(self, src_profile):
    profile = copy.deepcopy(src_profile)
    profile.compress()

    profile.skillRecords.sort(key=lambda x: x.relevance, reverse=True)

    # Remove non-relevant projects
    non_relevant_projects = []
    for i in range(len(profile.projects), 0, -1):
      proj = profile.projects[i - 1]
      if proj.relevance == 0.0:
        log_print(LOG_LEVEL_INFO, 'Project "%s" is non-relevant and removed' % proj)
        del profile.projects[i - 1]

    profile.projects.sort(key=lambda x: x.relevance, reverse=True)

    # Remove non-relevant tasks from projects
    for proj in profile.projects:
      for i in range(len(proj.tasks), 0, -1):
        task = proj.tasks[i - 1]
        if task.relevance == 0.0:
          log_print(LOG_LEVEL_INFO, 'Task "%s" is non-relevant and removed' % task)
          del proj.tasks[i - 1]
      proj.tasks.sort(key=lambda x: x.relevance, reverse=True)

    # Convert references to non-relevant projects into notes
    for employments in profile.employments:
      for i in range(len(employments.projects), 0, -1):
        if employments.projects[i - 1].relevance == 0.0:
          del employments.projects[i - 1]

    return profile
