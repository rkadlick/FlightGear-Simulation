# Flight Gear

import enum
import os
import math
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np;
import geopy
from geopy import distance

# This program can be run multiple ways
# ---------------------------------------
# PREPROCESS DATA: This program pre-processes flight data. It adds two new columns to the .csv file,'Altitude from ground level' and 'Distance from start(nmi)'. 
# ----------------
# Accept a single input and output directory:
#           python3 flightprocess.py -in input.csv -out ./output
#
# Accept a single input file or directory (output directory will be created):
#           python3 flightprocess.py -in input.csv
#           python3 flightprocess.py -in ./input
#
# Accept a directory of input files and output directory:
#           python3 flightprocess.py -in ./input -out ./output
#
# Accept a combined list of directories and files:
#           python3 flightprocess.py -in ./input input1.csv, input2.csv
#           python3 flightprocess.py -in input1.csv, input2.csv, input3.csv
#
# Accept custom coordinates (lat, long, alt) for an airport other than the default: Logan Airport - Boston:
#           python3 flightprocess.py -in input.csv -out ./output -rlat xxx -rlong xxx -alt xxx -slat xxx -slong xxx
# ---------------
# VISUALIZE DATA: Turn newly created data from above into two different landing pattern graphs
# ----------------
# Accept a single input file or directory to turn into graph (MUST HAVE NEW COLUMNS FROM ABOVE -- HINT: USE OUTPUT FOLDER:
#           python3 flightprocess.py -v output.csv
#           puthon3 flightprocess.py -v ./output
#
# Accept a combined list of directories and files:
#           python3 flightprocess.py -v ./output output1.csv, output2.csv
#           python3 flightprocess.py -v output1.csv, output2.csv, output3.csv

# These coordinates below can be changed manually when running the program, however all 5 attributes must be changed to ensure the program runs correctly.
# Default for Boston Logan International
# Coordinates of runway 33L Logan Airport
rLat = 42.35462
rLong = -70.99158
# Coordinates of starting location 5nm from runway 33L
startLat = 42.29543
startLong = -70.91265
# Height (in feet) that runway 33L is above sea level
alt = 16

# Below calculates the angle between the starting position and runway position
# This angle is used in the future to create the top down graph
# Default (Logan airport runway 33L): Degrees: 53.13358686          Radians: 0.927356
angle = np.arctan(abs(rLong - startLong)/abs(rLat-startLat))

# Used to calculate the distance between the runway and each point in the csv file, currently in miles
def calc_distance(row):
    startPoint = (startLat, startLong)
    # Takes the lat and long coordinates from columns 'Lat' and 'Long'
    point = (row.Lat, row.Long)
    # Reverse the distance from runway into the distance from starting point
    # We start at 5 nautical miles, if we subtract that number and turn it positive we get distance from starting point
    d = (geopy.distance.distance(startPoint, point).nm)
    return(d)

# Process function to create the two new columns in the csv files
def flight_process(input, output):

    # input variable will be a list of 1 or more files and directories to pre-process
    for inp in input:

        if(os.path.isdir(inp)):
            # This loop runs for all files in the directory
            for subdir, dirs, files in os.walk(inp):
                for file in files:
                    # If statement included, due to accessing hidden Mac files
                    if file == '.DS_Store':
                        pass
                    else:
                        # Here the reader variable will read each .csv file placed in the input folder
                        fileName = os.path.basename(file)
                        reader = pd.read_csv(inp + "/" + file, encoding="Latin-1", engine='python')
                        
                        # The reader creates a new data column for ground level altitude which is calculated by subtracting 16 from the sea level altitude in column 'Alt'
                        # Runway 33L is 16ft above sea level
                        reader['Alt - Ground Level'] = reader['Alt'] - int(alt)
                        
                        # The reader creates a new data column for distance between the lat/long positions in the csv file and the runway
                        reader['Distance From Start (nmi)'] = reader.apply(calc_distance, axis=1)
                        
                        # The reader outputs the new .csv file to the output folder and adds 'out' to the file name to further differentiate
                        reader.to_csv(output+'/out'+fileName, index=False)

        if(os.path.isfile(inp)):
            # Here the reader variable will read each .csv file placed in the input folder
            fileName = os.path.basename(inp)
            reader = pd.read_csv(inp, encoding="Latin-1", engine='python')
            
            # The reader creates a new data column for ground level altitude which is calculated by subtracting the given altitude from the sea level altitude in column 'Alt'
            reader['Alt - Ground Level'] = reader['Alt'] - alt
            
            # The reader creates a new data column for distance between the lat/long positions in the csv file and the runway
            reader['Distance From Start (nmi)'] = reader.apply(calc_distance, axis=1)
            
            # The reader outputs the new .csv file to the output folder and adds 'out' to the file name to further differentiate
            reader.to_csv(output+'/out'+fileName, index=False)

    

