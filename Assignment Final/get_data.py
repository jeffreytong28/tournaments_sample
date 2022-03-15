# Problem 1
import glob, csv, os

# Create overall function to read data

def read_data():
    '''Reads each yearly csv file of tennis tournaments and returns a list of
    dictionaries with each dictionary representing a row that contains
    column names as keys and corresponding values as values(strings).'''

    # Access all csv files in data folder
    files = glob.glob(os.path.join('../assignment-final-data'+'/*.csv'))

    # Read row in each file as a dictionary to data
    data = [row for file in files for row in csv.DictReader(open(file, "r"))]

    return data

data = read_data()
