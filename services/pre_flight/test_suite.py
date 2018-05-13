import unittest

import pre_flight_test
import template_parser_test

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(pre_flight_test))
suite.addTests(loader.loadTestsFromModule(template_parser_test))

runner = unittest.TextTestRunner(verbosity=3)
print("\nPre-flight module: \n")
result = runner.run(suite)
