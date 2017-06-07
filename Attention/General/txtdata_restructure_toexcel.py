import numpy as np
import pandas as pd
import os
import glob
import openpyxl
from openpyxl import load_workbook

filelist_a=glob.glob("C:/Users/dbridges/Desktop/ALL_EXP/Exp_1/Exp_1_OrigData/DYSLEXIA_DATA/CANUN/*-list*.log")


def dataRestructure(filelist):
	for x in filelist:
		file=x[75:79]+x[85:91]
		data=pd.read_csv(x,skiprows=3,delim_whitespace=True)
		filename = file+'.xlsx'
		data.to_excel(os.path.join("C:/Users/dbridges/Desktop/ALL_EXP/Exp_1/Exp_1_OrigData/DYSLEXIA_DATA/CANUN/", filename), "sheet1", engine='openpyxl',index=False)



def toOneSheet(filelist):
	for x in filelist:
		filename=x[75:91]
		sheetname=x[75:85]
		data=pd.read_excel(x)
		book=load_workbook('C:/Users/dbridges/Desktop/ALL_EXP/Exp_1/Exp_1_OrigData/DYSLEXIA_DATA/CANUN/output.xlsx')
		writer=pd.ExcelWriter('C:/Users/dbridges/Desktop/ALL_EXP/Exp_1/Exp_1_OrigData/DYSLEXIA_DATA/CANUN/output.xlsx',engine='openpyxl')
		writer.book=book
		data.to_excel(writer,sheetname,index=False)
		writer.save()

dataRestructure(filelist_a)
filelist_b=glob.glob("C:/Users/dbridges/Desktop/ALL_EXP/Exp_1/Exp_1_OrigData/DYSLEXIA_DATA/CANUN/*list*.xlsx")
toOneSheet(filelist_b)