# Visualize function to take the processed files and turn them into graphs
def visualize(input):

    # The following functions are used to update the annotations for each line on the two different plots
    # Function used to update annotation lines for plot 1 (Horizontal View)
    # It reads the data from the line and using that index it matches it with the file used and it's dataframe from the dataframes variable.
    # Then each x/y position will match with a row on the dataframe in order to pull the other needed information for the annotations   
    def update_annot_d1(line, idx):
        posx, posy = [line.get_xdata()[idx], line.get_ydata()[idx]]
        annot1.xy = (posx, posy)
        index = lines1.index(line)
        text = 'Altitude: ' + str(posy) + '\n' + 'Distance traveled: ' + str(posx) + '\n' + 'Airspeed-kt: ' + str(dataframes[index].loc[dataframes[index]['Alt - Ground Level'] == posy, 'Airspeed-kt'].item()) + '\n' + 'Vertical-Speed-FPS: ' +  str(dataframes[index].loc[dataframes[index]['Alt - Ground Level'] == posy, 'Vert-Speed-FPS'].item()) + '\n' + 'Landing Angle: ' + str(np.rad2deg(np.arctan(posy/(30380.58 - (posx * 6076.115))))) + '\n' + 'Time Elapsed (s): ' + str(dataframes[index].loc[dataframes[index]['Alt - Ground Level'] == posy, 'Time'].item()) 
        annot1.set_text(text)
        annot1.get_bbox_patch().set_alpha(0.4)

    # Hover function to allow the annotation functions to annotate when hovering over each line for plot 1 (Horizontal View)
    def hover_d1(event):
        vis = annot1.get_visible()
        if event.inaxes == ax1:
            for line in lines1:
                cont, ind = line.contains(event)
                if cont:
                    update_annot_d1(line, ind['ind'][0])
                    annot1.set_visible(True)
                    fig1.canvas.draw_idle()
                else:
                    if vis:
                        annot1.set_visible(False)
                        fig1.canvas.draw_idle()

    # Function used to update annotation lines for plot 2 (Top-Down View)
    # It reads the data from the line and using that index it matches it with the file used and it's dataframe from the dataframes variable.
    # Then each x/y position will match with a row on the dataframe in order to pull the other needed information for the annotations   
    def update_annot_d2(line, idx):
        posx, posy = [line.get_xdata()[idx], line.get_ydata()[idx]]
        annot2.xy = (posx, posy)
        index = lines2.index(line)

        # The Top-Down View graph is rotated in order to show a straight horizontal line
        # Below will convert the points on the graph back into the Latitude form to match up with the dataframes/csv files
        lY = (posy - (dataframes[index]['Lat'] * (np.sin(angle))))/np.cos(angle)

        text = 'Altitude: ' + str(dataframes[index].loc[dataframes[index]['Long'] == lY , 'Alt - Ground Level'].item()) + '\n' + 'Distance traveled: ' + str(dataframes[index].loc[dataframes[index]['Long'] == lY, 'Distance From Start (nmi)'].item()) + '\n' + 'Airspeed-kt: ' + str(dataframes[index].loc[dataframes[index]['Long'] == lY, 'Airspeed-kt'].item()) + '\n' + 'Vertical-Speed-FPS: ' +  str(dataframes[index].loc[dataframes[index]['Long'] == lY, 'Vert-Speed-FPS'].item()) + '\n' + 'Landing Angle: ' + str(np.rad2deg(np.arctan(dataframes[index].loc[dataframes[index]['Long'] == lY, 'Alt - Ground Level'].item()/(30380.58 - (dataframes[index].loc[dataframes[index]['Long'] == lY, 'Distance From Start (nmi)'].item() * 6076.115))))) + '\n' + 'Time Elapsed (s): ' + str(dataframes[index].loc[dataframes[index]['Long'] == lY, 'Time'].item()) 
        annot2.set_text(text)
        annot2.get_bbox_patch().set_alpha(0.4)

    # Hover function to allow the annotation functions to annotate when hovering over each line for plot 2 (Top-Down View)
    def hover_d2(event):
        vis = annot2.get_visible()
        if event.inaxes == ax2:
            for line in lines2:
                cont, ind = line.contains(event)
                if cont:
                    update_annot_d2(line, ind['ind'][0])
                    annot2.set_visible(True)
                    fig2.canvas.draw_idle()
                else:
                    if vis:
                        annot2.set_visible(False)
                        fig2.canvas.draw_idle()

    # Creating first plot
    fig1, ax1 = plt.subplots()

    # Variables used for annotations
    # lines will hold an array of each line on plot 1 which represents each file
    # dataframes will hold an array of each csv file as a data frame
    lines1 = []
    dataframes = []

    # Reference line for a proper landing
    ref1X = np.array([0, 1, 3, 5])
    ref1Y = np.array([1200, 1200, 600, 0])
    ax1.plot(ref1X,ref1Y, 'r-', label='Reference Line')     
    
    # input variable is a list of 1 or more files or directories that we need to iterate through
    for inp in input:
        
        # checks if item in input list is a file or directory
        if(os.path.isdir(inp)):

            for subdir, dirs, files in os.walk(inp):
                # loop through all csv files in directory
                for file in files:
                    # Checks for .ds_Store (Mac issue)
                    if file == '.DS_Store':
                        pass
                    else:
                        df = pd.read_csv(inp+"/"+file, encoding="Latin-1", engine='python')
                        dataframes.append(df)

                        # X axis will be distance traveled from start
                        distX = df['Distance From Start (nmi)']
                        # Y axis will be altitude from ground
                        altY = df['Alt - Ground Level']
                        
                        # plot the line on the graph and add to array of all lines. Each file will be represented by 1 line
                        l, = ax1.plot(distX,altY)
                        lines1.append(l)
                        
                        # Create placeholder invisible annotations
                        annot1 = ax1.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                            bbox=dict(boxstyle="round", fc="w"),
                                            arrowprops=dict(arrowstyle="->"))
                        annot1.set_visible(False)

        if(os.path.isfile(inp)):
            # checsk for .DS_Store (mac issue)
            if inp == '.DS_Store':
                        pass
            else:
                df = pd.read_csv(inp, encoding="Latin-1", engine='python')
                dataframes.append(df)
                names = np.array(list("ABCDEFGHIJKLMNO"))

                # X axis will be distance traveled from start
                distX = df['Distance From Start (nmi)']
                # Y axis will be altitude from ground
                altY = df['Alt - Ground Level']
                
                # plot the line on the graph and add to array of all lines. Each file will be represented by a line.
                l, = ax1.plot(distX,altY)
                lines1.append(l)
                
                #Create placeholder invisible annotations
                annot1 = ax1.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="w"),
                                    arrowprops=dict(arrowstyle="->"))
                annot1.set_visible(False)

    


    # Last changes to the first figure before showing it
    fig1.canvas.mpl_connect("motion_notify_event", hover_d1)


        
    plt.title("Horizontal View")
    plt.xlabel("Distance from start (nm)")
    plt.ylabel("Altitude (ft)")
    plt.xlim([0,6])
    plt.ylim([-10,2000])


    plt.legend()


    # Beginning of figure 2's creation: Top-Down View
    fig2, ax2 = plt.subplots()
    lines2 = []

    # Creating the reference line
    # In order to make this line horizontal, we need to rotate it based on the angle between the start and runway created at the top of this page
    rX = (rLat * (np.cos(angle))) - (rLong * (np.sin(angle)))
    rY = (rLong * (np.cos(angle))) + rLat * (np.sin(angle))
    sX = (startLat * (np.cos(angle))) - (startLong * np.sin(angle))
    sY = (startLong * (np.cos(angle))) + startLat * (np.sin(angle))


    ref2X = np.array([rX,sX])
    ref2Y = np.array([rY,sY])

    # We also create a fake runway on the graph to help show how straight the landing path was
    runwayX = np.array([rX, rX, rX + 0.015, rX + 0.015, rX ])
    runwayY = np.array([rY + 0.0003, rY - 0.0003, rY - 0.0003, rY + 0.0003, rY + 0.0003])


    ax2.plot(runwayX, runwayY, 'g-', label="Runway")
    ax2.plot(ref2X, ref2Y, 'r-', label='Reference Line')


    # input variable is a list of 1 or more files and directories that we need to iterate through
    for inp in input:
        # check if item in input list is a directory
        if(os.path.isdir(inp)):    
            for subdir, dirs, files in os.walk(inp):
                # loop through all csv files in directory
                for file in files:
                    if file == '.DS_Store':
                        pass
                    else:
                        # Here we read each file in the directory and create a dotted line from start to runway to show how straight the landing pattern was
                        df = pd.read_csv(inp+"/"+file, encoding="Latin-1", engine='python')
                        names = np.array(list("ABCDEFGHIJKLMNO"))

                        latX = df['Lat']
                        longY = df['Long']

                        # Rotate each line along the angle between the start and runway to create a top-down graph
                        newX = (latX * (np.cos(angle)) - (longY * (np.sin(angle))))
                        newY = (longY * (np.cos(angle)) + latX * (np.sin(angle)))

                        l, = ax2.plot(newX, newY, '.')
                        lines2.append(l)
                        
                        # Create invisible placeholder annotations
                        annot2 = ax2.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                            bbox=dict(boxstyle="round", fc="w"),
                                            arrowprops=dict(arrowstyle="->"))
                        annot2.set_visible(False)

        if(os.path.isfile(inp)):
            if inp == '.DS_Store':
                        pass
            else:
                # Here we read each file in the input list and create a dotted line from start to runway to show how straight the landing pattern was
                df = pd.read_csv(inp, encoding="Latin-1", engine='python')

                latX = df['Lat']
                longY = df['Long']

                # Rotate each line along the angle between the start and runway to create a top-down graph
                newX = (latX * (np.cos(angle)) - (longY * (np.sin(angle))))
                newY = (longY * (np.cos(angle)) + latX * (np.sin(angle)))

                l, = ax2.plot(newX, newY, '.')
                lines2.append(l)
                
                # Create invisible placeholder annotations
                annot = ax2.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="w"),
                                    arrowprops=dict(arrowstyle="->"))
                annot.set_visible(False)
    
    # Last updates to the plot before showing it
    fig2.canvas.mpl_connect("motion_notify_event", hover_d2)

    plt.xlim([ref2X[0] - 0.1, ref2X[1] + 0.115])
    plt.ylim([ref2Y[0] - 0.005, ref2Y[1] + 0.005])
    plt.xticks([])
    plt.yticks([])
    plt.title('Top Down View')
    plt.legend()
    plt.show()
          

