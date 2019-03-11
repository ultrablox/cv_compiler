from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPlainTextEdit, QHBoxLayout, QListView, QWizardPage
from PyQt5.QtCore import QSize, Qt, QSortFilterProxyModel, QRandomGenerator
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QStandardItemModel, QStandardItem, QBrush, QIcon, QPixmap
from vacancy_analyzer import analyzer


class SkillSortModel(QSortFilterProxyModel):
  def __init__(self):
    QSortFilterProxyModel.__init__(self)

  def lessThan(self, left_idx, right_idx):
    left = self.sourceModel().itemFromIndex(left_idx)
    right = self.sourceModel().itemFromIndex(right_idx)

    if left.checkState() == right.checkState():
      return left.text() < right.text()
    else:
      return left.checkState() > right.checkState()


class SkillExtractWidget(QWizardPage):
  def __init__(self, skills_db):
    QWizardPage.__init__(self)

    self._generate_colors()

    self._skillDb = skills_db

    self.setMinimumSize(QSize(640, 480))
    self.setTitle("Extracted Skills")

    # centralWidget = QWidget(self)
    # self.setCentralWidget(centralWidget)

    lyt = QHBoxLayout(self)
    self.setLayout(lyt)

    self.textEdit = QPlainTextEdit(self)
    self.textEdit.setPlaceholderText('Paste vacancy text here')
    lyt.addWidget(self.textEdit, 3)

    self._matchedList = QListView(self)
    lyt.addWidget(self._matchedList, 1)

    self._load_skills()

    self.textEdit.textChanged.connect(self._extract_skills)
    self._extractionActive = False

  def _generate_colors(self):
    self._randomColors = []
    for i in range(0, 64):
      self._randomColors += [QColor.fromRgb(QRandomGenerator.global_().generate())]

  def _load_skills(self):
    self._skillsModel = QStandardItemModel()

    sortModel = SkillSortModel()
    sortModel.setSourceModel(self._skillsModel)
    sortModel.sort(0, Qt.AscendingOrder)

    self._matchedList.setModel(sortModel)

    self._skillItems = {}
    for skill in self._skillDb.skills:
      item = QStandardItem(skill.name)
      item.setCheckable(True)
      self._skillsModel.appendRow(item)
      self._skillItems[skill] = item

  def _clear_flash(self):
    cursor = self.textEdit.textCursor()
    cursor.setPosition(0, QTextCursor.MoveAnchor)
    cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
    cursor.setCharFormat(QTextCharFormat())

  def _clear_checked(self):
    for k, v in self._skillItems.items():
      v.setCheckState(Qt.CheckState.Unchecked)

  def _random_color(self, index):
    return self._randomColors[index]

  def _extract_skills(self):
    if not self._extractionActive:
      self._extractionActive = True
      self._clear_flash()
      self._clear_checked()

      v_analyzer = analyzer.Analyzer(self._skillDb)
      v_analyzer.parse(self.textEdit.toPlainText())

      idx = 0
      for skill in v_analyzer.matched_skills():
        self.flash_skill(skill.skill, skill.pos, skill.len, self._random_color(idx))
        idx += 1

      self._extractionActive = False

  def flash_skill(self, skill, pos, word_len, color):
    cursor = self.textEdit.textCursor()
    cursor.setPosition(pos, QTextCursor.MoveAnchor)
    cursor.setPosition(pos + word_len, QTextCursor.KeepAnchor)

    fmt = QTextCharFormat()
    fmt.setBackground(color)
    cursor.setCharFormat(fmt)

    skill_item = self._skillItems[skill]

    skill_item.setCheckState(Qt.CheckState.Checked)

    pix = QPixmap(16, 16)
    pix.fill(color)
    skill_item.setIcon(QIcon(pix))

  def matched_skills(self):
    res = []
    for k, v in self._skillItems.items():
      if v.checkState() == Qt.CheckState.Checked:
        res += [k.name]
    return res
