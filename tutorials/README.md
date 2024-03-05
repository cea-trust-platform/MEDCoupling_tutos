# Introduction

This repository contains python tutorials and scripts illustrating the use of the `MEDCoupling` library.
The tutorials are python Notebooks (`.ipynb` extension).  They cover several topics, from simple use of fundamental types, such as the `DataArray`, up to complete studies, such as the `RJH` tutorial.

Additional resource is [available online](https://docs.salome-platform.org/latest/dev/MEDCoupling/tutorial/index.html) and on the `SALOME` platform, at `Help > User's guide > Fields module > MEDCoupling > Tutorial`.

# Environment

The `LD_LIBRARY_PATH` and the `PYTHONPATH` environment variables must be set correctly, in order to use the `MEDCoupling` library.
Assuming that `MEDCoupling` has been installed at `<MC_INSTALL>/`:

- `LD_LIBRARY_PATH=...:<MC_INSTALL>/lib`
- `PYTHONPATH=...:<MC_INSTALL>/lib/<python?.??>/site-packages`

where `<python?.??>` depends on your local python interpreter version. For instance, it may be `python3.10`.

For users of the `SALOME` platform, those environment variables can be set automatically with the command:

```sh
salome context
```

For users of the `TRUST` platform, those environment variables can be set automatically with the command:

```sh
source env_for_python.sh
```

# Running a tutorial

Once your environment is correctly set (see **Environment** section above), any tutorial can be run by opening the corresponding `.ipynb` file.
This file can be openned in any notebook reader (e.g. `VSCode`, `Jupyter Notebook`, or the `Python Notebook Viewer` Firefox extension).
