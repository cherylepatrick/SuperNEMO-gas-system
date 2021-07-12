import numpy as np  #import the numpy library as np
import matplotlib.pyplot as plt #import the pyplot library as plt
import matplotlib.style #Some style nonsense
import matplotlib as mpl #Some more style nonsense

import csv # To read the input files
from datetime import datetime # To parse the dates and times

# Read CSV file
def parse_file(filename,dict):
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
  return dict

#Set default figure size
#mpl.rcParams['figure.figsize'] = [12.0, 8.0] #Inches... of course it is inches
mpl.rcParams["legend.frameon"] = False
mpl.rcParams['figure.dpi']=200 # dots per inch


dict={} # Create an empty dictionary
parse_file('data/Up_Pressure_Empty_1.txt',dict)


print(f'Dictionary contains {len(dict)} entries')

lists = sorted(dict.items()) # sorted by key, return a list of tuples

timestamps, values = zip(*lists) # unpack a list of pairs into two tuples
fig, ax = plt.subplots()
ax.plot(timestamps, values)
ax.set_xlabel("Timestamp")
ax.set_ylabel("Value")
plt.savefig("test.png")



