import os
import sys
import ctypes
import subprocess
from PyQt5.QtWidgets import QApplication, QSpacerItem, QWidget, QSizePolicy, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFileDialog, QMessageBox, QTextEdit
from PyQt5.QtGui import QColor, QCursor, QFont
from PyQt5.QtCore import Qt, QFileInfo

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LinkMaster')
        self.setStyleSheet("background-color: #2b2b2b; color: #a9b7c6;")  # Dark mode color scheme
        self.setFixedWidth(420)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.titleBar = QWidget()
        self.titleBar.setStyleSheet("background-color: #3b3b3b;")  # A bit lighter color than the main GUI
        self.titleBar.setFixedHeight(35)
        self.titleBarLayout = QVBoxLayout()
        self.titleBar.setLayout(self.titleBarLayout)

        self.titleLabel = QLabel(self.windowTitle())
        self.titleLabel.setAlignment(Qt.AlignCenter)
        font = QFont('Arial', 16)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleBarLayout.addWidget(self.titleLabel)

        layout.addWidget(self.titleBar)

        # QWidget for buttons
        self.buttonBar = QWidget()
        self.buttonBarLayout = QHBoxLayout()
        self.buttonBar.setLayout(self.buttonBarLayout)


        self.helpButton = QPushButton('?')
        self.helpButton.clicked.connect(self.showHelp)
        self.helpButton.setFixedWidth(12)
        self.buttonBarLayout.addWidget(self.helpButton)

        self.buttonBarLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.minimizeButton = QPushButton("-")
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.minimizeButton.setFixedSize(20, 20)
        self.buttonBarLayout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton("x")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setFixedSize(20, 20)
        self.buttonBarLayout.addWidget(self.closeButton)

        layout.addWidget(self.buttonBar)
        layout.addWidget(self.titleBar)

        self.sourceLabel = QLabel("Source: None")
        self.targetLabel = QLabel("Target: None")

        self.junctionButton = QPushButton('Create Directory Junction')
        self.junctionButton.clicked.connect(self.setJunction)
        self.junctionButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.symlinkButton = QPushButton('Create Symlink')
        self.symlinkButton.clicked.connect(self.setSymlink)
        self.symlinkButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.directoryLinkButton = QPushButton('Create Directory Link')
        self.directoryLinkButton.clicked.connect(self.setDirectoryLink)
        self.directoryLinkButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.generateButton = QPushButton('Generate Links')
        self.generateButton.clicked.connect(self.generateLinks)


        layout.addWidget(self.sourceLabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.targetLabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.junctionButton, alignment=Qt.AlignCenter)
        layout.addWidget(self.symlinkButton, alignment=Qt.AlignCenter)
        layout.addWidget(self.directoryLinkButton, alignment=Qt.AlignCenter)

        if not self.isAdmin():
            QMessageBox.warning(self, 'Warning', 'Administrator privileges are required for use.')

    def isAdmin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def showHelp(self):
        self.help_text = "this is a readme"
        self.help_window = QWidget()
        self.help_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.help_window.setStyleSheet("background-color: #2b2b2b; color: #a9b7c6;")

        help_text_edit = QTextEdit()
        help_text_edit.setReadOnly(True)
        help_text_edit.setText(self.help_text)

        ok_button = QPushButton("OK")
        ok_button.setFixedSize(50, 50)
        ok_button.clicked.connect(self.help_window.close)

        layout = QVBoxLayout()
        layout.addWidget(help_text_edit)
        layout.addWidget(ok_button, 0, Qt.AlignCenter)

        self.help_window.setLayout(layout)
        self.help_window.show()

    def setJunction(self):
        self.source = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if self.source:
            self.sourceLabel.setText(f"Source: {self.source}")
            self.target = QFileDialog.getExistingDirectory(self, 'Select Target Directory')
            if self.target:
                self.targetLabel.setText(f"Target: {self.target}")
                self.link_type = 'junction'

    def setSymlink(self):
        self.source = QFileDialog.getOpenFileName(self, 'Select Source File')[0]
        if self.source:
            self.sourceLabel.setText(f"Source: {self.source}")
            sourceFileInfo = QFileInfo(self.source)
            self.target, _ = QFileDialog.getSaveFileName(self, 'Select Target File', sourceFileInfo.fileName())
            if self.target:
                self.targetLabel.setText(f"Target: {self.target}")
                self.link_type = 'symlink'

    def setDirectoryLink(self):
        self.source = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if self.source:
            self.sourceLabel.setText(f"Source: {self.source}")
            sourceFileInfo = QFileInfo(self.source)
            self.target = QFileDialog.getExistingDirectory(self, 'Select Target Directory', sourceFileInfo.fileName())
            if self.target:
                self.targetLabel.setText(f"Target: {self.target}")
                self.link_type = 'directory_link'

    def generateLinks(self):
        if self.link_type == 'junction':
            self.createJunction()
        elif self.link_type == 'symlink':
            self.createSymlink()
        elif self.link_type == 'directory_link':
            self.createDirectoryLink()

    def createJunction(self):
        if os.path.exists(self.target):
            QMessageBox.warning(self, 'Error', 'Target directory already exists.')
        else:
            result = subprocess.run(f'mklink /J "{self.target}" "{self.source}"', shell=True, stderr=subprocess.PIPE)
            if result.returncode == 0:
                QMessageBox.information(self, 'Success', 'Directory Junction created successfully.')
            else:
                QMessageBox.warning(self, 'Error', f'Failed to create Directory Junction. Error: {result.stderr.decode()}')

    def createSymlink(self):
        if os.path.exists(self.target):
            QMessageBox.warning(self, 'Error', 'Target file already exists.')
        else:
            result = subprocess.run(f'mklink "{self.target}" "{self.source}"', shell=True, stderr=subprocess.PIPE)
            if result.returncode == 0:
                QMessageBox.information(self, 'Success', 'Symlink created successfully.')
            else:
                QMessageBox.warning(self, 'Error', f'Failed to create Symlink. Error: {result.stderr.decode()}')

    def createDirectoryLink(self):
        if os.path.exists(self.target):
            QMessageBox.warning(self, 'Error', 'Target directory already exists.')
        else:
            result = subprocess.run(f'mklink /D "{self.target}" "{self.source}"', shell=True, stderr=subprocess.PIPE)
            if result.returncode == 0:
                QMessageBox.information(self, 'Success', 'Directory Link created successfully.')
            else:
                QMessageBox.warning(self, 'Error', f'Failed to create Directory Link. Error: {result.stderr.decode()}')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_old_pos = event.pos()
            self.m_mouse_down = event.button() == Qt.LeftButton

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

        if self.m_mouse_down:
            self.move(self.pos() + (event.pos() - self.m_old_pos))

    def mouseReleaseEvent(self, event):
        m_mouse_down = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
