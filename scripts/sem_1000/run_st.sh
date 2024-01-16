#!/bin/bash

export OMP_NUM_THREADS=1
counter=10
while [ $counter -gt 0 ]; do
    echo "run $counter"
    nohup python3 evp_1000_st.py &
    sleep 1
    ((counter--))
done

