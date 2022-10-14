import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sys
import os

#parsing of arguments

if len(sys.argv) != 4:
    print("please use below command to execute code")
    print("python kmeans.py -cc num_clusters input_dataset_file")
    sys.exit(0)

if sys.argv[1] != '-cc':
    print("cc option and num clusters must be defined")
    sys.exit(0)

if sys.argv[2].strip().isdigit() == False:
    print("cluster count value must be numeric only")
    sys.exit(0)

if os.path.exists(sys.argv[3]) == False:
    print("Given dataset file does not exists")
    sys.exit(0)

#getting cc value from command line
cc = int(sys.argv[2].strip())

inputFile = sys.argv[3] #getting input file
outputFile = inputFile.replace(".csv","_kmeans.csv") #renaming input file to output file

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

kmeans = KMeans(n_clusters=cc, init='k-means++') #kmeans clustering object
kmeans.fit_predict(points) #start kmeans training
centers = kmeans.cluster_centers_ #get centers
dataset['Cluster_ID'] = pd.Series(kmeans.labels_, index=dataset.index)
inertia = kmeans.inertia_
dataset.to_csv(outputFile,index=False)

for i in range(0,cc):
    output = dataset.loc[dataset['Cluster_ID'] == i, 'Trajectories']
    print(str(i)+" : "+str(', '.join(output.tolist()))+"\n")
        

scores = []
cluster = []

inertias = []
cluster_num = []
for i in range(1,10): #generate elbow value with various K
    kmean = KMeans(n_clusters=i, init='k-means++')
    kmean = kmean.fit(points)
    inertias.append(kmean.inertia_)
    cluster_num.append(i)

for i in range(0,cc): #find silhoute score
    X_train, X_test, y_train, y_test = train_test_split(points, points, test_size=0.2)
    score = silhouette_score(X_test, kmeans.predict(X_test))
    scores.append(score)
    cluster.append(i)

fig, axs = plt.subplots(1,2)
axs[0].barh(cluster, scores, color='maroon')
  
axs[0].set_xlabel("Silhouette Score") #plot silhoutte graph
axs[0].set_ylabel("Number of Clusters")
axs[0].set_title("KMEANS Silhouette Score Graph")


axs[1].plot(cluster_num, inertias, 'bx-')
axs[1].set_xlabel('Cluster Number')
axs[1].set_ylabel('Inertia')
axs[1].set_title('Kmeans Elbow Graph')
plt.show()




