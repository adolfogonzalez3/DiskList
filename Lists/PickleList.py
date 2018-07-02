
from DiskList.Lists.FileBackedList import FileBackedList

import pickle

SAFETY_SIZE = 50*(2**30)

class PickleList(FileBackedList):
    def __init__(self, max_byte_size=2**16):
        super().__init__()
        self.current_list_size = 0
        self.max_byte_size = max_byte_size
        self.open()
        
    def __object_size(self):
        return self.max_byte_size + 1
        
    def __remove_fill(self, data):
        fill = data[self.__object_size()-1].to_bytes(1, byteorder='big')
        return data.rstrip(fill)
        
    def _fill(self, data_bytes):
        fill = ((data_bytes[-1] + 1)%256).to_bytes(1, byteorder='big')
        data_bytes_filled = data_bytes.ljust(self.__object_size(), fill)
        return data_bytes_filled
        
    def __depickle(self, data_bytes):
        data_bytes = self.__remove_fill(data_bytes)
        data = pickle.loads(data_bytes)
        return data
        
    def append(self, data):
        if self.current_list_size*self.max_byte_size > SAFETY_SIZE:
            raise MemoryError('You may not want to use that much memory.')
    
        self.file.seek(0, 2)
        data_bytes = pickle.dumps(data)
        if len(data_bytes) > self.max_byte_size:
            raise RuntimeError('Byte size of pickled object is greater than max size.')
        
        data_bytes_filled = self._fill(data_bytes)
        self.file.write(data_bytes_filled)
        self.current_list_size += 1
        
    def __len__(self):
        return self.current_list_size
        
    def __getitem__(self, key):
        if type(key) is int:
            if 0 <= key and key < self.current_list_size:
                self.file.seek(key*self.__object_size())
                data_bytes = self.file.read(self.__object_size())
                data = self.__depickle(data_bytes)
                return data
            elif self.current_list_size < key and key <= -1:
                key = -key
                self.file.seek(key*self.__object_size(), 2)
                data_bytes = self.file.read(self.__object_size())
                data = self.__depickle(data_bytes)
                return data
            else:
                raise IndexError()
        else:
            raise TypeError('Not a supported method of indexing.')
        
    def __del__(self):
        self.close()