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

    @property
    def source(self):
        return unicode(self.leSource.text())

    @source.setter
    def source(self, value):
        self.leSource.setText(value)

    @property
    def dest(self):
        return unicode(self.leDest.text())

    @dest.setter
    def dest(self, value):
        self.leDest.setText(value)

    def show_source_dialog(self):
        self.source = self.show_file_dialog(self.source)

    def show_dest_dialog(self):
        self.dest = self.show_file_dialog(self.dest)

    def show_file_dialog(self, default_dir):
        dialog = QtGui.QFileDialog()
        dialog.setWindowTitle(u"Выбрать директорию")
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setDirectory(default_dir)

        if dialog.exec_() == QtGui.QFileDialog.Accepted:
            return dialog.selectedFiles()[0]

        return default_dir