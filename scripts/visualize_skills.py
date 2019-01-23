#!/usr/bin/env python3

import logging
from skills_db import *


def main():
  logging.basicConfig(level=logging.INFO)

  skill_db = SkillsDB()
  skill_db.load(os.path.join('..', 'database'))

  plt.figure(figsize=(30, 30))
  res = nx.draw_networkx(skill_db.graph)
  plt.savefig("skills.pdf")


if __name__ == "__main__":
    main()