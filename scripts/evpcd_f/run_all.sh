#!/bin/bash

export OMP_NUM_THREADS=1
counter=5
while [ $counter -gt 0 ]; do
    echo "run $counter"
    # nohup python3 evpcd_800_all.py &
    # nohup python3 evpcd_800_st.py &
    # nohup python3 evpcd_900_all.py &
    # nohup python3 evpcd_900_st.py &
    nohup python3 evpcd_1000_st.py &
    nohup python3 evpcd_1000_all.py &
    sleep 1
    ((counter--))
done

