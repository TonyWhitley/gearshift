import unittest

from sharedMemoryAPI import test_main

class Test_sharedMemoryAPI(unittest.TestCase):
  def test_sharedMemoryAPI_main_runs(self):
    # Preliminary test - does main run?
    root = test_main()
    assert root != None



if __name__ == '__main__':
  unittest.main(exit=False)