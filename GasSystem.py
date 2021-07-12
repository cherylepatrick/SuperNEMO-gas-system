import numpy as np  #import the numpy library as np
import matplotlib.pyplot as plt #import the pyplot library as plt
import matplotlib.style #Some style nonsense
import matplotlib as mpl #Some more style nonsense

mpl.rcParams["legend.frameon"] = False
mpl.rcParams['figure.dpi']=200 # dots per inch


import csv # To read the input files
from datetime import datetime # To parse the dates and times

# Read timestamps / pressures from CSV files and return as a dictionary
# Takes a list of filenames, reads the lot, deduplicates as necessary
# (If two entries for the same time, it will use the latest)
def parse_files(filenames):
  dict={}
  for filename in filenames:
    with open(filename) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=';')
      line_count = 0
      for row in csv_reader:
        # Parse the date to the nearest microsecond
        # looks like it's always GMT so don't worry about that
        timestamp = datetime.strptime(row[0][0:24],'%m/%d/%y %H:%M:%S.%f')
        dict[timestamp]=float(row[1]) #Hopefully this deals with deduplicating
        line_count += 1
      print(f'{filename} contained {line_count} lines.')

  print(f'Total: {len(dict)} readings')
  return dict

# Takes a dictionary of timestamps vs pressures and plots it
def plot(dict, output_filename):
  lists = sorted(dict.items()) # sorted by key, return a list of tuples
  timestamps, values = zip(*lists) # unpack a list of pairs into two tuples
  fig, ax = plt.subplots()
  ax.plot(timestamps, values)
  ax.set_xlabel("Timestamp")
  ax.set_ylabel("Pressure")
  plt.savefig(output_filename+".png")

def find_slopes(dict):
  slopes = []
  return slopes

 # Read all CSV files to a dictionary of timestamp vs. value
 # That should deduplicate, so the individual totals don't necessarily add up to the final total
input_files=['data/Up_Pressure_Empty_1.txt',
    'data/Up_Pressure_Empty_2.txt',
    'data/Up_Pressure_Filled_1.txt',
    'data/Up_Pressure_Filled_2.txt']
dict=parse_files(input_files)
plot (dict,'pressures')






