#!/usr/bin/python3

# Script Name		: lain.py
# Author			: David Bridges
# Email				: david-bridges@hotmail.co.uk
# Created			: 27st October 2016
# Last Modified		: 27st October 2016
# Version			: 1.0
# Description		: A module for holding functions to operate latent inhibition task in Psychopy and to process data outputs (for task, see Granger, Moran, Buckley, & Haselgrove, 2016)

from psychopy import visual,core,monitors,gui,event
import teststim as ts
import time
import pandas as pd

# Exp version
version=1.0

def setWin():
	"""
	Function to return window properties, and stimuli durations
	"""
	# Set window 
	MON_SIZE=(1920,1080)
	MONITORS=monitors.Monitor('test_monitor')
	win=visual.Window(size=MON_SIZE, colorSpace='rgb255',color=(127,127,127),fullscr=True, monitor=MONITORS,allowGUI=False)
    
    # Set frame rates for presentation times
    
	FRAME_RATE=16.7 # use 31 for touch screens
	STIM_FRAMES=int(round(float(1000/FRAME_RATE)))
	ISI_FRAMES=int(round(float(50/FRAME_RATE)))
	return win, STIM_FRAMES,ISI_FRAMES
    
def getGui():
	"""
	Function to open GUI, collect participant number, and return condition parameters
	"""
    # Set GUI interface for collecting participant data

	info=dict(Participant='', ExpVersion=version, Condition=['P1','P2','C1','C2'])
	dictDLG=gui.DlgFromDict(dictionary=info,title='DB_EXP4', fixed=['ExpVersion'])
    
	if dictDLG.OK:
		return info
	else:
		core.quit()
    
def setStim(guiDict):
	"""
	Function taking GUI dict information and returning a stim lists from condition parameters
	"""        
	if guiDict.get('Condition')=='P1':
		return ts.create_pracStim('S')

	if guiDict.get('Condition')=='P2':
		return ts.create_pracStim('H')

	if guiDict.get('Condition')=='C1':        
		return ts.create_testStim('S', 'H') #(PE,NPE)
        
	if guiDict.get('Condition')=='C2':        
		return ts.create_testStim('H','S')
        
def createStim(win):
	"""
	Function to return stimulus objects
	"""
	blank=visual.TextStim(win,text='',color=(1,1,1))
	stimulus=visual.TextStim(win,text='1',color=(1,1,1), height=.07)
	return blank, stimulus

def respButton(keys):
	"""
	Function to collect responses and return RT and accuracy information
	"""
	for resp in keys:
		if 'space' in resp:
			return keys
		if 'q' in resp:
			core.quit()

def respAccuracy(data,condition):
	"""
	Function to analyse response data and return accuracy information, i.e., hit, miss, false alarm
	"""
	if condition in ('P1','P2'):
		return data
	else:
		RTs=data['RT']
		Con=data['Stim_type']
		Accuracy=[]
		PE_RT=['*']*len(RTs)
		NPE_RT=['*']*len(RTs)
		NC_RT=['*']*len(RTs)
		for i in range(0,len(RTs)):

			NA=False
			################ 
			# MISS
			################
			try:
				if Con[i]=='TARGET' and RTs[i]==-1 and RTs[i-1]==-1 and RTs[i+1]==-1:
					Accuracy.append('MISS')
					NA=True
			except KeyError:
				# KeyError if on last trial
				if Con[i]=='TARGET' and RTs[i]==-1 and RTs[i-1]==-1:
					Accuracy.append('MISS')
					NA=True

			################ 
			# False alarms
			################
			try:
				if Con[i]=='TARGET' or Con[i-1]=='TARGET' or Con[i+1]=='TARGET':
					pass
				elif (Con[i]!='TARGET' or Con[i-1]!='TARGET' or Con[i+1]!='TARGET') and RTs[i]!=-1.0:
					Accuracy.append('FALSE_ALARM')
					NA=True

			except KeyError:
				# KeyError if on first or last trial
				if (i==0 or i==1) and RTs[i]!=-1.0:
					Accuracy.append('FALSE_ALARM')
					NA=True
				elif i==(len(RTs)-1) and (Con[i]!='TARGET' or Con[i-1]!='TARGET') and RTs[i]!=-1.0:
					Accuracy.append('FALSE_ALARM')
					NA=True
			
			################ 
			# Early hits
			################
			# Check for PE prediction HIT
			if RTs[i]!=-1.0 and Con[i]=='PE':
				Accuracy.append('PE_PHIT')
				PE_RT[i]=0-(1-abs(RTs[i]))
				NA=True

			# Check for NPE prediction HIT
			if RTs[i]!=-1.0 and Con[i]=='NPE':
				Accuracy.append('NPE_PHIT')
				NPE_RT[i]=0-(1-abs(RTs[i]))
				NA=True

			# Check for NONCUED prediction HIT
			if RTs[i]!=-1.0 and Con[i]=='NONCUED' and Con[i+1]=='TARGET':
				Accuracy.append('NONCUED_PHIT')
				NC_RT[i]=0-(1-abs(RTs[i]))
				NA=True

			################ 
			# Hits on time
			################

			# Check for PE HIT
			try:
				if RTs[i]!=-1 and RTs[i-1]==-1 and Con[i-1]=='PE':
					Accuracy.append('PE_HIT')
					PE_RT[i]=RTs[i]
					NA=True

				# Check for NPE HIT
				if RTs[i]!=-1 and RTs[i-1]==-1 and Con[i-1]=='NPE':
					Accuracy.append('NPE_HIT')
					NPE_RT[i]=RTs[i]
					NA=True

				# Check for NONCUED HIT
				if RTs[i]!=-1 and RTs[i-1]==-1 and Con[i-1]=='NONCUED':
					Accuracy.append('NONCUED_HIT')
					NC_RT[i]=RTs[i]
					NA=True
			except KeyError:
				pass
			################ 
			# Late hits
			################
			
			try:
				# Check for PE late hits
				if RTs[i]!=-1 and RTs[i-1]==-1 and RTs[i-2]==-1 and Con[i-2]=='PE'and Con[i-1]=='TARGET':
					Accuracy.append('PE_HIT')
					PE_RT[i]=1+abs(RTs[i])
					NA=True

				# Check for NPE late hits
				if RTs[i]!=-1 and RTs[i-1]==-1 and RTs[i-2]==-1 and Con[i-2]=='NPE'and Con[i-1]=='TARGET':
					Accuracy.append('NPE_HIT')
					NPE_RT[i]=1+abs(RTs[i])
					NA=True

				# Check for NONCUED late hits
				if RTs[i]!=-1 and RTs[i-1]==-1 and RTs[i-2]==-1 and Con[i-2]=='NONCUED'and Con[i-1]=='TARGET':
					Accuracy.append('NONCUED_HIT')
					NC_RT[i]=1+abs(RTs[i])
					NA=True

			except KeyError:
				pass
			# If no matches, NA
			if NA==False:
				Accuracy.append('NA')

		data['Accuracy']=Accuracy[0:len(Accuracy)]
		data['PE_RT']=PE_RT
		data['NPE_RT']=NPE_RT
		data['NC_RT']=NC_RT
		return data

