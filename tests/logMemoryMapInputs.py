"""
Read the inputs at an interval and log them
To see rF2's response to Neutral button send
"Neutral" whenever gear is selected
"""
from directInputKeySend import DirectInputKeyCodeTable
import directInputKeySend

from scheduler import MyThread

from sharedMemoryAPI import SimInfoAPI, Cbytestring2Python
from mockMemoryMap import gui

tick_interval = 0.05 # seconds
_timestamp = 0

controls_o = None

class Controls:
  """
  Monitor the gears, clutch etc. in the shared memory.
  Send events to callback when there are changes
  """
  def __init__(self, debug=0, mocking=False):
    self.debug = debug
    self.mocking=mocking
    self.info = SimInfoAPI()
    if self.mocking:
      self.info.playersVehicleScoring().mControl = 0 # 0=local player
    self._graunching = False
    self.clutchState = self.__readClutch()
    self.currentGear = self.__readGear()

  def __readClutch(self):
    _c = self.info.playersVehicleTelemetry().mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    # We want 100 clutch released, 0 clutch pressed
    return int(-(_c-1)*100)
  def __readGear(self):
    _gear = self.info.playersVehicleTelemetry().mGear  # -1 to number of gears, 0 is neutral
    return _gear

  def monitor(self):
    # Run every tick_interval
    if self._graunching:
      self._graunching = False
      directInputKeySend.ReleaseKey('DIK_NUMPAD0')

    if self.currentGear != self.__readGear():
      self.currentGear   = self.__readGear()
      if self.debug > 0:
        print('[MemoryMapped] gear: %s' % self.currentGear)
      #driver = Cbytestring2Python(self.playersVehicleScoring().mDriverName)
      self.callback(gearEvent=self.currentGear+10)

    if self.clutchState != self.__readClutch():
      self.clutchState   = self.__readClutch()
      if self.getDriverType() == 0:
        self.callback(clutchEvent=self.clutchState)

  def run(self, callback):
    """ Event loop """
    self.callback = self.log_callback
    self.thread = MyThread(self.monitor, tick_interval)
    self.thread.start()

  def stop(self):
    """ Stop the event loop """
    self.thread.stop()

  def log_callback(self, clutchEvent=None, gearEvent=None, stopEvent=None):
      # Logging stub
      global controls_o

      if clutchEvent or gearEvent or stopEvent:
        clutch = controls_o.clutchState
        gear   = controls_o.currentGear
        driver = 'Max Snell'
        print('Driver %s, Gear: %d, Clutch position: %d' % (driver, gear, clutch))
      if gearEvent != None:
        self._graunching = True
        # Send the "Neutral" key press
        directInputKeySend.PressKey('DIK_NUMPAD0')

def test_main():
    global controls_o
    class graunch:  #dummy
      def isGraunching(self):
        return False

    controls_o = Controls(mocking=False)
    controls_o.run(None)
    controls_o.monitor()  # show initial state
    graunch_o = graunch()
    # gui just used for timer loop
    root = gui(10000, 
        6,
        mocking=True,
        graunch_o=graunch_o,
        controls_o=controls_o)
    
    #controls_o.stop()
    return root


if __name__ == '__main__':
   root = test_main()
   root.mainloop() # having that separate allows for unit testing test_main()