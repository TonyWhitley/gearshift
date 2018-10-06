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

from directInputKeySend import DirectInputKeyCodeTable

BUILD_REVISION = 30 # The git commit count
versionStr = 'gearshift V2.0.%d' % BUILD_REVISION
versionDate = '2018-10-06'

print(versionStr, versionDate)
print('https://github.com/TonyWhitley/gearshift')
print()


# Translated from gearshift.ahk V1.5 tjw 2017-12-28

from threading import Timer
from winsound import PlaySound, SND_FILENAME, SND_LOOP, SND_ASYNC

from configIni import Config
import directInputKeySend
from wheel import Controller
from memoryMapInputs import Controls

ForwardGears = 6            # Plus reverse
ReverseClutchAxis = False   # If True then the clutch input goes from 100 (down) to 0 (up)
TestMode       =    False   # If True then show shifter and clutch operation

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
#AutoRepeat     =   0
#NeutralBtn     The key used to force neutral, whatever the shifter says

# Gear change events
clutchDisengage         = 'clutchDisengage'
clutchEngage            = 'clutchEngage'
gearSelect              = 'gearSelect'
gearDeselect            = 'gearDeselect'

#globals 
gearState = 'neutral' # TBD

ClutchPrev = 0
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
  exit(errorCode)

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
        self.graunching = False
        SoundStop()  # stop the noise
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
        SetTimer(self.graunch1, 100)
        if debug >= 1:
            directInputKeySend.PressReleaseKey('DIK_G')



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
                gearState = neutral
                graunch_o.graunchStop()
        elif event == gearSelect:
                graunch_o.graunchStop()
                graunch_o.graunchStart()   # graunch again

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

def memoryMapCallback(clutchEvent=None, gearEvent=None):
  if clutchEvent:
    WatchClutch(clutchEvent)
  if gearEvent != None:
    if gearEvent == 0: # Neutral
            gearStateMachine(gearDeselect)
    else:
            gearStateMachine(gearSelect)


def ShowButtons():
  pass

if __name__ == "__main__":
  config_o = Config()
  debug = config_o.get('miscellaneous', 'debug')
  if not debug: debug = 0
  sharedMemory = config_o.get('miscellaneous', 'shared memory')
  graunchWav = config_o.get('miscellaneous', 'wav file')
  Shifter1 = config_o.get('shifter', '1st gear')
  Shifter2 = config_o.get('shifter', '2nd gear')
  Shifter3 = config_o.get('shifter', '3rd gear')
  Shifter4 = config_o.get('shifter', '4th gear')
  Shifter5 = config_o.get('shifter', '5th gear')
  Shifter6 = config_o.get('shifter', '6th gear')
  Shifter7 = config_o.get('shifter', '7th gear')
  Shifter8 = config_o.get('shifter', '8th gear')
  ShifterR = config_o.get('shifter', 'reverse')

  ClutchEngaged = config_o.get('clutch', 'bite point')
  ReverseClutchAxis = config_o.get('clutch', 'reversed')

  neutralButton = config_o.get('miscellaneous', 'neutral button')
  if neutralButton in DirectInputKeyCodeTable: # (it must be)
    _neutralButton = neutralButton[4:]
  else:
    print('\ngearshift.ini "neutral button" entry "%s" not recognised.\nIt must be one of:' % neutralButton)
    for _keyCode in DirectInputKeyCodeTable:
      print(_keyCode, end=', ')
    quit(99)

  print('\nIf gear selection fails %s will be sent to\nthe active window until you reselect a gear.' % 
        _neutralButton)
  print('\nYou can minimise this window now.\nDo not close it until you have finished racing.')
  graunch_o = graunch()

  if sharedMemory == 0:
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

  else: # Using shared memory, reading clutch state and gear selected direct from rF2
    controls_o = Controls()
    controls_o.run(memoryMapCallback)
