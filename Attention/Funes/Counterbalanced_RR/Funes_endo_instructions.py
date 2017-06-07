#import psychopy
from psychopy import visual, core, logging, event, monitors, gui
from random import shuffle
import matplotlib
import ppc # has writer class

#####
#Things to do to set up a PC for setting
#####
#1) Run screen_framerate_test.py to test the refresh rate of the screen - this will help determine stim frame display times
	##### this is extremely important as you then set all times according to thig

#Information about experiment.
	# number of reps - 8 trials per repetition - 192 trials for exo, 288 trials (67% predictive = 192 predictive trials + 96 normal trials)
		# so, 24 reps makes 192 trials in exo. For endo, 12 reps makes 96 trials, but 48 trials makes 192 trials (only 4 trials per rep). Note, reps index starts at zero = 60 reps for endo, 24 for exo
	# SOAs should be 100 an 800 ms, exo cerebral acitivity peaks at 100ms (see Chica review)
	# check all timings on uni computers, fixation, cue, SOA, target, ISI
"""
SET VARIABLES
"""
# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor
SAVE_FOLDER = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.

# Stimulus paramters
TARGETS = ['X','O']

# Timings - check refresh rate, should be 16ms per frame
FRAMES_FIX = 30 # 500ms 
FRAMES_CUE = 3   # 50ms 
FRAMES_TAR = 2   # 33ms	
SOA = [9,45] 	 # need SOA of 100 and 800 ms from cue onset, so SOA needs to be 50ms, and 750ms  
#Condition parameters

CUE_POSITIONS = [-5,5]
TARG_POSITIONS = [-5,5]
REPETITIONS = 1 # 

# Create base stim

# Create psychopy window
my_monitor = monitors.Monitor('testMonitor') # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
win = visual.Window(monitor=my_monitor, size=MON_SIZE,color=[-1,-1,-1],units='deg', fullscr=True, allowGUI=False)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

# Stuff
clock = core.Clock()

# create base stimli

square1=visual.Rect(win, width=2.85, height=2.45, pos=[-5, 0])
#square2=visual.Rect(win, width=2, height=2, pos=([0, 0]))
square3=visual.Rect(win, width=2.85, height=2.45, pos=[5, 0])
fixation=visual.Circle(win, pos=([0,.05]), radius = .2) # check sizes, should be 1x1 degrees


# Responses and keys
KEYS_QUIT = ['q']  # Keys that quits the experiment
RESPONSES = {'left': 'lctrl', 'right': 'rctrl'}

# Create text stimuli

breaktxt1 = 'You are now on a break. Please rest your eyes for a few seconds. When you are ready, please push a response key to continue.'
breaktxt2 = 'Ready?'
breakInstr=visual.TextStim(win, text=breaktxt1, pos=([0,0]), height = 1) # Break instructins
breakReady=visual.TextStim(win, text=breaktxt2, pos=([0,0]), height = 1) # Break - READY?

#Create exp stimuli
cue=visual.Circle(win, pos=([0,.05]), radius = .4)
RarrowRec = [(-0.15,0.05),(-0.15,-0.05),(-.0,-0.05),(-.0,0.05)]
RarrowHead = [(-.0,-0.19),(-.0,0.19),(.15,0)]
Rrec = visual.ShapeStim(win, vertices=RarrowRec, size=4, fillColor='white', lineColor='white')
Rhead = visual.ShapeStim(win, vertices=RarrowHead, size=4, fillColor='white', lineColor='white')
LarrowRec = [(0.15,0.05),(0.15,-0.05),(0,-0.05),(0,0.05)]
LarrowHead = [(-.0,-0.19),(-.0,0.19),(-.15,0)]
Lrec = visual.ShapeStim(win, vertices=LarrowRec, size=4, fillColor='white', lineColor='white')
Lhead = visual.ShapeStim(win, vertices=LarrowHead, size=4, fillColor='white', lineColor='white')
# Intructions text

ins_1 = 'Welcome to the experiment. Please push a button to continue.'
ins_2 = 'In this experiment, we are going to measure how you process things in the visual world. In general, you will be asked to discriminate the direction of a target arrow which appears on the screen in one of two locations.'
ins_3 = 'First, you will see a fixation point, with boxes at each side. Please centre your gaze on the fixation. Following this, you will see a coloured dot at the fixation, which will tell you with high probability where target will appear. Please push the button to see what the cues will look like.'
ins_4 = 'If the coloured dot is GREEN, there is a high probability that the target will appear to the LEFT of the fixation'
ins_5 = 'If the coloured dot is RED, there is a high probability that the target will appear to the RIGHT of the fixation'
ins_6 = 'After the cue disappears you will see the target arrow appear in one of the boxes to the left or right of the fixation.'
ins_7 = 'If the target arrow points LEFT, please push the LEFT CTRL button with your index finger on your left hand.'
ins_8 = 'If the target arrow points RIGHT, please push the RIGHT CTRL button with your index finger on your right hand.'
ins_9 = 'Please remember to keep your eyes fixated on the fixation cue presented at the beginning of each trial.\n\nPlease be as quick and accurate as you can with your response. If you give an incorrect reponse you will receive onscreen feedback that your response was incorrect.'
ins_10 = 'Please let the experimenter know if you have any questions. We will now have a practice run of the experiment.'

