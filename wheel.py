# G25 wheel class

import pygame
import sys

"""
G25 Axes:
  0 -ve      Left
  0 +ve      Right
  1          ???
  2 1 -> -1  Accelerator
  3 1 -> -1  Brake
  4 1 -> -1  Clutch
"""

class Controller:
  error_string = ''
  error = False
  num_controllers = 0
  num_buttons = 0
  num_axes = 0
  controllerNames = []

  def get_name(self, controller):
    """
    pygame's get_name() can give an exception "invalid utf-8 character"
    """
    _name = 'Error getting controller name'
    try:
      _name = controller.get_name()
    except UnicodeError as e:
      _name = 'Unicode error getting controller name'
    except:
      _name = 'Other error getting controller name'
      print("Unexpected error:", sys.exc_info()[0])
    return _name
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
      self.controllerNames.append(self.get_name(_j))

  def selectController(self, controllerName):
    self.controller = pygame.joystick.Joystick(0) # fallback value
    for j in range(self.num_controllers):
      _j = pygame.joystick.Joystick(j)
      if self.get_name(_j) == controllerName:
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

  def pygame_tk_check(self, callback, tk_main_dialog = None):
    """ Run pygame and tk to get latest events """
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            return
        # Possible controller actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYAXISMOTION:
            callback()
        if event.type == pygame.JOYBUTTONDOWN:
            callback()
        if event.type == pygame.JOYBUTTONUP:
            callback()
    if tk_main_dialog:  # Tk is running as well
      try:
        tk_main_dialog.update()
      except:
        pass # tk_main_dialog has been destroyed.


  def run(self, callback, tk_main_dialog = None):
    """ Run pygame and tk event loops """
    while 1:
      self.pygame_tk_check(callback, tk_main_dialog)
