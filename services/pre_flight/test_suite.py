import unittest

import pre_flight_test

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(pre_flight_test))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
