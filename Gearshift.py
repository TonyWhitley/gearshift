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
# V1.5.3 tjw 2018-09-27

# Translated from gearshift.ahk V1.5 tjw 2017-12-28

from threading import Timer
from winsound import PlaySound, SND_FILENAME, SND_LOOP, SND_ASYNC

import directInputKeySend
from wheel import Wheel

ForwardGears = 6            # Plus reverse
# Joystick buttons
Shifter1 = 8
Shifter2 = 9
Shifter3 = 10
Shifter4 = 11
Shifter5 = 12
Shifter6 = 13
ShifterR = 14
ClutchAxis = 'JoyU'         # R U V or Z
ReverseClutchAxis = False   # If True then the clutch input goes from 100 (down) to 0 (up)

ShifterNumber  =    1       # Shifter port
ClutchNumber   =    1       # Clutch port

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
#NeutralBtn     =   Numpad0 # The key used to force neutral, whatever the shifter says

firstGearJoyButton = Shifter1

# Gear change events
clutchDisengage         = 'clutchDisengage'
clutchEngage            = 'clutchEngage'
gearSelect              = 'gearSelect'
gearDeselect            = 'gearDeselect'

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

def GetKeyState(tbd, input):
  return wheel_o.getButtonState(input)

def GetClutchState():
  return wheel_o.getClutchState()

def SoundPlay(soundfile):
  PlaySound(soundfile, SND_FILENAME|SND_LOOP|SND_ASYNC)

def SoundStop():
  PlaySound(None, SND_FILENAME)

def msgBox(str):
  print(str)

#################################################################################

class graunch:
  def __init__(self):
        self.graunching = False
  def graunchStart(self):
        # Start the graunch noise and sending "Neutral"
        # Start the noise
        SoundPlay('Grind_default.wav')
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
        directInputKeySend.ReleaseKey('DIK_NUMPAD0')
        if self.graunching:
          SetTimer(self.graunch2, 20)


  def graunch2(self):
      if self.graunching:      
        # Send the "Neutral" key press
        directInputKeySend.PressKey('DIK_NUMPAD0')
        SetTimer(self.graunch1, 100)
        if debug >= 1:
            directInputKeySend.PressKey('DIK_G')
            time.sleep(.05)
            directInputKeySend.ReleaseKey('DIK_G')



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



def WatchClutch():
    # clutch
    global ClutchPrev
    global KeyToHoldDown
    ClutchState = 1 # engaged

    Clutch = GetClutchState()
    # Clutch 100 is up, 0 is down to the floor
    # Unless ReverseClutchAxis is True when it's the opposite.
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


    Gear1 = GetKeyState(ShifterNumber,Shifter1)
    Gear2 = GetKeyState(ShifterNumber,Shifter2)
    Gear3 = GetKeyState(ShifterNumber,Shifter3)
    Gear4 = GetKeyState(ShifterNumber,Shifter4)
    Gear5 = GetKeyState(ShifterNumber,Shifter5)
    Gear6 = GetKeyState(ShifterNumber,Shifter6)
    GearR = GetKeyState(ShifterNumber,ShifterR)

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
        KeyToHoldDown = 'DIK_NUMPAD6'
    elif GearR == 'D':
        KeyToHoldDown = 'DIK_NUMPAD9'
    else:
        KeyToHoldDown = 'DIK_NUMPAD0'

    if KeyToHoldDown == KeyToHoldDownPrev:  # The button is already down (or no button is pressed).
        #if AutoRepeat && KeyToHoldDown
        #   Send, KeyToHoldDown down  # Auto-repeat the keystroke.
        return

    if KeyToHoldDown == 'DIK_NUMPAD0':
            gearStateMachine(gearDeselect)
    else:
            gearStateMachine(gearSelect)

    # Otherwise, release the previous key and press down the new key:
    SetKeyDelay = -1  # Avoid delays between keystrokes.
    if KeyToHoldDownPrev:   # There is a previous key to release.
         directInputKeySend.ReleaseKey(KeyToHoldDownPrev)  # Release it.
    return

    #############################################################


def ShowButtons():
  pass

""" TBD

    #SetFormat, float, 03  # Omit decimal point from axis position percentages.

    neutral = "Neutral"

    Loop, ForwardGears

        gear = Shiftera_index
        GetKeyState, Geara_index, ShifterNumbergear
        _i = a_index
        joyButton := _i-1 + firstGearJoyButton
        _gear = ShifterNumberJoyjoyButton
        GetKeyState, Geara_index, ShifterNumberJoyjoyButton
        if Geara_index = D

            Geara_index := "Selected"
            neutral := ""

        else

            Geara_index := ""



    GetKeyState, Clutch,ClutchNumberClutchAxis
    GetKeyState, GearR, ShifterNumberShifterR
    GetKeyState, Esc,   Escape

    if GearR = D

        GearR := "Selected"
        neutral := ""

    else

        GearR := ""


    if ReverseClutchAxis = True

        if Clutch > ClutchEngaged
            ClutchState := "disengaged"
        else
            ClutchState := "engaged"

    else

        if Clutch < ClutchEngaged
            ClutchState := "disengaged"
        else
            ClutchState := "engaged"


    ToolTip, Test Mode`n`nClutch: Clutch ClutchState`nGear 1: Gear1`nGear 2: Gear2`nGear 3: Gear3`nGear 4: Gear4`nGear 5: Gear5`nGear 6: Gear6`nGear R: GearR`nneutral`n`nEsc to exit
    if Esc = D
        ExitApp
    return
"""

if __name__ == "__main__":
  wheel_o = Wheel('Logitech G25 Racing Wheel USB')
  graunch_o = graunch()
  if wheel_o.error:
    print(wheel_o.error_string)
    exit()
  if TestMode == False:
      #SetTimer(WatchClutch, 10)
      wheel_o.run(WatchClutch)
  else:
      SetTimer(ShowButtons, 100)

