#!/bin/bash

export OMP_NUM_THREADS=1

counter=10
while [ $counter -gt 0 ]; do
    echo "run $params ($counter)"
    nohup python3 evpwd_800_st.py $params &
    nohup python3 evpwd_900_st.py $params &
    nohup python3 evpwd_1000_st.py $params &
    sleep 1
    ((counter--))
done

