# EthovisionPathAnalysis
Plots and analyses tracked trials from raw Ethovision data
Written in Python 2.7
Data from my Hidden Food Maze behavioural experiment
If adapting for a different experiment:
- change background coordinates based on Ethovision's XY coordinates

New in Version 0.2:
- calc_DistanceAndSpeed.py added: interates over trials to gather distance and speed info
- changed filename from str to int
- Changed how target coordinates are calculated so it ends as soon as mouse reaches target
- added option to plot path with colour gradient
