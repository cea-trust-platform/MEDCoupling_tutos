# MEDCoupling Tutorials

This git repository contains python tutorials and scripts illustrating the use
of the MEDCoupling library.

You can find in the "tutorials" folder some tutorials and explanations for
several topics. Jupyter-lab should be used for ipynb extension files.

# Set runtime environment

Working in a MEDCoupling environment is required. For that, you should do the
following:

- For a `TRUST` user:

  ```bash
  source env_for_python.sh
  ```

- For a `Salome` user:

  ```bash
  salome context
  ```

- Installing other python packages:

  The recommended way to install new packages is to create a virtual
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

# Check environnement and all notebooks

To check all notebooks are running after initializing the environment please run:

```bash
source venv/bin/activate
pip install -r requirements-dev.txt
pytest --nbval
```

# Run a tutorial

- Activate the MEDCoupling environment
- `cd tutorials`
- Launch `jupyter-notebook` or `jupyter-lab`
- Enjoy MEDCoupling !
