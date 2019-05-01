# Gearshift.py - monitors a shifter and clutch and if a gear change is not
# done properly it repeatedly sends a "Neutral" key press to prevent the gear
# being selected.
# Designed for rFactor 2 but should work with any game. (Also tested on rFactor.)
#
# Inspired by http://www.richardjackett.com/grindingtranny
# I borrowed Grind_default.wav from there to make the noise of the grinding
# gears.
#
# The game has to have Numpad 0 mapped as "Neutral".
#
# Notes:
# Virtual env pygame runs OK but the exe pyinstaller produces has import errors.
# Instead install pygame into the main install with
# py -3.6 -m pip install pygame
# Comment out the last two lines of C:\Python36\Lib\site-packages\pygame\__init__.py
#print('pygame %s' % ver)
#print('Hello from the pygame community. https://www.pygame.org/contribute.html')

import sys
from directInputKeySend import DirectInputKeyCodeTable
from mockMemoryMap import gui

BUILD_REVISION = 44 # The git commit count
versionStr = 'gearshift V2.3.%d' % BUILD_REVISION
versionDate = '2019-04-28'

credits = "Reads the clutch and shifter from rF2 using k3nny's Python\n" \
 "mapping of The Iron Wolf's rF2 Shared Memory Tools.\n" \
 "https://github.com/TheIronWolfModding/rF2SharedMemoryMapPlugin\n" \
 "https://forum.studio-397.com/index.php?members/k3nny.35143/\n\n"

# Translated from gearshift.ahk V1.5 tjw 2017-12-28

from threading import Timer
from winsound import PlaySound, SND_FILENAME, SND_LOOP, SND_ASYNC

from configIni import Config
import directInputKeySend

from memoryMapInputs import Controls

ForwardGears = 6            # Plus reverse
ReverseClutchAxis = False   # If True then the clutch input goes from 100 (down) to 0 (up)
TestMode       =    False   # If True then show shifter and clutch operation
mockInput      =    False   # If True then use mock input

ClutchEngaged  =    90      # (0 - 100) the point in the travel where the clutch engages
                            # if ReverseClutchAxis then ClutchEngaged = 10
doubleDeclutch =    False   # Not yet implemented
reshift =           True    # If True then neutral has to be selected before
                            # retrying failed change. If False then just have
                            # to de-clutch

###############################################################################

# Nothing much to twiddle with from here on

global debug
debug           =   0       # 0, 1, 2 or 3
sharedMemory    =   1
#AutoRepeat     =   0
#NeutralBtn     The key used to force neutral, whatever the shifter says

# Gear change events
clutchDisengage         = 'clutchDisengage'
clutchEngage            = 'clutchEngage'
gearSelect              = 'gearSelect'
gearDeselect            = 'gearDeselect'
graunchTimeout          = 'graunchTimeout'  # Memory-mapped mode
smStop                  = 'stop'  # Stop the state machine

#globals 
gearState = 'neutral' # TBD

ClutchPrev = 2  # Active states are 0 and 1 so 2 is "unknown"
KeyToHoldDown = 0
Delete = -1  # delete timer

#################################################################################
# AHK replacement fns
def SetTimer(callback, mS):
  if mS > 0:
    timer = Timer(mS / 1000, callback)
    timer.start()
  else: 
    pass # TBD delete timer?

def GetKeyState(input):
  if input:
    return shifterController_o.getButtonState(input)

def GetClutchState():
  return clutchController_o.getAxis(clutchAxis)


def SoundPlay(soundfile):
  PlaySound(soundfile, SND_FILENAME|SND_LOOP|SND_ASYNC)

def SoundStop():
  PlaySound(None, SND_FILENAME)

def msgBox(str):
  print(str)

#################################################################################
def quit(errorCode):
  # User presses a key before exiting program
  print('\n\nPress Enter to exit')
  input()
  sys.exit(errorCode)

