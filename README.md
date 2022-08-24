![Timbr logo description](Timbr_logo.png)

# timbr Python connector sample file
This is a sample repository for how to connect to timbr using SQLAlchemy and Python.

## Dependencies
- Access to a timbr-server
- Python from 3.7.13 or newer

## Installation
- Install Python: https://www.python.org/downloads/release/python-3713/
- Run the following command to install the Python dependencies: `pip install -r requirements.txt`

## Sample usage
- For an example of how to use the Python connector for timbr, follow this [example file](example.py) 

## Known issues
If you encounter a problem installing `PyHive` with sasl dependencies on windows, install the following wheel (for 64bit Windows) by running:

`pip install https://download.lfd.uci.edu/pythonlibs/archived/cp37/sasl-0.3.1-cp37-cp37m-win_amd64.whl`

