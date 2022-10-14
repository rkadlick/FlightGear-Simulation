import os
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from scipy.optimize import curve_fit


# ------------------------------------------------------------------------------------------------------------
# Accept a input directory. If output directory is not passed output will be saved in input directory
#           python3 sigmoid.py -in ./input
# -------------------------------------------------------------------------------------------------------------
# Accept a input & output directory. Output directory will be created if it doesn't exist
#           python3 sigmoid.py -in ./input -out ./output
# --------------------------------------------------------------------------------------------------------------


def generate_csv():
    """
    Creates a Dataframe with all the column names

    :return:
    """
    # Adding the column names to the dataframe
    columns = ["Trajectories", "Coefficients"]
    return pd.DataFrame(columns=columns)


def sigmoid(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x - d))) + b


def calculate_sigmoid_coefficients(fileName, dataframe, data, trajectoriesCount):
    x = np.array(data["Distance From Start (nmi)"])
    y = np.array(data["Alt - Ground Level"])

    # Append the fileName to the list
    rowData = [fileName]

    # values = opt.curve_fit(sigmoid, x, y)
    popt, _ = curve_fit(sigmoid, x, y)

    # Append the trajectories to the list
    rowData.append(np.array2string(popt, separator=",")[1:-1])

    # Appending the list to the dataframe
    dataframe.loc[trajectoriesCount] = rowData


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

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

        for file in files:
            # Separates file name & file extension
            fileName = os.path.splitext(file)

            # Checks if the file is CSV
            if fileName[1] == ".csv" and fileName[0][:3] == "out":
                # Reads the CSV file
                data = pd.read_csv(inputDirectory + "/" + file, encoding="Latin-1", engine="python")

                # Calculates the coefficients for sigmoid function
                calculate_sigmoid_coefficients(fileName[0], dataframe, data, trajectoriesCount)

                trajectoriesCount += 1

        # Retrieve Current time
        currentTime = datetime.now()
        currentTime = currentTime.strftime("%Y%m%d-%H%M%S")

        # Creates file Path
        filePath = Path(outputDirectory + f"/sigmoidCoef-{currentTime}.csv")

        # Creates Directory if output path does not exist
        filePath.parent.mkdir(parents=True, exist_ok=True)

        # Saves the csv to output directory
        dataframe.to_csv(filePath, index=False)
