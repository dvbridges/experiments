#import psychopy
from psychopy import visual, core, logging, event, monitors, gui
from random import sample
import matplotlib
import ppc # has writer class

#####
#Things to do to set up a PC for setting
#####
#1) Run screen_framerate_test.py to test the refresh rate of the screen - this will help determine stim frame display times
	##### this is extremely important as you then set all times according to thig

"""
SET VARIABLES
"""

V = {'subject':'', 'condition': ['ex'], 'age':'', 'gender':['male', 'female']}
if not gui.DlgFromDict(V, order=['subject', 'age', 'gender']).OK:
    core.quit()
# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor
SAVE_FOLDER = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.

# Timings - check refresh rate, should be 16ms per frame

FRAMES_FIX = 45 # 750ms is 45 frames at 16ms
FRAMES_CUE = 3   # 50ms is 3 frames at 16ms
FRAMES_TAR = 2   # 33ms	is 2 frames at 16ms 
SOA = [3,48] 	 # need SOA of 100 and 850 ms from cue onset, so SOA needs to be 50ms (3 frames), and 800ms (48)

#Condition parameters

CUE_POSITIONS = [-5,5]
TARG_POSITIONS = [-5,5]
TARG_DIRECTION = [-5,5]
REPETITIONS = 4 # 16 trials per rep gives 64 trials per block

# Create base stim

# Create psychopy window
my_monitor = monitors.Monitor('testMonitor') # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
win = visual.Window(monitor=my_monitor, size=MON_SIZE,color=[-1,-1,-1],units='deg', fullscr=True, allowGUI=False)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

# Stuff
clock = core.Clock()
writer = ppc.csvWriter(str(V['subject']), saveFolder=SAVE_FOLDER)

# create base stimli

square1=visual.Rect(win, width=2.85, height=2.45, pos=[-5, 0])
#square2=visual.Rect(win, width=2, height=2, pos=([0, 0]))
square3=visual.Rect(win, width=2.85, height=2.45, pos=[5, 0])
fixation=visual.Circle(win, pos=([0,.05]), radius = .2) # check sizes, should be 1x1 degrees


# Responses and keys
KEYS_QUIT = ['q']  # Keys that quits the experiment
RESPONSES = {'left': 'lctrl', 'right': 'rctrl'}

# Create instruction stimuli

breaktxt1 = 'You are now on a break. Please rest your eyes for a few seconds. When you are ready, please push a response key to continue.'
breaktxt2 = 'Ready?'
breaktxt3 = 'The practice is over, and you are now about to start the main experiment.\n\n\n\nPlease remember to be as quick and accurate as you can with your responses. When you are ready to begin, push a button to continue.'
breaktxt4 = 'You have now finished the task.\n\n\n\nPlease sit and wait for the experimenter.'
breakInstr=visual.TextStim(win, text=breaktxt1, pos=([0,0]), height = 1, wrapWidth = 30) # Break instructins
breakReady=visual.TextStim(win, text=breaktxt2, pos=([0,0]), height = 1, wrapWidth = 30) # Break - READY?
mainBegin=visual.TextStim(win, text=breaktxt3, pos=([0,0]), height = 1, wrapWidth = 30) # Begin text
finText=visual.TextStim(win, text=breaktxt4, pos=([0,0]), height = 1, wrapWidth = 30) # fin text
#Create experimental stimuli - cue and target

cue=visual.Rect(win,width=2.85, height=2.45,lineWidth=5)
RarrowRec = [(-0.15,0.05),(-0.15,-0.05),(-.0,-0.05),(-.0,0.05)]
RarrowHead = [(-.0,-0.19),(-.0,0.19),(.15,0)]
Rrec = visual.ShapeStim(win, vertices=RarrowRec, size=4, fillColor='white', lineColor='white')
Rhead = visual.ShapeStim(win, vertices=RarrowHead, size=4, fillColor='white', lineColor='white')
LarrowRec = [(0.15,0.05),(0.15,-0.05),(0,-0.05),(0,0.05)]
LarrowHead = [(-.0,-0.19),(-.0,0.19),(-.15,0)]
Lrec = visual.ShapeStim(win, vertices=LarrowRec, size=4, fillColor='white', lineColor='white')
Lhead = visual.ShapeStim(win, vertices=LarrowHead, size=4, fillColor='white', lineColor='white')

# Stimulus paramters
#TARGETS = [Larrow, Rarrow]

# Experiment functions

