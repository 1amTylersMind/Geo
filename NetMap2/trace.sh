#!/bin/bash 
if [[ $# == 2 ]]; then
    case "$1" in 
	1) 
	    echo " SingleShot Trace Started "
	    traceroute $2
	    echo "----------------TRACE-FINISHED----------------"
	    host $2
	    echo "----------------------------------------------"
	    dig $2 
	    echo "----------------------------------------------"
	    GET ipinfo.io/$2
	    echo "----------------------------------------------"
	    ;;
	2) 
	    cat $2 | while read line; do
	        traceroute $line
		echo "-----------TRACE-FINISHED------------"
		host $line
		echo "-------------------------------------"
		dig $line
		echo "-------------------------------------"
		GET ipinfo.io/$line
	    done
	    echo "DONE!"
	    paplay ~/Desktop/complete.oga
	    ;;
	*) echo "Unrecognized arguments. Sorry " ;;
    esac
else
    echo "Usage: ./traceroute.sh <IP>"
fi
#EOF