# Instruction text drawing

page1=visual.TextStim(win, text=ins_1, pos=([0,0]), height = 1, wrapWidth = 30) 
page2=visual.TextStim(win, text=ins_2, pos=([0,0]), height = 1, wrapWidth = 30)
page3=visual.TextStim(win, text=ins_3, pos=([0,5]), height = 1, wrapWidth = 30)
page4=visual.TextStim(win, text=ins_4, pos=([0,5]), height = 1, wrapWidth = 30)
page5=visual.TextStim(win, text=ins_5, pos=([0,5]), height = 1, wrapWidth = 30)
page6=visual.TextStim(win, text=ins_6, pos=([0,5]), height = 1, wrapWidth = 30)
page7=visual.TextStim(win, text=ins_7, pos=([0,5]), height = 1, wrapWidth = 30)
page8=visual.TextStim(win, text=ins_8, pos=([0,5]), height = 1, wrapWidth = 30)
page9=visual.TextStim(win, text=ins_9, pos=([0,0]), height = 1, wrapWidth = 30)
page10=visual.TextStim(win, text=ins_10, pos=([0,0]), height = 1, wrapWidth = 30)

# Experiment functions

def blank_screen(switch):
	"""
	Switch for removing placeholders and fixation
	"""
	if switch == True:
		square1.setAutoDraw(False)
		#square2.setAutoDraw(False)
		square3.setAutoDraw(False)
		fixation.setAutoDraw(False)
	else:
		square1.setAutoDraw(True)
		#square2.setAutoDraw(True)
		square3.setAutoDraw(True)
		fixation.setAutoDraw(True)

def break_screen(number):
	"""
	Prints break screens
	"""
	blank_screen(True)
	if number != 'begin':
		breakInstr.draw()
		win.flip()
		event.waitKeys()
	breakReady.draw()
	win.flip()
	event.waitKeys()
	win.flip()
	core.wait(1)

def targ_shuffle(targetlist):
	"""
	Shuffles display of targ location
	"""
	shuffle(targetlist)
	targ=targetlist[0]
	return targ

def targetDirection(direction):
	"""
	Takes target direction, and applies to stimuli to create direction stimuli
	"""
	if direction == -5:
		rec=Lrec
		arrow=Lhead
	else:
		rec=Rrec
		arrow=Rhead
	return rec,arrow

def run_condition(condition):
	"""
    Runs a block of trials. This is the presentation of stimuli,
    collection of responses and saving the trial
    """
	blank_screen(True)
	win.flip()

	# Page 1
	while not event.getKeys():
		page1.draw()
		win.flip()
	#Page 2
	while not event.getKeys():
		page2.draw()	
		win.flip()
	#page3
	while not event.getKeys():
		blank_screen(False)
		page3.setAutoDraw(True)
		win.flip()
	#Page 4
	page3.setAutoDraw(False)
	page4.setAutoDraw(True)
	cue.fillColor='green'
	cue.lineColor='green'
	while not event.getKeys():
		fixation.setAutoDraw(False)
		cue.draw()
		win.flip()
	# Page 5
	page4.setAutoDraw(False)
	page5.setAutoDraw(True)
	cue.fillColor='red'
	cue.lineColor='red'
	while not event.getKeys():
		cue.draw()
		win.flip()
	#Page 6
	page5.setAutoDraw(False)
	page6.setAutoDraw(True)
	fixation.setAutoDraw(True)
	win.flip()
	while not event.getKeys():
		win.flip()
	#Page 7
	page6.setAutoDraw(False)
	page7.setAutoDraw(True)
	while not event.getKeys():
		for cues in CUE_POSITIONS:
			targetRec,targetHead=targetDirection(-5)
			targetRec.pos = [cues,0]
			targetHead.pos = [cues,0]
			targetRec.draw()
			targetHead.draw()
			win.flip()
			core.wait(.5)
	#Page 8
	page7.setAutoDraw(False)
	page8.setAutoDraw(True)
	while not event.getKeys():
		for cues in CUE_POSITIONS:
			targetRec,targetHead=targetDirection(5)
			targetRec.pos = [cues,0]
			targetHead.pos = [cues,0]
			targetRec.draw()
			targetHead.draw()
			win.flip()
			core.wait(.5)
	# Page 9
	page8.setAutoDraw(False)
	blank_screen(True)
	while not event.getKeys():
		page9.draw()
		win.flip()
	# Page 10
	while not event.getKeys():
		page10.draw()
		win.flip()
	win.close()
