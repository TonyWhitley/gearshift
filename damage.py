"""
Calculate damage done to engine/gearbox/clutch
and feed it back
* graunchy gear changes
   if not done slowly
   double declutching?
* missing gears
* blown engine

Damage is done by misuse or can just happen
Damage available even if manual gearbox or clutch not used.

Misuse
* change gear without clutch
* downshift at too higher speed
    damages engine (over rev)
    damages gearbox and clutch (torque mismatch)
* rev mismatch on upshift or downshift
    including starts

May need to calculate gear ratios from mLocalVel [velocity (m/S) in local vehicle coordinates]
current gear and revs.
"""

class Damage:
  def __init__(self):
    self.damage = {'engine': None,
                   'clutch': None,
                   'gearbox' :None}
  def gearChange(self, timeTaken, engineRPM, clutchRPM, to, _from):
    """
    The actual movement of the stick
    """
    pass
  def clutchEngage(self, engineRPM, clutchRPM):
    """
    Engaging the clutch
    What's the relation between clutchRPM and the speed of the car?
      A bad change means a difference between what the clutch will end 
      up running at and how fast the propshaft is driving the gearbox
    """
    pass


