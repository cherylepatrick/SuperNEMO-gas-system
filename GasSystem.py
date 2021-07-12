import numpy as np  #import the numpy library as np
import matplotlib.pyplot as plt #import the pyplot library as plt
import matplotlib.style #Some style nonsense
import matplotlib as mpl #Some more style nonsense

import csv # To read the input files
from datetime import datetime # To parse the dates and times

#Set default figure size
#mpl.rcParams['figure.figsize'] = [12.0, 8.0] #Inches... of course it is inches
mpl.rcParams["legend.frameon"] = False
mpl.rcParams['figure.dpi']=200 # dots per inch

# Read CSV file
with open('data/Up_Pressure_Empty_1.txt') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=';')
  line_count = 0
  #its_now= (datetime.now().strftime('%d/%m/%y %H:%M:%S.%f'))
  for row in csv_reader:
    # Parse the date to the nearest microsecond
    # looks like it's always GMT so don't worry about that
    timestamp = datetime.strptime(row[0][0:24],'%m/%d/%y %H:%M:%S.%f')
    #print(f'{timestamp}: {row[1]}')
    line_count += 1
print(f'Processed {line_count} lines.')


# Plot some crap to test matplotlib
#def true_f(x):
#  return f(x,[2.0,0.5])
#def f(x,theta):
#  return (theta[0])/(((theta[1]-x)**2)+1.0)

#fig, ax = plt.subplots()  #I like to make plots using this silly fig,ax method but plot how you like
#x=np.linspace(-10,10,100)  #Get 100 points from -10 to 10
#ax.plot(x,true_f(x),linewidth=3,label=r"True $f(\theta=[2,0.5])$")
#ax.plot(x,f(x,[1,-3]),linewidth=3,label=r'$f(\theta=[1,-3])$')
#ax.set_xlabel("x")
#ax.set_ylabel("f(x)")
#ax.legend()
#plt.savefig("test.png")


