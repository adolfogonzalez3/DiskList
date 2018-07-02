from DiskList import ArrayQueue

import unittest
import numpy as np

import random

from tqdm import trange

class TestArrayQueue(unittest.TestCase):
            
    def test_append(self):
        Q = ArrayQueue(10, shape=(10, 10), dtype=np.float)
        a = np.empty((10, 10))
        for i in range(11):
            Q.append(a)
            
    def test_index(self):
        L = ArrayQueue(10, shape=(10, 10), dtype=np.float)
        random_arrays = [np.random.rand(10, 10) for _ in range(10)]
        for a in random_arrays:
            L.append(a)
            
        self.assertEqual(type(L[0]), np.ndarray)
            
    def test_append_correctness(self):
        Q = ArrayQueue(10, shape=(10, 10), dtype=np.float)
        a = np.empty((10, 10))
        for i in range(11):
            a.fill(i)
            Q.append(a)
            
        for i in range(10):
            if i == 0:
                a.fill(10)
            else:
                a.fill(i)
            self.assertTrue(np.all(Q[i] == a))
            
        
if __name__ == '__main__':
    unittest.main()