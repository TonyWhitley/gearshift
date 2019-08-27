# Gearshift.py - monitors the rFactor 2 shared memory values for the shifter 
# and clutch and if a gear change is not done properly it repeatedly sends a
# "Neutral" key press to prevent the gear being selected.
#
# Inspired by http://www.richardjackett.com/grindingtranny
# I borrowed Grind_default.wav from there to make the noise of the grinding
# gears.
#
# The game has to have a key mapped as "Neutral". (Default: Numpad 0)
#

from pyDirectInputKeySend.directInputKeySend import DirectInputKeyCodeTable
from mockMemoryMap import gui

BUILD_REVISION = 75 # The git branch commit count
versionStr = 'gearshift V3.1.%d' % BUILD_REVISION
versionDate = '2019-08-21'

credits = "Reads the clutch and shifter from rF2 using a Python\n" \
 "mapping of The Iron Wolf's rF2 Shared Memory Tools.\n" \
 "https://github.com/TheIronWolfModding/rF2SharedMemoryMapPlugin\n" \
 "Original Python mapping implented by\n" \
 "https://forum.studio-397.com/index.php?members/k3nny.35143/\n\n" \
 "Icon made by https://www.flaticon.com/authors/those-icons"

import sys
from threading import Timer
from typing import Optional
from winsound import PlaySound, SND_FILENAME, SND_LOOP, SND_ASYNC # type: ignore

from gearshift.configIni import Config
import pyDirectInputKeySend.directInputKeySend as directInputKeySend

from memoryMapInputs import Controls

from memoryMapInputs import SuccessiveNeutral

# Main config variables, loaded from gearshift.ini
mockInput      =    False   # If True then use mock input

ClutchEngaged  =    90      # (0 - 100) the point in the travel where the clutch engages
doubleDeclutch =    False   # Not yet implemented
reshift =           True    # If True then neutral has to be selected before
                            # retrying failed change. If False then just have
                            # to de-clutch

###############################################################################

# Nothing much to twiddle with from here on

# Config variables, also loaded from gearshift.ini
global debug
debug           =   0       # 0, 1, 2 or 3
neutralButton   =   None  # The key used to force neutral, whatever the shifter says
graunchWav = ''

# Gear change events
clutchDisengage         = 'clutchDisengage'
clutchEngage            = 'clutchEngage'
gearSelect              = 'gearSelect'
gearDeselect            = 'gearDeselect'
successiveNeutral       = 'successiveNeutral'
graunchTimeout          = 'graunchTimeout'  # Memory-mapped mode
smStop                  = 'stop'  # Stop the state machine

#globals 
gearState = 'neutral' # TBD

ClutchPrev = 2  # Active states are 0 and 1 so 2 is "unknown"

#################################################################################
# AHK replacement fns
def SetTimer(callback, mS: int) -> Timer:
  if mS > 0:
    timer = Timer(mS / 1000, callback)
    timer.start()
  else: 
    pass # TBD delete timer?
  return timer

def StopTimer(timer) -> None:
  timer.cancel()

def SoundPlay(soundfile: str) -> None:
  PlaySound(soundfile, SND_FILENAME|SND_LOOP|SND_ASYNC)

def SoundStop() -> None:
  PlaySound(None, SND_FILENAME)

def msgBox(str: str) -> None:
  print(str)

#################################################################################
def quit(errorCode: int) -> None:
  # User presses a key before exiting program
  print('\n\nPress Enter to exit')
  input()
  sys.exit(errorCode)

