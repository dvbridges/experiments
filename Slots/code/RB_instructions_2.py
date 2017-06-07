from psychopy import visual, core, logging, event, monitors, gui
from random import shuffle
import time
import matplotlib
import pandas as pd

"""
SET VARIABLES
"""

# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor

# Create psychopy window
my_monitor = monitors.Monitor('testMonitor') # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
win = visual.Window(monitor=my_monitor, size=MON_SIZE,color=[-1,-1,-1],units='deg', fullscr=False, allowGUI=True)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

# Intructions text

ins_1="Now that you know how the game is played, you will be randomly assigned to the other two participants.\n\nAssigning participants"
load_wait=('','.','..','...','....')*4
load_wait2=('','.','..','...','....','.....','......')*8
ins_2="You have been randomly assigned to:\n\n***Participant B and Participant C***.\n\nYou now have an opportunity to send them a short message. You could wish them good luck or just day hi. Please type your response in the window that appears on the next screen.\n\nPush a button to continue."
ins_3="Here are the messages that each participant sent to you. These messages were sent before the other participants read your message:\n\nFrom participant B: Hi, good luck but I will try to win this\n\nFrom participant C: Let me win, play fair"
ins_4="Now lets play. Remember you are in competition with participant B but your decisions can affect participant C.\n\nPressing < Y > will ALWAYS gain you a point (even if the numbers you get don't add up to the target number), but this decision might take a point away from participant C.\n\nOn the next screen you will be asked for your participant number, age and gender. After, the screen will dissapear, wait a few seconds and the game will start! When you are ready to start press the space bar. Ready?"

# GUI fields

part_b='<<<<<<<<<<<<<Participant B>>>>>>>>>>>>'
part_c='<<<<<<<<<<<<<Participant C>>>>>>>>>>>>'

# Instruction text drawing

page1=visual.TextStim(win, text=ins_1, pos=([0,3]), height = 1, wrapWidth = 30,alignVert='top') 
page1_load=visual.TextStim(win, text='', pos=([-4.5,-.4]), height = 2, wrapWidth = 30, alignHoriz='left') 
page2=visual.TextStim(win, text=ins_2, pos=([0,0]), height = 1, wrapWidth = 30)
page2_load=visual.TextStim(win, text='', pos=([0,0]), height = 2, wrapWidth = 30, alignHoriz='center') 
page2_loadtext=visual.TextStim(win, text="Waiting for responses", pos=([0,1]), height = 1, wrapWidth = 30)
page3=visual.TextStim(win, text=ins_3, pos=([0,0]), height = 1, wrapWidth = 30)
page4=visual.TextStim(win, text=ins_4, pos=([0,0]), height = 1, wrapWidth = 30)

def run_condition(condition):
	# Page 1
	win.flip()
	for i in load_wait:
		page1.draw()
		page1_load.setText(text=i)
		page1_load.draw()
		core.wait(0.1)
		win.flip()
	event.clearEvents()
	while not event.getKeys():
		page1.setText(text="Now that you know how the game is played, we assign you to the other two participants.\n\nParticipants assigned!\n\nPlease press space bar to continue.")
		page1.draw()
		win.flip()
	event.clearEvents()
	#Page 2
	while not event.getKeys():
		page2.draw()
		win.flip()
	win.flip()
	event.clearEvents()
# Set Gui 
	info = {part_b:'                                                                                           ',part_c: '                                                                                           '}
	dictDlg = gui.DlgFromDict(dictionary=info, title="Send a short message to the other participants")
#	if dictDlg.OK:
#		print(info)
#	else:
#		print('User Cancelled')
	data=pd.DataFrame(info, index=[0])
	data.columns=['B','C']
	data.to_csv('resp_data/practice_responses'+'_'+time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) +'.csv', delimiter=',', columns=['B','C'])

	for i in load_wait2:
		page2_loadtext.draw()
		page2_load.setText(text=i)
		page2_load.draw()
		core.wait(0.1)
		win.flip()
	event.clearEvents()
	while not event.getKeys():
		page3.draw()
		win.flip()
	event.clearEvents()
	while not event.getKeys():
		page4.draw()
		win.flip()
    
	win.close()

# Run the condition
run_condition('ins')


