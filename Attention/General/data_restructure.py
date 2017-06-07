import numpy as np
import pandas as pd
import os
import glob

filelist=glob.glob("C:/Users/dbridges/Desktop/ALL_EXP/Exp_3/DATA/*")

def dataRestructure(filelist):
	for x in filelist:
		file=x[45:50]
		data=pd.read_csv(x, delimiter = ';')
		data=data[['trial_number','repetition', 'trial_start','fix_onset','cue_onset','soa_onset','targ_onset','total_time','condition','SOA','cue_pos','targ_pos','congruent','targ_direction','stroop_cong','target_name','response','Accuracy','rt']]
		filename = file+'.csv'
		data.to_csv(os.path.join("C:/Users/dbridges/Desktop/ALL_EXP/Exp_3/DATA/", filename), index=False)


dataRestructure(filelist)
