__author__ = 'friedrich'
from workflow.Service import Service
from setting import Setting as Env
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import os


class AdjustService(Service):

    __zip_file__ = None

    def __init__(self):
        pass

    def package_to_tar(self, _sn_number):
        _file_name = '{0}{1}{2}'.format(Env.DEFAULT_ZIP_DIC, _sn_number, '.zip')
        if os.path.exists(_file_name) is not True:
            os.mknod(_file_name)
        self.__zip_file__ = ZipFile(_file_name, 'w', ZIP_DEFLATED)

    def add_files(self, _files):
        for _file in _files:
            self.__zip_file__.write(Env.DEFAULT_FILE + _file, _file)
        self.__zip_file__.close()

    def get_zip(self):
        return self.__zip_file__
