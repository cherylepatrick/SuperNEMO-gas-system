# Reformat a paste from the Gas system raspberry pi command line
# to the format the fitter understands
import sys
from datetime import datetime # To parse the dates and times


def reformat(input_file, output_file):
  input = open(input_file, 'r')
  output = open(output_file, 'w+')
  lines = input.readlines()
  count=0
  timetext=""
  for line in lines:
    if line.find("Current Pressure") >=0:
      count+=1
      words=line.split(" ")
      timetext=words[0]+" "+words[1]
      timestamp = datetime.strptime(timetext,'%d/%m/%Y %H:%M:%S')
      newtext = timestamp.strftime('%m/%d/%y %H:%M:%S.%f0 GMT;'+words[-1])
      if count==1:
        firsttext=timetext
      output.write(newtext)
  input.close()
  output.write("\n")
  print(count, "lines written to", output_file)
  print("Data covers",firsttext,"to",timetext)
  output.close()

# Main function
# Read all CSV files to a dictionary of timestamp vs. pressure
# That should deduplicate, so the individual totals don't necessarily add up to the final total
if len(sys.argv) !=3:
  print("usage: python Reformat.py <input file> <output file>")
  sys.exit()
print("Reformatting ",sys.argv[1])
reformat(sys.argv[1], sys.argv[2])

