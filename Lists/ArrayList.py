
from DiskList.Lists.FileBackedList import FileBackedList

import numpy as np

from functools import reduce

from cachetools import LRUCache

SAFETY_SIZE = 50*(2**30)

class ArrayList(FileBackedList):
    def __init__(self, shape, dtype=np.float):
        dtype = np.dtype(dtype)
        super().__init__()
        self.current_list_size = 0
        self.shape = shape
        self.dtype = dtype
        self.array_byte_size = reduce(lambda x, y: x*y, shape)*dtype.itemsize
        self.open()
        self.cache = LRUCache(maxsize=128)
        self.misses = 0
        
    def __object_size(self):
        return self.array_byte_size
        
    def __restore(self, array_bytes):
        array_restored = np.frombuffer(array_bytes, self.dtype).reshape(self.shape)
        return array_restored
        
    def append(self, data):
        if type(data) is not np.ndarray:
            raise TypeError('Not a Numpy array.')
        if data.shape != self.shape:
            raise TypeError('Shape is {!s}, excepted {!s}'.format(data.shape, self.shape))
        if self.current_list_size*self.array_byte_size > SAFETY_SIZE:
            raise MemoryError('You may not want to use that much memory.')
    
        self.file.seek(0, 2)
        data_bytes = data.astype(self.dtype).tobytes()
        self.file.write(data_bytes)
        self.current_list_size += 1
        
    def __len__(self):
        return self.current_list_size
        
    
    def index(self, key):
        if type(key) is int:
            if key in self.cache:
                return self.cache[key]
            if 0 <= key and key < self.current_list_size:
                self.file.seek(key*self.__object_size())
                array_bytes = self.file.read(self.__object_size())
                data = self.__restore(array_bytes)
            elif self.current_list_size < key and key <= -1:
                key = -key
                self.file.seek(key*self.__object_size(), 2)
                array_bytes = self.file.read(self.__object_size())
                data = self.__restore(array_bytes)
            else:
                raise IndexError('Tried indexing {!s} from a list sized {!s}'.format(key, self.current_list_size))
            
            self.cache[key] = data
            self.misses += 1
            return data
        else:
            raise TypeError('Not a supported method of indexing.')
    
    #@lru_cache(maxsize=128)
    def __getitem__(self, key):
        return self.index(key)
        
    def __del__(self):
        self.close()