#################################################################################
class graunch:
  def __init__(self) -> None:
        self.graunching = False
        self.neutralTimer = None

  def graunchStart(self) -> None:
        # Start the graunch noise and sending "Neutral"
        # Start the noise
        global graunchWav
        SoundPlay(graunchWav)
        self.graunching = True
        self.__sendNeutralButton()
        if debug >= 2:
            msgBox('GRAUNCH!')
            
  def graunchStop(self) -> None:
        if self.graunching:
          SoundStop()  # stop the noise
        self.graunching = False
        self.stopNeutralTimeout()
        self.__releaseNeutralButton()

  def stopNeutralTimeout(self) -> None:
    """ 
    We were waiting to see if  the effect of the "Neutral" key 
    would persist but rF2 has selected the gear again
    """
    if self.neutralTimer:
      StopTimer(self.neutralTimer)
      self.neutralTimer = None
      self.__releaseNeutralButton()

  def isGraunching(self) -> bool:
    return self.graunching

  # Internal functions
  def __sendNeutralButton(self) -> None:
      global neutralButton
      if self.graunching:      
        # Send the "Neutral" key press
        directInputKeySend.PressKey(neutralButton)
        # If rF2 doesn't bounce it back into gear before this
        # timer times out then the driver has moved the stick
        # back to neutral
        self.neutralTimer = SetTimer(self.__neutralTimeout, 300) # type: ignore
        if debug >= 1:
            directInputKeySend.PressReleaseKey('DIK_G')
        SetTimer(self.__releaseNeutralButton, 20)

  def __releaseNeutralButton(self) -> None:
        # Send the "Neutral" key release
        global neutralButton
        directInputKeySend.ReleaseKey(neutralButton)
        if self.graunching:
          SetTimer(self.__sendNeutralButton, 20)

  def __neutralTimeout(self) -> None:
      """ Shared memory.
      Neutral key causes gearDeselect event but if player doesn't move shifter
      to neutral then rF2 will quickly report that it's in gear again,
      causing a gearSelect event.
      If SM is still in neutral (gearSelect hasn't happened) when 
      neutralTimer expires then player has moved shifter to neutral
      """
      #self.__sendNeutralButton()
      pass
      #gearStateMachine(graunchTimeout)


######################################################################

def gearStateMachine(event: str) -> str:
    global gearState 
    global graunch_o
    global debug

    # Gear change states
    neutral                = 'neutral'
    clutchDown             = 'clutchDown'
    waitForDoubleDeclutchUp= 'waitForDoubleDeclutchUp'
    clutchDownGearSelected = 'clutchDownGearSelected'
    inGear                 = 'inGear'
    graunching             = 'graunching'
    graunchingClutchDown   = 'graunchingClutchDown'
    graunchingNeutral      = 'graunchingNeutral'

    if debug >= 3:
        msgBox('gearState %s event %s' % (gearState, event))
    # event check (debug)
    if   event == clutchDisengage:
      pass
    elif event == clutchEngage:
      pass
    elif event == gearSelect:
      pass
    elif event == gearDeselect:
      pass
    elif event == successiveNeutral:
      pass
    elif event == graunchTimeout:
      pass
    elif event == smStop:
      graunch_o.graunchStop()
      gearState = neutral
      pass
    else:
            msgBox('gearStateMachine() invalid event %s' % event)

    if    gearState == neutral:
        if event == clutchDisengage:
                gearState = clutchDown
                if debug >= 1:
                    directInputKeySend.PressKey('DIK_D')
        elif event == gearSelect:
                graunch_o.graunchStart()
                gearState = graunching
        #elif event == graunchTimeout:
        #        graunch_o.graunchStop()

    elif gearState == clutchDown:
        if event == gearSelect:
                gearState = clutchDownGearSelected
        elif event == clutchEngage:
                gearState = neutral
                if debug >= 1:
                    directInputKeySend.PressKey('DIK_U')

    elif gearState == waitForDoubleDeclutchUp:
        if event == clutchEngage:
                gearState = neutral
                if debug >= 2:
                    msgBox('Double declutch spin up the box')
        elif event == gearSelect:
                graunch_o.graunchStart()
                gearState = graunching

    elif gearState == clutchDownGearSelected:
        if event == clutchEngage:
                gearState = inGear
                if debug >= 2:
                    msgBox('In gear')
        elif event == gearDeselect:
                if doubleDeclutch:
                    gearState = waitForDoubleDeclutchUp
                else:
                    gearState = clutchDown

    elif gearState == inGear:
        if event == gearDeselect:
                gearState = neutral
                if debug >= 2:
                    msgBox('Knocked out of gear')
        elif event == clutchDisengage:
                gearState = clutchDownGearSelected
        elif event == gearSelect: # smashed straight through without neutral.
                # I don't think this can happen if rF2, only with mock inputs...
                graunch_o.graunchStart()
                gearState = graunching

    elif gearState == graunching:
        if event == clutchDisengage:
                if reshift == False:
                        if debug >= 1:
                            directInputKeySend.PressKey('DIK_R')
                        gearState = clutchDownGearSelected
                else:
                        gearState = graunchingClutchDown
                graunch_o.graunchStop()
                if debug >= 1:
                    directInputKeySend.PressKey('DIK_G')
        elif event == clutchEngage:
                graunch_o.graunchStart()   # graunch again
        elif event == gearDeselect:
                # Neutral key press received
                """
                gearState = graunchingNeutral
                #graunch_o.__neutralTimeout()

    elif gearState == graunchingNeutral:
        # rF2 will have put it into neutral but if shifter
        # still in gear it will have put it back in gear again
        if event == gearSelect:
                gearState = graunching
                graunch_o.stopNeutralTimeout()
        elif event == SuccessiveNeutral:
                # Neutral read twice
                # was graunchTimeout:
                # timed out and still not in gear, player has
                # shifted to neutral
                gearState = neutral
                graunch_o.graunchStop()
                """
                pass

        elif event == gearSelect:
                graunch_o.graunchStop()
                graunch_o.graunchStart()   # graunch again

    elif gearState == graunchingClutchDown:
        if event == clutchEngage:
                graunch_o.graunchStart()   # graunch again
                gearState = graunching
        elif event == gearDeselect or event == gearSelect:
                gearState = clutchDown
                graunch_o.graunchStop()

    else:
           msgBox('Bad gearStateMachine() state gearState')

    if gearState != graunching and gearState != graunchingNeutral:
        pass
        #graunch_o.graunchStop()   # belt and braces - sometimes it gets stuck.

    return gearState # for unit testing

