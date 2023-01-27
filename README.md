# Calibrate

The repository contains code for calibrating the constitutive parameters of phenomenological creep models.

# Dependencies

The code relies on several libraries to work.

### NEML

NEML (Nuclear Engineering Material model Library) is a tool for developing / running structural material models. To install NEML, please follow the [official instructions](https://neml.readthedocs.io/en/dev/started.html). However, instead of a normal `git clone`, please clone the NEML repository recursively. In other words, use the following command to clone the NEML repository.

```
git clone --recursive https://github.com/Argonne-National-Laboratory/neml.git
```

After installing NEML using the official instructions, add NEML to the system path. You can do this by going to your home directory, adding the following line to the `.bashrc` file or the `.profile` file, and restarting the terminal.

```
export PYTHONPATH=<path_to_neml>:$PYTHONPATH
```

Please replace `<path_to_neml>` with the absolute path to the installed NEML folder.

### PyPI Libraries

In addition to NEML, the code in the repository also relies on several Python libraries that can be installed via `pip`.

* Pandas (`pip3 install pandas`) for creating and manipulating Excel files.
* PyMOO (`pip3 install pymoo`) for parameter optimisation.
* XLSXWriter (`pip3 install xlsxwriter`) for creating Excel files to store results.

# Repository Structure

The following diagram shows the high level structure of the repository. 

```
neml/
├── __common__/
├── __models__/
├── analyser/
├── optimiser/
└── surrogator/
```

# Common

The `__common__` directory (`calibrate/__common__/`) contains common helper code used in the programs in the repository. Each program is contained within their own directory with a `main.py` file. Once the user has moved into the directory (via `cd`), they can make function calls in `main.py` using the provided `API` class, and run the program via `python3 main.py`.

# Models

The `__models__` directory (`calibrate/__models__/`) contains implementations of the phenomenological models, with many of the models taken from [NEML](https://github.com/Argonne-National-Laboratory/neml). The following is a list of models that have been implemented so far.

* **Time-Hardening**, which is an empirical model for the prediction of primary creep.
* **Kachanov-Rabotnov Time-Hardening**, which couples the Time-Hardening model (primary) with the Kachanov-Rabotnov model (secondary and tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic**, which is a semi-empirical model for the prediction of primary and secondary creep.
* **Elastic Visco-Plastic Creep Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Creep Damage model (tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic Work Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Work Damage model (tertiary), to predict the entire creep life.

# Analyser

The `analyser` directory (`calibrate/analyser/`) contains code for analysing the phenomenological models.

# Optimiser

The `optimiser` directory (`calibrate/optimiser/`) contains code for optimising various phenomenological models.

# Surrogator

The `surrogator` directory (`calibrate/surrogator/`) contains code for developing surrogate models for phenomenological models, using [TensorFlow](https://www.tensorflow.org/).

To install TensorFlow, please follow the installation instructions on the [official website](https://www.tensorflow.org/install/pip).