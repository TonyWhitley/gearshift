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
    button = controller.get_button( i )
    print("Button {:>2} value: {}".format(i+1,button) )
    if i == 19-1 and button:
      print('Button 19 pressed')
      directInputKeySend.PressKey('DIK_NUMPAD0')

def printAxis(controller):
  for axis_index in range(controller.get_numaxes()):
      axis_status = controller.get_axis(axis_index)
      if axis_status < -.5 and axis_state[axis_index] == 0:
        print('%s pressed' % axis_names[axis_index])
        axis_state[axis_index] = 1
      if axis_status > .5 and axis_state[axis_index] == 1:
        print('%s released' % axis_names[axis_index])
        axis_state[axis_index] = 0



class Controller:
  error_string = ''
  error = False
  num_controllers = 0
  num_buttons = 0
  num_axes = 0
  controllerNames = []

  def __init__(self):
    pygame.init()

    self.num_controllers = pygame.joystick.get_count()
    if self.num_controllers < 1:
        self.error_string = 'No Controllers'
        self.error = True
        return

    self.controllerNames = []
    for j in range(self.num_controllers):
      _j = pygame.joystick.Joystick(j)
      self.controllerNames.append(_j.get_name())

  def selectController(self, controllerName):
    self.controller = pygame.joystick.Joystick(0) # fallback value
    for j in range(self.num_controllers):
      _j = pygame.joystick.Joystick(j)
      if _j.get_name() == controllerName:
        self.controller = pygame.joystick.Joystick(j)

    self.controller.init()
    self.num_axes = self.controller.get_numaxes()
    self.axis_state = [0] * self.num_axes
    self.num_buttons = self.controller.get_numbuttons()
    self.controller_name = self.controller.get_name()
    if self.controller_name != controllerName:
        self.error_string = 'Controller is "%s" not "%s"' % (self.controller_name, controllerName)
        self.error = True
        return

  def getAxis(self, axis):
    """ return 100 clutch released, 0 clutch pressed """
    axisValue = self.controller.get_axis(axis)
    # 1 is released, -1 is pressed
    return int((axisValue * 50)) + 50

  def getButtonState(self, buttonNumber):
    state = self.controller.get_button(buttonNumber)
    if state:
      result = 'D'
    else:
      result = 'U'
    return result

  def run(self, callback, tk_main_dialog = None):
    while 1:
      for event in pygame.event.get(): # User did something
          if event.type == pygame.QUIT: # If user clicked close
              return
          # Possible controller actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
          if event.type == pygame.JOYAXISMOTION:
              #printAxis(self.controller)
              callback()
          if event.type == pygame.JOYBUTTONDOWN:
              #self.buttonPushed()
              callback()
          if event.type == pygame.JOYBUTTONUP:
              #self.buttonReleased()
              callback()
      if tk_main_dialog:  # Tk is running as well
        try:
          tk_main_dialog.update()
        except:
          pass # tk_main_dialog has been destroyed.


