import os

__author__ = 'sofiaelm'
import manager
import maya.cmds as cmds
from pymel.all import mel
import pymel.core as pm


SCENE_FOLDER = "scenes"
TURNTABLE_FOLDER = "turnTable"
EXPORT_FOLDER = "export"
SOURCEIMAGES_FOLDER = "sourceimages"
startDir = "S:\3DDA_12\Student_shared\semester5\gameDevelopment\02_production\assets"


    # Gets first and last letter of username
def getAuthorInitials():
    user = os.getenv('user', "na")
    return str(user[0] + user[-1]).lower()


class ModuleScene(manager.Module):

    cleanScene = "cleanScene"

    def __init__(self, mngr):
        manager.Module.__init__(self, mngr)

    def new_scene(self):
        window = None

        cmds.file(newFile=True, force=True)
        location = "{0}{1}{2}".format(os.path.dirname(os.path.realpath(__file__)), os.path.sep, self.cleanScene)
        self.set_project(location)
        cmds.file("cleanScene.ma", open=True)


        selectDir = pm.fileDialog2(fileMode=2,dialogStyle=3,startingDirectory=startDir)
        print selectDir[0]
        sDir = str(selectDir[0])

        result = cmds.promptDialog(
                        title='Asset Name',
                        message='Enter Name:',
                        button=['OK', 'Cancel'],
                        defaultButton='OK',
                        cancelButton='Cancel',
                        dismissString='Cancel')

        if result == 'OK':
            assetName = cmds.promptDialog(query=True, text=True)
        print assetName

        # makes project folder
        projectFolder = os.path.join(sDir, assetName)
        if not os.path.exists(projectFolder):
              print "Creating {0}".format(projectFolder)
              os.makedirs(projectFolder)

        # makes scenes folder
        scenesFolder = os.path.join(projectFolder, SCENE_FOLDER)
        if not os.path.exists(scenesFolder):
              print "Creating {0}".format(scenesFolder)
              os.makedirs(scenesFolder)

         # makes turntable folder
        turntableFolder = os.path.join(projectFolder, TURNTABLE_FOLDER)
        if not os.path.exists(turntableFolder):
              print "Creating {0}".format(turntableFolder)
              os.makedirs(turntableFolder)

         # makes export folder
        exportFolder = os.path.join(projectFolder, EXPORT_FOLDER)
        if not os.path.exists(exportFolder):
              print "Creating {0}".format(exportFolder)
              os.makedirs(exportFolder)

        # makes sourceimages folder
        sourceimagesFolder = os.path.join(projectFolder, SOURCEIMAGES_FOLDER)
        if not os.path.exists(sourceimagesFolder):
              print "Creating {0}".format(sourceimagesFolder)
              os.makedirs(sourceimagesFolder)



        fileName = assetName + "_v001_" + getAuthorInitials() + ".ma"
        fileSavePath = os.path.join(scenesFolder, fileName)
        print fileSavePath
        cmds.file(rename=fileSavePath)
        cmds.file(save=True)

        self.setProjectAsCurrDirectory()
        cmds.currentUnit( linear='m' )


    def set_project(self, location):
        mel.setProject(location)

    def setProjectAsCurrDirectory(self):
        filePath = cmds.file(query =True, expandName=True)
        directory = os.path.dirname(filePath)
        project = os.path.dirname(directory)
        self.set_project(project)

    def importRefCube(self):
        location = "{0}{1}{2}".format(os.path.dirname(os.path.realpath(__file__)), os.path.sep, self.cleanScene)
        self.set_project(location)
        cmds.file("refCube.ma", i=True)
        self.setProjectAsCurrDirectory()

    def create_ui(self):

        tab = str(cmds.columnLayout())
        cmds.separator(style="none")
        cmds.frameLayout(collapsable=True, label="Common")
        cmds.columnLayout()
        cmds.button(command=lambda *args: self.new_scene(), label="New Work Scene")
        cmds.button(command=lambda *args: self.setProjectAsCurrDirectory(), label="Set Project")
        cmds.button(command=lambda *args: self.importRefCube(), label="Import Reference Cube")
        cmds.button(command=lambda *args: mel.deleteUnusedNodes(), label="Delete Unused Nodes")
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        return tab, "Scene"


def initModule(manager):
    return ModuleScene(manager)