from psychopy import visual, core, logging, event, monitors, gui
from random import sample
import pandas as pd
import numpy as np
import time
import csv

# Runs counterfactual thinking and deception experiment using PsychoPy for Briazu et al.
# Author: DAvid Bridges, email: david.bridges@plymouth.ac.uk
"""
SET VARIABLES
"""
# Set condition file
conditions=pd.read_csv("conditions/practice_con.csv", delimiter=',')

#Set GUI
V = {'subject':''}

if not gui.DlgFromDict(V, order=['subject']).OK:
    core.quit()
# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor

# Timings - check refresh rate, should be 16ms per frame


# Create psychopy window
my_monitor = monitors.Monitor('testMonitor') # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
win = visual.Window(monitor=my_monitor, size=MON_SIZE,color=[-1,-1,-1],units='deg', fullscr=True, allowGUI=False)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

# Create target to win place holder

winThis=visual.TextStim(win, text='', pos=(0,8), height=2, units='cm')

#Feedback text

FB=visual.TextStim(win, text='', pos=(0,-8), height=2, units='cm')
didyouWin=visual.TextStim(win, text="Did you win?\n\nPush < Y > for YES\n\nPush < N > for NO.",alignHoriz='center', pos=(0,0), height=2, wrapWidth=30)


# Create actual target place holder
y_ax=-6
l1=visual.TextStim(win, text=0, pos=(-2,y_ax), height=2, units='cm')
r1=visual.TextStim(win, text=0, pos=(-2,y_ax), height=2, units='cm')

# Layout graphics
lineW=5
upper_box=visual.Rect(win, width=10, height=16, pos=(0,10), lineColor="black", fillColor="black", lineWidth=lineW)
lower_box=visual.Rect(win, width=10, height=16, pos=(0,-10), lineColor="black", fillColor="black", lineWidth=lineW)
outlinel=visual.Rect(win,width=4, height=4, pos=(-2,0),lineColor="white", lineWidth=lineW)
outliner=visual.Rect(win,width=4, height=4, pos=(2,0),lineColor="white", lineWidth=lineW)
centre_line=visual.Line(win, start=(-.5,0), end=(.5,0), lineWidth=lineW)
left_line=visual.Line(win, start=(-4.5,0), end=(-3.5,0), lineWidth=lineW)
right_line=visual.Line(win, start=(4.5,0), end=(3.5,0), lineWidth=lineW)

# Set response keys 
KEY_RESPONSE=["y","n","q"]
KEY_STOP=["space","q"]

def makeReels():
    """
    Creates a long string for spinning reels for left and right reels - note, does not hold target
    """
    nums1=np.random.randint(0,9,1000)
    nums2=np.random.randint(0,9,1000)

    ls1=''
    rs1=''
    for i in nums1:
        ls1=ls1+str(i)+'\n'
    for i in nums2:
        rs1=rs1+str(i)+'\n'
    return ls1,rs1
    
def spinWheels():
    return l1.setText(text=makeReels()[0]),r1.setText(text=makeReels()[1])

def drawLayout(switch):
    """
    Function to draw basic layout of slot machine
    """
    upper_box.setAutoDraw(switch)
    lower_box.setAutoDraw(switch)
    outlinel.setAutoDraw(switch)
    outliner.setAutoDraw(switch)
    centre_line.setAutoDraw(switch)
    left_line.setAutoDraw(switch)
    right_line.setAutoDraw(switch)

def setColor(col, switch):
    """
    Function to change color of basic layout of slot machine, according to condition
    """
    if switch == True:
        if col == "Near" or col == "Loss":
            color = "red"
        else: color="lime"
    elif switch == False:
        color = "white"

    outlinel.setLineColor(color)
    outliner.setLineColor(color)
    centre_line.setLineColor(color)
    left_line.setLineColor(color)
    right_line.setLineColor(color)
    winThis.setColor(color)
    FB.setColor(color)
    l1.setColor(color)
    r1.setColor(color)

    
def target2Str(left,right):
    """
    Take target inserted into surrounding numbers and convert to vertical string
    
    """
    l_str=''
    r_str=''
    
    for i in left:
        l_str=l_str+str(i)+'\n'
    for i in right:
        r_str=r_str+str(i)+'\n'
    return l_str,r_str
        
    
def setTarget(trial_num):
    """
    Take trial number, and add target information
    """
    # Get stop point with jitter
    y_lax=np.random.uniform(-.2,.2)-1.1
    y_rax=np.random.uniform(-.2,.2)-1.1
    
    # Set upper and lower surrounding numbers
    left=np.random.randint(0,9,2)
    right=np.random.randint(0,9,2)
    
    #If near condition, change the number of right upper wheel to match remainder-left (the winning value)
    #Numbers for Right block
    if trials.iloc[trial_num]['Condition']=='Near' and trials.iloc[trial_num]['CB']==2:
        right[0]=trials.iloc[trial_num]['Remainder']-trials.iloc[trial_num]['Left']
    #Numbers for Right block
    if trials.iloc[trial_num]['Condition']=='Near' and trials.iloc[trial_num]['CB']==1:
        left[0]=trials.iloc[trial_num]['Remainder']-trials.iloc[trial_num]['Right']
    
    # Create list of numbers with target in center
    left=np.insert(left,1,trials.iloc[trial_num]['Left'])
    right=np.insert(right,1,trials.iloc[trial_num]['Right'])
    
    # Create string list of targets 
    texts=target2Str(left,right)
    
    #Set Target 
    l1.setText(text=texts[0])
    r1.setText(text=texts[1])
        
    # Set stop point
    
    if trials.iloc[trial_num]['Condition']=='Near' and trials.iloc[trial_num]['CB']==2 or trials.iloc[trial_num]['Condition']=='Loss' and trials.iloc[trial_num]['CB']==2:
        l1.setPos((-2,y_lax))
        r1.setPos((2,(y_rax-1)))        
    elif trials.iloc[trial_num]['Condition']=='Near' and trials.iloc[trial_num]['CB']==1 or trials.iloc[trial_num]['Condition']=='Loss' and trials.iloc[trial_num]['CB']==1:
        l1.setPos((-2,(y_lax-1)))
        r1.setPos((2,y_rax))
    else:
        l1.setPos((-2,y_lax))
        r1.setPos((2,y_rax))
    
    return l1,r1

