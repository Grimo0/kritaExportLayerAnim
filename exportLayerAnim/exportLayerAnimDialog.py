from PyQt5.QtCore import (Qt)

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QLabel, QComboBox, 
                             QCheckBox, QFrame, 
                             QDialogButtonBox, QMessageBox)
import os


class ExportLayerAnimDialog(QDialog):

    def __init__(self, exportLayerAnim, parent=None):
        super(ExportLayerAnimDialog, self).__init__(parent)

        self.exportLayerAnim = exportLayerAnim

        self.mainLayout = QVBoxLayout(self)
        self.formLayout = QHBoxLayout()
        self.exportDirLineEdit = QLineEdit()
        self.namePrefixLineEdit = QLineEdit()
        self.exampleLabel = QLabel()
        self.helpLabel = QLabel()
        self.extensionComboBox = QComboBox()
        self.useCompositionsBox = QCheckBox(i18n("Use compositions"))
        self.firstFrameBox = QCheckBox(i18n("First frame only"))
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        self.exportDirLineEdit.textChanged.connect(self.updateLabels)
        self.namePrefixLineEdit.textChanged.connect(self.updateLabels)
        self.extensionComboBox.addItems(["png", "jpg"])
        self.exampleLabel.setWordWrap(True)
        self.exampleLabel.setTextFormat(Qt.RichText)
        self.exampleLabel.setIndent(5)
        self.useCompositionsBox.stateChanged.connect(self.updateLabels)
        self.firstFrameBox.stateChanged.connect(self.updateLabels)
        self.helpLabel.setWordWrap(True)
        self.helpLabel.setTextFormat(Qt.RichText)
        self.helpLabel.setText(i18n("Add the followings to layer's name:")
            + "<br/>- <code>NE</code>: " + i18n("won't be exported")
            + "<br/>- <code>EC</code>: " + i18n("export children")
        )
                
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.formLayout.addWidget(QLabel(i18n("Directory:")))
        self.formLayout.addWidget(self.exportDirLineEdit)
        self.formLayout.addWidget(QLabel(i18n("Prefix:")))
        self.formLayout.addWidget(self.namePrefixLineEdit)
        self.formLayout.addWidget(QLabel(i18n("Type:")))
        self.formLayout.addWidget(self.extensionComboBox)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.exampleLabel)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.useCompositionsBox)
        hLayout.addWidget(self.firstFrameBox)
        self.mainLayout.addLayout(hLayout)
        line = QFrame()
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.mainLayout.addWidget(line)
        self.mainLayout.addWidget(self.helpLabel)
        line = QFrame()
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken)
        self.mainLayout.addWidget(line)
        self.mainLayout.addWidget(self.buttonBox)
        
        self.setWindowTitle(i18n("Export layers & anim"))
        self.resize(400, 100)

    def initialize(self):
        self.exportDirLineEdit.setText(self.exportLayerAnim.exportDir)
        self.namePrefixLineEdit.setText(self.exportLayerAnim.namePrefix)
        self.extensionComboBox.setCurrentText(self.exportLayerAnim.extension)
        self.useCompositionsBox.setChecked(self.exportLayerAnim.useCompositions)
        self.firstFrameBox.setChecked(self.exportLayerAnim.firstFrame)
        self.updateLabels()

        self.show()
        self.activateWindow()
        self.exec_()

    def updateLabels(self):
        self.exampleLabel.setText(i18n("Files path example:") + " "
            + self.exportLayerAnim.exportPath 
            + ("/" + self.exportDirLineEdit.text() if self.exportDirLineEdit.text() != "" else "")
            + "/" + self.namePrefixLineEdit.text() 
            + "<i>" + (i18n("Composition") if self.useCompositionsBox.isChecked() else "")
            + ("_" if self.namePrefixLineEdit.text() != "" or self.useCompositionsBox.isChecked() else "") + (i18n("Layer_Frame") if not self.firstFrameBox.isChecked() else i18n("Layer"))
            + "</i>." + self.extensionComboBox.currentText())

    def accept(self):
        self.exportLayerAnim.exportDir = self.exportDirLineEdit.text()
        self.exportLayerAnim.namePrefix = self.namePrefixLineEdit.text()
        self.exportLayerAnim.extension = self.extensionComboBox.currentText()
        self.exportLayerAnim.useCompositions = self.useCompositionsBox.isChecked()
        self.exportLayerAnim.firstFrame = self.firstFrameBox.isChecked()
        self.exportLayerAnim.export()

        QMessageBox.information(Application.activeWindow().qwindow(), i18n("Exportation done"), i18n("Files created in") + " " + self.exportLayerAnim.exportPath + " :" + self.exportLayerAnim.layersName)

        super(ExportLayerAnimDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
