#!/bin/bash
#Progress bar with a For Loop
 
#Bar
BAR='##########'
 
for COUNTER in {1..10}
do
#Print the bar progress starting from the zero index
echo -ne "\r${BAR:0:$COUNTER}"
#Sleep for 1 second
sleep 1
done
