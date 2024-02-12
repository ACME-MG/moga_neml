#!/bin/bash

export OMP_NUM_THREADS=1
params=0
while [ $params -lt 10 ]; do
    counter=10
    while [ $counter -gt 0 ]; do
        echo "run $params ($counter)"
        # nohup python3 evpwdb_800_st.py $params &
        # nohup python3 evpwdb_900_st.py $params &
        nohup python3 evpwdb_1000_st.py $params &
        sleep 1
        ((counter--))
    done
    ((params++))
done

