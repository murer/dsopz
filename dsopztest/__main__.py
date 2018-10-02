import sys
from unittest import TestLoader, TextTestRunner
from dsopztest.datastore_emulator import dsemulator

def main():
    dsemulator.start()
    try:
        loader = TestLoader()
        suite = loader.discover('dsopztest', pattern='*_test.py')
        runner = TextTestRunner(verbosity=2, failfast=True)
        success = runner.run(suite).wasSuccessful()
    finally:
        dsemulator.stop()
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
