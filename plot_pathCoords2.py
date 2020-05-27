# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:15:30 2020

New version of plot_pathCoords
Added in this version: automatic reading of trial start & end times
automatic detection of when mice is near target. This makes the trial times excel redundant
Calculation of distance and speed

@author: Kelly
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg #for plotting the image
import numpy as np #for the array
import pandas as pd

#variables to change each time
experiment = '23May' #Options: pilot, 23May, 08July, 06Sept, 07Oct
trial = '144'  #trial number, add space before double digits

#sets path of folder with raw trial data and times
def set_experiment_path(experiment):
    if experiment == 'pilot':
        raw_data_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\Pilot\Raw Trial Data\Raw data-Hidden Food Maze - Pilot-Trial   '
        trial_times_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\Pilot\TrialTimes_Pilot'
    if experiment == '23May':
        raw_data_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-05-23\Raw Trial Data\\Raw data-Hidden Food Maze-23May2019-Trial   '
        trial_times_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-05-23\TrialTimes_23May2019'
    if experiment == '08July':
        raw_data_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-07-08\Raw Trial Data\Raw data-Hidden Food Maze-08Jul2019-Trial   '
        trial_times_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-07-08\TrialTimes_08July2019'
    if experiment == '06Sept':
        raw_data_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-09-06\Raw Trial Data\\Raw data-Hidden Food Maze-06Sept2019-Trial   '
        trial_times_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-09-06\TrialTimes_06Sept2019'
    if experiment == '07Oct':
        raw_data_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-10-07\Raw Trial Data\\Raw data-Hidden Food Maze-07Oct2019-Trial   '
        trial_times_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-10-07\TrialTimes_07Oct2019'
    return raw_data_path, trial_times_path

#gets raw trial coordinates from ethovision
def read_excel(trial):
    df = pd.read_excel(set_experiment_path(experiment)[0] + trial + '.xlsx', header=None, na_values=['-'])
    data_coords = np.asarray(df)
    return data_coords
data_coords = read_excel(trial)
data_coords_string = np.asarray(data_coords, dtype=np.dtype('U25')) #converts to string so I can read the data in variable explorer

if data_coords[34,1].startswith(u'R') == True or data_coords[34,1].startswith(u'Flip') == True: is_reverse = True 
else: is_reverse = False

trial_condition = data_coords[34,1]
mouse = data_coords[32,1]

#gets trial times from excel
def get_trial_times():
    df = pd.read_excel(set_experiment_path(experiment)[1]+'.xlsx', header=None, na_values=['-'])
    data_times = np.asarray(df)
    
    trial_condition = data_coords[34,1]
    mouse = data_coords[32,1]
    
    #iterate through excel to mouse
    for i in range(len(data_times[0,1:])):
        if 'M'+mouse == data_times[0,i]: break
        else: i+1
    #iterate through excel to trial
    for j in range(len(data_times[0:,0])): 
        if data_times[j,0] == trial_condition:
            start_time = data_times[j,i]
            end_time = data_times[j,i+1]
            break
        else: j+1
    
    return data_times, start_time, end_time, mouse, trial_condition
#data_times, time_start, time_end, mouse, trial_condition = get_trial_times()
#data_times_string=np.asarray(data_times, dtype=np.dtype('U25'))

#find index of nearest value in array
def find_nearest(array, value):
    array = np.array(array, dtype=np.float64)
    nearest_idx = np.where(abs(array-value)==abs(array-value).min())[0]
    return nearest_idx

def set_background_image():
    entrance = data_coords[33,1]
    background_path = 'C:\Users\Kelly\Desktop\Kelly Docs\Kelly_School\University of Ottawa\Experiments\Hidden Food Maze - Big\\2019-05-23\\'
    if entrance == u'SW': background = background_path+'BKGDimage-pilot.png'
    if entrance == u'SE': background = background_path+'BKGDimage-pilot2.png'
    if entrance == u'NE': background = background_path+'BKGDimage-pilot3.png'
    if entrance == u'NW': background = background_path+'BKGDimage-pilot4.png'
    return background

