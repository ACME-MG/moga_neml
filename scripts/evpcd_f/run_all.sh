#!/bin/bash

export OMP_NUM_THREADS=1
counter=10
while [ $counter -gt 0 ]; do
    echo "run $counter"
    nohup python3 evpcd_800_st.py &
    nohup python3 evpcd_900_st.py &
    nohup python3 evpcd_1000_st.py &
    sleep 1
    ((counter--))
done

