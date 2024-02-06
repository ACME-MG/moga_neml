#!/bin/bash

nohup python3 combiner.py "creep" 800 &
nohup python3 combiner.py "creep" 900 &
nohup python3 combiner.py "creep" 1000 &
nohup python3 combiner.py "tensile" 800 &
nohup python3 combiner.py "tensile" 900 &
nohup python3 combiner.py "tensile" 1000 &
