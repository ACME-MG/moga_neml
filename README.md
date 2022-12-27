## Repository Structure

The following diagram shows the high level structure of the repository. 

```
neml/
├── __common__/
├── __models__/
├── optimiser/
└── surrogate/
```

## Common Directory

The `__common__` directory (`calibrate/__common__/`) contains common helper code used in the programs in the repository. Each program is contained within their own directory with a `main.py` file. Once the user has moved into the directory (via `cd`), they can make function calls in `main.py` using the provided `API` class, and run the program via `python3 main.py`.

## Optimiser

The `optimiser` directory (`calibrate/optimiser/`) contains code for optimising various creep models, with several models using [NEML](https://github.com/Argonne-National-Laboratory/neml). The following models have been developed so far.

* **Time-Hardening**, which is an empirical model for the prediction of primary creep.
* **Kachanov-Rabotnov Time-Hardening**, which couples the Time-Hardening model (primary) with the Kachanov-Rabotnov model (secondary and tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic**, which is a semi-empirical model for the prediction of primary and secondary creep.
* **Elastic Visco-Plastic Creep Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Creep Damage model (tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic Work Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Work Damage model (tertiary), to predict the entire creep life.

## Surrogate

The `surrogate` directory (`calibrate/surrogate/`) contains code for developing surrogate models for creep models, using [TensorFlow](https://www.tensorflow.org/).

To install TensorFlow, please follow the installation instructions on the [official website](https://www.tensorflow.org/install/pip).