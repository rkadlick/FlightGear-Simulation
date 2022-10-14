import pandas as pd
import numpy as np
from sklearn_som.som import SOM
import sys
import os

#parsing of arguments

if len(sys.argv) != 2:
    print("please use below command to execute code")
    print("python som.py input_dataset_file")
    sys.exit(0)

if os.path.exists(sys.argv[1]) == False:
    print("Given dataset file does not exists")
    sys.exit(0)

inputFile = sys.argv[1] #getting input file
outputFile = inputFile.replace(".csv","_som.csv") #renaming input file to output file

trajectory = []
points = []
dataset = pd.read_csv(inputFile) #dataset reading
dataset.fillna(0, inplace = True)
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

som_cls = SOM(dim=5) #som clustering object
som_cls.fit(points) #start som training
predict = som_cls.predict(points)
centers = np.unique(predict) #get centers
dataset['Cluster_ID'] = pd.Series(predict, index=dataset.index)
dataset.to_csv(outputFile,index=False)
print("\nSOM Clustering Output\n")
dataset = dataset.values
for i in range(0,len(centers)):
    output = []
    for j in range(len(dataset)):
        if dataset[j,2] == centers[i]:
            output.append(dataset[j,0])
    print(str(centers[i])+" : "+str(', '.join(output))+"\n")        





