# -*- coding: utf-8 -*-

"""
***************************************************************************
    CSVFieldSelectionPanel.py
    ---------------------
    Date                 : August 2017

        email                : hugues.boussard at inra.fr
***************************************************************************

"""

__author__ = 'Jean-Charles Naud'
__date__ = 'August 2017'
__copyright__ = '(C) 2017, Jean-Charles Naud'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QMenu, QAction, QInputDialog, QListWidget, QListWidgetItem, QDialog
from qgis.PyQt.QtGui import QCursor

from qgis.gui import QgsMessageBar, QgsExpressionBuilderDialog, QgsFileWidget
from qgis.core import QgsRasterLayer, QgsVectorLayer, QgsApplication
from qgis.utils import iface

from processing.gui.RectangleMapTool import RectangleMapTool
from processing.core.parameters import ParameterRaster
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterMultipleInput
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools import dataobjects

from processing.gui.ListMultiselectWidget import ListMultiSelectWidget



from .components.DialListCheckBox import DialListCheckBox
import math
import re

#from PyQt4.QtGui import

pluginPath = str(QgsApplication.pkgDataPath())
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'python','plugins','processing','ui', 'widgetBaseSelector.ui'))


class CSVFieldSelectionPanel(BASE, WIDGET):

    def __init__(self, dialog, alg, default=None):
        super(CSVFieldSelectionPanel, self).__init__(None)
        self.setupUi(self) 
        self.dialog = dialog
        self.params = alg.parameters
        self.alg = alg
        if hasattr(self.leText, 'setPlaceholderText'):
            self.leText.setPlaceholderText('Field 1;Field 2')
        
        self.btnSelect.clicked.connect(self.selectValues) # Bouton "..."


    def selectValues(self):
        """Values selector
            return item (duck typing)
        """
        # Get initial value
        text = self.leText.text()
        texts = text.split(';')
        values = ""

        p = self.alg.getParameterFromName("INPUT_FILE_CSV")
        f_input = p.value

        if f_input:
            with open(f_input,'r') as f:
                line = f.readline()
                line = line.rstrip('\n') # Delete \n
                fields = line.split(';')
                fields.remove('X')       # remove "X" field
                fields.remove('Y')       # remove "Y" field


            # Dialog list check box
            dial = DialListCheckBox(values=fields,checked_values=texts)
            result = dial.run()
        else:
            result = ""
        # result
        self.leText.setText(result)


    def getValue(self):
        return unicode(self.leText.text())

    def setExtentFromString(self, s):
        self.leText.setText(s)

    def text(self):
        return self.leText

