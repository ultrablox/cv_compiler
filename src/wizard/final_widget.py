from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPlainTextEdit, QVBoxLayout, QListView, QWizardPage, QTreeView, QSlider, QPushButton, QSpinBox
from PyQt5.QtCore import QSize, Qt, QSortFilterProxyModel, QRandomGenerator, QUrl
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QStandardItemModel, QStandardItem, QBrush, QIcon, QPixmap, QDesktopServices
from utils import *
import shutil
import tempfile
from tex_cards_printer import *
from letter import cl_printer


class FinalWidget(QWizardPage):
  def __init__(self, profile_filter_page, letter_wdg, input_dir):
    QWizardPage.__init__(self)
    self._profileFilter = profile_filter_page
    self._letterWidget = letter_wdg
    self._profileInputDir = input_dir
    self._outDir = tempfile.mkdtemp()

    bnCompile = QPushButton('Compile')
    bnCompile.clicked.connect(self._compile_data)

    bnOpenDir = QPushButton('Open Output Directory')
    bnOpenDir.clicked.connect(self._open_out_dir)

    # , 'Visual Skill Count'
    self._visualSkillCount = QSpinBox(self)
    self._visualSkillCount.setValue(10)

    lyt = QVBoxLayout()
    lyt.addWidget(self._visualSkillCount)
    lyt.addWidget(bnCompile)
    lyt.addWidget(bnOpenDir)
    self.setLayout(lyt)

  def __del__(self):
    shutil.rmtree(self._outDir)

  def _open_out_dir(self):
    # print('openin'g)
    QDesktopServices.openUrl(QUrl('file:///{}'.format(self._outDir), QUrl.TolerantMode))

  def _compile_cv(self, profile):
    out_fname = os.path.join(self._outDir, '%s_CV.pdf' % to_file_name(profile.personal['name']))

    with tempfile.TemporaryDirectory() as tmpdir:
      profile.save_to(tmpdir)
      with TexCardsPrinter(out_fname) as tex_printer:
        tex_printer.rcPaths = [os.path.join(os.pardir, 'resources'), tmpdir, self._profileInputDir]

        # Copy static resources
        for file in glob.glob(r'../resources/styles/*.*') + glob.glob(r'../resources/fonts/*.*'):
          shutil.copy(file, tex_printer.tmpDirName)
  
        cfg = {
          'visual_skill_count': self._visualSkillCount.value(),
        }

        tex_printer.print_profile(profile, cfg)

  def _compile_letter(self, profile):
    body = self._letterWidget.assemble_body()

    out_fname = os.path.join(self._outDir, '%s_letter.pdf' % to_file_name(profile.personal['name']))

    with cl_printer.LetterPrinter(out_fname, profile) as tex_printer:
      tex_printer._company = self._letterWidget.company_name()
      tex_printer._role = self._letterWidget.role()

      with cl_printer.LetterDocument(tex_printer):
        tex_printer.print_heading()

        for section in body:
          tex_printer.write([
            section,
            ''
          ])

        tex_printer.write([r'\makeletterclosing'])

  def initializePage(self):
    pass

  def _compile_data(self):
    profile = self._profileFilter.filtered_profile()
    self._compile_letter(profile)
    self._compile_cv(profile)
