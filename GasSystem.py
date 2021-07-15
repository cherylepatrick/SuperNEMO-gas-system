import numpy as np  #import the numpy library as np
import matplotlib.pyplot as plt #import the pyplot library as plt
import matplotlib.style #Some style nonsense
import matplotlib as mpl #Some more style nonsense
from scipy import stats

import csv # To read the input files
from datetime import datetime # To parse the dates and times


mpl.rcParams["legend.frameon"] = False
mpl.rcParams['figure.dpi']=200 # dots per inch


def parse_files(filenames):
  """
  Takes a list of paths to CSV files in gas system format.
  Reads the files and returns a dictionary of timestamp to pressure.
  If there are multiple records for the same time, it will overwrite.
  """
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

def plot(dict, output_filename):
  """
  Takes a dictionary of timestamps vs pressures and plots it
  """
  lists = sorted(dict.items()) # sorted by key, return a list of tuples
  timestamps, values = zip(*lists) # unpack a list of pairs into two tuples
  fig, ax = plt.subplots()
  ax.plot(timestamps, values)
  ax.set_xlabel("Timestamp")
  ax.set_ylabel("Pressure")
  plt.savefig(output_filename+".png")


def is_slope_start (values, pos):
  """
  Is this position in list of values the first in an increasing slope?
  Return true if yes
  """
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

def is_slope_end (values, pos):
  """
  Is this position in list of values the start of a plateau/downwards slope?
  Return true if yes
  """
  # We can refine this later, for now I am going to say:
  # - 1) This value is greater than or equal to the next
  # - 2) from this point, the average of readings 0-2 >= 1-3 >= 2-4
  if pos + 5 > len(values):
    return False # No room for this kerfuffle
  if values[pos] < values[pos+1]: return False # condition 1
  if (np.mean(values[pos:pos+2]) < np.mean(values[pos+1:pos+3]) and
      np.mean(values[pos+1:pos+3]) < np.mean(values[pos+2:pos+4])): return False
  return True

def calculate_slope(timestamps, values, start_pos, end_pos):
  """
  Calculate the slope of a pressure (y axis) vs timestamp (x axis)
  pair of arrays, between specified start and end positions in the array
  """
  # start_pos corresponds to the last entry before the slope begins
  # end_pos is the last entry before it flattens
  # to make sure we're only fitting the sloping part, fit between
  # start_pos+1 and end_pos
  timestamp_subset = timestamps[start_pos+1:end_pos+1]
  x=[]
  for ts in timestamp_subset:
    x.append(ts.timestamp())
  y = values[start_pos+1:end_pos+1]
  slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
  return slope * 60 # convert to bars per minute (from per second)

def find_next_slope(timestamps, values, position):
  """
  Find the start time, end time, and slope of the next rising slope after
  the specified position in the array of timestamps (x) vs pressures (y)
  """
  current_pos = position
  list_length=len(values)
  while current_pos < list_length:
    if is_slope_start(values, current_pos):
      new_pos = find_slope_end(values, current_pos)
      # current_pos is the entry BEFORE the rise
      # new_pos is the last entry in the rise
      # Calculate the slope between them
      slope = calculate_slope(timestamps, values, current_pos, new_pos)
      return new_pos, timestamps[current_pos], timestamps[new_pos], slope
    else:
      current_pos +=1
  return -999, timestamps[-1], timestamps[-1], 0 #Return value -999 means STOP
 

def find_slope_end(values, position):
  """
    Get the position of the end of the slope in progress
  """
  current_pos = position
  list_length=len(values)
  while current_pos < list_length:
    if is_slope_end(values, current_pos):
      return current_pos
    else:
      current_pos +=1
  return list_length
 
 
def find_slopes(dict):
  """
    Get a list of all rising slopes found in the dataset of
    timestamps (x) vs pressures (y)
  """
  slopes = []
  # Sort the value/timestamp pairs by time
  lists = sorted(dict.items())
  timestamps, values = zip(*lists)
  list_position = 0 # Start at the beginning of the list

  # Keep looking for slopes, if we don't find one, return -999 (so we don't just add 1 to it and end up back at the start!)
  while list_position >= 0:
    list_position, start_time, end_time, slope  = find_next_slope(timestamps,values,list_position)
    if list_position >=0:
      print (f'Ramp of {slope:.3} bar/min from {start_time.strftime("%d/%m %H:%M:%S")} to {end_time.strftime("%H:%M:%S")}')

    list_position +=1
    slopes.append(slope)
  return slopes


# Main function
# Read all CSV files to a dictionary of timestamp vs. value
# That should deduplicate, so the individual totals don't necessarily add up to the final total
input_files=['data/Up_Pressure_Empty_1.txt',
    'data/Up_Pressure_Empty_2.txt',
    'data/Up_Pressure_Filled_1.txt',
    'data/Up_Pressure_Filled_2.txt']
dict=parse_files(input_files) # Read file contents into dictionary of timestamps and pressures
plot (dict,'pressures') # Plot them
find_slopes(dict) # Extract a list of slopes