if __name__ == '__main__':
    # if you type --help
    parser = argparse.ArgumentParser(description="This program pre-processes flight data. It adds two new columns to the .csv file,'Altitude from ground level' and 'Distance from start(nmi)'. The default airport and runway is Boston - Logan International, runway 33. It can also show two separate graphs visualizing the landing patterns of the planes. Either -in or -v is required to run the program, other arguments are optional")

    # Commands for input, output, lat, long, and alt arguments
    # input or visualize is required, if no output is added the program will create an output directory
    # the default airport and runway is Boston - Logan International runway 33L. Alternate coordinates and altitude of a runway can be added as arguments
    parser.add_argument('-in', metavar="INPUT", nargs="+", help='input file/directory')
    parser.add_argument('-out', metavar="OUTPUT", help='output directory')
    parser.add_argument('-rlat', metavar="LATITUDE", help="Latitude of destination airport runway")
    parser.add_argument('-rlong', metavar="LONGITUDE", help="Longitude of destination airport runway")
    parser.add_argument('-slat', metavar="LATITUDE", help="Latitude of starting position")
    parser.add_argument('-slong', metavar="LONGITUDE", help="Longitude of starting position")
    parser.add_argument('-alt', metavar="ALTITUDE", help="Altitude above sea level of runway")
    parser.add_argument('-v', metavar="VISUALIZE", nargs="+", help="Shows graph of file or directory of files")

    # Get our arguments from the user
    args = vars(parser.parse_args())

    # set input as list of arguments given
    # Below allows the user to input 'output' instead of 'output.csv'... The '.csv' will be added
    input = args['in']
    if args['in'] is not None:
        for idx, inp in enumerate(input):
            l = len(inp)
            if inp[-1] == ',':
                input[idx] = inp[:l-1] 
            if(os.path.isdir(input[idx])):
                pass
            else:
                if not input[idx].endswith('.csv'):
                    input[idx] += ".csv"

    # set output
    output = args['out']

    # picks up arguments for new airport/runway
    if args['rlat'] is not None:
        rlat = args['rlat']
    if args['rlong'] is not None:
        rlong = args['rlong']
    if args['alt'] is not None:
        alt = args['alt']
    if args['rlat'] is not None:
        startLat = args['slat']
    if args['rlong'] is not None:
        startLong = args['slong']

    # set visual as list of arguments given
    # Below allows the user to input 'output' instead of 'output.csv'... The '.csv' will be added
    if args['v'] is not None:
        visual = args['v']    
        for idx, inp in enumerate(visual):
            l = len(inp)
            if inp[-1] == ',':
                visual[idx] = inp[:l-1] 
            if(os.path.isdir(visual[idx])):
                pass
            else:
                if not visual[idx].endswith('.csv'):
                    visual[idx] += ".csv"
        visualize(visual)
    
    # if output was given
    elif args['out'] is not None:
        if not os.path.isdir(output):
            os.makedirs(output)
        flight_process(input, output)
    # create output if none was given
    else:
        if not os.path.isdir('output'):
            os.makedirs('output')
        output = 'output'
        flight_process(input, output)