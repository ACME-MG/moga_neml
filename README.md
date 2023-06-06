# Introduction (Calibrate)

The repository contains code for calibrating the constitutive parameters of phenomenological creep models. The following README was last updated on the 6th of June, 2023.

# Dependencies

The following section details the requirements to run the script.

## NEML

NEML (Nuclear Engineering Material model Library) is a tool for developing / running structural material models. To install NEML, please follow the [official instructions](https://neml.readthedocs.io/en/dev/started.html). However, instead of a normal `git clone`, please clone the NEML repository recursively. In other words, use the following command to clone the NEML repository.
```
$ git clone --recursive https://github.com/Argonne-National-Laboratory/neml.git
```

For multi-threading capabilities, use the following configurations when running `cmake`.
```
$ cmake -D WRAP_PYTHON=ON -D USE_OPENMP=ON .
```

After installing NEML using the official instructions, add NEML to the system path. You can do this by going to your home directory, adding the following line to the `.bashrc` file or the `.profile` file, and restarting the terminal.
```
$ export PYTHONPATH=<path_to_neml>:$PYTHONPATH
```

Please replace `<path_to_neml>` with the absolute path to the installed NEML folder.

## Python Packages

The scripts also require several Python packages. To install these packages, `pip` is required. If you do not have `pip` installed, please following [these instructions](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/).

* Numpy (`pip install numpy`).
* Pandas (`pip install pandas`) for creating and manipulating Excel files.
* PyMOO (`pip install pymoo`) for parameter optimisation.
* XLSXWriter (`pip install xlsxwriter`) for creating Excel files to store results.