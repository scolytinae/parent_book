# -*- coding:utf-8 -*-
from PyQt4 import QtCore, QtGui, uic


class SettingsDialog(QtGui.QDialog):

    def __init__(self):
        super(SettingsDialog, self).__init__()
        uic.loadUi("settings.ui", self)
 
        # signal/slot
        self.connect(self.tbSourceDialog, QtCore.SIGNAL("clicked()"), self.show_source_dialog)
        self.connect(self.tbDestDialog, QtCore.SIGNAL("clicked()"), self.show_dest_dialog)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

    def show_source_dialog(self):
        self.leSource.setText(self.show_file_dialog(self.leSource.text()))

    def show_dest_dialog(self):
        self.leDest.setText(self.show_file_dialog(self.leDest.text()))

    def show_file_dialog(self, default_dir):
        dialog = QtGui.QFileDialog()
        dialog.setWindowTitle(u"Выбрать директорию")
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setDirectory(default_dir)

        if dialog.exec_() == QtGui.QFileDialog.Accepted:
            return dialog.selectedFiles()[0]

        return default_dir