def expRun(stim_list,STIM_FRAMES,ISI_FRAMES,info,win):
	"""
	Function to run experiment
	"""
    # Create stim dict for storing data
	data={'Trial':[],'Condition':[], 'Stim_type':[], 'Abs_start':[],'Abs_stim_end':[],'Abs_trial_end':[], 'RT':[], 'Stimulus':[]}
    
    # Stim is dataframe: unpack cols into two variables
	condition_list=stim_list.conditions
	stim_list=stim_list.stimuli

    # Create stim objects
	blank,stim=createStim(win)

	# Create blank READY screen
	stim.setText(text="Ready? Push <spacebar> to continue.")
	while not event.getKeys():
		stim.draw()
		win.flip()

	# Start time
	start_time=int(round(time.time()*1000))

	#Create RT object for trial time based RT
	RT=core.Clock()

	# For all trials
	for trials in range(0,len(stim_list)):
		stim.setText(text=stim_list[trials])
		event.clearEvents()
		RT.reset()
		
    	# For frames in STIM_FRAMES (i.e. 1000ms)
		for frames in range(0,STIM_FRAMES):
			stim.draw()
			win.flip()

    	# Collect RT and trial Times    
		stim_end=int(round(time.time()*1000))
		resp=respButton(event.getKeys(keyList=["space","q"], timeStamped=RT))

    	# for frames in ISI_FRAMES, i.e., 50ms
		for frames in range(0,ISI_FRAMES):
			blank.draw()
			win.flip()
        # Fill RT if empty and get trial Times 
		trial_end=int(round(time.time()*1000))
		if resp is None:
			resp=[(-1,-1)]

   		# Write data to dict    
		data['Trial'].append(trials)
		data['Condition'].append(str(info.get('Condition')))
		data['Stim_type'].append(condition_list[trials])
		data['Abs_start'].append(start_time)
		data['Abs_stim_end'].append(stim_end)
		data['Abs_trial_end'].append(trial_end)
		data['RT'].append(resp[0][1])
		data['Stimulus'].append(stim_list[trials])
	
	# Close window
	win.close()

	# Back up data: preprocessed
	if str(info.get('Condition')) not in ('P1','P2'):
		backup=pd.DataFrame(data)
		backup.to_csv('data/'+str(info.get('Participant'))+str(info.get('Condition'))+'_backup.csv', delimiter=',')

	# Write data to dataframe
	origdata=respAccuracy(pd.DataFrame(data),str(info.get('Condition')))
	
	# write data to CSV and reorder cols
	origdata.to_csv(setFilename(info), delimiter=',', columns=['Trial','Condition','Stimulus', 'Abs_start','Abs_stim_end','Abs_trial_end','RT','Stim_type','Accuracy', 'PE_RT','NPE_RT','NC_RT'])

def setFilename(subject):
	"""
	Function to set filename for each participant: subject number plus datetime
	"""
	# Choose folder to store data
	if subject.get('Condition')=='P1' or subject.get('Condition') == 'P2':
		path='practice/'
	else:
		path='data/'

	# Create path and file name
	fix='_'+time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) +'.csv'
	subject=subject.get('Participant')+'_'+subject.get('Condition')
	return (path+subject+fix)


def Main():
    pass

if __name__=="__main__":
	Main()
else:
	print("Importing lain module")