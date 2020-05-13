Here are instructions for using the codes in the subfolders.


conference building/
If you want to simulate an evacuation from the conference building, set the files from this folder to crowddynamics/crowddynamics/simulation/


hexagon-shaped area/
If you want to simulate an evacuation from the hexagon-shaped area, set the files from this folder to crowddynamics/crowddynamics/simulation/


misc/

-"agents_initialization.py" was used to generate the fixed initial positions for the exiting agents. "feasible_regions_simple.py" was used to check which are the feasible grid cells for guides in the hexagon shaped area. "feasible_regions_conference.py" was used to check which are the feasible grid cells for guides in the conference building.

-agents_initialization_conference.npy / agents_initialization_simple.npy
Data file that includes the initial positions of the exiting agents. We need this so that the guides are not positioned so that they overlap with the exiting agents.

-finlandia_talo.py
Contains the floor of the conference building.

-simple_scenario.py
Contains the floor of the hexagon-shaped area.

