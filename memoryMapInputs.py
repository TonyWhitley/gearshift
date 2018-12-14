# Reading the clutch and shifter from rF2 using k3nny's Python 
# mapping of The Iron Wolf's rF2 Shared Memory Tools
# https://github.com/TheIronWolfModding/rF2SharedMemoryMapPlugin
# https://forum.studio-397.com/index.php?members/k3nny.35143/

from scheduler import MyThread
from ctypes import addressof, c_char_p

from Mmap_for_DSPS_V22 import SimInfo

tick_interval = 0.1 # seconds

class Controls:
  def __init__(self, debug=0):
    self.debug = debug
    self.info = SimInfo()
    if self.debug > 5:
      self.clutchState = 0
      self.currentGear = 0
    else:
      self.clutchState = self.__readClutch()
      self.currentGear = self.__readGear()
  def __readClutch(self):
    if self.debug > 5:
      return 100 # clutch is not pressed
    _c = self.info.Rf2Tele.mVehicles[0].mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    # We want 100 clutch released, 0 clutch pressed
    return int(-(_c-1)*100)
  def __readGear(self):
    if self.debug > 5:
      return 1  # trying to get first
    return self.info.Rf2Tele.mVehicles[0].mGear  # -1 to number of gears, 0 is neutral
  def monitor(self):
    # Run every tick_interval
    if self.currentGear != self.__readGear():
      self.currentGear   = self.__readGear()
      driver = str(c_char_p(addressof(self.info.Rf2Scor.mVehicles[0].mDriverName)).value)
      # still not right, gives "b'svensmiles '"
      #self.info.Rf2Scor.mVehicles[0].mDriverName.value
      self.callback(gearEvent=self.currentGear)
    if self.clutchState != self.__readClutch():
      self.clutchState   = self.__readClutch()
      self.callback(clutchEvent=self.clutchState)
    #print('tick')
    #Timer(tick_interval, self.monitor, ()).start()
    #self.t.start()

  def run(self, callback):
    """ Event loop """
    self.callback = callback
    thread = MyThread(controls_o.monitor, tick_interval)
    thread.start()

def callback(clutchEvent=None, gearEvent=None):
    clutch = controls_o.clutchState
    gear   = controls_o.currentGear
    driver = 'Max Snell'
    print('Driver %s, Gear: %d, Clutch position: %d' % (driver, gear, clutch))

if __name__ == '__main__':
    controls_o = Controls()
    controls_o.monitor()  # show initial state
    controls_o.run(callback)


