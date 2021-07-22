from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                             QLineEdit, QLabel, QComboBox, QFrame, QDialogButtonBox)
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
        self.extensionComboBox = QComboBox()
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.extensionComboBox.addItems(["png", "jpg"])
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        self.exportDirLineEdit.textChanged.connect(self.updateLabels)        
        self.formLayout.addRow(i18n("Directory name:"), self.exportDirLineEdit)
        self.formLayout.addRow(i18n("File prefix:"), self.namePrefixLineEdit)
        self.formLayout.addWidget(self.exampleLabel)
        self.formLayout.addWidget(self.line)
        self.formLayout.addRow(i18n("Extension:"), self.extensionComboBox)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)
        
        self.setWindowTitle(i18n("Export layers & anim"))
        self.resize(350, 100)

    def initialize(self):
        self.exportDirLineEdit.setText(self.exportCompositionAnim.exportDir)
        self.namePrefixLineEdit.setText(self.exportCompositionAnim.namePrefix)
        self.extensionComboBox.setCurrentText(self.exportCompositionAnim.extension)
        self.updateLabels()

        self.show()
        self.activateWindow()
        self.exec_()

    def updateLabels(self):
        self.exampleLabel.setText(i18n("Files path example:") + " "
            + os.path.join(self.exportCompositionAnim.exportPath, self.exportDirLineEdit.text()) 
            + self.namePrefixLineEdit.text() + "LAYERNAME_FRAME." + self.extensionComboBox.currentText())

    def accept(self):
        self.exportCompositionAnim.exportDir = self.exportDirLineEdit.text()
        self.exportCompositionAnim.namePrefix = self.namePrefixLineEdit.text()
        self.exportCompositionAnim.extension = self.extensionComboBox.currentText()
        self.exportCompositionAnim.export()

        super(ExportCompositionAnimDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
