from krita import *
import os
from . import exportLayerAnimDialog

class ExportLayerAnim(Extension):

    def __init__(self, parent):
        super(ExportLayerAnim, self).__init__(parent)

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

    def isLayerAnimated(self, node):
        if node.animated():
            return True
        elif node.type() == "grouplayer":
            child = node.childNodes()
            for c in child:
                if c.animated():
                    return True
                elif c.type() == "grouplayer" and self.isLayerAnimated(c):
                    return True
        return False

    def getCompositionIdx(self, name):
        # Get composition docker, view, model
        docker = next(d for d in Application.dockers() if d.objectName() == 'CompositionDocker')
        view = docker.findChild(QListView, 'compositionView')
        model = view.model()

        # Get a composition based on its name
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            text = index.data(role=Qt.DisplayRole)
            if text == name:
                return index
        else:
            raise RuntimeError(f'Unknown composition. (did get: {name=})')

    # A generator activating compositions one by one then returning to the previous state
    def composition(self):
        if not self.useCompositions:
            yield ""
            return

        # Get composition docker
        docker = next(d for d in Application.dockers() if d.objectName() == 'CompositionDocker')
        view = docker.findChild(QListView, 'compositionView')
        model = view.model()
        
        meta = docker.metaObject()
        activated = meta.method(meta.indexOfSlot(b'activated(QModelIndex)'))

        # Save current state
        saveClicked = meta.method(meta.indexOfSlot(b'saveClicked()'))
        saveClicked.invoke(docker)

        try:
            # Browse all composition
            for row in range(model.rowCount() - 1): # -1 because of the saved compo
                index = model.index(row, 0)
                checked_state = index.data(role=Qt.CheckStateRole)
                if checked_state == Qt.Checked:
                    # Activate the composition  
                    activated.invoke(docker, Q_ARG("QModelIndex", index))
                    yield index.data(role=Qt.DisplayRole)

        finally:
            lastIdx = model.index(model.rowCount() - 1, 0)

            # Reverse to the previous state
            activated.invoke(docker, Q_ARG("QModelIndex", lastIdx))

            # Remove the tmp save
            selectionModel = view.selectionModel()
            selectionModel.setCurrentIndex(lastIdx, QItemSelectionModel.Current)
            deleteClicked = meta.method(meta.indexOfSlot(b'deleteClicked()'))
            deleteClicked.invoke(docker)

    def initForExport(self):
        self.doc = Application.activeDocument()
        if not self.doc: return
        
        self.layersName = ""

        p = os.path.split(self.doc.fileName())
        self.exportPath = p[0]
        filename = os.path.splitext(p[1])[0]
        path = self.exportPath + "/" + filename
        if (os.path.exists(path) and os.path.isdir(path)):
            self.exportDir = filename
            self.namePrefix = ""
        else:
            self.exportDir = ""
            self.namePrefix = filename
        self.extension = "png"
        self.useCompositions = False

    def export(self):
        Application.setBatchmode(True)

        # Create the folder if missing
        self.exportPath = self.exportPath + "/" + self.exportDir
        self.mkdir(self.exportPath)

        haveAnimatedLayers = False
        for compo in self.composition():
            # Gets animated layers list and export others
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
                if node.type() == "grouplayer" and "EC" in node.name():
                    child = node.childNodes()
                    for c in child:
                        topLevelLayers.append(c)
                else:
                    if self.isLayerAnimated(node):
                        animatedLayers.append(node)
                    else: 
                        self.exportLayer(node, compo)

            # Export animated layers
            if range(animatedLayers) > 0:
                haveAnimatedLayers = True
                for i in range(self.doc.animationLength()):
                    self.doc.setCurrentTime(i)

                    for node in animatedLayers:
                        if node.hasKeyframeAtTime(i):
                            self.exportLayer(node, compo, "_" + str(i))
                        elif node.type() == "grouplayer":
                            child = node.childNodes()
                            for c in child:
                                if c.hasKeyframeAtTime(i):
                                    self.exportLayer(node, compo, "_" + str(i))
                                    break
        
        # Undo the setCurrentTime
        if haveAnimatedLayers and self.doc.animationLength() > 0:
            Application.action('edit_undo').trigger()
            self.doc.save()
        Application.setBatchmode(False)
    
    # Create a file for the specified layer
    def exportLayer(self, node, prefix = "", suffix = ""):
        fileName = f'{self.namePrefix}{prefix}{"_" if self.namePrefix != "" or prefix != "" else ""}{node.name()}{suffix}.{self.extension}'
        self.layersName += "\n" + fileName
        path = self.exportPath + "/" + fileName
        bounds = QRect(0, 0, self.doc.width(), self.doc.height())
        if self.extension == "png":
            node.save(path, self.doc.resolution() / 72., self.doc.resolution() / 72., self.pngInfo, bounds)
        else:
            node.save(path, self.doc.resolution() / 72., self.doc.resolution() / 72., self.jpgInfo, bounds)

    # Show a dialogue asking for the folder name and files prefix
    def exportDialog(self):
        self.initForExport()
        if not self.doc: return
        
        self.mainDialog = exportLayerAnimDialog.ExportLayerAnimDialog(self, Application.activeWindow().qwindow())
        self.mainDialog.initialize()

    # called after setup(self)
    def createActions(self, window):
        action = window.createAction("export_layer_anim", i18n("Export layer anim"))
        action.setToolTip(i18n("Plugin to manipulate properties of selected documents."))
        action.triggered.connect(self.exportDialog)