def set_graunch_o(_graunch_o: graunch) -> None:
    global graunch_o
    graunch_o = _graunch_o




def WatchClutch(Clutch: int=100) -> None:
    # Clutch 100 is up, 0 is down to the floor
    global ClutchPrev
    ClutchState = 1 # engaged

    if Clutch < ClutchEngaged:
        ClutchState = 0  # clutch is disengaged

    if ClutchState != ClutchPrev:
        if ClutchState == 0:
            gearStateMachine(clutchDisengage)
        else:
            gearStateMachine(clutchEngage)

    ClutchPrev = ClutchState

#############################################################

def memoryMapCallback(clutchEvent: int=None, gearEvent: int=None, stopEvent: bool=False) -> None:
  if clutchEvent != None:
    WatchClutch(clutchEvent) # type: ignore
  if gearEvent != None:
    if gearEvent == 0: # Neutral
            gearStateMachine(gearDeselect)
    elif gearEvent == SuccessiveNeutral:
            gearStateMachine(successiveNeutral)
    else:
            gearStateMachine(gearSelect)
  if stopEvent:
    gearStateMachine(smStop)

def ShowButtons() -> None:
  pass

global neutralButtonKeycode

def main(): # -> (int, Controls):
  global graunch_o
  global debug
  global graunchWav
  global neutralButton

  config_o = Config()
  debug = config_o.get('miscellaneous', 'debug')
  if not debug: debug = 0
  graunchWav = config_o.get('miscellaneous', 'wav file')
  mockInput = config_o.get('miscellaneous', 'mock input')
  reshift = config_o.get('miscellaneous', 'reshift') == 1

  ClutchEngaged = config_o.get('clutch', 'bite point')

  neutralButton = config_o.get('miscellaneous', 'neutral button')
  ignitionButton = config_o.get('miscellaneous', 'ignition button')
  if neutralButton in DirectInputKeyCodeTable: # (it must be)
    neutralButtonKeycode = neutralButton[4:]
  else:
    print('\ngearshift.ini "neutral button" entry "%s" not recognised.\nIt must be one of:' % neutralButton)
    for _keyCode in DirectInputKeyCodeTable:
      print(_keyCode, end=', ')
    quit(99)
  if ignitionButton in DirectInputKeyCodeTable: # (it must be)
    _ignitionButton = ignitionButton[4:]
  else:
    print('\ngearshift.ini "ignition button" entry "%s" not recognised.\nIt must be one of:' % ignitionButton)
    for _keyCode in DirectInputKeyCodeTable:
      print(_keyCode, end=', ')
    quit(99)

  graunch_o = graunch()

  controls_o = Controls(debug=debug,mocking=mockInput)

  return controls_o, graunch_o

def main_gui(controls_o, graunch_o):
  instructions = 'If gear selection fails this program will send %s ' \
    'to the active window until you reselect a gear.\n\n' \
    'You can minimise this window now.\n' \
    'Do not close it until you have finished racing.' % neutralButtonKeycode


  #############################################################
  # Using shared memory, reading clutch state and gear selected direct from rF2
  controls_o.run(memoryMapCallback)
  # mockInput: testing using the simple GUI to poke inputs into the memory map
  # otherwise just use the GUI slightly differently
  root = gui(mocking=mockInput,
              instructions=instructions,
              graunch_o=graunch_o,
              controls_o=controls_o)
  return root, controls_o
#############################################################

if __name__ == "__main__":
  controls_o, graunch_o = main()
  root = main_gui()
  if root != 'OK':
    root.mainloop()
    controls_o.stop()
