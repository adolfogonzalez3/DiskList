
from DiskList.Lists import PickleList

import pickle

SAFETY_SIZE = 50*(2**30)

class PickleQueue(PickleList):
    def __init__(self, max_size, max_byte_size=2**16):
        super().__init__(max_byte_size)
        self.current_list_size = 0
        self.current_index = 0
        self.max_byte_size = max_byte_size
        self.max_size = max_size
        self.open()
        
    def append(self, data):
        if self.current_list_size*self.max_byte_size > SAFETY_SIZE:
            raise MemoryError('You may not want to use that much memory.')
        
        data_bytes = pickle.dumps(data)
        
        if len(data_bytes) > self.max_byte_size:
            raise RuntimeError('Byte size of pickled object is greater than max size.')
    
        if self.current_list_size < self.max_size:
            self.file.seek(0, 2)
            self.current_list_size += 1
        else:
            self.file.seek(self.current_index*self.max_byte_size)
        
        data_bytes_filled = super()._fill(data_bytes)
        self.file.write(data_bytes_filled)
        self.current_index = (self.current_index+1)%self.max_size