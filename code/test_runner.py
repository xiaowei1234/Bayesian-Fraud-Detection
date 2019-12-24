import unittest

import test_fpd_analysis
import test_stats
import test_cart_analysis

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_fpd_analysis))
suite.addTest(loader.loadTestsFromModule(test_cart_analysis))
suite.addTests(loader.loadTestsFromModule(test_stats))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)