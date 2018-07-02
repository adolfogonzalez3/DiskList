from tempfile import TemporaryFile
from abc import ABC, abstractmethod
from collections.abc import Sequence

class FileBackedList(Sequence):
    def __init__(self):
        self.file = None
        
    def open(self):
        self.file = TemporaryFile()
        
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close(type, value, traceback)

    def close(self, type=None, value=None, traceback=None):
        self.file.close()