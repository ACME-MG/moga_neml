# Calibrate

The repository contains code for calibrating the constitutive parameters of phenomenological creep models.

# (1) Repository Structure

The following diagram shows the high level structure of the repository. 

```
neml/
├── __common__/
├── __models__/
├── analyser/
├── optimiser/
└── surrogator/
```

# (2) Common Directory

The `__common__` directory (`calibrate/__common__/`) contains common helper code used in the programs in the repository. Each program is contained within their own directory with a `main.py` file. Once the user has moved into the directory (via `cd`), they can make function calls in `main.py` using the provided `API` class, and run the program via `python3 main.py`.

# (3) Model Directory

The `__model__` directory (`calibrate/__model__/`) contains implementations of the phenomenological models, with many of the models taken from [NEML](https://github.com/Argonne-National-Laboratory/neml). The following is a list of models that have been implemented so far.

* **Time-Hardening**, which is an empirical model for the prediction of primary creep.
* **Kachanov-Rabotnov Time-Hardening**, which couples the Time-Hardening model (primary) with the Kachanov-Rabotnov model (secondary and tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic**, which is a semi-empirical model for the prediction of primary and secondary creep.
* **Elastic Visco-Plastic Creep Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Creep Damage model (tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic Work Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Work Damage model (tertiary), to predict the entire creep life.

To install NEML, please follow the [official instructions](https://neml.readthedocs.io/en/dev/started.html). However, instead of a normal `git clone`, please clone the NEML repository recursively. In other words, use the following command to clone the NEML repository.

```
git clone --recursive https://github.com/Argonne-National-Laboratory/neml.git
```

After installing NEML using the official instructions, add NEML to the system path. You can do this by going to your home directory, adding the following line to the `.bashrc` file or the `.profile` file, and restarting the terminal.

```
export PYTHONPATH=<path_to_neml>:$PYTHONPATH
```

Please replace `<path_to_neml>` with the absolute path to the installed NEML folder.

# (4) Analyser

The `analyser` directory (`calibrate/analyser/`) contains code for analysing the phenomenological models.

# (5) Optimiser

The `optimiser` directory (`calibrate/optimiser/`) contains code for optimising various phenomenological models.

# (6) Surrogator

The `surrogator` directory (`calibrate/surrogator/`) contains code for developing surrogate models for phenomenological models, using [TensorFlow](https://www.tensorflow.org/).

To install TensorFlow, please follow the installation instructions on the [official website](https://www.tensorflow.org/install/pip).