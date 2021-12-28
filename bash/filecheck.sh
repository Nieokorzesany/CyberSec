SYSNAME="$(uname -n)_$(date +'%m_%d_%Y')" ; sudo find / -type f | xargs -d '\n' sha1sum > ${SYSNAME}_baseline.txt 2>${SYSNAME}_error.txt
