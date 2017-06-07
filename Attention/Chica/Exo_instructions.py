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

square1=visual.Rect(win, width=2, height=2, pos=([-5, 0]))
square2=visual.Rect(win, width=2, height=2, pos=([0, 0]))
square3=visual.Rect(win, width=2, height=2, pos=([5, 0]))
fixation=visual.TextStim(win, text='+', pos=([0,.05]), height = 1) # check sizes, should be 1x1 degrees


# Responses and keys
KEYS_QUIT = ['q']  # Keys that quits the experiment
RESPONSES = {'left': 'lctrl', 'right': 'rctrl'}
RESP_POS = {'lctrl': 'X', 'rctrl': 'O'}

# Create stimuli

breaktxt1 = 'You are now on a break. Please rest your eyes for a few seconds. When you are ready, please push a response key to continue.'
breaktxt2 = 'Ready?'
cue=visual.Rect(win,width=2, height=2,lineWidth=10)
breakInstr=visual.TextStim(win, text=breaktxt1, pos=([0,0]), height = 1) # Break instructins
breakReady=visual.TextStim(win, text=breaktxt2, pos=([0,0]), height = 1) # Break - READY?

# Intructions text

ins_1 = 'Welcome to the experiment. Please push a button to continue.'
ins_2 = 'In this experiment, we are going to measure how you process things in the visual world. You will be asked to discriminate the identity of a target which appears on the screen in one of two locations.'
ins_3 = 'First, you will see a fixation point, with boxes at each side. Within these boxes a cue will appear, which may or may not tell you where the target will appear. Please push the button to see what the cues will look like.'
ins_4 = 'In the experiment, a single cue will appear once at one of these two locations. Please push a button to continue.'
ins_5='After the cue appears a target will appear in one of the boxes. Your task is to indicate whether the target you saw was an '"'X'"' or an '"'O'"'. Please push a button to see some targets.'
ins_6='A target will appear once in one of the boxes. When ready, please push a button to continue.'
ins_7='If the target was an '"'X'"', please push the [XX] button with your index finger on your right hand.\n\n\nIf the target was an '"'O'"', please push the [XX] button with your middle finger on your right hand.'
ins_8='Please be as quick and accurate as you can with your response. If you give an incorrect reponse, or if you fail to respond in time, you will receive onscreen feedback that your response was incorrect.'
ins_9='Please let the experimenter know if you have any questions. We will now have a practice run of the experiment.'

# Instruction text drawing

page1=visual.TextStim(win, text=ins_1, pos=([0,0]), height = 1, wrapWidth = 30) 
page2=visual.TextStim(win, text=ins_2, pos=([0,0]), height = 1, wrapWidth = 30)
page3=visual.TextStim(win, text=ins_3, pos=([0,5]), height = 1, wrapWidth = 30)
page4=visual.TextStim(win, text=ins_4, pos=([0,5]), height = 1, wrapWidth = 30)
page5=visual.TextStim(win, text=ins_5, pos=([0,5]), height = 1, wrapWidth = 30)
page6=visual.TextStim(win, text=ins_6, pos=([0,5]), height = 1, wrapWidth = 30)
page7=visual.TextStim(win, text=ins_7, pos=([0,0]), height = 1, wrapWidth = 30)
page8=visual.TextStim(win, text=ins_8, pos=([0,0]), height = 1, wrapWidth = 30)
page9=visual.TextStim(win, text=ins_9, pos=([0,0]), height = 1, wrapWidth = 30)
# Experiment functions

def blank_screen(switch):
	"""
	Switch for removing placeholders and fixation
	"""
	if switch == True:
		square1.setAutoDraw(False)
		square2.setAutoDraw(False)
		square3.setAutoDraw(False)
		fixation.setAutoDraw(False)
	else:
		square1.setAutoDraw(True)
		square2.setAutoDraw(True)
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
	shuffle(targetlist)
	targ=targetlist[0]
	return targ
		
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
	while not event.getKeys():
		page3.setAutoDraw(False)
		page4.setAutoDraw(True)
		for pos in CUE_POSITIONS:
			cue.pos=[pos,0]
			for frames in range(10):
				cue.draw()
				win.flip()
			for frames in range(30):
				win.flip()
			win.flip()
			core.wait(1)
			win.flip()
	# Page 5
	while not event.getKeys():
		page4.setAutoDraw(False)
		page5.draw()
		win.flip()
	#Page 6
	while not event.getKeys():
		page6.setAutoDraw(True)
		for pos in TARG_POSITIONS:
			target=visual.TextStim(win, text=targ_shuffle(TARGETS), pos=([pos,0]), height = 1) 
			for frames in range(10):
				target.draw()
				win.flip()
			win.flip()
			core.wait(1)
			win.flip()
	#Page 7
	while not event.getKeys():
		blank_screen(True)
		page6.setAutoDraw(False)
		page7.draw()
		win.flip()
	# Page 8
	while not event.getKeys():
		page8.draw()
		win.flip()
	# Page 9
	while not event.getKeys():
		page9.draw()
		win.flip()
	win.close()


			
# Run Experiment
# break_screen('begin')
# run_condition('instructions')
# # break_screen('break_1')
# # run_condition('exo_b2')
# # break_screen('break_2')
# # #run_condition('exo_b3')