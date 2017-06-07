import os
import shutil
import pandas as pd

from pyexcel.cookbook import merge_all_to_a_book
from pyexcel.ext import xlsx
import glob
import math

def move(depth = None):
	"""
	Moves each sheet from its own folder into group folder for processing
	"""

	# Create new path
	destination = os.path.join(os.getcwd(),"allFiles")
	path = os.getcwd()
	file_list = []

	# Check path exists, if not create path
	if not os.path.exists(path):
		os.makedirs(path)

	# Look for directories in path
	for i in os.listdir():
		if os.path.isdir(os.path.join(path,i)):
			for files in os.listdir(os.path.join(path,i)):
				if not files.endswith("backup.csv") and not os.path.isfile(os.path.join(destination,files)):
					shutil.move(os.path.join(path,i,files), destination)


def convert2num():

	"""
	Takes CSV files and converts RTs from string form to integer, and saves in Excel
	"""

	destination = os.path.join(os.getcwd(),"allFiles")

	for files in os.listdir(destination):
		data=pd.read_csv(os.path.join(destination,files))
		data["RT"]=pd.to_numeric(data["RT"],errors='coerce').round(3) #,"PE_RT","NPE_RT","NC_RT"]
		data["PE_RT"]=pd.to_numeric(data["PE_RT"],errors='coerce').round(3)
		data["NPE_RT"]=pd.to_numeric(data["NPE_RT"],errors='coerce').round(3)
		data["NC_RT"]=pd.to_numeric(data["NC_RT"],errors='coerce').round(3)
		data.to_excel(os.path.join(destination, files[:-3]+"xlsx"))


def num_num(data,label):
	"""
	Counts the number of RTs per column and returns that value
	"""

	num_nums = 0
	for i in range(0,len(data[label])):
			if not math.isnan(data[label].iloc[i]):
				num_nums +=1
	return num_nums


def enum():

	"""
	Adds numbers to RTs, so first instance of PE is 1, 2nd is 2 and so on
	"""

	destination = os.path.join(os.getcwd(),"allFiles")
	new_cols=["PE_RT_Count","NPE_RT_Count", "NonCued"]
	RT_col = ["PE_RT", "NPE_RT", "NC_RT"]

	for files in os.listdir(destination):
		if files.endswith(".xlsx"):
			data=pd.read_excel(os.path.join(destination,files))
			

			data[new_cols[0]] = ""
			data[new_cols[1]] = ""

			for c in range (0,len(RT_col)):

				count=1
				nums = num_num(data,RT_col[c])

				while count <= nums:
					for i in range(0,len(data[RT_col[c]])):
						if not math.isnan(data[RT_col[c]].iloc[i]):
							data.loc[i,new_cols[c]]=count
							count=count+1

				data.to_excel(os.path.join(destination, files))

def collectRTs():
	"""
	Finds RTs numbered 1 - 20. A dataframe is created with columns for trials, and rows for participant.
	When number of trial is found (1-20), the RT is put in that column, for that participant.
	"""
	
	destination = os.path.join(os.getcwd(),"allFiles")
	
	new_cols=["PE_RT_Count","NPE_RT_Count", "NonCued"]
	RT_col = ["PE_RT", "NPE_RT", "NC_RT"]
	false_alarms=[]
	# For 2 conditions 
	for c in range(0,len(new_cols)):
		#Create dataframe and start count
		collection = pd.DataFrame(index=range(1,81),columns=range(1,21))
		count=1 # Count is participant number
		# For each file in destination, ending with .xlsx
		for files in os.listdir(destination):
			if files.endswith(".xlsx"):
				data=pd.read_excel(os.path.join(destination,files))
				# For each row in the data
				for i in range(0, len(data[new_cols[c]])):
					# Check whether RT number is a number - if its a number, add it to corresponding column and row in dataframe
					if not math.isnan(data[new_cols[c]].iloc[i]):
						collection.loc[count, data[new_cols[c]].iloc[i]] = data[RT_col[c]].iloc[i]
				# Add count of false alarms
				false_alarms.append( data["Accuracy"].str.count("FALSE_ALARM").sum() )
				#collection.loc[count, "21"] = data["Stim_type"].str.count("FALSE_ALARM") 
				count+=1
		#Save dataframe by condition
		collection["FA"] = false_alarms
		false_alarms=[]
		collection.to_excel(os.path.join(os.getcwd(), new_cols[c]+".xlsx"))

def csvMerger(your_csv_directory):
	"""
	Merges all CSVs into one big Excel
	"""
	merge_all_to_a_book(glob.glob(os.path.join(your_csv_directory,"*.xlsx")), "LI_DATA_ALL.xlsx")

#move()
#convert2num()
#csvMerger(os.path.join(os.getcwd(),"allFiles"))
#enum()
collectRTs()