def set_target():
    entrance = data_coords[33,1]
    trial_condition = data_coords[34,1]
    
    if experiment == '23May' or experiment == 'pilot': 
        target_coords = 20.47, -39.91 #default coordinates
    elif experiment == '06Sept' or experiment == '07Oct' or experiment == '08July':
        if trial_condition.isdigit() is True:
            if entrance == u'SW':
                target_coords = 11.07, -30.48
            if entrance == u'SE':
                target_coords = 35.64, 2.58
            if entrance == u'NE':
                target_coords = 2.88, 27.45
            if entrance == u'NW':
                target_coords = -21.68, -5.61     
        elif trial_condition.startswith(u'R90'):
            if entrance == u'SW':
                target_coords = -21.68, -5.61
            if entrance == u'SE':
                target_coords = 11.07, -30.48
            if entrance == u'NE':
                target_coords = 35.64, 2.58
            if entrance == u'NW':
                target_coords = 2.88, 27.45
        elif trial_condition.startswith(u'R180'):
            if entrance == u'SW':
                target_coords = 2.88, 27.45
            if entrance == u'SE':
                target_coords = -21.68, -5.61
            if entrance == u'NE':
                target_coords = 11.07, -30.48
            if entrance == u'NW':
                target_coords = 35.64, 2.58
        elif trial_condition.startswith(u'R270'):
            if entrance == u'SW':
                target_coords = 35.64, 2.58
            if entrance == u'SE':
                target_coords = 2.88, 27.45
            if entrance == u'NE':
                target_coords = -21.68, -5.61
            if entrance == u'NW':
                target_coords = 11.07, -30.48
    return target_coords

def set_reverse_target():
    entrance = data_coords[33,1]
    trial_condition = data_coords[34,1]
    
    if experiment == '23May': 
        reverse_target_coords = -6.32, 36.62 #default coordinates
    elif experiment == '06Sept' or '07Oct' or '08July':
        if trial_condition.isdigit() is True:
            if entrance == u'SW':
                reverse_target_coords = 11.07, -30.48
            if entrance == u'SE':
                reverse_target_coords = 35.64, 2.58
            if entrance == u'NE':
                reverse_target_coords = 2.88, 27.45
            if entrance == u'NW':
                reverse_target_coords = -21.68, -5.61     
        elif trial_condition.startswith(u'R90'):
            if entrance == u'SW':
                reverse_target_coords = 35.64, 2.58
            if entrance == u'SE':
                reverse_target_coords = 2.88, 27.45
            if entrance == u'NE':
                reverse_target_coords = -21.68, -5.61
            if entrance == u'NW':
                reverse_target_coords = 11.07, -30.48
        elif trial_condition.startswith(u'R180'):
            if entrance == u'SW':
                reverse_target_coords = 11.07, -30.48
            if entrance == u'SE':
                reverse_target_coords = 35.64, 2.58
            if entrance == u'NE':
                reverse_target_coords = 2.88, 27.45
            if entrance == u'NW':
                reverse_target_coords = -21.68, -5.61  
        elif trial_condition.startswith(u'R270'):
            if entrance == u'SW':
                reverse_target_coords = 11.07, -30.48
            if entrance == u'SE':
                reverse_target_coords = 35.64, 2.58
            if entrance == u'NE':
                reverse_target_coords = 2.88, 27.45
            if entrance == u'NW':
                reverse_target_coords = -21.68, -5.61 
    return reverse_target_coords

#find index when mouse is in a particular x y location
def find_timepoint(x,y, array):
    array = np.array(array, dtype=np.float64)
    radius = 5
    time_in_range = ((array >= [x-radius, y-radius]) & (array <= [x+radius, y+radius])).all(axis=1)
    timepoint = np.around(np.median(np.where(abs(time_in_range)==True)[0]))#gets median value of timepoint range, then rounds so it has no decimals
#    timepoint = np.around(np.where(abs(time_in_range)==True)[0])
    if np.isnan(timepoint): timepoint = 0. #turns nan value to zero
    return timepoint

