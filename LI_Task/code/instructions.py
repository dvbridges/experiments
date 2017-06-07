#!/usr/bin/python3

# Script Name		: instructions.py
# Author			: David Bridges
# Email				: david-bridges@hotmail.co.uk
# Created			: 27st October 2016
# Last Modified		: 27st October 2016
# Version			: 1.0
# Description		: A module for holding latent inhibition task instructions (for task, see Granger, Moran, Buckley, & Haselgrove, 2016)

from psychopy import visual,event
import lain

# Set text
text1="In this task I want you to say out loud each letter that appears on the screen. This task will take approximately 3 minutes. When this task ends, you will be given a new set of instructions. Press the <spacebar> when you are ready to start the experiment."
text2a="Please wait for the experimenter."
text2b="In this task I want you to watch the sequence of letters appearing on the screen. Your task is to try and predict when a letter 'X' is going to appear.\n\nIf you think you know when the 'X' will appear then you can press the <spacebar> early in the sequence, that is before the 'X' appears on screen. Alternatively, if you are unable to do this please press the <spacebar> as quickly as possible when you see the letter 'X'.\n\nPlease try to be as accurate as you can, but do not worry about making the occasional error. If you understand the task and are ready to start press the <spacebar> to begin." 
text3="Ready? Press <spacebar> to begin."
text4="This task is over. Please wait for the experimenter for your next task."


def pracIns():
	"""
	Display practice instuctions
	"""
	win,STIM_FRAMES,ISI_FRAMES=lain.setWin()
	ins=visual.TextStim(win, text=' ',color=(1,1,1), height=.07)

	ins.setText(text=text1)
	while not event.getKeys():
		ins.draw()
		win.flip()
	win.close()

def mainIns():
	"""
	Display main experiment instuctions
	"""
	win,STIM_FRAMES,ISI_FRAMES=lain.setWin()
	ins=visual.TextStim(win, text=' ',color=(1,1,1), height=.07)

	ins.setText(text=text2a)
	while not event.getKeys():
		ins.draw()
		win.flip()
	ins.setText(text=text2b)
	while not event.getKeys():
		ins.draw()
		win.flip()
	ins.setText(text=text3)	
	while not event.getKeys():
		ins.draw()
		win.flip()
	win.close()

def endIns():
	"""
	Display end instuctions
	"""
	win,STIM_FRAMES,ISI_FRAMES=lain.setWin()
	ins=visual.TextStim(win, text=' ',color=(1,1,1), height=.07)

	ins.setText(text=text4)
	while not event.getKeys():
		ins.draw()
		win.flip()
	win.close()