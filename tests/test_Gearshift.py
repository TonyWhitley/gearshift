import unittest

from Gearshift import main, gearStateMachine, set_graunch_o
from Gearshift import clutchDisengage, clutchEngage, gearSelect
from Gearshift import gearDeselect, graunchTimeout, smStop
from Gearshift import SetTimer, StopTimer

# Gear change states (internal to gearStateMachine()) 
neutral                = 'neutral'
clutchDown             = 'clutchDown'
waitForDoubleDeclutchUp= 'waitForDoubleDeclutchUp'
clutchDownGearSelected = 'clutchDownGearSelected'
inGear                 = 'inGear'
graunching             = 'graunching'
graunchingClutchDown   = 'graunchingClutchDown'
graunchingNeutral      = 'graunchingNeutral'

# Mock class to satisfy gearStateMachine
class graunch:
  def __init__(self):
        self.graunching = False
        self.neutralTimer = None

  def graunchStart(self):
        self.graunching = True
        self.__sendNeutralButton()
            
  def graunchStop(self):
        self.graunching = False
        self.stopNeutralTimeout()
        self.__releaseNeutralButton()

  def stopNeutralTimeout(self):
    """ 
    We were waiting to see if  the effect of the "Neutral" key 
    would persist but rF2 has selected the gear again
    """
    if self.neutralTimer:
      StopTimer(self.neutralTimer)
      self.neutralTimer = None

  def isGraunching(self):
    return self.graunching

  # Internal functions
  def __sendNeutralButton(self):
      if self.graunching:      
        # If rF2 doesn't bounce it back into gear before this
        # timer times out then the driver has moved the stick
        # back to neutral
        self.neutralTimer = SetTimer(self.__neutralTimeout, 300)
        self.rF2endsNeutralTimer = SetTimer(self.rF2endsNeutral, 200)

  def __releaseNeutralButton(self):
      if self.graunching:
        SetTimer(self.__sendNeutralButton, 209)

  def rF2endsNeutral(self):
      # rF2 sees shifter still trying to select gear
      gearStateMachine(gearSelect)

  def __neutralTimeout(self):
      """ Shared memory.
      Neutral key causes gearDeselect event but if player doesn't move shifter
      to neutral then rF2 will quickly report that it's in gear again,
      causing a gearSelect event.
      If SM is still in neutral (gearSelect hasn't happened) when 
      neutralTimer expires then player has moved shifter to neutral
      """
      gearStateMachine(graunchTimeout)

stateMachineTestSequences = [
  {'testName': 'clutchDownNeutral', # Meaningful name for error reports
   'events': [clutchDisengage],     # Events
   'endState': clutchDown           # the state the SM should end up in
   },
  {'testName': 'clutchDownGear',
   'events': [clutchDisengage, gearSelect],
   'endState': clutchDownGearSelected 
   },
  {'testName': 'clutchDownGearEngage',
   'events': [clutchDisengage, gearSelect, clutchEngage],
   'endState': inGear 
   },
  {'testName': 'gearGearGraunch',
   'events': [clutchDisengage, gearSelect, clutchEngage, gearSelect],
   'endState': graunching 
   },
  {'testName': 'clutchUpGearGraunch',
   'events': [clutchEngage, gearSelect],
   'endState': graunching
   },
  {'testName': 'graunchingGearDeselect',
   'events': [clutchEngage, gearSelect, gearDeselect],
   # gearDeselect is a result of the Neutral key press
   'endState': graunchingNeutral
   },
  {'testName': 'graunchingClutchDown',
   'events': [clutchEngage, gearSelect, gearDeselect, clutchDisengage],
   'endState': graunchingClutchDown
   },
  {'testName': 'graunchingNeutralTimeout',
   'events': [clutchEngage, gearSelect, gearDeselect, graunchTimeout],
   'endState': neutral
   },
  # still in gear, rf2 has "recovered" from Neutral button
  {'testName': 'graunchingNeutralGearSelect',
   'events': [clutchEngage, gearSelect, gearDeselect, gearSelect],
   'endState': graunching
   },
  # still in gear, rf2 has "recovered" from Neutral button - twice
  {'testName': 'graunchingNeutralGearSelectTwice',
   'events': [clutchEngage, gearSelect, gearDeselect, gearSelect, gearDeselect, 
              gearSelect],
   'endState': graunching
   },
  # still in gear, rf2 has "recovered" from Neutral button - twice then 
  # player shifts to neutral
  {'testName': 'graunchingNeutralGearSelectTwiceThenNeutral',
   'events': [clutchEngage, gearSelect, gearDeselect, gearSelect, gearDeselect,
              gearSelect, gearDeselect, graunchTimeout],
   'endState': neutral
   },


  ]

class Test_Gearshift(unittest.TestCase):
  def setUp(self):
    set_graunch_o(graunch())
    pass
  def test_Gearshift_main_runs(self):
    # Preliminary test - does main run?
    root, controls_o = main()
    controls_o.stop()
    assert root != None

  def test_SM_clutchDownNeutral(self):
    # preliminary test, same as stateMachineTestSequences[0]
    gearstate = gearStateMachine(clutchDisengage)
    assert gearstate == clutchDown

  def test_SM_scenarios(self):
    for scenario in stateMachineTestSequences:
      for event in scenario['events']:
        gearstate = gearStateMachine(event)
    #assert gearstate == scenario['endState'], "{} expected end state {}, got {}" \
    #  .format(scenario['testName'], scenario['endState'], gearstate)
    # Using string interpolation:
    assert gearstate == scenario['endState'], f"{scenario['testName']} "\
      f"expected end state {scenario['endState']}, got {gearstate}"

if __name__ == '__main__':
  unittest.main(exit=False)