def get_keys(keyList=None,onset=None):

	"""	
	Gets response, calculates RT
	"""
	if keyList:
		keyList += KEYS_QUIT

	time_flip = onset # onset of target (absolute time)

	try:
		key, time_key = event.waitKeys(maxWait = 1.5, keyList=keyList, timeStamped=True)[0]  # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer. 
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
	if target == Lhead and response == 'lctrl':
		acc=1
	elif target == Rhead and response == 'rctrl':
		acc=1
	else:
		acc = 0
	return acc
	
def congruent(cue, target):
	"""
	Returns congruent value = 1 for valid position match between cue and target, -1 for invalid match
	"""
	if cue == target:
		congruent=1
	else:
		congruent=-1
	return congruent

def stroopCong(position, direction):
	"""
	Returns congruent value = 1 for valid match between target location and target direction,-1 for invalid match
	"""	
	if position==direction:
		stroopCong=1
	else:
		stroopCong=-1
	return stroopCong

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
	if number=='break1':
		mainBegin.draw()
		win.flip()
		event.waitKeys()
	elif number=='finish':
		finText.draw()
		win.flip()
		event.waitKeys()
	elif number != 'begin':
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
	if accuracy==0 and response !=0:
		acc='Incorrect'
		feedback=visual.TextStim(win, text=acc, pos=([0,0]), height = 1)
		blank_screen(True)
		feedback.draw()
		win.flip()
		core.wait(.5)
		win.flip()
		core.wait(.5)
		blank_screen(False)
	else:
		blank_screen(True)
		win.flip()
		core.wait(1)

def trialshuffle(triallist, condition):
	"""
	Checks condition, if practice, trials sampled is 20, else all trials sampled
	"""
	if condition == 'practice':
		num_oftrials=32
	else:
		num_oftrials=len(triallist)
	return num_oftrials

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

def targetName(target):
	""" 
	returns a string description of target
	"""
	if target == Lhead:
		name='Left'
	else:
		name='Right'
	return name

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
	trial_list = sample(trial_list, trialshuffle(trial_list, condition))
    	# Add trial numbers and return
    	for i, trial in enumerate(trial_list):
    		trial['trial_number'] = i + 1  # start at 1 instead of 0
    	return trial_list

def run_condition(condition):
	"""
    Runs a block of trials. This is the presentation of stimuli,
    collection of responses and saving the trial
    """
	blank_screen(False)
	win.flip()

	for trial in make_trial_list(condition):
		response=[]
    # Prepare trial here, before entering the time-critical period
		blank_screen(False)
		targetRec,targetHead=targetDirection(trial['targ_direction'])
		cue.pos = [trial['cue_pos'],0]
		targetRec.pos = [trial['targ_pos'],0]
		targetHead.pos = [trial['targ_pos'],0]

		soa=trial['SOA']

		# Start trial on zero
		win.callOnFlip(clock.reset)
		win.flip()
		trial_start=clock.getTime()		

		#Fixation
		fix_onset=clock.getTime()
		for frame in range(FRAMES_FIX): 
			win.flip()
		#Cue
		cue_onset=clock.getTime()
		for frame in range(FRAMES_CUE):
			cue.draw()
			win.flip()
		#Blank
		soa_onset=clock.getTime()
		for frame in range(soa):
			win.flip()
		#Target
		event.clearEvents(eventType = 'keyboard') # clears any key press before actual response period
		onset=core.monotonicClock.getTime() 	  # Absolute time
		targ_onset=clock.getTime()
		for frame in range(FRAMES_TAR):
			targetRec.draw()
			targetHead.draw()
			win.flip()
		
		# Get response
		for frame in range(FRAMES_TAR): 
			win.flip()
		response=get_keys(RESPONSES.values(), onset) # Put response collection here, as target lasts only 33ms

		trial['trial_start']=round(trial_start,3)
		trial['fix_onset']=round(fix_onset,3)
		trial['cue_onset']=round(cue_onset,3)
		trial['soa_onset']=round(soa_onset,3)
		trial['targ_onset']=round(targ_onset,3)
		trial['target_name']=targetName(targetHead)
		trial['response'], trial['rt']=response	
		trial['Accuracy'] = accuracy(targetHead, trial['response'])
		feedback(trial['Accuracy'], trial['response']) # Calls function which gives feedback and inter trial interval
				
		# End of trial time
		final=clock.getTime()
		trial['total_time'] = round(final,3)
		#save trial
		writer.write(trial)	

