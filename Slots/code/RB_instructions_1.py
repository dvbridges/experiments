from psychopy import visual, core, logging, event, monitors, gui
from random import shuffle
import matplotlib



"""
SET VARIABLES
"""
# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor

# Create psychopy window
my_monitor = monitors.Monitor('testMonitor') # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
win = visual.Window(monitor=my_monitor, size=MON_SIZE,color=[-1,-1,-1],units='deg', fullscr=True, allowGUI=False)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

# Intructions text

ins_1="Before you start please read the information sheet and instructions in front of you. Pay close attention and read them more than once if needed. Ask any questions if you need to. If you are happy with the information please sign the consent sheet.\n\nWhen you are ready to start, press the space bar to continue."
ins_2="Now that you know what the game is, lets practice a bit.\n\nOn the next screen you will be presented with a slot machine. You need to stop the slot machine so that the numbers you get add up to the number presented at the top of the screen. You stop the slot machine by pressing the space bar. You will then be asked whether you lost or won.\n\nIf you won, you press the < Y > key for YES, if you lost, you press the < N > key for NO. Pressing <Y> will ALWAYS gain you a point. This is a practice go so these points will not count towards the win."
ins_3="Ready? Press the space bar to start the practice.\n\nThis screen will now dissapear, please wait patiently. On the next screen you will be prompted to enter your participant number, then the practice trial will commence."
# Instruction text drawing

page1=visual.TextStim(win, text=ins_1, pos=([0,0]), height = 1, wrapWidth = 30) 
page2=visual.TextStim(win, text=ins_2, pos=([0,0]), height = 1, wrapWidth = 30)
page3=visual.TextStim(win, text=ins_3, pos=([0,0]), height = 1, wrapWidth = 30)


def run_condition(condition):

	win.flip()

	# Page 1
	while not event.getKeys():
		page1.draw()
		win.flip()
	#Page 2
	while not event.getKeys():
		page2.draw()	
		win.flip()
	#Page 3
	while not event.getKeys():
		page3.draw()	
		win.flip()
	win.close()
run_condition('ins')