#gets coordinates from between the time interval defined in the trial
def get_coords():
    #gets index values for start and end times
    idx_start = int(find_nearest(data_coords[39:,0],time_start)+39) #numbers added so it matches with index of original excel file
    idx_end = int(find_nearest(data_coords[39:,0],time_end)+40)
    
    #gets nose point coordinates. To get center point, use 2 & 3 insead of 4 & 5
    x = np.array(data_coords[idx_start:idx_end,4], dtype=np.float64)
    y = np.array(data_coords[idx_start:idx_end,5], dtype=np.float64)
    
    #gets rid of the NaN values, might not actually be useful
#    x = x[~np.isnan(x)]
#    y = y[~np.isnan(y)]
    
    #gets nose point coordinates for return path
    last_time = int(39. + len(np.array(data_coords[39:,0], dtype=np.float64))) #by default, plot until the end of the trial
    x_return = np.array(data_coords[idx_end:last_time,4], dtype=np.float64)
    y_return = np.array(data_coords[idx_end:last_time,5], dtype=np.float64)
    
    return x,y, x_return, y_return

#automatically detect start and end points without excel
def get_coords_auto():
    idx_start = 39
    if find_timepoint(set_target()[0],set_target()[1],data_coords[39:,2:4]) != 0.:
        idx_end = int(find_timepoint(set_target()[0],set_target()[1],data_coords[39:,2:4])+40)
    else: idx_end = int(39. + len(np.array(data_coords[39:,0], dtype=np.float64)))
    
    #gets nose point coordinates. To get center point, use 2 & 3 insead of 4 & 5
    x = np.array(data_coords[idx_start:idx_end,2], dtype=np.float64)
    y = np.array(data_coords[idx_start:idx_end,3], dtype=np.float64)
    return x,y, idx_end
idx_end = get_coords_auto()[2]

def set_pathColor():
    pallet = plt.get_cmap('Set1')#gets colours from defined set
    mouse = data_coords[32,1]
    if experiment == 'pilot': mouseNo = 1
    if experiment == '23May' or '08July': mouseNo = 5
    if experiment == '06Sept': mouseNo = 9
    if experiment == '07Oct': mouseNo = 13
    if mouse == str(mouseNo): pathColor = pallet(1)
    if mouse == str(mouseNo+1): pathColor = pallet(2)
    if mouse == str(mouseNo+2): pathColor = pallet(3)
    if mouse == str(mouseNo+3): pathColor = pallet(4)
    return pathColor

def plot_coordinates():
    
    fig, ax = plt.subplots()
    
    #import image
    img = mpimg.imread(set_background_image())
    ax.imshow(img, extent=[-97, 97, -73, 73]) #plot image to match ethovision coordinates
    
    #plot path
#    ax.plot(get_coords()[0],get_coords()[1], ls='-', color = set_pathColor())
    #plot return path
#    ax.plot(get_coords()[2],get_coords()[3], ls='-', color = 'k')
    #plot auto path
    ax.plot(get_coords_auto()[0],get_coords_auto()[1], ls='-', color = 'green')
    
    #annotate image
    target = plt.Circle((set_target()), 2.5, color='g')
    ax.add_artist(target)
    if is_reverse is True: #annotates false target, optional
        prev_target = plt.Circle((set_reverse_target()), 2.5, color='r')
        ax.add_artist(prev_target)
    
    plt.style.use('default')
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    
#    plt.savefig('M'+ mouse + '_' + trial_condition + '.png', dpi=600, bbox_inches='tight', pad_inches = 0)
    plt.show()
    
plot_coordinates()

#calculates path length from coordinates
def calc_distance(x,y):
    dist = [np.sqrt((x[n]-x[n-1])**2 + (y[n]-y[n-1])**2) for n in range(1,len(x))]
    distance = np.nansum(dist)
    return distance
distance = calc_distance(get_coords_auto()[0],get_coords_auto()[1])

def calc_speed(distance, start,end):
    speed = np.nanmean(np.array(data_coords[start:end,13], dtype=np.float64))
    return speed
speed = calc_speed(distance,39,idx_end)

#report the data
print(experiment + ' Mouse ' + mouse + ' Trial ' + trial_condition)
print("Distance is "+str(distance) + ' cm')
print("Speed is "+str(speed)+' cm/s')