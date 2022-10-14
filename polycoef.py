import os
import random
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from matplotlib import pyplot as plt

# ------------------------------------------------------------------------------------------------------------
# Accept a input directory. If output directory is not passed output will be saved in input directory
#           python3 polycoef.py -in ./input
# -------------------------------------------------------------------------------------------------------------
# Accept a input & output directory. Output directory will be created if it doesn't exist
#           python3 polycoef.py -in ./input -out ./output
# --------------------------------------------------------------------------------------------------------------


def generate_csv():
    """
    Creates a Dataframe with all the column names

    :return: Returns a dataframe with all the necessary column names
    """
    columns = ["Trajectories"]
    for idx in range(1, 10):
        columns.append(f"Degree={idx} Coefficients")
        columns.append("MSR")
    df = pd.DataFrame(columns=columns)
    return df


def visualize_trajectory(x, y):
    """
    Visualizes all the trajectories from Degree 1 to 9 & plots them in a single figure

    :param x: Distance to Runway
    :param y: Alt - Ground level
    :return: Visualizes the plot
    """
    fig, axs = plt.subplots(3, 3, figsize=(3, 3))
    degree = 1
    for i in range(3):
        for j in range(3):
            if i == 2:
                axs[i, j].set_xlabel("Distance to Runway (nmi)")
            axs[i, j].set_ylabel("Alt - Ground Level")
            axs[i, j].set_title(f"Degree-{degree}")
            coefficients, residual, _, _, _ = np.polyfit(x, y, degree, full=True)
            poly1d_fn = np.poly1d(coefficients)
            axs[i, j].plot(x, y, 'yo', x, poly1d_fn(x))
            degree += 1
    plt.show()


def calculate_coefficients(fileName, dataframe, data, trajectoriesCount, randomTrajectory):
    """
    Calculates the coefficients & MSR for all the data & appends it to the final dataframe

    :param dataframe: Final Dataframe
    :param data: Landing Data
    :param trajectoriesCount: Number of trajectories
    :param randomTrajectory: Randomly selected trajectory to visualize the data
    :return:
    """

    x = np.array(data["Distance From Start (nmi)"])
    y = np.array(data["Alt - Ground Level"])

    # Getting the number of rows in the dataframe
    numberOfRows = data.shape[0]

    # Visualising random trajectory
    if trajectoriesCount == randomTrajectory:
        # Un-comment to visualize the trajectories
        visualize_trajectory(x, y)

    # Appending file name to the rows in the dataframe
    rowData = [fileName]

    for degree in range(1, 10):

        # Calculate coefficients & SSR for X, Y
        coefficients, residual, _, _, _ = np.polyfit(x, y, degree, full=True)

        # Checking if the residual is Empty
        residual = 0 if len(residual) == 0 else residual[0]

        # Calculating MSR (SSR / Number of rows in dataframe)
        residualMSR = round((residual / numberOfRows), 2)

        # Appends coefficients & MSR to the rowData list
        rowData.append(np.array2string(coefficients, separator=",")[1:-1])
        rowData.append(residualMSR)

    # Appends the calculated coefficients & MSR of a trajectory to the final Dataframe
    dataframe.loc[trajectoriesCount] = rowData


def calculate_mean_msr(dataframe, trajectoriesCount):
    """
    Calculates the Mean-MSR for all the trajectories

    :param dataframe: Final Dataframe
    :param trajectoriesCount: Number of trajectories
    :return:
    """
    rowData = [""]
    for idx in range(1, 19):
        if idx % 2 == 0:
            # Calculates the Mean of MSR for all the trajectories from degree 1 to degree 9
            rowData.append(dataframe.iloc[:, idx].mean())
        else:
            rowData.append("")

    # Appends the calculated MEAN-MSR of a trajectory to the final Dataframe
    dataframe.loc[trajectoriesCount] = rowData


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # Commands for input and output
    parser.add_argument('-in', metavar="INPUT", help='input file/directory')
    parser.add_argument('-out', metavar="OUTPUT", help='output directory')

    args = vars(parser.parse_args())

    # Raises an Exception if input path is not specified
    if not args["in"]:
        raise Exception("Please pass input directory")
    else:
        inputDirectory = args['in']

    # If output path is not specified final csv will be saved in the input path
    if not args["out"]:
        outputDirectory = inputDirectory
    else:
        outputDirectory = args["out"]

    # Generates a CSV with all the required column names
    dataframe = generate_csv()

    for subdir, dirs, files in os.walk(inputDirectory):

        # Counts the number of trajectories in the folder
        trajectoriesCount = 1

        # Selecting a random trajectory to visualize
        randomTrajectory = random.randint(0, len(files))

        for file in files:
            # Separates file name & file extension
            fileName = os.path.splitext(file)

            # Checks if the file is CSV
            if fileName[1] == ".csv" and fileName[0][:3] == "out":
                # Reads the CSV file
                data = pd.read_csv(inputDirectory + "/" + file, encoding="Latin-1", engine="python")

                # Calls calculate-coefficients method
                calculate_coefficients(fileName[0], dataframe, data, trajectoriesCount, randomTrajectory)
                trajectoriesCount += 1

        # Calculates the MEAN of MSR
        calculate_mean_msr(dataframe, trajectoriesCount)

        # Retrieve Current time
        currentTime = datetime.now()
        currentTime = currentTime.strftime("%Y%m%d-%H%M%S")

        # Creates file Path
        filePath = Path(outputDirectory + f"/polycoef-{currentTime}.csv")

        # Creates Directory if output path does not exist
        filePath.parent.mkdir(parents=True, exist_ok=True)

        # Saves the csv to output directory
        dataframe.to_csv(filePath, index=False)
