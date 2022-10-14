# FlightGear Project Overview

This was a semester long Capstone project, completed in my final semester of graduate school at University of Massachusetts - Boston. This was completed in a team of 5 members.

The goal of this project was to capture and analyze the trajectory of an aircraft landing and use this data to characterize what a successful landing was, for real world use in training and auto-landing purposes. We were given references to what a successful landing looked like to compare our runs to.

The project began by learning how to fly a plane using the free flight simulation program FlightGear. After learning how to fly and land a particular aircraft (Cessna) to a particular airport (Logan - Boston), we were to extract certain data from the flight record for each landing attempt. This data included latitude, longitude, elevation, airspeed, etc. With this data we were then to visualize the data to show the difference between a successful and unsuccessful landing. After visualizing the data our final task was to perform regression for the trajectories:\ 
	- to mathematically characterize them\
	- to classify them and measure similarity among them\
	- to derive a representative trajectory from them\

The work was divided up among the team members, although we brainstormed and conversed together, the first section of the project, pre-processing the data, was my task.


Project Sections


Section 1 - Flightprocess.py 

Extract required data from raw flight data and pre-process the extracted data based on a given data collection frequency (in Hz). Visualize a specified set of trajectories in two different types of 2D 
graphs. One of them is shown in the project presentation slides (the one with x-axis for ground level and y-axis for elevation). A center/median line will be identified on each graph.


Section 2 - Sigmoid..py, Polycoef.py

Perform non-linear curve fitting (regression) for each trajectory and visualize flight data and a fitted curve. Will use a few fitting/regression methods such as 2nd/3rd polynomial fitting and model function based fitting (e.g. sigmoid function). All these curve fitting methods are implemented/available in numpy (polyfit) and scipy (curve_fit).


Part 3 - kmeans.py, hcout.py, meanshift.py, som.py

Perform a few clustering algorithms such as k-means, mean shift, mini-batch k-means and DBSCAN (Density-based Spatial Clustering of Applications with Noise) to cluster trajectories. All these algorithms are implemented/available in scikit-learn.

Part 4 -  ClusterEval.py

Perform time series clustering for trajectories. A simple one like "time series k-means" is fine. It is implemented/available in tslearn 
