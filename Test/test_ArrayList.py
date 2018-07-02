from DiskList import ArrayList

import unittest
import numpy as np

import random

from tqdm import trange

class TestArrayList(unittest.TestCase):
            
    def test_append(self):
        L = ArrayList(shape=(10, 10), dtype=np.float)
        a = np.zeros((10, 10))
        L.append(a)
        
    def test_index(self):
        L = ArrayList(shape=(10, 10), dtype=np.float)
        random_arrays = [np.random.rand(10, 10) for _ in range(10)]
        for a in random_arrays:
            L.append(a)
            
        self.assertEqual(type(L[0]), np.ndarray)
        
    def test_append_correctness(self):
        L = ArrayList(shape=(10, 10), dtype=np.float)
        random_arrays = [np.random.rand(10, 10) for _ in range(10)]
        for a in random_arrays:
            L.append(a)
            
        for i, a in enumerate(random_arrays):
            self.assertTrue(np.all(L[i] == a))
            
    
            
        
if __name__ == '__main__':
    unittest.main()