# Python 3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font 

from configIni import Config
from wheel import Controller

gears = {      #tkButton, 
                      #tkLabel, 
                            #tkStringVar, 
                                  #JoystickButton
  '1st gear' : [None, None, None, 8],
  '2nd gear' : [None, None, None, 9],
  '3rd gear' : [None, None, None, 10],
  '4th gear' : [None, None, None, 11],
  '5th gear' : [None, None, None, 12],
  '6th gear' : [None, None, None, 13],
  '7th gear' : [None, None, None, 0],
  '8th gear' : [None, None, None, 0],
  'Reverse'  : [None, None, None, 14]
  }

def setGear(name, controller_o):
  messagebox.showinfo('', 'Select %s then press OK' % name)
  for g in range(controller_o.num_buttons):
    if controller_o.getButtonState(g) == 'D':
      gears[name][2].set(g)
      gears[name][1].configure(text=str(g))
      return g
  messagebox.showinfo('', 'No gear pressed')
  gears[name][2].set(None)
  gears[name][1].configure(text='')

def setClutch(controller_o):
  messagebox.showinfo('', 'Press the clutch then press OK')
  for g in range(controller_o.num_axes):
    print(g, controller_o.getAxis(g))
    if controller_o.getAxis(g) < 90:
      pass
  messagebox.showinfo('', 'Clutch not pressed')

def dummy():
  pass

#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    self.controller_o = Controller()
    self.config_o = Config()

    xPadding = 10
    tkFrame_Shifter = tk.LabelFrame(parentFrame, text='Shifter')
    tkFrame_Shifter.grid(column=1, row=2, sticky='ew', padx=xPadding)

    # Create a Tkinter variable
    self.shifterController = tk.StringVar(root)

    self.controllerChoice(tkFrame_Shifter, self.shifterController)

    for _gear, (name, gear) in enumerate(gears.items()):
      gears[name][0] = tk.Button(tkFrame_Shifter, text=name, width=12, 
                                 command=lambda n=name, w=self.controller_o: setGear(n,w))
      gears[name][0].grid(row = _gear+2, sticky='w')
      gear[3] = self.config_o.get('shifter', name)
      gears[name][1] = tk.Label(tkFrame_Shifter, text=gear[3])
      gears[name][1].grid(row = _gear+2, column=2, sticky='w')
      gears[name][2] = tk.StringVar()

    self.shifterController.set(self.config_o.get('shifter', 'controller'))


    tkFrame_Clutch = tk.LabelFrame(parentFrame, text='Clutch', padx=xPadding)
    tkFrame_Clutch.grid(column=3, row=2, sticky='ew')

    # Create a Tkinter variable
    self.clutchController = tk.StringVar(root)

    self.controllerChoice(tkFrame_Clutch, self.clutchController)
    self.clutchController.set(self.config_o.get('clutch', 'controller'))

    tkButton_selectClutch = tk.Button(tkFrame_Clutch, text='Select clutch', width=12, 
                                command=lambda w=self.controller_o: setClutch(w))
    tkButton_selectClutch.grid(row = 2, sticky='w')

    tkLabel_clutchBitePoint = tk.Label(tkFrame_Clutch, text='Clutch bite point')
    tkLabel_clutchBitePoint.grid(column=0, row=3, sticky='e')

    tkScale_clutchBitePoint = tk.Scale(tkFrame_Clutch, from_=0, to=100, orient=tk.HORIZONTAL)
    tkScale_clutchBitePoint.grid(column=1, row=2, sticky='ewns')

    tkCheckbutton_GearClutch = tk.Checkbutton(tkFrame_Clutch, text='Shifter damage (Grinding Tranny)')

    tkCheckbutton_GearClutch.grid(sticky='w')

    buttonFont = font.Font(weight='bold', size=10)

    self.tkButtonSave = tk.Button(
        parentFrame,
        text="Save configuration",
        width=20,
        height=2,
        background='green',
        font=buttonFont,
        command=self.save)
    self.tkButtonSave.grid(column=2, row=3, pady=25)


    self.controller_o.run(dummy, parentFrame)

  def controllerChoice(self, parent, tkvar):
    # List with options
    choices = self.controller_o.controllerNames

    tkvar.set(choices[0]) # set the default option
 
    popupMenu = tk.OptionMenu(parent, tkvar, *choices)
    tk.Label(parent, text="Choose a controller").grid(row = 0, column = 0)
    popupMenu.grid(row=0, column=2)
 
    # on change dropdown value
    def change_dropdown(*args):
        name = tkvar.get()
        #self.controller_o.del()
        self.controller_o.selectController(name)

    # link function to change dropdown
    tkvar.trace('w', change_dropdown)

  def save(self):
    self.config_o.set('shifter','controller', self.shifterController.get())
    self.config_o.set('clutch','controller', self.clutchController.get())
    for name, gear in gears.items():
      self.config_o.set('shifter', name, gear[2].get())
    self.config_o.write()

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Options']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabOptions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabOptions.grid()
    
  o_tab = Tab(tabOptions)
  root.mainloop()
