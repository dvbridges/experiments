import psychopy
from psychopy import visual, core, logging, event, monitors, gui
from random import sample
import matplotlib
import ppc # has writer class

#####
#Things to do to set up a PC for setting
#####
#1) Run screen_framerate_test.py to test the refresh rate of the screen - this will help determine stim frame display times
#2) Change condition table entry to reflect blocks, create a separate one for condition (i.e. practice or not practice)
#3) Create correct response
#4) Create accuracy - evaluation of response

#position of cue
#position of target
#number of reps
"""
SET VARIABLES
"""

# V = {'subject':'', 'condition': ['All'], 'age':'', 'gender':['male', 'female']}
# if not gui.DlgFromDict(V, order=['subject', 'age', 'gender']).OK:
#     core.quit()
# Monitor parameters
# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor
SAVE_FOLDER = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.

# Timings - check refresh rate, should be 16ms per frame
FRAMES_FIX = 30 # 500ms 
FRAMES_CUE = 3   # 50ms 
FRAMES_TAR = 2   # 33ms	
SOA = [9,45] 	 # need SOA of 100 and 800 ms from cue onset, so SOA needs to be 50ms, and 750ms  
#Condition parameters

CUE_POSITIONS = [-5,5]
TARG_POSITIONS = [-5,5]
TARG_DIRECTION = [-5,5]
REPETITIONS = 4 # 24 for ENDO conditions

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

# Create instruction stimuli

breaktxt1 = 'You are now on a break. Please rest your eyes for a few seconds. When you are ready, please push a response key to continue.'
breaktxt2 = 'Ready?'
breakInstr=visual.TextStim(win, text=breaktxt1, pos=([0,0]), height = 1) # Break instructins
breakReady=visual.TextStim(win, text=breaktxt2, pos=([0,0]), height = 1) # Break - READY?

#Create experimental stimuli - cue and target

cue=visual.Rect(win,width=2, height=2,lineWidth=10)
arrowVert = [(-0.2,0.05),(-0.2,-0.05),(-.0,-0.05),(-.0,-0.1),(.2,0),(-.0,0.1),(-.0,0.05)] # centred circle
Rarrow = visual.ShapeStim(win, vertices=arrowVert, size=4, lineColor='white', pos =[0,0],ori=0)
Larrow = visual.ShapeStim(win, vertices=arrowVert, size=4, lineColor='white', pos =[0,0],ori=180)

# Stimulus paramters
TARGETS = [Larrow, Rarrow]

# Experiment functions



def get_keys(keyList=None,onset=None):

	"""	
	Gets response, calculates RT
	"""
	if keyList:
		keyList += KEYS_QUIT

	time_flip = onset # onset of target (absolute time)

	try:
		key, time_key = event.waitKeys(maxWait = 2, keyList=keyList, timeStamped=True)[0]  # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer. 
	except IndexError:
		key,time_key = (0,0)
	except TypeError:
		key,time_key = (0,0)	
	if key in KEYS_QUIT:  # Look at first reponse [0]. Quit everything if quit-key was pressed
		core.quit()
	return key, abs(round((time_key - time_flip),3))

def accuracy(target, response):
	"""
	Decides if participant response is correct
	"""
	if target == Larrow and response == 'lctrl':
		acc=1
	elif target == Rarrow and response == 'rctrl':
		acc=1
	else:
		acc = 0
	return acc
	
def congruent(cue, target):
	"""
	Returns congruent value = 1 for valid match between cue and target, -1 for invalid match
	"""
	if cue == target:
		congruent=1
	else:
		congruent=-1
	return congruent

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

def feedback(accuracy, response):
	"""
	gives feedback 
	"""
	if response==0:
		acc='No response'
		feedback=visual.TextStim(win, text=acc, pos=([0,0]), height = 1)
		blank_screen(True)
		feedback.draw()
		win.flip()
		core.wait(.5)
		blank_screen(False)
	elif accuracy ==0:
		acc='Incorrect'
		feedback=visual.TextStim(win, text=acc, pos=([0,0]), height = 1)
		blank_screen(True)
		feedback.draw()
		win.flip()
		core.wait(.5)
		blank_screen(False)
	else:
		blank_screen(True)
		win.flip()
		core.wait(.5)

def trialshuffle(triallist, condition):
	"""
	Checks condition, if practice, trials sampled is 20, else all trials sampled
	"""
	if condition == 'practice':
		num_oftrials=20
	else:
		num_oftrials=len(triallist)
	return num_oftrials

def enumerateTrials(triallist):
	"""
	Takes trial list, enumerates (gives number sequentially) and adds to trial dict
	"""
	for i, trial in enumerate(triallist):
		trial['trial_number'] = i + 1  # start at 1 instead of 0
	return triallist

def stroopCong(position, direction):
	"""
	Returns congruent value = 1 for valid match between target location and target direction,-1 for invalid match
	"""	
	if position==direction:
		stroopCong=1
	else:
		stroopCong=-1
	return stroopCong

def make_trial_list(condition):
	"""
	Creates list of stimuli
	"""
	trial_list=[]
	for rep in range(REPETITIONS):
		for soa in SOA:
			for c_pos in CUE_POSITIONS:
				for t_pos in TARG_POSITIONS:
					for direction in TARG_DIRECTION:
					#Add a dictionary for every trial
						trial_list+=[{
						'repetition': rep,
						'cue_pos':c_pos,
						'targ_pos':t_pos,
						'targ_direction': direction,
						'target_name': '',
						'condition':condition,
						'congruent': congruent(c_pos, t_pos),
						'stroop_cong': stroopCong(t_pos, direction),
						'SOA': soa,
						'trial_start': '',
						'fix_onset': '',
						'cue_onset': '',
						'soa_onset': '',
						'targ_onset': '',
						'total_time': '',												
						'response': '',
						'rt': '',
						'Accuracy':'',
						}]

	# Randomize order
	#trial_list = sample(trial_list, trialshuffle(trial_list, condition))
 	enumerateTrials(trial_list)

	for trial in trial_list:
		print trial
	print len(trial_list)

make_trial_list('practice')
print 
print
print
make_trial_list('all')
