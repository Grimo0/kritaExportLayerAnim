from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                             QLineEdit, QLabel, QComboBox, QFrame, QDialogButtonBox)
import os


class ExportLayerAnimDialog(QDialog):

    def __init__(self, exportLayerAnim, parent=None):
        super(ExportLayerAnimDialog, self).__init__(parent)

        self.exportLayerAnim = exportLayerAnim

        self.mainLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.exportDirLineEdit = QLineEdit()
        self.namePrefixLineEdit = QLineEdit()
        self.exampleLabel = QLabel()
        self.extensionComboBox = QComboBox()
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.exampleLabel.setWordWrap(True)
        self.extensionComboBox.addItems(["png", "jpg"])
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        self.exportDirLineEdit.textChanged.connect(self.updateLabels)        
        self.formLayout.addRow(i18n("Directory name:"), self.exportDirLineEdit)
        self.formLayout.addRow(i18n("File prefix:"), self.namePrefixLineEdit)
        self.formLayout.addWidget(self.exampleLabel)
        self.formLayout.addRow(i18n("Extension:"), self.extensionComboBox)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)
        
        self.setWindowTitle(i18n("Export layers & anim"))
        self.resize(400, 100)

    def initialize(self):
        self.exportDirLineEdit.setText(self.exportLayerAnim.exportDir)
        self.namePrefixLineEdit.setText(self.exportLayerAnim.namePrefix)
        self.extensionComboBox.setCurrentText(self.exportLayerAnim.extension)
        self.updateLabels()

        self.show()
        self.activateWindow()
        self.exec_()

    def updateLabels(self):
        self.exampleLabel.setText(i18n("Files path example:") + " "
            + self.exportLayerAnim.exportPath + "/" + self.exportDirLineEdit.text() + "/"
            + self.namePrefixLineEdit.text() + "LAYERNAME_FRAME." + self.extensionComboBox.currentText())

    def accept(self):
        self.exportLayerAnim.exportDir = self.exportDirLineEdit.text()
        self.exportLayerAnim.namePrefix = self.namePrefixLineEdit.text()
        self.exportLayerAnim.extension = self.extensionComboBox.currentText()
        self.exportLayerAnim.export()

        super(ExportLayerAnimDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
