import unittest

import post_flight_test

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(post_flight_test))

runner = unittest.TextTestRunner(verbosity=3)
print("\n")
result = runner.run(suite)
