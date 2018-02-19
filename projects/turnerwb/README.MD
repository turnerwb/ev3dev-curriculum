Operation Red Light/Green Light:

*****
NB: If you're looking for the main file, on the PC end it's FinalProject.py and on the EV3 end it's EV3Controller.py
*****

Goal: To create an Arduino/EV3 interface to play Red Light, Green Light with an EV3 Robot using a Tkinter
interface.
LIST OF FILES(See Doc-Strings at top of files for more information):
PC Side:
ArduinoController.py
Communication.py
FinalProject.py
TkinterWindow.py

EV3 Side:
EV3Communications.py
EV3Controller.py
EV3Gamemaster.py

Files For Debug Only:
PCEV3Simulator.py
fake_robot_controller.py


KNOWN BUGS:
1.)The PIXY does not like to always pick up the LEDs (especially the red LED) without giving false positives:
PROPOSED FIX: None; Optimal conditions are non-red tinted light or dim lighting, no software fix possible.
2.)The PIXY will not pick up either LED and/or will not distinguish between the green and red LEDs:
PROPOSED FIX: Hold a sheet of printer paper over the light, this diffuses the light and gives the PIXY a swatch of
colour rather than a point of light
3.)Queued update scripts throw errors after Tkinter window is destroyed
NO KNOWN FIX
4.)New Game Windows don't always appropriately have the radio button variables set when a new game is called. The
circumstances which cause this are unknown
NO KNOWN FIX

CHANGELOG:
2/8/2018: Tweaked Blink sample code as proof of concept of Arduino as light control.
2/10/2018: Completed Tkinter/Arduino System
2/14/2018: Completed program, list of completed TODOs at bottom of file.
2/15/2018: Added a digital input (Touch Sensor)

COMPLETED TASKS:
FinalProject.py:
# DONE 1: Verify that PIXY will work with LED, Note changes to camera needed to make it work
# DONE 2: Tkinter Gui, Red Light/Green Light Buttons, Call out button, Difficulty buttons?
# DONE 2A: Progress Bar on Tkinter? Other visual rep. of robot progress, Goes w/ DONE 9!!
# DONE 3: Random number generator to cause robot to 'Cheat.' Perhaps vary distance
# DONE 4: Robot/Light system
# DONE 5: Tkinter/Arduino System
# DONE 6: Test lag between Light change and robot stop. Is it slow enough that the user can see a delay if no cheat?
# DONE 7: MQTT Computer to Robot: Difficulty information
# DONE 8: MQTT Computer to Robot: Testing if the robot cheated
# (I'm thinking something like the Gamemaster from "Petals on a Rose")
# DONE 9: MQTT Robot to Computer: Testing how far the robot went (Decide on a victory condition)
# DONE 10: How to multitask and determine Win/Loss and Progress
# DONE 11: Add Doc Strings

Communication.py:
# DONE Write victory/defeat functions
# DONE Write comm for robot in case of early quit from game window
# DONE Write comm for caught_cheating

EV3Gamemaster.py:
# DONE Test and decide on final speed values for difficulties
# DONE Test and decide on final bounds for difficulties

TkinterWindow.py:
# DONE 1 Add buttons for cheating
# DONE 2 Add difficulty buttons
# DONE 3 Make Window Look Nice
# DONE 4 New Game Window?
# DONE 5 Progress Bar for distance until victory