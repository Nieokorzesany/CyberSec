#!/bin/bash -
#
# Description:
# Perform a port scan of a specified host
#
# Usage: ./scan.sh <output file>
# <output file> File to save results in
#
function scan ()
{
 host=$1
 printf '%s' "$host" 
 for ((port=1;port<1024;port++))
 do
 # order of redirects is important for 2 reasons
 echo >/dev/null 2>&1 < /dev/tcp/${host}/${port} 
 if (($? == 0)) ; then printf ' %d' "${port}" ; fi 
 done
 echo # or printf '\n'
}
#
# main loop
# read in each host name (from stdin)
# and scan for open ports
# save the results in a file
# whose name is supplied as an argument
# or default to one based on today's date
#
printf -v TODAY 'scan_%(%F)T' -1 # e.g., scan_2017-11-27 
OUTFILE=${1:-$TODAY} 
while read HOSTNAME
do
 scan $HOSTNAME
done > $OUTFILE
