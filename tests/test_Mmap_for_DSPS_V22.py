import unittest

from Mmap_for_DSPS_V22 import main

class Test_Mmap_for_DSPS_V22(unittest.TestCase):
  def test_Mmap_for_DSPS_V22_main_runs(self):
    # Preliminary test - does main run?
    root = main()
    assert root != None



if __name__ == '__main__':
  unittest.main(exit=False)