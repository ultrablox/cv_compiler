from cv.time import *
from utils import *
import logging

class Employment:
  def __init__(self):
    self.notes = []

  def deserialize(self, json_node, profile):
    self.name = json_node['name']
    self.period = TimePeriod(json_node['period'])
    self.web = json_node['web']
    self.role = json_node['role']
    self.description = json_node['description']
    self.logo = json_node['logo']
    if 'notes' in json_node:
      self.notes = json_node['notes']
    
    logging.debug('Deserializing projects for {} employment...'.format(self.name))
    self.projects = []
    for prj in json_node['projects']:
      prj_ref = first_true(profile.projects, None, lambda p: p.name == prj)
      assert prj_ref, 'Invalid project reference: %s' % prj
      prj_ref.parent = self
      self.projects += [prj_ref]

  def serialize(self):
    return {
      'name': self.name,
      'period': str(self.period),
      'web': self.web,
      'role': self.role,
      'description': self.description,
      'notes': self.notes,
      'logo': self.logo,
      'projects': list(str(x) for x in self.projects)
    }
