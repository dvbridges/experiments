import numpy as np
import pandas as pd
import os
import glob
import openpyxl
from openpyxl import load_workbook
filelist=glob.glob("C:/Users/dbridges/Desktop/ALL_EXP/Exp_3/DATA/*")

def dataRestructure(filelist):
	for x in filelist:
		file=x[45:50]
		data=pd.read_csv(x, delimiter = ';')
		data=data[['trial_number','repetition', 'trial_start','fix_onset','cue_onset','soa_onset','targ_onset','total_time','condition','SOA','cue_pos','targ_pos','congruent','targ_direction','stroop_cong','target_name','response','Accuracy','rt']]
		filename = file+'.xlsx'
		data.to_excel(os.path.join("C:/Users/dbridges/Desktop/ALL_EXP/Exp_3/DATA/", filename), "sheet1", engine='openpyxl',index=False)

dataRestructure(filelist)

filelist=glob.glob("C:/Users/dbridges/Desktop/ALL_EXP/Exp_3/DATA/*.xlsx")
def toOneSheet(filelist):
	for x in filelist:
		file=x[45:50]
		if x[49]=='X':
			output='exo_output.xlsx'
		else:
			output='endo_output.xlsx'
		data=pd.read_excel(x)
		book=load_workbook(output)
		writer=pd.ExcelWriter(output,engine='openpyxl')
		writer.book=book
		data.to_excel(writer,file,index=False)
		writer.save()

toOneSheet(filelist)