
from DiskList.Lists import ArrayList

import numpy as np

from functools import reduce

SAFETY_SIZE = 50*(2**30)

class ArrayQueue(ArrayList):
    def __init__(self, max_size, shape, dtype=np.float):
        dtype = np.dtype(dtype)
        super().__init__(shape, dtype)
        self.current_list_size = 0
        self.shape = shape
        self.dtype = dtype
        self.array_byte_size = reduce(lambda x, y: x*y, shape)*dtype.itemsize
        self.max_size = max_size
        self.current_index = 0
        self.open()
        
    def append(self, data):
        if type(data) is not np.ndarray:
            raise TypeError('Expected np.ndarray, got {!s}.'.format(type(data)))
        if data.shape != self.shape:
            raise TypeError('Shape is {!s}, excepted {!s}'.format(data.shape, self.shape))
        if self.current_list_size*self.array_byte_size > SAFETY_SIZE:
            raise MemoryError('You may not want to use that much memory.')
    
        if self.current_list_size < self.max_size:
            self.file.seek(0, 2)
            self.current_list_size += 1
        else:
            self.file.seek(self.current_index*self.array_byte_size)
            
        data_bytes = data.astype(self.dtype).tobytes()
        self.file.write(data_bytes)
        self.current_index = (self.current_index+1)%self.max_size