#################################################################################
class graunch:
  def __init__(self):
        self.graunching = False
  def graunchStart(self):
        # Start the graunch noise and sending "Neutral"
        # Start the noise
        SoundPlay(graunchWav)
        self.graunching = True
        self.graunch2()
        if debug >= 2:
            msgBox('GRAUNCH!')


  def graunchStop(self):
        if self.graunching:
          SoundStop()  # stop the noise
        self.graunching = False
        self.graunch1()


  def graunch1(self):
        # Send the "Neutral" key release
        directInputKeySend.ReleaseKey(neutralButton)
        if self.graunching:
          SetTimer(self.graunch2, 20)


  def graunch2(self):
      if self.graunching:      
        # Send the "Neutral" key press
        directInputKeySend.PressKey(neutralButton)
        if sharedMemory != 0:
          SetTimer(self.graunch3, 3000)
        else:
          SetTimer(self.graunch1, 100)
        if debug >= 1:
            directInputKeySend.PressReleaseKey('DIK_G')

  def graunch3(self):
      """ Shared memory.
      Neutral key causes gearDeselect event but if player doesn't move shifter
      to neutral then rF2 will quickly report that it's in gear again,
      causing a gearSelect event.
      If SM is still in neutral (gearSelect hasn't happened) when this timer 
      expires then player has moved shifter to neutral
      """
      gearStateMachine(graunchTimeout)

  def isGraunching(self):
    return self.graunching


######################################################################

def gearStateMachine(event):
    global gearState 

    # Gear change states
    neutral                = 'neutral'
    clutchDown             = 'clutchDown'
    waitForDoubleDeclutchUp= 'waitForDoubleDeclutchUp'
    clutchDownGearSelected = 'clutchDownGearSelected'
    inGear                 = 'inGear'
    graunching             = 'graunching'
    graunchingClutchDown   = 'graunchingClutchDown'
    neutralKeySent         = 'neutralKeySent'

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
    elif event == graunchTimeout:
      pass
    elif event == smStop:
      graunch_o.graunchStop()
      gearState = neutral
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
        elif event == graunchTimeout:
                graunch_o.graunchStop()

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
                if sharedMemory == 0:
                  # When the Neutral button is banged rF sets gear to Neutral
                  gearState = neutral
                  graunch_o.graunchStop()
                else:
                  gearState = neutralKeySent
                pass
        elif event == gearSelect:
                graunch_o.graunchStop()
                graunch_o.graunchStart()   # graunch again
                pass

    elif gearState == neutralKeySent:
        # rF2 will have put it into neutral but if shifter
        # still in gear it will have put it back in gear again
        if event == gearSelect:
                gearState = graunching
        elif event == graunchTimeout:
                # timed out and still not in gear, player has
                # shifted to neutral
                gearState = neutral
                graunch_o.graunchStop()

    elif gearState == graunchingClutchDown:
        if event == clutchEngage:
                graunch_o.graunchStart()   # graunch again
                gearState = graunching
        elif event == gearDeselect:
                gearState = clutchDown
                graunch_o.graunchStop()

    else:
           msgBox('Bad gearStateMachine() state gearState')

    if gearState != graunching:
        graunch_o.graunchStop()   # belt and braces - sometimes it gets stuck.



def WatchClutch(Clutch):
    # Clutch 100 is up, 0 is down to the floor
    # Unless ReverseClutchAxis is True when it's the opposite.
    global ClutchPrev
    ClutchState = 1 # engaged

    if ReverseClutchAxis == False:
        if Clutch < ClutchEngaged:
            ClutchState = 0  # clutch is disengaged
    else:
      if Clutch > ClutchEngaged:
            ClutchState = 0  # clutch is disengaged

    if ClutchState != ClutchPrev:
        if ClutchState == 0:
            gearStateMachine(clutchDisengage)
        else:
            gearStateMachine(clutchEngage)

    ClutchPrev = ClutchState

def WatchClutchAndShifter():
    global KeyToHoldDown

    WatchClutch(GetClutchState())

    Gear1 = GetKeyState(Shifter1)
    Gear2 = GetKeyState(Shifter2)
    Gear3 = GetKeyState(Shifter3)
    Gear4 = GetKeyState(Shifter4)
    Gear5 = GetKeyState(Shifter5)
    Gear6 = GetKeyState(Shifter6)
    Gear7 = GetKeyState(Shifter7)
    Gear8 = GetKeyState(Shifter8)
    GearR = GetKeyState(ShifterR)

    KeyToHoldDownPrev = KeyToHoldDown  # Prev now holds the key that was down before (if any).

    if   Gear1 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD1'
    elif Gear2 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD2'
    elif Gear3 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD3'
    elif Gear4 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD4'
    elif Gear5 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD5'
    elif Gear6 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD7'
    elif Gear7 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD6'
    elif Gear8 == 'D':
        KeyToHoldDown = 'DIK_NUMPAD8'
    elif GearR == 'D':
        KeyToHoldDown = 'DIK_NUMPAD9'
    else:
        KeyToHoldDown = neutralButton

    if KeyToHoldDown == KeyToHoldDownPrev:  # The button is already down (or no button is pressed).
        #if AutoRepeat && KeyToHoldDown
        #   Send, KeyToHoldDown down  # Auto-repeat the keystroke.
        return

    if KeyToHoldDown == neutralButton:
            gearStateMachine(gearDeselect)
    else:
            gearStateMachine(gearSelect)

    # Otherwise, release the previous key and press down the new key:
    # AHK only  SetKeyDelay = -1  # Avoid delays between keystrokes.

    if KeyToHoldDownPrev:   # There is a previous key to release.
         directInputKeySend.ReleaseKey(KeyToHoldDownPrev)  # Release it.
    return

