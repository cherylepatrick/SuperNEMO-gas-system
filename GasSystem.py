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

def is_slope_start (values, pos):
  # We can refine this later, for now I am going to say:
  # - 1) This value must be less than the next value
  # - 2) The average of this value and the next 4 must be less than the
  #   average of the following 5 values
  # - 3) from this point, the average of readings 0-2 < 1-3 < 2-4
  if pos + 10 > len(values):
    return False # No room for this kerfuffle
  if values[pos] >= values[pos+1]: return False # condition 1
  if np.mean(values[pos:pos+4]) >= np.mean(values[pos+5:pos+9]): return False
  if np.mean(values[pos:pos+2]) >= np.mean(values[pos+1:pos+3]): return False
  if np.mean(values[pos+1:pos+3]) >= np.mean(values[pos+2:pos+4]): return False
  return True

def find_next_slope(timestamps, values, position):
  current_pos = position
  list_length=len(values)
  while current_pos < list_length:
    if is_slope_start(values, current_pos):
      return current_pos, timestamps[current_pos], timestamps[-1], 0
    else:
      current_pos +=1
  return -2, timestamps[-1], timestamps[-1], 0
      

def find_slopes(dict):
  slopes = []
  # Sort the value/timestamp pairs by time
  lists = sorted(dict.items())
  timestamps, values = zip(*lists)
  list_position = 0 # Start at the beginning of the list

  # Keep looking for slopes, if we don't find one, return -2
  while list_position >= 0:
    list_position, start_time, end_time, slope  = find_next_slope(timestamps,values,list_position)
    print (f'Position is {list_position}')
    list_position +=1
    print (f'Slope found at {start_time}')
    return
  return slopes

 # Read all CSV files to a dictionary of timestamp vs. value
 # That should deduplicate, so the individual totals don't necessarily add up to the final total
input_files=['data/Up_Pressure_Empty_1.txt',
    'data/Up_Pressure_Empty_2.txt',
    'data/Up_Pressure_Filled_1.txt',
    'data/Up_Pressure_Filled_2.txt']
dict=parse_files(input_files)
plot (dict,'pressures')
find_slopes(dict)






