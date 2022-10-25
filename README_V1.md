# For the  Birds!

Added a second readme we can use for us until we need the split in the venv - cost me yesterday 2 hrs to find out why Keras and Tensorflow were not working properly. 

## Requirements:

- pyenv with Python: 3.9.4

For you have not installed ntworkx do so: is used for the visuals in the baseline model: 

```BASH
pip install networkx
```

### Setup

Use the requirements file in this repo to create a new environment.

```BASH
pyenv local 3.9.8
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```
