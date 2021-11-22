# Plot temperature from one of the files in TemperatureLogs directory on raspberry pi
# C Patrick Nov 2021
# Read the contents of one of those files and plot temperature vs time
# Probably best to grep for about a day's data and plot that

import argparse
import sys
import numpy as np  #import the numpy library as np
import matplotlib.pyplot as plt #import the pyplot library as plt
import matplotlib.style #Some style nonsense
import matplotlib.dates as dates
import time
import matplotlib as mpl #Some more style nonsense
from scipy import stats
from scipy.optimize import curve_fit

import csv # To read the input files
from datetime import datetime # To parse the dates and times


mpl.rcParams["legend.frameon"] = False
mpl.rcParams['figure.dpi']=200 # dots per inch


def parse_files(filenames):
  """
  Takes a list of paths to CSV files in gas system format.
  Reads the files and returns a dictionary of timestamp to temperature
  If there are multiple records for the same time, it will overwrite.
  """
  dict={}
  first=""
  last=""
  for filename in filenames:
    with open(filename) as csv_file:
      line_count = 0
      for row in csv_file:
        # Parse the date to the nearest microsecond
        # looks like it's always GMT so don't worry about that
        timestamp = datetime.strptime(row[11:36],'%Y-%m-%d %H:%M:%S.%f')
        dict[timestamp]=float(row[47:52]) #Hopefully this deals with deduplicating
        line_count += 1
  print(f'Total: {len(dict)} readings')
  return dict

def plot(dict, output_filename):
  """
  Takes a dictionary of timestamps vs temperatures and plots it
  """
  lists = sorted(dict.items()) # sorted by key, return a list of tuples
  timestamps, temps = zip(*lists) # unpack a list of pairs into two tuples
  first=timestamps[0].strftime('%d/%m/%Y %H:%M:%S')
  last=timestamps[-1].strftime('%d/%m/%Y %H:%M:%S')
  print(f'Time range {first} to {last}')
  fig, ax = plt.subplots()
  ax.plot(timestamps, temps)
  #Dubious attempt to make the axis labels legible
  interval_hours=6
  if (len(dict)<250):
    interval_hours=1
  elif (len(dict)<500):
    interval_hours=2
  elif (len(dict)<1000):
    interval_hours=4
    
  ax.xaxis.set_minor_locator(dates.HourLocator(interval=interval_hours))   # every ? hours
  ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))  # hours and minutes
  ax.xaxis.set_major_locator(dates.DayLocator(interval=1))    # every day
  ax.xaxis.set_major_formatter(dates.DateFormatter('\n%d/%m/%Y'))
  ax.set_ylabel("Temperature (Celsius)")
  plt.savefig(outfile)

def fit_func(x, a,b,c):
    return  a*x*x + b*x + c

def fit(dict):
  lists = sorted(dict.items()) # sorted by key, return a list of tuples
  datetimes, temps = zip(*lists) # unpack a list of pairs into two tuples
  timestamps=[dt.timestamp() for dt in datetimes]
  #endtime=datetime.now().timestamp()
  #print (datetime.now().timestamp())
  endtime=datetime(2021, 11, 22,9).timestamp()
  #endtime=datetime.now().timestamp()
  #print(endtime)
  popt,pcov = curve_fit(fit_func, timestamps, temps)
  print (popt[0]*endtime*endtime+ popt[1]*endtime +popt[2])


def fit2(dict):
  lists = sorted(dict.items()) # sorted by key, return a list of tuples
  datetimes, temps = zip(*lists) # unpack a list of pairs into two tuples
  timestamps=[dt.timestamp() for dt in datetimes]
  #endtime=datetime.now().timestamp()
  endtime=datetime(2021, 11, 22,9).timestamp()

  p = np.polyfit(timestamps, temps,4)

  print (p[0]*endtime**4 + p[1]*endtime**3 + p[2]*endtime**2 + p[3]*endtime**1 + p[4] )



# Main function
# Read all CSV files to a dictionary of timestamp vs. temperature
# That should deduplicate, so the individual totals don't necessarily add up to the final total
# Allow a single datafile name, or a file containing a list of data files


parser = argparse.ArgumentParser(description='Plot time vs temperature from the TemperatureLogs files on the gas system, in 2-hour intervals')
parser.add_argument('filename',
                    help='Datafile path/name (or file containing list of names)')
parser.add_argument('--list', dest='filelist', action='store_const',
const=True, default=False,
                    help='Process a file containing a list of datafile names, rather than an individual datafile')

args = parser.parse_args()

input_files=[]
if (args.filelist): # Input filename is a file containing a list of paths/names of individual datafiles
  with open(args.filename) as file_in:
    for line in file_in:
        input_files.append(line. rstrip("\n"))
  file_in.close()
else:
  input_files.append(args.filename) # Just process a single datafile
if (args.filelist):
  outfile='temperatures.png'
else:
  outfile = args.filename[:-4]+".png"

dict=parse_files(input_files) # Read file contents into dictionary of timestamps and pressures
plot (dict,outfile) # Plot them

