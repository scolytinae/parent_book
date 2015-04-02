# -*- coding:utf-8 -*-
from os import path, makedirs
from zipfile import ZipFile
from rarfile import RarFile
import shutil


def unpack_rar(fname, dest):
    with RarFile(fname, "r") as rf:
        rf.extractall(dest)


def unpack_zip(fname, dest):
    with ZipFile(fname, "r") as zf:
        for m in zf.namelist():
            try:
                new_name = m.decode("utf-8")
            except Exception:
                new_name = m.decode("cp866")
            new_name = path.join(dest, new_name)
            try:
                if path.isfile(new_name):
                    with open(new_name, "w") as f:
                        f.write(zf.read(m))
                else:
                    makedirs(new_name)
            except Exception as e:
                print 'Error extracting archive: %s' % e.message


def unpack_file(fname, dest):
    shutil.copy(fname, dest)