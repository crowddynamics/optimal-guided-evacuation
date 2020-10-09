# optimal-guided-evacuation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3831338.svg)](https://doi.org/10.5281/zenodo.3831338)


Research code and data (for data click on DOI identifier) used in von Schantz & Ehtamo. (submitted manuscript). Minimizing the evacuation time of a crowd from a complex building using rescue guides. arXiv:2007.00509 [physics.soc-ph]. 

The paper presents a procedure for solving the minimum time evacuation from a complex building using rescue guides, and this repository is its implementation. The crowd is modeled with the physics-inspired agent-based social force model. The solution procedure is a combined numerical simulation and genetic algorithm (GA). The GA iteratively searches for the optimal evacuation plan, while the evacuation plan is evaluated with numerical simulations.

The repository includes codes for the GA, simulation and a graphical user interface (GUI). The folders in the repository:
* crowddynamics-simulation contains files for running the GUI
* crowddynamics-qtgui contains the files that build the GUI
* crowddynamics contains all files for simulating the movement of a crowd
* genetic algorithm includes files to run the genetic algorithm
* simulation files includes files specific for the simulating the conference building and hexagon-shaped area

The numerical evacuation simulations are implemented in Python and the GA is implemented as Bash scripts that were run on a high performance computing cluster. It should be noted that the procedure is currently computationally very demanding.

See the "readme.txt" file in each folder for a more detailed overview of the codes in each folder. The numerical evacuation simulation and its GUI is based on research assistant Jaan Tollander's codes https://github.com/jaantollander/crowddynamics and https://github.com/jaantollander/crowddynamics-qtgui, which he created when he was working in our research group in Aalto University School of Science, Department of Mathematics and Systems Analysis summers 2016 and 2017.

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
