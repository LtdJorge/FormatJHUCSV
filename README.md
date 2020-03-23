# FormatJHUCSV
I created this script to reformat the Coronavirus CSV files that JHU is uploading into a layout that can be easily understood by other tools.
It basically creates a row for each date, which contains the 'State', 'Country', 'Lat', 'Long', 'Date' and 'People count' values.

I made this so I could easily parse the files with Logstash for sending it to Elasticsearch, as manipulating the columns with Logstash itself is between difficult and impossible.

## How to run it
```
$ python formatcsv.py <folder with the original .csv files>
```
It will search for the original files (don't rename them) and create the new ones with the same name but "formatted-" prepended.
