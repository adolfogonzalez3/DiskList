from DiskList import PickleQueue

import unittest
import numpy as np

import random

from tqdm import trange

class TestPickleQueue(unittest.TestCase):

    def test_append_simple(self):
        Q = PickleQueue(10)
        
        for i in range(10):
            Q.append(i)
            
    def test_index(self):
        Q = PickleQueue(10)
        for i in range(10):
            Q.append(i)
            
        self.assertEqual(type(Q[0]), int)
            
    def test_append_correctness(self):
        Q = PickleQueue(10)
        random_arrays = [np.random.rand(10, 10) for _ in range(10)]
        for a in random_arrays:
            Q.append(a)
            
        for i, a in enumerate(random_arrays):
            self.assertTrue(np.all(Q[i] == a))
            
        
if __name__ == '__main__':
    unittest.main()