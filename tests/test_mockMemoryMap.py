import unittest

from mockMemoryMap import main

class Test_mockMemoryMap(unittest.TestCase):
  def test_mockMemoryMap_main_runs(self):
    # Preliminary test - does main run?
    root = main()
    assert root != None



if __name__ == '__main__':
  unittest.main(exit=False)