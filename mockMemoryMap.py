# Simple GUI to poke inputs into the memory map

import tkinter as tk
from tkinter import font, ttk
from time import sleep

from Mmap_for_DSPS_V22 import SimInfo

#fontBold = font.Font(family='Helvetica', size=8, weight='bold', slant='italic')

GEARS = ['Reverse', 'Neutral','1','2','3','4','5','6']
CLUTCH_DELAY = 100.0 / 1000.0   # 100 mS
GEAR_DELAY = 200.0 / 1000.0   # 100 mS
TICKOVER = 1000

class Gui:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    self.parentFrame = parentFrame
    self.info = SimInfo()
    clutch = self.info.Rf2Tele.mVehicles[0].mUnfilteredClutch # 1.0 clutch down, 0 clutch up
    gear  = self.info.Rf2Tele.mVehicles[0].mGear  # -1 to 6

    tkLabel_Options = tk.Label(parentFrame, 
                                text='Simple GUI to fake clutch, gear selection and revs\n'
                                '"Auto clutch" presses and releases the clutch')
    tkLabel_Options.grid(column=1, row=1, columnspan=3)
    self.settings = {}
    self.vars = {}
    _tkCheckbuttons = {}
    _tkRadiobuttons = {}

    xPadding = 10
    ####################################################
    tkFrame_Gearbox = tk.LabelFrame(parentFrame, text='Clutch')
    tkFrame_Gearbox.grid(column=1, row=2, sticky='ew', padx=xPadding)

    self._createBoolVar('Clutch pressed', False)
    _tkCheckbuttons['Clutch pressed'] = tk.Checkbutton(tkFrame_Gearbox, 
                                                 text='Pressed',
                                                 variable=self.vars['Clutch pressed'],
                                                 command=self.clutchOperation)

    _tkCheckbuttons['Clutch pressed'].grid(sticky='w')

    self._createBoolVar('Auto clutch', True)
    _tkCheckbuttons['Auto clutch'] = tk.Checkbutton(tkFrame_Gearbox, 
                                                 text='Automatic',
                                                 variable=self.vars['Auto clutch'])

    _tkCheckbuttons['Auto clutch'].grid(sticky='w')

    ####################################################
    tkFrame_Gear = tk.LabelFrame(parentFrame, text='Gear', padx=xPadding)
    tkFrame_Gear.grid(column=1, row=3, sticky='ew')

    self._createVar('Gear', 'Neutral')
    for gear in GEARS:
      _tkRadiobuttons[gear] = tk.Radiobutton(tkFrame_Gear, 
                                                  text=gear, 
                                                  variable=self.vars['Gear'], 
                                                  value=gear,
                                                  command=self.gearChange)
      _tkRadiobuttons[gear].grid(sticky='w')
      _tkRadiobuttons[gear].update()

    ####################################################
    tkFrame_GraphicsSetup = tk.LabelFrame(parentFrame, text='Revs')
    tkFrame_GraphicsSetup.grid(column=2, row=1, rowspan=3, sticky='ew', padx=xPadding)

    _EngineRPMCol = 1
    self._createVar('EngineRPM', TICKOVER)
    
    tkLabel_EngineRPM = tk.Label(tkFrame_GraphicsSetup, 
                                          text='Engine revs',
                                          #font=fontBold,
                                          justify=tk.LEFT)
    tkLabel_EngineRPM.grid(column=_EngineRPMCol, row=1, sticky='nw')

    tkScale_EngineRPM = tk.Scale(tkFrame_GraphicsSetup, 
                                  from_=TICKOVER, 
                                  to=10000, 
                                  orient=tk.VERTICAL, 
                                  variable=self.vars['EngineRPM'],
                                  command=self.EngineRPM)
    tkScale_EngineRPM.grid(column=_EngineRPMCol, row=2, rowspan=3, sticky='ew')

    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsSetup, text='Tickover')
    tkLabel_Graphics_0.grid(column=_EngineRPMCol, row=2, sticky='nw')
    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsSetup, text='Rev limit')
    tkLabel_Graphics_10.grid(column=_EngineRPMCol, row=4, sticky='nw')

    _ClutchRPMCol = 2
    self._createVar('ClutchRPM', 0)
    
    tkLabel_ClutchRPM = tk.Label(tkFrame_GraphicsSetup, 
                                          text='Gearbox Revs',
                                          #font=fontBold,
                                          justify=tk.LEFT)
    tkLabel_ClutchRPM.grid(column=_ClutchRPMCol, row=1, sticky='n')
    tkScale_ClutchRPM = tk.Scale(tkFrame_GraphicsSetup, 
                                  from_=0, 
                                  to=20000, 
                                  orient=tk.VERTICAL, 
                                  variable=self.vars['ClutchRPM'],
                                  command=self.ClutchRPM)
    tkScale_ClutchRPM.grid(column=_ClutchRPMCol, row=3, sticky='ewns')

    tkLabel_Graphics_10 = tk.Label(tkFrame_GraphicsSetup, text='Stationary')
    tkLabel_Graphics_10.grid(column=_ClutchRPMCol, row=2, sticky='nw')
    tkLabel_Graphics_0 = tk.Label(tkFrame_GraphicsSetup, text='Downshift\nover rev')
    tkLabel_Graphics_0.grid(column=_ClutchRPMCol, row=4, sticky='nw')
  
  def _createVar(self, name, value):
    self.vars[name] = tk.StringVar(name=name)
    self.vars[name].set(value)

  def _createBoolVar(self, name, value):
    self.vars[name] = tk.BooleanVar(name=name)
    self.vars[name].set(value)

  ####################################### Commands
  def _operateClutch(self, pressed):
    if pressed:
      self.info.Rf2Tele.mVehicles[0].mUnfilteredClutch = 1.0 # 1.0 clutch down, 0 clutch up
      sleep(CLUTCH_DELAY)
      print('[Mock: Clutch pressed]')
    else:
      self.info.Rf2Tele.mVehicles[0].mUnfilteredClutch = 0.0 # 1.0 clutch down, 0 clutch up
      sleep(CLUTCH_DELAY)
      print('[Mock: Clutch released]')
  def clutchOperation(self):
    self._operateClutch(self.vars['Clutch pressed'].get())

  def gearChange(self):
    if self.vars['Auto clutch'].get():
      self._operateClutch(True)
    print('[Mock: gear %s]' % self.vars['Gear'].get())
    self.info.Rf2Tele.mVehicles[0].mGear = GEARS.index(self.vars['Gear'].get())-1 
    # -1=reverse, 0=neutral, 1+=forward gears
    sleep(GEAR_DELAY)
    if self.vars['Auto clutch'].get():
      self._operateClutch(False)

  def EngineRPM(self, event):
    self.info.Rf2Tele.mVehicles[0].mEngineRPM = int(self.vars['EngineRPM'].get())

  def ClutchRPM(self, event):
    self.info.Rf2Tele.mVehicles[0].mClutchRPM = int(self.vars['ClutchRPM'].get())

  def on_closing(self):
    self.info.close()
    self.parentFrame.destroy()

def gui():
  root = tk.Tk()
  mockMemoryMap = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  mockMemoryMap.grid()
    
  o_gui = Gui(mockMemoryMap)
  # Trying for a clean shutdown 
  # root.protocol("WM_DELETE_WINDOW", o_gui.on_closing)
  root.mainloop()
  pass

if __name__ == '__main__':
  # To run this frame by itself for development
  gui()