import unittest

if __name__ == "__main__":
    # Discover and run all tests under the tests/ directory
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.defaultTestLoader.discover('tests')
    result = runner.run(suite)
    # Exit with non-zero on failure for CI compatibility
    import sys
    sys.exit(0 if result.wasSuccessful() else 1)
