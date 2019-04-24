# Reading the clutch and shifter from rF2 using k3nny's Python 
# mapping of The Iron Wolf's rF2 Shared Memory Tools
# https://github.com/TheIronWolfModding/rF2SharedMemoryMapPlugin
# https://forum.studio-397.com/index.php?members/k3nny.35143/

from scheduler import MyThread

from Mmap_for_DSPS_V22 import SimInfo, Cbytestring2Python
from mockMemoryMap import gui

tick_interval = 0.1 # seconds
_timestamp = 0

class Controls:
  def __init__(self, debug=0):
    self.debug = debug
    self.info = SimInfo()
    self._SMactive = False
    if self.debug > 5:
      self.clutchState = 0
      self.currentGear = 0
    else:
      self.clutchState = self.__readClutch()
      self.currentGear = self.__readGear()

  def __readClutch(self):
    if self.debug > 5:
      return 100 # clutch is not pressed
    _c = self.info.playersVehicleTelemetry().mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    # We want 100 clutch released, 0 clutch pressed
    return int(-(_c-1)*100)
  def __readGear(self):
    if self.debug > 5:
      return 1  # trying to get first
    return self.info.playersVehicleTelemetry().mGear  # -1 to number of gears, 0 is neutral

  def monitor(self):
    # Run every tick_interval
    stop= self.reasons2stop()
    if stop:
      self.callback(stopEvent=True)
      self._SMactive = False
      if self.debug:
        print('SM stopped because %s' % stop)
    else:
      self._SMactive = True
      if self.currentGear != self.__readGear():
        self.currentGear   = self.__readGear()
        if self.debug > 0:
          print('[MemoryMapped] gear: %s' % self.currentGear)
        #driver = Cbytestring2Python(self.playersVehicleScoring().mDriverName)
        self.callback(gearEvent=self.currentGear)

      if self.clutchState != self.__readClutch():
        self.clutchState   = self.__readClutch()
        if self.getDriverType() == 0:
          self.callback(clutchEvent=self.clutchState)

      # debug print when clutch RPM > engine RPM (when slamming down a gear)
      mEngineRPM = int(self.info.playersVehicleTelemetry().mEngineRPM)
      mClutchRPM = int(self.info.playersVehicleTelemetry().mClutchRPM)

      if self.info.playersVehicleTelemetry().mUnfilteredClutch < .9: # 1.0 clutch down, 0 clutch up
        if mClutchRPM > mEngineRPM:
          #print(mClutchRPM, mEngineRPM)
          pass

  def reasons2stop(self):
    # Return text if the state machine should stop
    # and with it the graunching
    global _timestamp
    ret = ''

    if not self.info.isRF2running():
      return 'rF2 not running'
    if not self.info.isTrackLoaded():
      return 'Track not loaded'
    if not self.info.isOnTrack():
      return 'Not on track'
    if self.getDriverType() != 0:
      return 'AI in control'
    #if not self.info.playersVehicleTelemetry().mIgnitionStarter:  # Ignition off
    #  return 'Ignition off'
    if self.info.playersVehicleTelemetry().mEngineRPM == 0:  # Engine has stopped
      return 'Engine stopped'
    if not _timestamp < self.info.playersVehicleTelemetry().mElapsedTime:
        ret = 'Esc pressed, mElapsedTime stopped'

    _timestamp = self.info.playersVehicleTelemetry().mElapsedTime
    # OK, no reason NOT to run the state machine
    return ret

  def SMactive(self):
    return self._SMactive

  def getMaxRevs(self):
    return self.info.playersVehicleTelemetry().mEngineMaxRPM

  def getDriverType(self):
    return self.info.playersVehicleScoring().mControl  # who's in control: -1=nobody (shouldn't get this), 0=local player, 1=local AI, 2=remote, 3=replay (shouldn't get this)

  def run(self, callback):
    """ Event loop """
    self.callback = callback
    self.thread = MyThread(self.monitor, tick_interval)
    self.thread.start()

  def stop(self):
    self.thread.stop()

def callback(clutchEvent=None, gearEvent=None):
    clutch = controls_o.clutchState
    gear   = controls_o.currentGear
    driver = 'Max Snell'
    print('Driver %s, Gear: %d, Clutch position: %d' % (driver, gear, clutch))

if __name__ == '__main__':
    controls_o = Controls()
    controls_o.monitor()  # show initial state
    controls_o.run(callback)
    gui(controls_o.getMaxRevs())
    controls_o.stop()


