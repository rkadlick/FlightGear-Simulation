import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster


def dendro(file, clusterCount, isCCPassed):
    """
    :param file: Input File
    :param clusterCount: If not passed the default is 3
    :param isCCPassed: Check if clusterCount is passed & create a CSV
    :return:
    """

    dataframe = pd.read_csv(file)
    dataframe = dataframe.dropna()

    # Get data for column 'Degree = 4 Coefficients' The column contains the points in a string '[ .. ]',
    # so we will have to parse that string to remove the brackets and extract the float values

    pointsRaw = dataframe.iloc[:, [1]].to_numpy()  # extract values and convert to numpy
    # Now, take each row, remove first and last characters ( [] ), and split

    X = None

    # Loop through each raw sample
    for i, points_str in enumerate(pointsRaw):
        # Convert to float
        points_i = list(map(float, [x for x in points_str[0].split(",")]))

        if i == 0:
            X = np.zeros((pointsRaw.shape[0], len(points_i)))  # Matrix to store all trajectories
        # Add to matrix
        X[i, :] = points_i

    # Hierarchical Clustering
    Z = linkage(X, method='ward', metric='euclidean')

    # Dendrogram
    # creating label dictionary based on index and 'Trajectories' column for x-axis tick labels 
    label_dict = dict(zip(dataframe['Trajectories'].index, dataframe['Trajectories']))

    # Create figure
    plt.figure(figsize=(15, 10))
    # Create dendrogram
    dn = dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x-axis labels
        leaf_font_size=8,  # font size for the x-axis labels
        leaf_label_func=lambda x: label_dict[x]
    )

    plt.xticks()
    plt.savefig('dendrogram.png')
    plt.show()

    if isCCPassed:
        # calculating clusters using dendrogram height with fcluster
        f_labs = fcluster(Z, t=clusterCount, criterion='maxclust')

        dataframe['Cluster Label'] = f_labs
        dataframe.to_csv(file.split('.csv')[0] + '_clustered.csv', index=False)
        for group, rows in dataframe.groupby(by='Cluster Label'):
            print(str(group) + ':', ', '.join(rows['Trajectories']))


if __name__ == '__main__':

    cc = None
    file = None
    isCCPassed = False

    if len(sys.argv) == 1:
        raise Exception("Please Pass Input CSV")
    elif len(sys.argv) == 2:
        file = sys.argv[1]
    elif len(sys.argv) == 4:
        isCCPassed = True
        cc, file = int(sys.argv[2]), sys.argv[3]

    dendro(file, cc, isCCPassed)
