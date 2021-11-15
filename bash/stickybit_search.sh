#!/bin/bash

find / -perm -u=s -type f 2>/dev/null
find / -user root -perm -6000 -type f 2>/dev/null
