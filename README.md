# optimal-guided-evacuation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3824028.svg)](https://doi.org/10.5281/zenodo.3824028)

Research code used in von Schantz & Ehtamo "Minimizing the evacuation time of a crowd from a complex building using rescue guides". The repository includes code for simulation, data analysis and visual representation of data.

Folders in the repository:
* crowddynamics-simulation contains files for running the GUI
* crowddynamics-qtgui contains the files that build the GUI
* crowddynamics contains all files for simulating the movement of a crowd
* genetic algorithm includes files to run the genetic algorithm
* simulation files includes files specific for the simulating the conference building and hexagon-shaped area

See the "readme.txt" file in each folder for a more detailed overview of the codes in each folder. The repository is based on research assistant Jaan Tollander's codes https://github.com/jaantollander/crowddynamics and https://github.com/jaantollander/crowddynamics-qtgui, which he created when he was working in our research group in Aalto University School of Science, Department of Mathematics and Systems Analysis summers 2016 and 2017.

Using Linux is recommended. The code works at least on Ubuntu 16.04. Do the following steps to install the repository:
* Install anaconda (https://docs.anaconda.com/anaconda/install/linux)
* Set environment variables `export PATH=/.../anaconda3/bin:$PATH"` and `export PYTHONPATH=/.../anaconda3/bin:$PYTHONPATH"`
* Clone the repository
* On terminal run `conda config --add channels conda-forge`
* Create a conda environment from the file *crowddynamics/environment.yml*
* On terminal run `source activate optimal-guided-evacuation`
* On terminal, in folder *crowddynamics*, run `pip install --editable .` 
* Change to folder *crowddynamics-qtgui* and run `pip install -r requirements.txt`
* Run `conda install pyqt=4`
* Run `conda install pyqtgraph==0.10.0`
* Run `conda install scikit-fmm==0.0.9`
* Run `pip install anytree==2.1.4`
* Run `pip install --editable .`

You might occur problems in installing some of the python packages. You can install these packages manually using `conda install` or `pip install`.
