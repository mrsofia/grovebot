#!/bin/bash

# cd to repository
cd {your/repo}

git reset --hard HEAD # discard local changes

git pull origin master # pull new changes

# find last created  PID from file and kill it
while  read -r line || [[ -n "$line" ]]; do
     echo "attempting to kill process id: $line"
 kill -9 $line
done < "../grovebot/PID"
echo "kill successful or no such process was found"


# delete any existing PID_last files
if [ -e ../grovebot/PID_last ] ; then
 echo "removing old PID_last"
 rm -f ../grovebot/PID_last
fi

# rename old PID file for debug purposes
if [ -e PID ] ; then
 echo "changing old PID to PID_last"
 mv PID PID_last
fi

echo "starting bot..."

nohup python3 Main.py > /dev/null 2>&1 & echo $! > PID

echo "bot started."

echo "done"

