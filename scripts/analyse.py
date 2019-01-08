#!/usr/bin/env python3
import os
from skills_db import *


def main():
  skill_db = SkillsDB()
  skill_db.load(os.path.join('..', 'database'))


if __name__ == "__main__":
    main()
