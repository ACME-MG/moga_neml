#!/bin/bash

export OMP_NUM_THREADS=1
nohup python3 evpwdb_800_all.py &
nohup python3 evpwdb_800_st.py &
nohup python3 evpwdb_900_all.py &
nohup python3 evpwdb_900_st.py &
# nohup python3 evpwd_1000_st.py &
# nohup python3 evpwd_1000_all.py &
