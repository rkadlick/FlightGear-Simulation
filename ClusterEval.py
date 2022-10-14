from tslearn.clustering import TimeSeriesKMeans
import csv
import numpy as np
import glob
from tslearn.utils import to_time_series_dataset
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_samples, silhouette_score
from tslearn.metrics import cdist_soft_dtw, cdist_dtw
import matplotlib.cm as cm

def getAlt(filename):
    alt = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            alt.append(float(row[3]))
    return alt


rs = np.random.seed(1266)

dat = glob.glob("Data/*")

flightAlts = []
for flight in dat:
    flightAlts.append(getAlt(flight))
flightAlts = to_time_series_dataset(flightAlts)

clusters = [2, 3, 4, 5, 6]
inertia = []

cdist = cdist_dtw(flightAlts)

for i in clusters:
    sdtw = TimeSeriesKMeans.from_pickle(str(i) + "_cluster.pickle")
    y_pred = sdtw.predict(flightAlts)
    inertia.append(sdtw.inertia_)
    print(y_pred)

    # Create data visualization
    plt.figure(figsize=(4 * i, 6), dpi=80)
    for yi in range(i):
        plt.subplot(1, i, 1 + yi)
        for xx in flightAlts[y_pred == yi]:
            plt.plot(xx.ravel(), "k-", alpha=.2)

        plt.plot(sdtw.cluster_centers_[yi].ravel(), "r-")
        plt.xlim(0, 400)
        plt.ylim(0, 2200)
        plt.title(str(i) + " Cluster $k$-means: Cluster " + str(yi + 1))
    plt.savefig(str(i) + "_clusterGraph.png")


    # Silhouette Plot
    avg_score = silhouette_score(cdist, y_pred)
    print("Average silhouette score for", i, "clusters is: ", avg_score)
    silVals = silhouette_samples(cdist, y_pred)
    # print(silVals)
    fig, ax = plt.subplots()
    y_lower = 5
    for j in range(i):
        jth_clusterVals = silVals[y_pred == j]
        jth_clusterVals.sort()

        size_cluster_j = jth_clusterVals.shape[0]
        y_upper = y_lower + size_cluster_j
        color = cm.nipy_spectral(float(j)/i)
        ax.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            jth_clusterVals,
            facecolor=color,
            edgecolor=color,
            alpha=0.7)
        ax.text(-0.05, y_lower + 0.5 * size_cluster_j, str(j+1))
        y_lower = y_upper + 5
        ax.axvline(x=avg_score, color="red", linestyle="--")
        ax.set_title("Silhouette plot for "+str(i)+" clusters")
        ax.set_xlabel("Silhouette score")
        ax.set_ylabel("Cluster")
        ax.set_yticks([])

    plt.savefig(str(i)+ "_clusterSilhouette.png")



# Elbow Analysis
plt.subplots()
plt.plot(clusters, inertia)
plt.xlabel("Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Analysis")
plt.savefig("ElbowAnalysis.png")
