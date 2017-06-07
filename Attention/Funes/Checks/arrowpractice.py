from psychopy import visual, event, core, monitors
MON_SIZE = [1920, 1080]
my_monitor = monitors.Monitor('testMonitor') # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
win = visual.Window(monitor=my_monitor, size=MON_SIZE,color=[-1,-1,-1],units='deg', fullscr=True, allowGUI=False)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!


# # some shapes:
# arrowVert = [(-0.2,0.05),(-0.2,-0.05),(-.0,-0.05),(-.0,-0.1),(.2,0),(-.0,0.1),(-.0,0.05)] # centred circle
# Rarrow = visual.ShapeStim(win, vertices=arrowVert, size=4, lineColor='white', pos =[0,5], lineWidth=2)
# Larrow = visual.ShapeStim(win, vertices=arrowVert, size=4, lineColor='white', pos =[0,0],ori=180)
# cue=visual.Circle(win, radius=.5, lineColor='red', fillColor='red')
# arrow2=visual.ShapeStim(win, vertices=arrowVert, size=4, lineColor='white', pos =[0,0],ori=180)
# while not event.getKeys():
# 	Larrow.draw()
# 	Rarrow.draw()
# 	#cue.draw()
# 	win.flip()


# arrow made of two

square1=visual.Rect(win, width=2.85, height=2.45, pos=([-5, 0]))
#square2=visual.Rect(win, width=2, height=2, pos=([0, 0]))
square3=visual.Rect(win, width=2.85, height=2.45, pos=([5, 0]))
fixation=visual.Circle(win, pos=([0,.05]), radius = .2) # check sizes, should be 1x1 degrees
cue=visual.Circle(win, pos=([0,2.5]), radius = .4, lineColor='green', fillColor='green')

#Arrow
RarrowRec = [(-0.15,0.05),(-0.15,-0.05),(-.0,-0.05),(-.0,0.05)]
RarrowHead = [(-.0,-0.19),(-.0,0.19),(.15,0)]
Rrec = visual.ShapeStim(win, vertices=RarrowRec, size=4, fillColor='white', lineColor='white')
Rhead = visual.ShapeStim(win, vertices=RarrowHead, size=4, fillColor='white', lineColor='white')
LarrowRec = [(0.15,0.05),(0.15,-0.05),(0,-0.05),(0,0.05)]
LarrowHead = [(-.0,-0.19),(-.0,0.19),(-.15,0)]
Lrec = visual.ShapeStim(win, vertices=LarrowRec, size=4, fillColor='white', lineColor='white')
Lhead = visual.ShapeStim(win, vertices=LarrowHead, size=4, fillColor='white', lineColor='white')


while not event.getKeys():
	square1.draw()
	square3.draw()
	fixation.draw()
	cue.draw()
	Rrec.draw()
	Rhead.draw()
	Lrec.draw()
	Lhead.draw()
	win.flip()


