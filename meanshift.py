import pandas as pd
import numpy as np
from sklearn.cluster import MeanShift
import sys
import os

#parsing of arguments

if len(sys.argv) != 2:
    print("please use below command to execute code")
    print("python meanshift.py input_dataset_file")
    sys.exit(0)

if os.path.exists(sys.argv[1]) == False:
    print("Given dataset file does not exists")
    sys.exit(0)

inputFile = sys.argv[1] #getting input file
outputFile = inputFile.replace(".csv","_meanshift.csv") #renaming input file to output file

trajectory = []
points = []
dataset = pd.read_csv(inputFile) #dataset reading
df = dataset.values
for i in range(len(df)):
    t = df[i,0] #extracting trajectory
    p = df[i,1] #extracting points
    arr = p.split(",")
    temp = []
    for j in range(len(arr)): #converting points in string to float
        temp.append(float(arr[j].strip()))
    points.append(temp)
    trajectory.append(t)

points = np.asarray(points)
trajectory = np.asarray(trajectory)

mean_shift = MeanShift() #meahshift clustering object
mean_shift.fit_predict(points) #start meanshift training
centers = mean_shift.cluster_centers_ #get centers
dataset['Cluster_ID'] = pd.Series(mean_shift.labels_, index=dataset.index)
dataset.to_csv(outputFile,index=False)
print("\nMeanShift Clustering Output\n")
for i in range(0,len(centers)):
    output = dataset.loc[dataset['Cluster_ID'] == i, 'Trajectories']
    print(str(i)+" : "+str(', '.join(output.tolist()))+"\n")
        





