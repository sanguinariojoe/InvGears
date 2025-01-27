# ***************************************************************************
# *   Copyright (c) 2021 Sebastian Ernesto García <sebasg@outlook.com>      *
# *                                                                         *
# *   newSlaveCmd.py                                                        *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD as App
import FreeCADGui as Gui

from PySide2.QtWidgets import QDialogButtonBox

from freecad.invgears import local
from freecad.invgears.featureClasses import SlaveGear, ViewProviderSlaveGear
from freecad.invgears.widgets import GearWidget
from freecad.invgears.observers import SelObserver


class createInvoluteGears2():
    def __init__(self, fp_master, angle_list):

        list_s_gear = "[" + angle_list + "]"
        if list_s_gear:
            for item in eval(list_s_gear):
                body_slave = App.activeDocument().addObject('PartDesign::Body', 'body_slave')
                fp_slave = App.activeDocument().addObject("PartDesign::FeaturePython", "fp_slave")
                ViewProviderSlaveGear(fp_slave.ViewObject)
                SlaveGear(fp_slave, body_slave, fp_master, item)
                App.activeDocument().recompute()

        Gui.SendMsgToActiveView("ViewFit")


class SlaveGearTaskPanel:
    def __init__(self):
        self.form = GearWidget("Slave", self.attach_master_gear)
        self.master_gear_Button = self.form.master_gear_Button
        self.master_gear_Edit = self.form.master_gear_Edit
        self.print_warnings = self.form.print_warnings
        self.sel_o = SelObserver(self.master_gear_Button, self.master_gear_Edit, self.print_warnings)

        self.attach_master_gear()

    def attach_master_gear(self):
        self.master_gear_Button.setText("Selecting master gear...")
        self.master_gear_Button.setEnabled(False)
        self.sel_o.addSelection(0, 0, 0, 0)

    def accept(self):
        angle_list = self.form.list_angular_s_Edit2.text()
        if not self.sel_o.sel_flag:
            self.print_warnings.setText("First you have to choose a master gear and then click on ok.")
        elif not angle_list:
            self.print_warnings.setText("First you have to put angular locations and then click on ok.")
        else:
            createInvoluteGears2(self.sel_o.selection, angle_list)
            Gui.Selection.removeObserver(self.sel_o)
            Gui.Control.closeDialog()

    def reject(self):
        Gui.Selection.removeObserver(self.sel_o)
        Gui.Control.closeDialog()

    def getStandardButtons(self):
        return QDialogButtonBox.Cancel | QDialogButtonBox.Ok


class makeSlaveGearCmd():
    def GetResources(self):
        return {"MenuText": "Add Slave Gear",
                "ToolTip": "Add a new slave gear",
                "Pixmap": "slave_gear"}

    def IsActive(self):
        if App.activeDocument() is None:
            return False
        else:
            return True

    def Activated(self):
        panel = SlaveGearTaskPanel()
        Gui.Control.showDialog(panel)


Gui.addCommand('AddSlaveGear', makeSlaveGearCmd())
