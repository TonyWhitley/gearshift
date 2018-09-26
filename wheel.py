# G25 wheel class

import pygame

"""
Axes:
  0 -ve      Left
  0 +ve      Right
  1          ???
  2 1 -> -1  Accelerator
  3 1 -> -1  Brake
  4 1 -> -1  Clutch
"""

axis_names = [
  'wheel',
  '?????',
  'accelerator',
  'brake',
  'clutch'
  ]

clutch_index = 4

def buttonPushed():
  for i in range( buttons ):
    button = joystick.get_button( i )
    print("Button {:>2} value: {}".format(i+1,button) )
    if i == 19-1 and button:
      print('Button 19 pressed')
      directInputKeySend.PressKey('DIK_NUMPAD0')

def printAxis(joystick):
  for axis_index in range(joystick.get_numaxes()):
      axis_status = joystick.get_axis(axis_index)
      if axis_status < -.5 and axis_state[axis_index] == 0:
        print('%s pressed' % axis_names[axis_index])
        axis_state[axis_index] = 1
      if axis_status > .5 and axis_state[axis_index] == 1:
        print('%s released' % axis_names[axis_index])
        axis_state[axis_index] = 0



class Wheel:
  error_string = ''
  error = False

  def __init__(self, wheelName):
    pygame.init()

    num_joysticks = pygame.joystick.get_count()
    if num_joysticks < 1:
        self.error_string = 'No Wheel'
        self.error = True
        return

    self.joystick = pygame.joystick.Joystick(0)
    self.joystick.init()
    self.axis_state = [0] * self.joystick.get_numaxes()

    self.joystick_name = self.joystick.get_name()
    if self.joystick_name != wheelName:
        self.error_string = 'Wheel is "%s" not "%s"' % (self.joystick_name, wheelName)
        self.error = True
        return

    buttons = self.joystick.get_numbuttons()

  def getClutchState(self):
    """ return 100 clutch released, 0 clutch pressed """
    clutchValue = self.joystick.get_axis(clutch_index)
    # 1 is released, -1 is pressed
    return (clutchValue * 50) + 50

  def getButtonState(self, buttonNumber):
    state = self.joystick.get_button(buttonNumber)
    if state:
      result = 'D'
    else:
      result = 'U'
    return result

  def run(self, callback):
    while 1:
      for event in pygame.event.get(): # User did something
          if event.type == pygame.QUIT: # If user clicked close
              return
          # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
          if event.type == pygame.JOYAXISMOTION:
              printAxis(joystick)
              callback()
          if event.type == pygame.JOYBUTTONDOWN:
              self.buttonPushed()
              callback()
          if event.type == pygame.JOYBUTTONUP:
              self.buttonReleased()
              callback()


