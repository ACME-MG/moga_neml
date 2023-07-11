# MOGA NEML

The repository contains code for calibrating the constitutive parameters of phenomenological creep models. The code combines the multi-objective genetic algorithm (MOGA) implemented in Pymoo with the nuclear engineering material model library (NEML). The following README was last updated on the 27th of June, 2023.

# Dependencies

The following section details the requirements to run the script.

## NEML

NEML is a tool for developing / running structural material models. To install NEML for this repository, please follow the instructions below. Note that these instructions are slightly modified from the [official instructions](https://neml.readthedocs.io/en/dev/started.html).

To install NEML, first clone the repository recursively using the following command.
```
git clone --recursive https://github.com/Argonne-National-Laboratory/neml.git
```

Then, move into the NEML directory and compile NEML using `cmake` and `make`.
```
cd neml
cmake -D WRAP_PYTHON=ON -D USE_OPENMP=ON -D CMAKE_BUILD_TYPE=Release .
make -j 2
```

After installing NEML, add NEML to the system path. You can do this by going to your home directory, adding the following line to the `.bashrc` file. Note that `<path_to_neml>` refers to the absolute path to the installed NEML directory.
```
export PYTHONPATH=$PYTHONPATH:<path_to_neml>
```

Make sure to source the `.bashrc` file or restart the terminal, so that NEML is added to the system path properly.

## Python Packages

The scripts also require several Python packages.

To install these packages, `pip` is required.

If you do not have `pip` installed, please following [these instructions](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/).

Once `pip` is installed, you can run `pip3 install -r requirements.txt` from the directory to install the Python packages.