from DiskList import PickleList

import unittest
import numpy as np

import random

from tqdm import trange

class TestPickleList(unittest.TestCase):

    def test_append_simple(self):
        L = PickleList()
        a = 1
        L.append(a)
        
        for i in range(10):
            L.append(i)
            
    def test_append_complex(self):
        L = PickleList()
        a = np.zeros((10, 10))
        L.append(a)
            
    def test_index_simple(self):
        L = PickleList()
        for i in range(10):
            L.append(i)
            
        for i in range(10):
            self.assertEqual(L[i], i)
            
    def test_index_simple(self):
        L = PickleList()
        random_arrays = [np.random.rand(10, 10) for _ in range(10)]
        for a in random_arrays:
            L.append(a)
            
        for i, a in enumerate(random_arrays):
            self.assertTrue(np.all(L[i] == a))
            
        
if __name__ == '__main__':
    unittest.main()