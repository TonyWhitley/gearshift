import unittest

from Gearshift import main, gearStateMachine, set_graunch_o
from Gearshift import clutchDisengage, clutchEngage, gearSelect
from Gearshift import gearDeselect, graunchTimeout, smStop

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
    self.t3 = None
  def graunchStart(self):
    # Start the graunch noise and sending "Neutral"
    #self.graunch2()
    pass

  def graunchStop(self):
    self.graunching = False

  def graunch3(self):
    pass

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
   'events': [gearSelect],
   'endState': graunching
   },
  {'testName': 'graunchingGearDeselect',
   'events': [gearSelect, gearDeselect],
   'endState': graunchingNeutral
   },
  {'testName': 'graunchingClutchDown',
   'events': [gearSelect, clutchDisengage],
   'endState': graunchingClutchDown
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