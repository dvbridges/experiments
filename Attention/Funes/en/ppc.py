
class csvWriter(object):
	def __init__(self, saveFilePrefix='', saveFolder=''):

		import csv, time

		#create folder if doesnt exist
		if saveFolder:
			import os
			saveFolder +='/'
			if not os.path.isdir(saveFolder):
				os.makedirs(saveFolder)

		# generate self.saveFolder and self.writer

		self.saveFile = saveFolder + str(saveFilePrefix) + '_' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) +'.csv'  # Filename for csv. E.g. "myFolder/subj1_cond2 (2013-12-28 09-53-04).csv
		self.writer = csv.writer(open(self.saveFile, 'wb'), delimiter=';').writerow  # The writer function to csv. It appends a single row to file
		self.headerWritten=False

	def write(self,trial):
		###Trial: a dictionary###
		if not self.headerWritten:
			self.headerWritten=True
			self.writer(trial.keys())
		self.writer(trial.values())

def getActualFrameRate(frames=1000):
	from psychopy import visual, core
	import numpy as np

	#set stimulus
	durations=[]
	clock=core.Clock()
	win = visual.Window(color='pink')

	# Show brief instruction warning
	visual.TextStim(win, text='Now wait and \ndon\'t do anything', color='black').draw()
	win.flip()
	core.wait(1.5)

	#blank screen and sync clock to vertical blanks
	win.flip()
	clock.reset()

	# Run the test!
	for i in range(frames):
		win.flip()
		durations += [clock.getTime()]
		clock.reset()
	win.close()

# Print summary
    
	print 'average frame duration was', round(np.average(durations) * 1000, 3), 'ms (SD', round(np.std(durations), 5), ') ms'
	print 'corresponding to a framerate of', round(1 / np.average(durations), 3), 'Hz'
	print '60 frames on your monitor takes', round(np.average(durations) * 60 * 1000, 3), 'ms'
	print 'shortest duration was ', round(min(durations) * 1000, 3), 'ms and longest duration was ', round(max(durations) * 1000, 3), 'ms'

def deg2cm(angle, distance):
    """
    Returns the size of a stimulus in cm given:
        :distance: ... to monitor in cm
        :angle: ... that stimulus extends as seen from the eye
    Use this function to verify whether your stimuli are the expected size.
    (there's an equivalent in psychopy.tools.monitorunittools.deg2cm)
    """
    import math
    return math.tan(math.radians(angle)) * distance  # trigonometry