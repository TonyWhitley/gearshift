# This works 25/9/2018

import pygame

import directInputKeySend

pygame.init()

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

num_joysticks = pygame.joystick.get_count()
if num_joysticks < 1:
    print("You didn't plug in a joystick.")
    pass

joystick = pygame.joystick.Joystick(0)
joystick.init()
axis_state = [0] * joystick.get_numaxes()
joystick_name = joystick.get_name()
print(joystick_name)

buttons = joystick.get_numbuttons()
print("Number of buttons: {}".format(buttons) )

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
  print(joystick.get_axis(4))

pass

while 1:
  for event in pygame.event.get(): # User did something
      if event.type == pygame.QUIT: # If user clicked close
          exit()

      # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
      if event.type == pygame.JOYAXISMOTION:
          printAxis(joystick)
      if event.type == pygame.JOYBUTTONDOWN:
          print("Joystick button pressed.")
          #VK2.pressAndHold('esc')
          buttonPushed()
      if event.type == pygame.JOYBUTTONUP:
          #VK2.release('esc')
          directInputKeySend.ReleaseKey('DIK_NUMPAD0')
          print("Joystick button released.")

