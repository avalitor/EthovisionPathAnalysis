# -*- coding: utf-8 -*-
"""
Created on Thu Jun 03 20:32:22 2021

extracts information from excel file

@author: Kelly
"""
import numpy as np #for the array
import pandas as pd

experiment = '06Sept' #Options: pilot, 23May, 08July, 06Sept, 07Oct
trial = 88  #trial number on excel file


def get_trial(experiment, trial):
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
        return raw_data_path
    
    def read_excel(trial):
        #adjusts filename to have correct number of spaces
        if trial < 10: filename = "  "+str(trial)
        elif trial <100: filename = " "+str(trial)
        else: filename = str(trial)
        
        df = pd.read_excel(set_experiment_path(experiment) + filename + '.xlsx', header=None, na_values=['-'])
        data_coords = np.asarray(df)
        return data_coords
    data_coords = read_excel(trial)