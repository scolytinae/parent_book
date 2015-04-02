# -*- coding:utf-8 -*-
from os import listdir, path
from shutil import rmtree
from PyQt4 import QtCore, QtGui, uic
from settings import SettingsDialog


import unpacker

DEFAULT_SOURCE = u'/home/igor/Загрузки'

DEFAULT_DEST = u'/home/igor'

PACKER_RULES = {
    "rar": unpacker.unpack_rar,
    "zip": unpacker.unpack_zip,
    "txt": unpacker.unpack_file,
    "fb2": unpacker.unpack_file,
    "epub": unpacker.unpack_file,
    "pdf": unpacker.unpack_file
}

AVAIL_EXT = ["txt", "fb2", "epub", "pdf"]


class MainForm(QtGui.QDialog):

    def __init__(self):
        super(MainForm, self).__init__()
        uic.loadUi("mainform.ui", self)

        self.file_watcher = QtCore.QFileSystemWatcher()
        self.packers = PACKER_RULES
        self.source = DEFAULT_SOURCE
        self.dest = DEFAULT_DEST

        self.list_dest_menu = QtGui.QMenu(self.listDest)
        self.list_dest_menu.addAction(u"Удалить файл", self.act_delete_file)

        # signal/slot
        self.listDest.customContextMenuRequested.connect(self.dest_show_menu)
        self.listDest.itemDoubleClicked.connect(self.dest_double_clicked)
        self.file_watcher.directoryChanged.connect(self.files_changed)
        self.btnSettings.clicked.connect(self.show_settings_dialog)
        self.btnCopy.clicked.connect(self.copy_book)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if hasattr(self, "_source") and self.source != self.dest:
            self.file_watcher.removePath(self.source)
        self._source = value
        self.listSource.clear()
        self.fill_source_list()
        self.file_watcher.addPath(self.source)

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, value):
        if hasattr(self, "_dest") and self.source != self.dest:
            self.file_watcher.removePath(self.dest)
        self._dest = value
        self.listDest.clear()
        self.fill_dest_list()
        self.file_watcher.addPath(self.dest)

    def dest_double_clicked(self, item):
        abs_path = path.join(self.dest, unicode(item.text()))
        if path.isdir(abs_path):
            self.dest = abs_path

    def filtered_source_dir(self, dir):
        def file_filter(f):
            try:
                fname = path.join(self.source, f)
                return path.isfile(fname) and \
                    (path.splitext(f)[1][1:] in self.packers.keys())
            except Exception:
                return False

        ls = filter(file_filter, listdir(dir))
        return ls

    def fill_source_list(self):
        self.listSource.addItems(self.filtered_source_dir(self.source))

    def fill_dest_list(self):
        files = listdir(self.dest)
        for fn in files:
            list_item = QtGui.QListWidgetItem(fn)
            try:
                abs_name = path.join(self.dest, fn)
                if path.isdir(abs_name):
                    list_item.setTextColor(QtCore.Qt.blue)
                elif not (path.splitext(fn)[1][1:] in AVAIL_EXT):
                    list_item.setTextColor(QtCore.Qt.red)
            except Exception:
                list_item.setTextColor(QtCore.Qt.red)
            self.listDest.addItem(list_item)

    def act_delete_file(self):
        try:
            f = path.join(self.dest, unicode(self.listDest.currentItem().text()))
            rmtree(f)
        except Exception:
            QtGui.QMessageBox.warning(self, u"Внимание", u"Невозможно удалить файл")

    def dest_show_menu(self, pos):
        self.list_dest_menu.popup(self.listDest.mapToGlobal(pos))

    def copy_book(self):
        fname = unicode(self.listSource.currentItem().text())
        try:
            f = self.packers[path.splitext(fname)[1][1:]]
            f(path.join(self.source, fname), self.dest)
        except KeyError:
            self.no_packer()
        except Exception as e:
            self.err_packer(e)

    def show_settings_dialog(self):
        dialog = SettingsDialog()
        dialog.leSource.setText(self.source)
        dialog.leDest.setText(self.dest)
        if dialog.exec_():
            self.source = unicode(dialog.leSource.text())
            self.dest = unicode(dialog.leDest.text())

    def files_changed(self, dir):
        if dir == self.source:
            self.listSource.clear()
            self.fill_source_list()
        if dir == self.dest:
            self.listDest.clear()
            self.fill_dest_list()

    def no_packer(self):
        QtGui.QMessageBox.warning(self.sender(), u"Внимание", u"Невозможно работать с таким типом файлов")

    def err_packer(self, e):
        QtGui.QMessageBox.warning(self.sender(), u"Внимание", u"Ошибка чтения файла:\n %s" % e.message)