#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Missing path to network config file"
    exit 1
fi

echo "Press 'q' to stop"

./start_network_runner.sh &
network_runner=$!
sleep 2
../testbed/testbed $1 &
testbed=$!
#echo $network_runner
#echo $$

while : ; do
read -n 1 key <&1
if [[ $key = q ]] ; then
printf "\nHalting Experiment\n"
break
elif [[ $key = x ]] ; then
printf "\nExiting without stopping\n"
exit 0
fi
done

kill -TERM $network_runner
kill -TERM $(($network_runner+1))
kill -9 $testbed