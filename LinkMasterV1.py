import os
import sys
import ctypes
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy, QPushButton, QVBoxLayout, QFileDialog, QLabel, QMessageBox, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Directory Junctions, Symlinks, and Directory Links Creator')
        self.setStyleSheet("background-color: #2b2b2b; color: #a9b7c6;")  # Dark mode color scheme
        # Set the size of the main GUI
        #self.setFixedSize(300, 300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

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
        self.generateButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.helpButton = QPushButton('?')
        self.helpButton.clicked.connect(self.showHelp)
        # Set the font size of the "?" button
    #    self.helpButton.setStyleSheet("font-size: 14pt;")
    #    self.helpButton.setFixedSize(50, 50)
        self.helpButton.setFixedWidth(12)

        layout.addWidget(self.sourceLabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.targetLabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.junctionButton, alignment=Qt.AlignCenter)
        layout.addWidget(self.symlinkButton, alignment=Qt.AlignCenter)
        layout.addWidget(self.directoryLinkButton, alignment=Qt.AlignCenter)

        # Create a QGridLayout
        gridLayout = QGridLayout()

        # Create the generateButton and add it to the grid layout
        self.generateButton = QPushButton('Generate Links')
        self.generateButton.clicked.connect(self.generateLinks)
        self.generateButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        gridLayout.addWidget(self.generateButton, 0, 1)  # Add the button to the center column

        # Create the helpButton and add it to the grid layout
        self.helpButton = QPushButton('?')
        self.helpButton.clicked.connect(self.showHelp)
        self.helpButton.setFixedWidth(12)
        gridLayout.addWidget(self.helpButton, 0, 2, alignment=Qt.AlignRight)  # Add the button to the right column

        # Add the grid layout to the main QVBoxLayout
        layout.addLayout(gridLayout)

        # Check for administrator privileges
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
        self.help_window.setStyleSheet("background-color: #2b2b2b; color: #a9b7c6;")  # Same color scheme as the main GUI

        help_text_edit = QTextEdit()
        help_text_edit.setReadOnly(True)
        help_text_edit.setText(self.help_text)

        # Add an "OK" button that closes the help window when clicked
        ok_button = QPushButton("OK")
        ok_button.setFixedSize(50, 50)  # Set the size of the "OK" button to 50x50 pixels
        ok_button.clicked.connect(self.help_window.close)

        layout = QVBoxLayout()
        layout.addWidget(help_text_edit)
        layout.addWidget(ok_button, 0, Qt.AlignCenter)  # Center the "OK" button

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
            self.target, _ = QFileDialog.getSaveFileName(self, 'Select Target File')
            if self.target:
                self.targetLabel.setText(f"Target: {self.target}")
                self.link_type = 'symlink'

    def setDirectoryLink(self):
        self.source = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if self.source:
            self.sourceLabel.setText(f"Source: {self.source}")
            self.target = QFileDialog.getExistingDirectory(self, 'Select Target Directory')
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
