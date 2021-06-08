# -*- coding: utf-8 -*-
"""
Created on Thu Jun 03 20:27:51 2021

plots learning curve, relying on pathcoords module

@author: Kelly
"""

from plot_pathCoords_module import plot_path_coords
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#%%
experiment = '26May_21'

def init_array(experiment):
    if experiment == 'pilot':
        latency = np.zeros((41,4)) #initalize arrays with correct data size
        start = 13
        i = 14
        end = 177
    if experiment == '23May':
        latency = np.zeros((14,4))
        start = 9
        i = 13
        end = 68
    if experiment == '07Oct':
        latency = np.zeros((14,4))
        start = 13
        i = 13 #06Sept is 13-68 (training), 73-156(rotations)
        end = 68
    if experiment == '11Dec':
        latency = np.zeros((18,4))
        start = 1
        i = 1
        end = 72
    if experiment == '08Mar_21' or experiment == '06May_21':
        latency = np.zeros((18,4))
        start = 13
        i = 13
        end = 84
    if experiment == '26May_21':
        latency = np.zeros((18,4))
        start = 1
        i = 1
        end = 68
    return latency, start, i, end

latency, start, i, end = init_array(experiment)

#%%
while i <= end: #determines ending trial
    
    print('File '+str(i)) #keeps track of which file is being processed
    
    #calls the function and gathers variables
    temp = plot_path_coords(experiment, trial = i, plot = False, calc = True)
    mouse = int(temp[2])
#    trial = int(temp[3])-1 #minus 1 so it starts at 0
    trialNo = (i-start)/4 #trial number, divide by four to fill up same row
    
    #writes the result into arrays
    if mouse%4 == 1:
        latency[trialNo, 0] = temp[4]
    if mouse%4 == 2:
        latency[trialNo, 1] = temp[4]
    if mouse%4 == 3:
        latency[trialNo, 2] = temp[4]
    if mouse%4 == 0:
        latency[trialNo, 3] = temp[4]
    i=i+1
    
#%%
def plot_LearningCurve():
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))
    
    #collects data into variables
    y = np.array(latency, dtype=np.float64)
    x = np.arange(1, len(y)+1)
    M1 = np.array(latency[0:,0], dtype=np.float64)
    M2 = np.array(latency[0:,1], dtype=np.float64)
    M3 = np.array(latency[0:,2], dtype=np.float64)
    M4 = np.array(latency[0:,3], dtype=np.float64)
    avg = np.nanmean(y, 1)
    SE = np.nanstd(y, 1)/np.sqrt(len(y[0,:])) #calculates SE along rows
                     
    #plot data
    pallet = plt.get_cmap('Set1')#gets colours from defined set
    ax1.plot(x, avg,  linewidth=3)
#    ax1.plot(x, y, 'k.', linestyle="None", markersize=5) #plot individual Y data points
    ax1.errorbar(x, avg, yerr=SE, linestyle="None", color=pallet(1)) #plot vertical error bars
    ax1.plot(x,M1, marker = '.', color=pallet(2), linestyle="None", markersize=5) #plot individual Y data points
    ax1.plot(x,M2, marker = '.', color=pallet(3), linestyle="None", markersize=5)
    ax1.plot(x,M3, marker = '.', color=pallet(4), linestyle="None", markersize=5)
    ax1.plot(x,M4, marker = '.', color=pallet(0), linestyle="None", markersize=5)
    
    #plots range
    dataRange = np.array(latency, dtype=np.float64)
    ax1.fill_between(x, np.nanmin(dataRange, axis=1), np.nanmax(dataRange, axis=1), facecolor='#cccccc')
    
    #styling
    plt.rc('font', size = 9)
    plt.style.use('seaborn-whitegrid')
    
    ax1.set_title("Average Latency " +str(experiment), size=14)
    ax1.set_xlabel('Trials')
    ax1.set_ylabel("Time (s)")
    ax1.legend(['Average', 'Mouse29','Mouse30','Mouse31','Mouse32']) #legend for average line
    
    ax1.spines['top'].set_visible(False) 
    ax1.spines['right'].set_visible(False) 
    ax1.spines['left'].set_position('zero')
    ax1.spines['bottom'].set_position('zero')
#    plt.ylim(0, 400) #fixes the y-axis range for easy comparison between graphs
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(1)) #sets x-axis spacing
#    plt.xticks(x, data[1:,0], rotation=90) #order is important, don't move this line
    
    #show and save graph
#    plt.savefig('Latency '+experiment+ '.png', dpi=600, bbox_inches='tight', pad_inches = 0)
    plt.show()
    return