# gearshift
Clutch/gearbox simulation for rFactor 2 in particular.

Inspired by the "Grinding Tranny Mod" (http://www.richardjackett.com/grindingtranny) written for rFactor 1 this program monitors a shifter and clutch and if the clutch is not pressed when changing gear it sounds a graunching noise and repeatedly sends a **Neutral** key press to prevent the gear being selected .

Nothing is specific to rFactor, gearshift will work with other games including rF1.

# Installing
1. Go to the [Releases page](releases) and download the latest **gearshift.exe, Configurer.exe** and **Grind_default.wav** to a folder on your PC.

2. Run Configurer.exe to set up for your shifter and pedals (that creates gearshift.ini).

3. Once configured, run gearshift.exe then start rFactor 2.  

4. In rF2 set the **Neutral** control to **Numpad 0** - now if you try to select a gear without the clutch pressed **gearshift** will send Numpad 0 repeatedly to stop rFactor selecting the gear, it will also make the sound of the gears grinding :scream:

