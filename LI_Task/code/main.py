#!/usr/bin/python3

# Script Name		: practice.py
# Author			: David Bridges
# Email				: david-bridges@hotmail.co.uk
# Created			: 21st October 2016
# Last Modified		: 21st October 2016
# Version			: 1.0
# Description		: Execution of latent inhibition task (see Granger, Moran, Buckley, & Haselgrove, 2016)

import teststim as ts
import lain
import instructions as ins

#######################
# PRAC-INSTRUCTIONS
#######################

ins.pracIns()

#######################
# PRACTICE 
#######################

# Set participant info
p_info=lain.getGui()
#Set stim
stim=lain.setStim(p_info)
# Set window, and timeframes  
win, STIM_FRAMES, ISI_FRAMES=lain.setWin()
# run practice
lain.expRun(stim,STIM_FRAMES,ISI_FRAMES,p_info,win)

#######################
# MAIN-INSTRUCTIONS
#######################

ins.mainIns()

#######################
# MAIN 
#######################

# Set participant info
p_info=lain.getGui()
#Set stim
stim=lain.setStim(p_info)
# Set window, and timeframes
win, STIM_FRAMES, ISI_FRAMES=lain.setWin()
# run main
lain.expRun(stim,STIM_FRAMES,ISI_FRAMES,p_info,win)

#######################
# End 
#######################

ins.endIns()