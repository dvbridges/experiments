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

#Information about experiment.
	# number of reps - 16 trials per repetition - 192 trials for exo, 288 trials (67% predictive = 192 predictive trials + 96 normal trials)
		# Endo = 288 trials, 192 congruent, 96 incongruent. So, make 192 trials at 50/50 accuracy, and add 96 congruent trials (gives 96 cong, 96 incong, plus 96 cong = 192 cong, 96 incong)
		# So, 192/16=12 reps, then add 12 reps with congruent ==1 rule. Thats a total of 24 trials
	# SOAs should be 100 an 800 ms, exo cerebral acitivity peaks at 100ms (see Chica review)
	# check all timings on uni computers, fixation, cue, SOA, target, ISI
"""
SET VARIABLES
"""

V = {'subject':'', 'condition': ['All'], 'age':'', 'gender':['male', 'female']}
if not gui.DlgFromDict(V, order=['subject', 'age', 'gender']).OK:
    core.quit()
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
REPETITIONS = 12 # 24 for ENDO conditions

# Create base stim

# Create psychopy window
my_monitor = monitors.Monitor('testMonitor') # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
win = visual.Window(monitor=my_monitor, size=MON_SIZE,color=[-1,-1,-1],units='deg', fullscr=True, allowGUI=False)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

# Stuff
clock = core.Clock()
writer = ppc.csvWriter(str(V['subject']), saveFolder=SAVE_FOLDER)

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
	if target == 'X' and response == 'lctrl':
		acc=1
	elif target == 'O' and response == 'rctrl':
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

def make_trial_list(condition):
	"""
	Creates list of stimuli
	"""
	trial_list=[]
	for rep in range(REPETITIONS):
		for soa in SOA:
			for c_pos in CUE_POSITIONS:
				for t_pos in TARG_POSITIONS:
					for target_id in TARGETS:						
					#Add a dictionary for every trial
						trial_list+=[{
						'repetition': rep,
						'cue_pos':c_pos,
						'targ_pos':t_pos,
						'condition':condition,
						'congruent': congruent(c_pos, t_pos),
						'target': target_id,
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
		target=visual.TextStim(win, text=trial['target'], height = 1) # check sizes, should be 1x1 degrees
		cue.pos = [trial['cue_pos'],0]
		target.pos = [trial['targ_pos'],0]
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
			target.draw()
			win.flip()
		
		# Get response
		for frame in range(FRAMES_TAR): 
			win.flip()
		response=get_keys(RESPONSES.values(), onset) # Put response collection here, as target lasts only 33ms
		
		# Wait for remaining time 
		
		t_time = onset # relative onset of target
		fin_time=onset+1.967 # time we aim to finish trial
		time2wait=t_time+response[1] # RT time from 0ms

		if time2wait<fin_time:
			core.wait(fin_time-time2wait)

		trial['trial_start']=round(trial_start,3)
		trial['fix_onset']=round(fix_onset,3)
		trial['cue_onset']=round(cue_onset,3)
		trial['soa_onset']=round(soa_onset,3)
		trial['targ_onset']=round(targ_onset,3)
		trial['response'], trial['rt']=response	
		trial['Accuracy'] = accuracy(trial['target'], trial['response'])
		feedback(trial['Accuracy'], trial['response']) # Calls function which gives feedback and inter trial interval
				
		# End of trial time
		final=clock.getTime()
		trial['total_time'] = round(final,3)
		#save trial
		writer.write(trial)	
# Run Experiment
# break_screen('begin')
# run_condition('practice')
# break_screen('break_1')
# run_condition('block_1')
