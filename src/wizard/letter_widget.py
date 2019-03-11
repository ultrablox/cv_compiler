from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QFormLayout, QListView, QWizardPage, QTreeView, QSlider, QPushButton, QGroupBox, QRadioButton, QLineEdit
from PyQt5.QtCore import QSize, Qt, QSortFilterProxyModel, QRandomGenerator, QUrl
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QStandardItemModel, QStandardItem, QBrush, QIcon, QPixmap, QDesktopServices
from utils import *
import shutil
import tempfile
from tex_cards_printer import *
from letter import letter_project


class LetterWidget(QWizardPage):
  def __init__(self, letter_path, filter_widget):
    QWizardPage.__init__(self)
    self._letterProject = letter_project.LetterProject()
    self._letterProject.deserialize(letter_path)
    self._profileFilter = filter_widget
    self._checkedSections = {}

    lyt = QVBoxLayout()
    self.setLayout(lyt)

    self._edRole = QLineEdit(self)
    self._edRole.setText('Software Engineer')

    self._edCompany = QLineEdit(self)
    self._edCompany.setText('UltraSofrware')

    formLyt = QFormLayout()
    formLyt.addRow('Role', self._edRole)
    formLyt.addRow('Company', self._edCompany)
    lyt.addLayout(formLyt)

  def _select_section(self, sec):
    self._checkedSections[sec._kind] = sec

  def initializePage(self):
    profile = self._profileFilter.filtered_profile()
    # self._letterProject.create_intro_section(profile.personal['name'], 'Software Engineer')

    for sec_id in letter_project.SectionId:
      groupBox = QGroupBox(str(sec_id))
      self.layout().addWidget(groupBox)

      hbox = QHBoxLayout()
      groupBox.setLayout(hbox)

      hbox.addStretch()
      for sec in self._letterProject.variants(sec_id):
        item_box = QHBoxLayout()

        radio = QRadioButton()
        radio.clicked.connect(lambda: self._select_section(sec))
        label = QLabel(sec._text)
        label.setFixedWidth(300)
        label.setWordWrap(True)

        item_box.addWidget(radio)
        item_box.addWidget(label)

        hbox.addLayout(item_box)

        radio.click()

      hbox.addStretch()

  def assemble_body(self):
    res = []
    for sec_id in letter_project.SectionId:
      res += [self._checkedSections[sec_id]._text]
    return res

  def company_name(self):
    return self._edCompany.text()

  def role(self):
    return self._edRole.text()
