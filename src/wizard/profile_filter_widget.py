from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPlainTextEdit, QHBoxLayout, QListView, QWizardPage, QTreeView, QSlider
from PyQt5.QtCore import QSize, Qt, QSortFilterProxyModel, QRandomGenerator
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QStandardItemModel, QStandardItem, QBrush, QIcon, QPixmap
from db import skills_db
from cv.employee_profile import *
from cv import profile_filter
import logging
import math
from datetime import datetime


class RelevanceSortModel(QSortFilterProxyModel):
  def __init__(self):
    QSortFilterProxyModel.__init__(self)

  def lessThan(self, left_idx, right_idx):
    ldata = left_idx.data(Qt.UserRole)
    rdata = right_idx.data(Qt.UserRole)

    if ldata and rdata:
      return ldata < rdata
    else:
      return False


class ProfileFilterWidget(QWizardPage):
  def __init__(self, matcher_page, input_dir):
      QWizardPage.__init__(self)
      self.setMinimumSize(QSize(640, 480))

      self._matcherPage = matcher_page
      self._skillDb = skills_db.SkillsDB()
      self._skillDb.load_from_default_location()

      self._profile = EmployeeProfile(self._skillDb)
      self._profile.load(input_dir)

      self._treeProfile = QTreeView(self)

      self._relevanceLimit = QSlider(self)
      self._relevanceLimit.setOrientation(Qt.Orientation.Vertical)
      self._relevanceLimit.setTickInterval(1)
      self._relevanceLimit.setRange(0, 100)
      self._relevanceLimit.valueChanged.connect(lambda: self._update_relevance_limit(self._relevanceLimit.value() / 100.0))

      lyt = QHBoxLayout()
      lyt.addWidget(self._treeProfile)
      lyt.addWidget(self._relevanceLimit)
      self.setLayout(lyt)

      self._employmentItems = {}
      self._taskItems = {}
      self._projectItems = {}
      self._skillItems = {}

  def _build_relevance(self, value):
    item = QStandardItem()
    item.setText('{:.2%}'.format(value))
    item.setData(value, Qt.UserRole)
    return item

  def _build_project(self, project):
    project_item = QStandardItem(project.name)
    project_item.setCheckable(True)
    for task in project.tasks:
      task_item = QStandardItem(task.description)
      task_item.setCheckable(True)
      project_item.appendRow([task_item, self._build_relevance(task.relevance)])
      self._taskItems[task] = task_item

    self._projectItems[project] = project_item
    return project_item

  def _build_projects(self):
    projects_item = QStandardItem('Projects')
    for project in self._profile.projects:
      projects_item.appendRow([self._build_project(project), self._build_relevance(project.relevance)])
    return projects_item

  def _build_employments(self):
    employments_item = QStandardItem('Employments')
    for employment in self._profile.employments:
      employment_item = QStandardItem(employment.name)
      employment_item.setCheckable(True)
      employments_item.appendRow([employment_item, self._build_relevance(employment.relevance)])
      self._employmentItems[employment] = employment_item
    return employments_item

  def _build_skills(self):
    skills_item = QStandardItem('Skills')
    for skill in self._profile.skillRecords:
      skill_item = QStandardItem(skill.skill.name)
      skill_item.setCheckable(True)
      skills_item.appendRow([skill_item, self._build_relevance(skill.relevance)])
      self._skillItems[skill] = skill_item
    return skills_item

  def _build_model(self):
    model = QStandardItemModel()
    model.setColumnCount(2)
    model.setHorizontalHeaderLabels(['Name', 'Relevance'])
    model.appendRow(self._build_skills())
    model.appendRow(self._build_projects())
    model.appendRow(self._build_employments())

    sort_model = RelevanceSortModel()
    sort_model.setSourceModel(model)
    sort_model.sort(1, Qt.DescendingOrder)

    self._treeProfile.setModel(sort_model)

  def task_relevance(self, task, skill_table, skill_db, vacancy_skill_count):
    # Less skill you have - more focused you are
    # Take product of skill usage by their relevance and divide it by full task length
    # It's rough averaging, but looks good for now

    # Check intersection with vacancy requirements
    res = 0.0
    for skill in task.skills:
      res += skill_table[skill]
    res = res / vacancy_skill_count

    if task.achievements:
      res = res * 1.2

    # Check how long time passed since then
    # After 5 years (T) relevance becomes 1/4 (R)
    # r(t) = exp(-k*t), k = - ln(R)/T
    t1 = (datetime.today() - task.period.endDate).days
    t2 = (datetime.today() - task.period.startDate).days

    # print('t1=%f, t2=%f' % (t1, t2))

    T = 5 * 365.0
    R = 0.25
    k = - math.log(R) / T

    elapsed_rel = (math.exp(-k * t1) - math.exp(-k * t2)) / (k * (t2 - t1))

    res *= elapsed_rel
    assert res <= 1.0, 'Task relevance cant exceed 1.0'
    return res

  def project_relevance(self, project):
    # (sum task_time * task_relevance ) / project_length
    # relevant_timespan = sum((x.relevance * x.period.get_length()) for x in project.tasks)
    # total_timespan = project.get_period().get_length()
    # res = relevant_timespan / total_timespan
    res = max(x.relevance for x in project.tasks)
    
    # Nobody believes that hobby projects worth discussing...
    # ..except me
    if not project.parent:
      res = 0.7 * res

    assert res <= 1.0, 'Relevance cant exceed 1.0'
    return res

  def employment_relevance(self, employment):
    return max(x.relevance for x in employment.projects)

  def _compute_relevance(self):
    matched_skills = [self._skillDb.find_skill(x) for x in self._matcherPage.matched_skills()]

    for skill in matched_skills:
      self._skillDb.connect_to_matcher(skill)

    # Compute skill relevance
    logging.info('Skill Relevances:')
    skill_relevance = {}
    for skill_rec in self._profile.skillRecords:
      skill_ref = skill_rec.skill
      # print('%s' % skill_ref)
      relevance = self._skillDb.get_relevance(skill_ref)
      skill_relevance[skill_ref] = relevance
      skill_rec.relevance = relevance
      if relevance:
        logging.info('::: %s: %f' % (skill_ref.name, relevance))

    # Compute tasks and project relevances
    for project in self._profile.projects:
      logging.info('Checking tasks for "%s" project:' % project.name)
      for task in project.tasks:
        task_assesment = self.task_relevance(task, skill_relevance, self._skillDb, len(matched_skills))
        task.relevance = task_assesment
        logging.info('::: %s -> %f' % (task, task.relevance))

      proj_assesment = self.project_relevance(project)
      project.relevance = proj_assesment

    # Compute employments relevances
    logging.info('Employments relevance:')
    for employment in self._profile.employments:
      employment.relevance = self.employment_relevance(employment)
      logging.info('::: %s -> %f' % (employment.name, employment.relevance))

  def _update_relevance_limit(self, val):
    for empl, item in self._employmentItems.items():
      item.setCheckState(Qt.CheckState.Checked if empl.relevance >= val else Qt.CheckState.Unchecked)

    for task, item in self._taskItems.items():
      item.setCheckState(Qt.CheckState.Checked if task.relevance >= val else Qt.CheckState.Unchecked)

    for prj, item in self._projectItems.items():
      item.setCheckState(Qt.CheckState.Checked if prj.relevance >= val else Qt.CheckState.Unchecked)

    for skill, item in self._skillItems.items():
      item.setCheckState(Qt.CheckState.Checked if skill.relevance >= val else Qt.CheckState.Unchecked)

  def initializePage(self):
    self._compute_relevance()
    self._build_model()

    self._treeProfile.expandAll()
    # self._treeProfile.resizeColumnToContents(0)
    self._treeProfile.header().resizeSection(1, 40)
    self._treeProfile.header().resizeSection(0, 500)

    self._relevanceLimit.setValue(15)

  def filtered_profile(self):
    for empl, item in self._employmentItems.items():
      empl.keep = (item.checkState() == Qt.CheckState.Checked)

    for task, item in self._taskItems.items():
      task.keep = (item.checkState() == Qt.CheckState.Checked)

    for prj, item in self._projectItems.items():
      prj.keep = (item.checkState() == Qt.CheckState.Checked)

    for skill, item in self._skillItems.items():
      skill.keep = (item.checkState() == Qt.CheckState.Checked)

    pr_filter = profile_filter.ProfileFilter()
    res = pr_filter.create_relevant_projection(self._profile)
    res.compress()
    return res
