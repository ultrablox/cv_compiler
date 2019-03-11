from enum import IntEnum
import json


class SectionId(IntEnum):
  INTRO = 1
  CHARACTER = 2
  EDUCATION = 3
  EXPERIENCE = 4
  CONCLUSION = 5


# Letter consists of a few unique sections:
# 1. Introduction (who am I, what I am applying to)
# 2. Why I am the best
# 3. Education
# 4. Experience
# 5. Conclusion


class LetterSection:
  def __init__(self, kind, text):
    self._kind = kind
    self._text = text
    self._skills = []

  def set_skills(self, skills):
    self._skills = skills


class LetterProject:
  def __init__(self):
    self.data = {}
    for sec_id in SectionId:
      self.data[sec_id] = []

  # def create_intro_section(self, name, vacancy):
  #   sec = LetterSection(SectionId.INTRO, r'My name is %s and I would like to apply for the vacancy \textbf{%s}, where I guess my skills and experience fit good.')
  #   self.data[SectionId.INTRO] += [sec]

  # def create_conclusion_section(self):
  #   sec = LetterSection(SectionId.CONCLUSION, r'I have enclosed my resume for your review and would be thankful for an opportunity to meet with you and discuss my application more detailed.')
  #   self.data[SectionId.CONCLUSION] += [sec]

  def variants(self, kind):
    return self.data[kind]

  def deserialize(self, file_name):
    with open(file_name, 'r') as f:
      data = json.loads(f.read())

      for sec in data:
        kind = SectionId[sec['kind']]
        sec = LetterSection(kind, sec['text'])
        self.data[kind] += [sec]



# My name is Yuri Blokhin and I would like to apply for the vacancy \vacancy, where I guess my skills and experience fit good. I am a big fan of your company and things you do, and I hope my skills and experience might be interesting for you.

# I became software engineer because I always had passion in programming. My first video game in the middle school with QBasic language. My commercial experience started since 2008, I have worked in four software companies, where I have been repeatedly recognized not only for developing qualitative software, but for inventing and implementing innovative ideas, which led to increasing company capital. During my employment history, I was responsible for full lifecycle software development from initial requirement gathering to design, coding, testing, documentation and implementation. I was also managing a small development team and as a result we successfully created a innovative RTR 3d engine for structural monitoring visualization.

# I use QT I use it since high school and love it very much, and this is the reason of my interest to become part of the team. My technical expertise includes perfect knowledge of C++ which I use every day, good skills in QT, Computer Graphics and OpenGL, working with many scripting languages (including Ruby, Go, Python, SQL and others), embedded development (as a hobby), cross-platform development (Linux, Windows, Mac OS) and advanced knowledge of modern IDEs, automation tools and development methodologies.

# As a creative person, I made a lot of software hobby projects, including ultra\_outliner - a unique innovative production-level tool for screenwriters, which I created alone and from scratch, basing on QT. I am also PhD in Engineering Sciences (in AI), and my science activity is represented in regular publications in area of AI and software development automation and presentations in scientific conferences.

# I have enclosed my resume for your review and would be thankful for an opportunity to meet with you and discuss my application more detailed.