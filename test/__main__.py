import sys
from unittest import TestLoader, TextTestRunner

def main():
    loader = TestLoader()
    suite = loader.discover('test', pattern='*_test.py')
    runner = TextTestRunner(verbosity=2, failfast=True)
    success = runner.run(suite).wasSuccessful()
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
