from wordweaver.tests import run
import sys

try:
    run.run_tests(sys.argv[1])
except IndexError:
    print("Please specify a test suite to run: i.e. 'dev' or 'prod'")