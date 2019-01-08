
import os
import json
import networkx as nx


class Skill:
  def __init__(self, json_node):
    self.name = json_node['full_name']


class SkillsDB:
  def find_skill(self, skill_name):
    return next(x for x in self.skills if x.name == skill_name)

  def load(self, db_dir):
    skill_nodes = []
    with open(os.path.join(db_dir, 'skills.json')) as f:
      skill_nodes = json.loads(f.read())

    connections = []
    with open(os.path.join(db_dir, 'skill_connections.json')) as f:
      connections = json.loads(f.read())

    # Build graph
    graph = nx.Graph()

    self.skills = []
    for skill_node in skill_nodes:
      new_skill = Skill(skill_node)
      self.skills += [new_skill]
      graph.add_node(new_skill)

    for conn in connections:
      src_node = self.find_skill(conn['src'])
      dst_node = self.find_skill(conn['dst'])
      graph.add_edge(src_node, dst_node, weight=conn['value'])
