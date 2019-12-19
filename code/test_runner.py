import unittest

import test_fpd_analysis
import test_stats

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_fpd_analysis))
suite.addTests(loader.loadTestsFromModule(test_stats))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)