def setWinNum(remainder):
    """
    Set text window to display remainder value"
    """
    text = "Try to get %s" % (remainder)
    
    return text 
    
def Feedback_text(condition):
    """ Set feedback text
    """
    text=trials.iloc[trial_nums]['Left']+trials.iloc[trial_nums]['Right']

    # Win, Loss, Near=[x for x in ('You won!','You lost!','You nearly won!')]
    # options=[Near,Loss,Win]
    # text=options[['Near','Loss','Win'].index(condition)]
    return "You got %s!" % (text)
        
# Create conditions
trials = conditions.sample(n=len(conditions))
dict={"condition":[],
    "target":[],
    "left":[],
    "right":[],
    "remainder":[],
    "near_miss_side":[],
    "onset_utc":[],
    "stop_utc":[],
    "decision":[],
    "decision_utc":[],
    "trial_start":[],
    "spin_start_tt":[],
    "spin_stop_tt":[],
    "decision_start_tt":[],
    "decision_tt":[]}
#For number of trials, perform loop
start_time=time.time()

#Start experiment
for trial_nums in range(0,len(trials)):

    # Event controller
    Spin=True
    Stopped=True
    Feedback=True
    Response=True

    # Set target text that participant has to win, for trial_num
    drawLayout(True)
    winThis.setText(text=setWinNum(trials.iloc[trial_nums]['Remainder']))
    winThis.draw()
    
    # Spin the wheels
    spinWheels()
    onset = time.time()
    y_ax=-6
    
    for seconds in range(0,120):
        winThis.setAutoDraw(True)
        win.flip()
        if seconds==119:
            event.clearEvents()
            spin_start_utc=time.time()
    while Spin:
        
        # Set position of left and right reels running
        l1.setPos((-2,y_ax))
        r1.setPos((2,y_ax))

        # Draw reels
        l1.draw()
        r1.draw()
        
         #Set y_axis to create spin
        y_ax+=.5
        
        win.flip()
        stop_key = event.getKeys(keyList=["space","q"])
        if stop_key:
            spin_stop_utc=time.time()
            #If response, stop spinning
            Spin=False
            if stop_key[0][0] == "q":
                core.quit()
            
    while Stopped:
        setTarget(trial_nums)
        l1.draw()
        r1.draw()
        win.flip()
        core.wait(1)
        break
        
                
    while Feedback:
                
        # Set feedback color
        setColor(trials.iloc[trial_nums]['Condition'], True)
        FB.setText(text=Feedback_text(trials.iloc[trial_nums]['Condition']))
        
        # Draw text and wait 
        l1.draw()
        r1.draw()
        FB.setAutoDraw(True)
        win.flip()
        core.wait(3)


        event.clearEvents()
        decision_start=time.time()
        break
        
    while Response:
        # Clear screen
        FB.setAutoDraw(False)
        winThis.setAutoDraw(False)
        drawLayout(False)

        # Draw response text 
        didyouWin.draw()
        win.flip()
        decision = event.getKeys(keyList=["y","n","q"])
        if decision:
            decision_utc=time.time()
            if decision[0][0] == "y" or decision[0][0]=="n":
                event.clearEvents()
                win.flip()
                setColor(trials.iloc[trial_nums]['Condition'], False)
                break
            if decision[0][0] == "q":
                core.quit()
                
    dict["condition"].append(trials.iloc[trial_nums]['Condition'])
    dict["target"].append(trials.iloc[trial_nums]['Remainder'])
    dict["left"].append(trials.iloc[trial_nums]['Left'])
    dict["right"].append(trials.iloc[trial_nums]['Right'])
    dict["remainder"].append(trials.iloc[trial_nums]['Remainder']-trials.iloc[trial_nums]['Left'])
    dict["near_miss_side"].append(trials.iloc[trial_nums]['CB'])
    dict["decision"].append(decision[0][0])
    dict["onset_utc"].append(onset-start_time)
    dict["stop_utc"].append(spin_stop_utc-start_time)
    dict["decision_utc"].append(decision_utc-start_time)
    dict["trial_start"].append(0)
    dict["spin_start_tt"].append(spin_start_utc-onset)
    dict["spin_stop_tt"].append(spin_stop_utc-onset)
    dict["decision_start_tt"].append(decision_start-onset)
    dict["decision_tt"].append(decision_utc-onset)

data=pd.DataFrame(dict)
data.to_csv('resp_data/'+V['subject']+'_'+'practice'+'_'+time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) +'.csv', delimiter=',', columns=[
'condition','target','left','right','remainder','near_miss_side','decision','onset_utc',
'stop_utc','decision_utc','trial_start','spin_start_tt','spin_stop_tt','decision_start_tt','decision_tt'
])

