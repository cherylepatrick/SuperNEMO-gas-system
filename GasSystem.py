import numpy as np  #import the numpy library as np
import matplotlib.pyplot as plt #import the pyplot library as plt
import matplotlib.style #Some style nonsense
import matplotlib as mpl #Some more style nonsense

import csv # To read the input files
from datetime import datetime # To parse the dates and times

# Read CSV file
def parse_files(filenames):
  for filename in filenames:
  
    dict={}
    with open(filename) as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=';')
      line_count = 0
      for row in csv_reader:
        # Parse the date to the nearest microsecond
        # looks like it's always GMT so don't worry about that
        timestamp = datetime.strptime(row[0][0:24],'%m/%d/%y %H:%M:%S.%f')
        dict[timestamp]=row[1] #Hopefully this deals with deduplicating
        line_count += 1
      print(f'{filename} contained {line_count} lines.')
      lists = sorted(dict.items()) # sorted by key, return a list of tuples
      timestamps, values = zip(*lists) # unpack a list of pairs into two tuples

      ax.plot(timestamps, values,label=filename)
  return #dict

#Set default figure size
#mpl.rcParams['figure.figsize'] = [12.0, 8.0] #Inches... of course it is inches
mpl.rcParams["legend.frameon"] = False
mpl.rcParams['figure.dpi']=200 # dots per inch

fig, ax = plt.subplots()
 # Read all CSV files to a dictionary of timestamp vs. value
 # That should deduplicate, so the individual totals don't necessarily add up to the final total
input_files=['data/Up_Pressure_Filled_2.txt','data/Up_Pressure_Filled_1.txt','data/Up_Pressure_Empty_1.txt','data/Up_Pressure_Empty_2.txt']
dict=parse_files(input_files)

#print(f'Dictionary contains {len(dict)} entries')


ax.set_xlabel("Timestamp")
ax.set_ylabel("Value")
ax.legend()
plt.savefig("test.png")



