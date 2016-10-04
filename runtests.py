import unittest

import logging
logging.disable(logging.DEBUG)  # Disable logging


if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    #  test_suite = test_loader.discover('test_ponyup', pattern='test_*.py')
    test_suite = test_loader.discover('.', pattern='test_*.py')

    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)

    #  test_loader.run(test_suite)

    # This is for the end of test_modules
    #  unittest.main()
