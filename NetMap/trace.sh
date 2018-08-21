#!/bin/bash 
touch trace.txt 
echo 'Enter IP to Trace:'
read input
echo 'Starting Virtual Trace...'
traceroute $input > trace.txt 
touch tracer.txt
touch geodmp.txt
javac TextFileReader.java 
java TextFileReader -trace trace.txt > tracer.txt 
# Now get Geo IP data 
cat tracer.txt | while read line 
do 
    python PhysicalTracer.py -geo $line >> geodmp.txt 
    sleep 1
done
cat geodmp.txt
# Log all the Geo_IP Data for later analysis 
cat geodmp.txt >> geoip_history.txt
# Parse the geo location data, create graphs 
java TextFileReader -geo geodmp.txt
rm geodmp.txt
rm trace.txt 
rm tracer.txt 
# Also grab the human readable name of the inital request
host $input

