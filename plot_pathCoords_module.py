# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 15:15:30 2020
Python Version 2.7.14 

New version of plot_pathCoords2
New in this version: wrapped into a function so it can be used as a module
Changed how target coordinates are calculated so it ends as soon as mouse reaches target
Changed filename to int
Improved some comment explanations

@author: Kelly
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg #for plotting the image
import numpy as np #for the array
import pandas as pd
from matplotlib import cm

#variables to change each time
experiment = '26May_21' #Options: pilot, 23May, 08July, 06Sept, 07Oct, 11Dec, 08Mar_21, 06May_21, 26May_21
trial = 72  #trial number on excel file

def plot_path_coords(experiment, trial, plot, calc):
        
    #sets path of folder with raw trial data and times
    def set_experiment_path(experiment):
        if experiment == 'pilot':
            raw_data_path = 'Raw Trial Data\pilot_Raw Trial Data\Raw data-Hidden Food Maze - Pilot-Trial   '
        if experiment == '23May':
            raw_data_path = 'Raw Trial Data\\2019-05-23_Raw Trial Data\Raw data-Hidden Food Maze-23May2019-Trial   '
        if experiment == '08July':
            raw_data_path = 'Raw Trial Data\\2019-07-08_Raw Trial Data\Raw data-Hidden Food Maze-08Jul2019-Trial   '
        if experiment == '06Sept':
            raw_data_path = 'Raw Trial Data\\2019-09-06_Raw Trial Data\Raw data-Hidden Food Maze-06Sept2019-Trial   '
        if experiment == '07Oct':
            raw_data_path = 'Raw Trial Data\\2019-10-07_Raw Trial Data\Raw data-Hidden Food Maze-07Oct2019-Trial   '
        if experiment == '11Dec':
            raw_data_path = 'Raw Trial Data\\2019-12-11_Raw Trial Data\Raw data-Hidden Food Maze-11Dec2019-Trial   '
        if experiment == '08Mar_21':
            raw_data_path = 'Raw Trial Data\\2021-03-08_Raw Trial Data\Raw data-Hidden Food Maze-08Mar2021-Trial   '
        if experiment == '06May_21':
            raw_data_path = 'Raw Trial Data\\2021-05-06_Raw Trial Data\Raw data-Hidden Food Maze-06May2021-Trial   '
        if experiment == '26May_21':
            raw_data_path = 'Raw Trial Data\\2021-05-26_Raw Trial Data\Raw data-Hidden Food Maze-26May2021-Trial   '
         
        return raw_data_path
    
    #gets raw trial coordinates from ethovision
    def read_excel(trial):
        #adjusts filename to have correct number of spaces
        if trial < 10: filename = "  "+str(trial)
        elif trial <100: filename = " "+str(trial)
        else: filename = str(trial)
        
        if experiment.endswith('21') is True: skip = range(30, 32) #accomadates version change in ethovision file
        else: skip = 0
        
        df = pd.read_excel(set_experiment_path(experiment) + filename + '.xlsx', header=None, skiprows=skip, na_values=['-'])
        data_coords = np.asarray(df)
        return data_coords
    data_coords = read_excel(trial)
    
    if data_coords[34,1].startswith(u'R') == True or data_coords[34,1].startswith(u'Flip') == True: is_reverse = True 
    else: is_reverse = False
    
    trial_condition = data_coords[34,1]
    mouse = data_coords[32,1]
    
    #find index of nearest value in array
    def find_nearest(array, value):
        array = np.array(array, dtype=np.float64)
        nearest_idx = np.where(abs(array-value)==abs(array-value).min())[0]
        return nearest_idx
    
    def set_background_image():
        entrance = data_coords[33,1]
        background_path = 'BackgroundImage\\'
        if entrance == u'SW': background = background_path+'BKGDimage-pilot.png'
        if entrance == u'SE': background = background_path+'BKGDimage-pilot2.png'
        if entrance == u'NE': background = background_path+'BKGDimage-pilot3.png'
        if entrance == u'NW': background = background_path+'BKGDimage-pilot4.png'
        if experiment == '11Dec': background = background_path+'BKGDimage-localCues.png'
        if experiment == '08Mar_21': background = background_path+'BKGDimage-localCues_clear.png'
        if experiment == '06May_21': background = background_path+'BKGDimage-localCues_Letter.png'
        if experiment == '26May_21': background = background_path+'BKGDimage-localCues_LetterTex.png'
        return background
    
    #manually sets food target coordinates based on experiment
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
        elif experiment == '11Dec': target_coords = 2.88, 27.45
        elif experiment == '08Mar_21' or experiment == '06May_21' or experiment == '26May_21': target_coords = 24.47, 21.80
        return target_coords
    
    #sets the rotationally equivalent location of the target, only use during rotation trials
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
            elif experiment == '11Dec': reverse_target_coords = 11.07, -30.48
            elif experiment == '08Mar_21' or experiment == '06May_21' or experiment == '26May_21': reverse_target_coords = -19.61, -16.63
        return reverse_target_coords
    
    #find index when mouse is in a particular x y location
    def find_timepoint(x,y, array):
        array = np.array(array, dtype=np.float64)
        radius = 5 #change this radius if you want the target to be bigger or smaller, normally 5
        time_in_range = ((array >= [x-radius, y-radius]) & (array <= [x+radius, y+radius])).all(axis=1)
        timepoint = np.around(np.where(abs(time_in_range)==True)[0])
        if timepoint.size == 0: 
            timepoint = 0. #turns nan value to zero
            print("WARNING target never reached")
        else: timepoint = timepoint[0]
        return timepoint

    #automatically detect start and end points without excel
    def get_coords_auto():
        idx_start = 39
        if find_timepoint(set_target()[0],set_target()[1],data_coords[39:,2:4]) != 0.:
            idx_end = int(find_timepoint(set_target()[0],set_target()[1],data_coords[39:,2:4])+40)
        else: idx_end = int(39. + len(np.array(data_coords[39:,0], dtype=np.float64)))
        
        #gets nose point coordinates. To get center point, use 2 & 3 insead of 4 & 5
        x = np.array(data_coords[idx_start:idx_end,4], dtype=np.float64)
        y = np.array(data_coords[idx_start:idx_end,5], dtype=np.float64)
        return x,y, idx_end
    idx_end = get_coords_auto()[2]
    
    #gets return trajectory coords. needs index calculation from get_coords_auto
    def get_coords_return():
        idx_last = int(39. + len(np.array(data_coords[39:,0], dtype=np.float64)))
        
        x = np.array(data_coords[idx_end:idx_last,4], dtype=np.float64)
        y = np.array(data_coords[idx_end:idx_last,5], dtype=np.float64)
        return x,y
    
    def plot_coordinates():
        
        fig, ax = plt.subplots()
        
        #import image
        img = mpimg.imread(set_background_image())
        ax.imshow(img, extent=[-97, 97, -73, 73]) #plot image to match ethovision coordinates
        if experiment == '11Dec': ax.imshow(img, extent=[-129.58, 129.58, -73.03, 73.03])
        if experiment == '08Mar_21' or experiment == '06May_21' or experiment == '26May_21': ax.imshow(img, extent=[-151.06, 150.43, -84.23, 84.86])
        
        #collect variables
        x = get_coords_auto()[0]
        y = get_coords_auto()[1]
        
        #plot auto path
        ax.plot(x, y, ls='-', color = 'red')
        #plot return path
#        ax.plot(get_coords_return()[0],get_coords_return()[1], ls='-', color = 'k')
        
        #plot path with colours
#        N = np.linspace(0, 10, np.size(y))
#        ax.scatter(x, y, s=1.5, c = N, cmap=cm.jet_r, edgecolor='none')
        
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
        
#        plt.savefig('M'+ mouse + '_' + trial_condition + '.png', dpi=600, bbox_inches='tight', pad_inches = 0)
        plt.show()
    
    if plot == True:    
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
    
    def calc_latency():
        latency = data_coords[idx_end-1,1]
        return latency
    latency = calc_latency()
    
    if calc == True:
        #report the data
        print(experiment + ' Mouse ' + mouse + ' Trial ' + trial_condition)
        print("Distance is "+str(distance) + ' cm')
        print("Speed is "+str(speed)+' cm/s')
        print("index end is " + str(idx_end))
        print("Latency is "+str(latency)+' s')
        
    return distance, speed, mouse, trial_condition, latency
    
    
def main():
    plot_path_coords(experiment, trial, plot = True, calc = True)
 
if __name__ == '__main__': #only runs this function if the script top level AKA is running by itself 
    main()