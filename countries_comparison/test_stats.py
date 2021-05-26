import unittest
import numpy as np
import pandas as pd
from stats import Stats

class myTests(unittest.TestCase):

    def test_normal(self):
        stats = Stats()
        y = np.random.normal(0,1,1000)

        my_df = pd.DataFrame({'y':y}) 

        new_df = stats.get_stationary(my_df)
        self.assertTrue(stats.unit_root_test(new_df['y']) < 0.1)

    def test_linear_normal(self):
        stats = Stats()
        x = np.linspace(0,1,1000)

        y = 5*x + np.random.normal(0,1,1000)

        my_df = pd.DataFrame({'y':y}) 

        new_df = stats.get_stationary(my_df)
        self.assertTrue(stats.unit_root_test(new_df['y']) < 0.1)


if __name__ == '__main__':
    unittest.main()