#############################################################

def memoryMapCallback(clutchEvent=None, gearEvent=None, stopEvent=False):
  if clutchEvent != None:
    WatchClutch(clutchEvent)
  if gearEvent != None:
    if gearEvent == 0: # Neutral
            gearStateMachine(gearDeselect)
    else:
            gearStateMachine(gearSelect)
  if stopEvent:
    gearStateMachine(smStop)

def ShowButtons():
  pass

global neutralButtonKeycode

def main():
  #global neutralButtonKeycode

  config_o = Config()
  debug = config_o.get('miscellaneous', 'debug')
  if not debug: debug = 0
  sharedMemory = config_o.get('miscellaneous', 'shared memory')
  graunchWav = config_o.get('miscellaneous', 'wav file')
  mockInput = config_o.get('miscellaneous', 'mock input')
  reshift = config_o.get('miscellaneous', 'reshift') == 1

  ClutchEngaged = config_o.get('clutch', 'bite point')
  ReverseClutchAxis = config_o.get('clutch', 'reversed')

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

  instructions = 'If gear selection fails this program will send %s ' \
    'to the active window until you reselect a gear.\n\n' \
    'You can minimise this window now.\n' \
    'Do not close it until you have finished racing.' % neutralButtonKeycode

  graunch_o = graunch()

#############################################################
  if sharedMemory == 0:
    print(versionStr, versionDate)
    Shifter1 = config_o.get('shifter', '1st gear')
    Shifter2 = config_o.get('shifter', '2nd gear')
    Shifter3 = config_o.get('shifter', '3rd gear')
    Shifter4 = config_o.get('shifter', '4th gear')
    Shifter5 = config_o.get('shifter', '5th gear')
    Shifter6 = config_o.get('shifter', '6th gear')
    Shifter7 = config_o.get('shifter', '7th gear')
    Shifter8 = config_o.get('shifter', '8th gear')
    ShifterR = config_o.get('shifter', 'reverse')

    print(instructions)

    from wheel import Controller

    shifterController_o = Controller()
    shifterControllerName = config_o.get('shifter', 'controller')
    shifterController_o.selectController(shifterControllerName)
    clutchController_o = Controller()
    clutchControllerName = config_o.get('clutch', 'controller')
    clutchController_o.selectController(clutchControllerName)
    clutchAxis = config_o.get('clutch', 'axis')

    if shifterController_o.error:
      print(shifterController_o.error_string)
      quit(80)
    if clutchController_o.error:
      print(clutchController_o.error_string)
      quit(81)

    if len(shifterControllerName) < 3:
      print('Shifter Controller "%s" not valid.  Please run Configurer.exe again.' % shifterControllerName)
      quit(90)
    if len(clutchControllerName) < 3:
      print('Clutch Controller "%s" not valid.  Please run Configurer.exe again.' % clutchControllerName)
      quit(91)

    print('Ready for shifts on "%s"\nusing clutch on "%s".' %
         (shifterControllerName,clutchControllerName))

    if TestMode == False:
        #SetTimer(WatchClutch, 10)
        shifterController_o.run(WatchClutchAndShifter)
    else:
        SetTimer(ShowButtons, 100)
    return 'OK'

#############################################################
  else: # Using shared memory, reading clutch state and gear selected direct from rF2
    controls_o = Controls(debug=debug,mocking=mockInput)
    controls_o.run(memoryMapCallback)
    # mockInput: testing using the simple GUI to poke inputs into the memory map
    # otherwise just use the GUI slightly differently
    root = gui(mocking=mockInput,
               instructions=instructions,
               graunch_o=graunch_o,
               controls_o=controls_o)
    controls_o.stop()
    return root
#############################################################

if __name__ == "__main__":
  root = main()
  if root != 'OK':
    root.mainloop()
