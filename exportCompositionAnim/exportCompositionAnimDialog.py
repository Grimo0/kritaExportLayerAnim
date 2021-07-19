from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                             QLineEdit, QLabel, QFrame, QDialogButtonBox)
import os


class ExportCompositionAnimDialog(QDialog):

    def __init__(self, exportCompositionAnim, parent=None):
        super(ExportCompositionAnimDialog, self).__init__(parent)

        self.exportCompositionAnim = exportCompositionAnim

        self.mainLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.exportDirLineEdit = QLineEdit()
        self.namePrefixLineEdit = QLineEdit()
        self.exampleLabel = QLabel()
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        self.exportDirLineEdit.textChanged.connect(self.updateLabels)        
        self.formLayout.addRow(i18n("Directory name:"), self.exportDirLineEdit)
        self.formLayout.addRow(i18n("File prefix:"), self.namePrefixLineEdit)
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.exampleLabel)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)
        
        self.setWindowTitle(i18n("Export layers & anim"))
        self.resize(300, 100)

    def initialize(self):
        self.exportDirLineEdit.setText(self.exportCompositionAnim.exportDir)
        self.namePrefixLineEdit.setText(self.exportCompositionAnim.namePrefix)
        self.updateLabels()

        self.show()
        self.activateWindow()
        self.exec_()

    def updateLabels(self):
        self.exampleLabel.setText(i18n("Files path example:") + " "
            + os.path.join(self.exportCompositionAnim.exportPath, self.exportDirLineEdit.text()) 
            + self.namePrefixLineEdit.text() + "LAYERNAME_FRAME.png")

    def accept(self):
        self.exportCompositionAnim.exportDir = self.exportDirLineEdit.text()
        self.exportCompositionAnim.namePrefix = self.namePrefixLineEdit.text()
        self.exportCompositionAnim.export()

        super(ExportCompositionAnimDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
