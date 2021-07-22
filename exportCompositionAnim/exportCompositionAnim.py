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

        # Jpg save info
        self.jpgInfo = InfoObject()
        self.jpgInfo.setProperty('quality', 85)           # 0 (high compression/low quality) to 100 (low compression/higher quality)
        self.jpgInfo.setProperty('smoothing', 0)         # 0 to 100    
        self.jpgInfo.setProperty('subsampling', 0)        # 0=4:2:0 (smallest file size)   1=4:2:2    2=4:4:0     3=4:4:4 (Best quality)
        self.jpgInfo.setProperty('progressive', False)
        self.jpgInfo.setProperty('optimize', True)
        self.jpgInfo.setProperty('saveProfile', True)
        self.jpgInfo.setProperty("transparencyFillcolor", [0,0,0])

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
        self.doc = Application.activeDocument()
        if not self.doc: return
        
        p = os.path.split(self.doc.fileName())
        self.exportPath = p[0]
        filename = os.path.splitext(p[1])[0]
        exportPath = os.path.join(self.exportPath, filename)
        if (os.path.exists(exportPath) and os.path.isdir(exportPath)):
            self.exportDir = filename
            self.namePrefix = ""
        else:
            self.exportDir = ""
            self.namePrefix = filename
        self.extension = "png"

    def export(self):
        Application.setBatchmode(True)

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
            elif node.type() == "grouplayer":
                child = node.childNodes()
                animated = False
                for c in child:
                    if c.animated():
                        animated = True
                        break
                if animated: animatedLayers.append(node)
                else: self.exportLayer(node)
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
                elif node.type() == "grouplayer":
                    child = node.childNodes()
                    for c in child:
                        if c.hasKeyframeAtTime(i):
                            self.exportLayer(node, i)
                            break
                
            i += 1
        
        if i > 1 :
            self.doc.setCurrentTime(currTime)
        Application.setBatchmode(False)

        # QMessageBox creates quick popup with information
        QMessageBox.information(Application.activeWindow().qwindow(), i18n("Exportation done"), i18n("Files created in") + " " + self.exportPath + " :" + self.layersName)
        
    def exportLayer(self, node, anim = 0):
        fileName = self.namePrefix + node.name() + "_" + str(anim) + "." + self.extension
        self.layersName += "\n" + fileName
        path = os.path.join(self.exportPath, fileName)
        bounds = QRect(0, 0, self.doc.width(), self.doc.height())
        if self.extension == "png":
            node.save(path, self.doc.resolution() / 72., self.doc.resolution() / 72., self.pngInfo, bounds)
        else:
            node.save(path, self.doc.resolution() / 72., self.doc.resolution() / 72., self.jpgInfo, bounds)

    # Show a dialogue asking for the folder name and files prefix
    def exportDialog(self):
        self.initForExport()
        if not self.doc: return
        
        # QDialog & layout
        self.mainDialog = exportCompositionAnimDialog.ExportCompositionAnimDialog(self, Application.activeWindow().qwindow())
        self.mainDialog.initialize()

    # called after setup(self)
    def createActions(self, window):
        action = window.createAction("export_composition_anim", i18n("Export composition anim"))
        action.setToolTip(i18n("Plugin to manipulate properties of selected documents."))
        action.triggered.connect(self.exportDialog)