#!/usr/bin/python3

# Script Name		: teststim.py
# Author			: David Bridges
# Email				: david-bridges@hotmail.co.uk
# Created			: 27st October 2016
# Last Modified		: 27st October 2016
# Version			: 1.0
# Description		: Test stimuli for latent inhibition task (see Granger, Moran, Buckley, & Haselgrove, 2016)


import numpy as np
import pandas as pd
import random

def create_pracStim(PE):
	"""
	Function for creating and shuffling list of practice stim
	"""
	# Create stimuli dict
	exposure = dict(pe=[PE]*20, filler=['D','M','T','V']*15 )
	exposure_list=np.array
	exposure_list=exposure.get('pe')
	exposure_list=exposure_list+exposure.get('filler')
	np.random.shuffle(exposure_list)

	# Create new list of stimuli type
	conds=[]
	for i in exposure_list:
		if i==PE:
			conds.append('PE')
		else:
			conds.append('FILLER')

	# Combine stimuli and stimuli type into dataframe
	expo_list=pd.DataFrame({'stimuli': exposure_list, 'conditions': conds})

	return expo_list

def reshuffle(stim):
	"""
	Function to make sure targets are not in 1st or 2nd position
	"""
	random.shuffle(stim)
	while len(stim[0])==2 or len(stim[1])==2:
		random.shuffle(stim)
	return stim

def sudoShuffle(stim):
	"""
	Pseudo shuffle so no PE, NPE or NONCUED targets cannot follow each other
	"""
	# Shuffle list
	reshuffle(stim)

	# Psuedo randomise main stimuli list
	# If three neighbouring characters are lists, shuffle. Else, if two neighbours are lists, insert the third single character neighbour between them and then delete that character from original position
	i=0
	while i < len(stim)-2:
		if len(stim[i])==2 and len(stim[i+1])==2 and len(stim[i+2])==2:
			reshuffle(stim)
			i=0
		elif len(stim[i])==2 and len(stim[i+1])==2 and len(stim[i+2])==1:
			stim.insert((i+1), stim[i+2])
			del stim[i+3]
			i=0
		else:
			i+=1

	return stim

def create_testStim(PE,NPE):
	"""
	Function for creating main task stimuli list. Given PE and NPE identity when called from lain.setStim.
	"""
	TARGET='X'
	# Create stimuli dict
	test=dict(test=[[[PE,TARGET],[NPE,TARGET]]*20], filler=['D','M','T','V']*59,noncued=[[['D',TARGET],['M',TARGET],['T',TARGET],['V',TARGET]]*5])

	# Create list from dictionary test items
	test_list=[]
	for levels in test.get('test'): 
		test_list+=levels
	test_list+=test.get('filler')
	for levels in test.get('noncued'): 
		test_list+=levels

	# Shuffle List
	sudoShuffle(test_list)

	# Flatten nested List
	flattened = [val for sublist in test_list for val in sublist]

	# Create list holding conditions etc
	conds=[]
	for i in range(0,len(flattened)):
		if flattened[i] == 'X' and flattened[i-1] in test['filler']:
			conds.append('NONCUED')
		elif flattened[i] == PE:
			conds.append('PE')
		elif flattened[i] == NPE:
			conds.append('NPE')
		elif flattened[i] == TARGET:
			conds.append('TARGET')
		else:
			conds.append('FILLER')
	
	for i in range(0,len(conds)):
		if conds[i]=='NONCUED':
			conds[i-1]=conds[i]
			conds[i]='TARGET'

	# Combine stimuli and stimuli type into dataframe
	conditions=pd.DataFrame({'stimuli': flattened, 'conditions': conds})
	return conditions


def Main():
	pass
	# PE='S'
	# NPE='H'
	# TARGET='X'		

	# practice=create_pracStim(PE)
	# test_stim=create_testStim(PE, NPE)
	# print(test_stim)
	# print (test_stim.stimuli.value_counts())
if __name__=="__main__":
	Main()
else:
	print("Importing teststim module")





