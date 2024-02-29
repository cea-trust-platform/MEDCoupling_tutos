# MEDCoupling Tutorials

This git repository contains python tutorials and scripts illustrating the use
of the MEDCoupling library.

You can find in the "tutorials" folder some tutorials and explanations for
several topics. Jupyter-lab should be used for ipynb extension files.

Additional resource is [available online](https://docs.salome-platform.org/latest/dev/MEDCoupling/tutorial/index.html)
and on the `SALOME` platform, at `Help > User's guide > Fields module > MEDCoupling > Tutorial`.

# Set runtime environment

## MEDCoupling environment

Working in a MEDCoupling environement is required. For that, you should do the
following:

- For a `TRUST` user:

  ```bash
  source env_for_python.sh
  ```

- For a `Salome` user:

  ```bash
  salome context
  ```

- Environment variables:

  The `LD_LIBRARY_PATH` and the `PYTHONPATH` environment variables must be set
  correctly, in order to use the `MEDCoupling` library.
  Assuming that `MEDCoupling` has been installed at `<MC_INSTALL>/`:

  - `LD_LIBRARY_PATH=...:<MC_INSTALL>/lib`
  - `PYTHONPATH=...:<MC_INSTALL>/lib/<python?.??>/site-packages`

  where `<python?.??>` depends on your local python interpreter version. For
  instance, it may be `python3.10`.

## Extending the environment

- Installing other python packages:

  The recommanded way to install new packages is to create a virtual
  environment. The downside is that it will hide all system packages by
  default. To install it run:

  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -U pip
  pip install mynewpypackage
  ```

  As system packages will be hidden, in some configurations (native
  medcoupling/salome), numpy and scipy need to be installed in this
  environment. A `requirements.txt` file is provided which lists needed
  packages:

  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

# Check environment and all notebooks

To check all notebooks are running after initializing the environment please run:

```bash
source venv/bin/activate
pip install -r requirements-dev.txt
pytest --nbval
```

# Run a tutorial

- Activate the MEDCoupling environement
- Source the extending python virtual environment
- cd tutorials
- Launch jupyter-notebook/jupyter-lab/VSCode
