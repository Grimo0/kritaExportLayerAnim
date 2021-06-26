from krita import *
import os
from PyQt5.QtWidgets import QMessageBox
from . import exportCompositionAnimDialog

class ExportCompositionAnim(Extension):

    def __init__(self, parent):
        super(ExportCompositionAnim, self).__init__(parent)

        # Png save info
        self.pngInfo = InfoObject()
        self.pngInfo.setProperty("alpha", True)
        self.pngInfo.setProperty("compression", 3)
        self.pngInfo.setProperty("forceSRGB", False)
        self.pngInfo.setProperty("indexed", False)
        self.pngInfo.setProperty("interlaced", False)
        self.pngInfo.setProperty("saveSRGBProfile", False)
        self.pngInfo.setProperty("transparencyFillcolor", [0,0,0])

    # Krita.instance() exists, so do any setup work
    def setup(self):
        pass

    def mkdir(self, directory):
        if (os.path.exists(directory) and os.path.isdir(directory)):
            return

        try:
            os.makedirs(directory)
        except OSError as e:
            raise e

    def initForExport(self):
        app = Krita.instance()
        self.doc = app.activeDocument()
        if not self.doc: return
        
        p = os.path.split(self.doc.fileName())
        self.exportPath = p[0]
        self.exportDir = os.path.splitext(p[1])[0]
        self.namePrefix = ""

    def export(self):
        app = Krita.instance()
        app.setBatchmode(True)

        # Create the folder if missing
        self.exportPath = os.path.join(self.exportPath, self.exportDir)
        self.mkdir(self.exportPath)

        # Gets animated layers list and export others
        self.layersName = ""
        topLevelLayers = self.doc.topLevelNodes()
        animatedLayers = []
        for node in topLevelLayers:
            if (node.type() != "paintlayer"
                and node.type() != "grouplayer"
                and node.type() != "filelayer"
                and node.type() != "vectorlayer"):
                continue
            if "NE" in node.name():
                continue
            if node.animated():
                animatedLayers.append(node)
            else:
                self.exportLayer(node)

        # Export animated layers
        currTime = self.doc.currentTime()
        i = 0
        while i < self.doc.animationLength():
            self.doc.setCurrentTime(i)

            for node in animatedLayers:
                if node.hasKeyframeAtTime(i):
                    self.exportLayer(node, i)
                
            i += 1
        
        self.doc.setCurrentTime(currTime)
        app.setBatchmode(False)

        # QMessageBox creates quick popup with information
        QMessageBox.information(app.activeWindow().qwindow(), i18n("Exportation done"), i18n("Files created in") + " " + self.exportPath + ":" + self.layersName)
        
    def exportLayer(self, node, anim = 0):
        fileName = self.namePrefix + node.name() + "_" + str(anim) + ".png"
        self.layersName += "\n" + fileName
        path = os.path.join(self.exportPath, fileName)
        bounds = QRect(0, 0, self.doc.width(), self.doc.height())
        node.save(path, self.doc.resolution() / 72., self.doc.resolution() / 72., self.pngInfo, bounds)

    # Show a dialogue asking for the folder name and files prefix
    def exportDialog(self):
        self.initForExport()
        if not self.doc: return
        
        app = Krita.instance()

        # QDialog & layout
        self.mainDialog = exportCompositionAnimDialog.ExportCompositionAnimDialog(self, app.activeWindow().qwindow())
        self.mainDialog.initialize()

    # called after setup(self)
    def createActions(self, window):
        action = window.createAction("export_composition_anim", i18n("Export composition anim"))
        action.setToolTip(i18n("Plugin to manipulate properties of selected documents."))
        action.triggered.connect(self.exportDialog)