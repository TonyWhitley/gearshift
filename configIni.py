from configparser import ConfigParser
import os

configFileName = 'gearshift.ini'
sections = ['clutch', 'shifter', 'miscellaneous']
clutchValues = ['controller', 'axis', 'reversed', 'bite point']
shifterValues = ['controller', '1st gear', '2nd gear', '3rd gear', '4th gear', 
                 '5th gear', '6th gear', '7th gear', '8th gear', 'Reverse']
miscValues = ['damage', 'wav file', 'debug', 'test mode', 'double declutch', 
              'preselector', 'reshift', 'neutral button']


class Config:
  def __init__(self):
    # instantiate
    self.config = ConfigParser()

    # parse existing file if there is one
    if os.path.exists(configFileName):
      self.config.read(configFileName)
    else: # set default values
      for val in clutchValues:
        self.set('clutch', val, '')
      for val in shifterValues:
          self.set('shifter', val, '')
      for val in miscValues:
          self.set('miscellaneous', val, '')
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
