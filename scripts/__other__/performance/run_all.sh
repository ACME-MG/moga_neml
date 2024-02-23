#!/bin/bash

model_index=1
nohup python3 plot_perf.py 0 $model_index &
nohup python3 plot_perf.py 1 $model_index &
nohup python3 plot_perf.py 2 $model_index &
nohup python3 plot_perf.py 3 $model_index &
nohup python3 plot_perf.py 4 $model_index &
nohup python3 plot_perf.py 5 $model_index &
