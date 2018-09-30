from configparser import ConfigParser
import os

configFileName = 'gearshift.ini'
sections = ['clutch', 'shifter', 'miscellaneous']
clutchValues = {
  'controller' : 'Not yet selected',
  'axis'       : '0',
  'reversed'   : '0',
  'bite point' : '90'
 }
shifterValues = {
  'controller' : 'Not yet selected',
  '1st gear' : '0',
  '2nd gear' : '0',
  '3rd gear' : '0',
  '4th gear' : '0',
 
  '5th gear' : '0',
  '6th gear' : '0',
  '7th gear' : '0',
  '8th gear' : '0',
  'Reverse'  : '0'
  }
miscValues = {
  'damage'          : '0',
  'wav file'        : 'Grind_default.wav',
  'debug'           : '0',
  'test mode'       : '0',
  'double declutch' : '0',
  'preselector'     : '0',
  'reshift'         : '1',
  'neutral button'  : 'DIK_NUMPAD0'
  }


class Config:
  def __init__(self):
    # instantiate
    self.config = ConfigParser()

    # parse existing file if there is one
    if os.path.exists(configFileName):
      self.config.read(configFileName)
    else: # set default values
      for val, default in clutchValues.items():
          self.set('clutch', val, default)
      for val, default in shifterValues.items():
          self.set('shifter', val, default)
      for val, default in miscValues.items():
          self.set('miscellaneous', val, default)
      self.write()
      return

  def set(self, section, val, value):
    # update existing value
    if not self.config.has_section(section):
      self.config.add_section(section)
    self.config.set(section, val, value)

  def get(self, section, val):
    try:
      # get existing value
      if val in ['controller', 'wav file', 'neutral button'] :
        return self.config.get(section, val)
      else:
        return self.config.getint(section, val)
    except:
      self.set(section, val, '')
      return None

  def write(self):
    # save to a file
    with open(configFileName, 'w') as configfile:
        self.config.write(configfile)

if __name__ == "__main__":
  _config_o = Config()
  section = 'clutch'
  val = 'controller'
  value = _config_o.get(section, val)
  if value:
    if val == 'controller':
      print('%s/%s: %s' % (section, val, value))
    else:
      print('%s/%s: %d' % (section, val, value))
  else:
    print('%s/%s: <None>' % (section, val))
  _config_o.write()
