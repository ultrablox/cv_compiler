

class Skill:
  def __init__(self, name):
    self.name = name
    self.synonims = []

  def get_synonims(self):
    return [self.name] + self.synonims

  def __str__(self):
    return self.name

  def has_synonim(self, name):
    return name in self.get_synonims()
  
  def set_display_name(self, new_name):
    self.displayName = new_name

  def display_name(self):
    return self.displayName
