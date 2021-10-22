# SuperNEMO-gas-system


## GasSystem.py 

Takes a file in Lauren's input format and looks for rising slopes, identifies start and end, and calculates the slope in bars/minute.

Can also take as an argument a list of files:
`usage: GasSystem.py [-h] [--list] filename`. If you choose the
`--list`    option, it will read the `filename` as the path/name of a file containing a list of datafile names (one filename/path per line), rather than an individual datafile. If not, it will look for an individual datafile formatted like this:
 ```      
10/22/21 15:10:06.0000000 GMT;0.798
10/22/21 15:10:09.0000000 GMT;0.816
10/22/21 15:10:11.0000000 GMT;0.827
```

...with date/timestamps and pressures in bars.

A file you pass with the `--list` option might look like
 ```   
data/first_datafile.txt
data/second_datafile.txt
 ```   
 Where `first_datafile.txt` and `second_datafile.txt` are in the `data` subdirectory of the directory where you're running the script, and where they are each formatted like the example shown above.
 
 ## Reformat.py
 
 Takes an input file pasted from the gasy system's Raspberry Pi command line, and reformats it to the datafile format shown above, so that it can be processed by ` `GasSystem.py`. Use it like this: ` python Reformat.py <input file> <output file>`
 
 
 
