
import os
import json
import networkx as nx


class Skill:
  def __init__(self, json_node):
    self.name = json_node['full_name']
    self.synonims = []

  def get_synonims(self):
    return [self.name] + self.synonims

  def __str__(self):
    return self.name


class SkillsDB:
  def __init__(self):
    self.graph = nx.Graph()
    self.matchNode = Skill({'full_name': '#matcher#'})
    self.graph.add_node(self.matchNode)

  def find_skill(self, skill_name):
    found_skills = list(x for x in self.skills if x.name == skill_name)
    if found_skills:
      return found_skills[0]
    else:
      return None
  
  def connect_to_matcher(self, node):
    self.graph.add_edge(node, self.matchNode, weight=0.0)

  def load(self, db_dir):
    skill_nodes = []
    with open(os.path.join(db_dir, 'skills.json')) as f:
      skill_nodes = json.loads(f.read())

    connections = []
    with open(os.path.join(db_dir, 'skill_connections.json')) as f:
      connections = json.loads(f.read())

    # Build graph

    self.skills = []
    for skill_node in skill_nodes:
      new_skill = Skill(skill_node)
      self.skills += [new_skill]
      self.graph.add_node(new_skill)

    for conn in connections:
      src_node = self.find_skill(conn['src'])
      dst_node = self.find_skill(conn['dst'])
      self.graph.add_edge(src_node, dst_node, weight=(1.0 - conn['value']))

  def get_relevance(self, skill_node):
    try:
      p = nx.shortest_path_length(self.graph, source=self.matchNode, target=skill_node, weight='yes')
      # print('Found path:')
      # for node in p:
      #   print(str(node))
      return 1.0 / p
    except nx.networkx.exception.NetworkXNoPath:
      return 0.0
