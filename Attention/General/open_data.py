# Open file
import numpy as np
import csv

x=[]
with open('C:\snog.csv', 'rb') as csvfile:
	data = csv.reader(csvfile, delimiter=';')
	for row in data:
		x.append(row)

def convert2float(row): # converts values to float
	del row[0]
	rt=[]
	for items in row:
		rt.append(float(items[8]))
	return rt

def average(inputs): # computes averages
	fail=0.0
	if fail in inputs: # removes any zeros from the list
		inputs.remove(0.0)
	return round(np.average(inputs),3)

def check(rts): # checks for non responses - find another way using all data
	new=[]
	fail=0.0
	for items in rts:
		if items < 2.0:
			new.append(items)
		else:
			new.append(fail)
	return new

rt=convert2float(x)
print rt
print average(rt)
print check(rt)
newrt=check(rt)
print average(newrt)


