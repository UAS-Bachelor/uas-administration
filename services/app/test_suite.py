import unittest

import app_test

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(app_test))

runner = unittest.TextTestRunner(verbosity=3)
print("\n")
result = runner.run(suite)
