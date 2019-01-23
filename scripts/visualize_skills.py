#!/usr/bin/env python3

import logging
import os
import matplotlib.pyplot as plt
import networkx as nx
from db import skills_db


def main():
  logging.basicConfig(level=logging.INFO)

  skill_db = skills_db.SkillsDB()
  skill_db.load(os.path.join('..', 'database'))

  plt.figure(figsize=(20, 20))
  res = nx.draw_networkx(skill_db.graph)
  plt.savefig("skills.pdf")


if __name__ == "__main__":
    main()