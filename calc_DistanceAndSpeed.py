# -*- coding: utf-8 -*-
"""
Created on Wed May 27 03:14:28 2020

Iterate across the trials to get distance and speeds

@author: Kelly
"""

from plot_pathCoords_module import plot_path_coords
import numpy as np
#%%
#initalize arrays with correct data size
distance = np.zeros((42,4)) #number of rows for pilot = 41, #rows for other = 14
speed = np.zeros((42,4))
start = 9 #number of first trial, 13 for most, 9 for 23May
i = 69 #pilot goes from 14-177, 06Sept is 13-68 (training), 73-156(rotations)
#%%
while i <= 152: #determines ending trial
    
    print('File '+str(i)) #keeps track of which file is being processed
    
    #calls the function and gathers variables
    temp = plot_path_coords('23May',trial = i,plot = False, calc = True)
    mouse = int(temp[2])
#    trial = int(temp[3])-1 #minus 1 so it starts at 0
    trialNo = (i-start)/4
    
    #writes the result into arrays
    if mouse%4 == 1:
        distance[trialNo, 0] = temp[0]
        speed[trialNo, 0] = temp[1]
    if mouse%4 == 2:
        distance[trialNo, 1] = temp[0]
        speed[trialNo, 1] = temp[1]
    if mouse%4 == 3:
        distance[trialNo, 2] = temp[0]
        speed[trialNo, 2] = temp[1]
    if mouse%4 == 0:
        distance[trialNo, 3] = temp[0] 
        speed[trialNo, 3] = temp[1]
    i=i+1
    
#plot_path_coords('23May'," 45",plot = True, calc = True)
