import os
from qtgui.cli import run_gui

if __name__ == '__main__':
    # Full (absolute) path to finlandia_talo.py file
    root = os.path.dirname(__file__)
    #run_gui(os.path.join(root, "simple_scenario.py"))
    run_gui(os.path.join(root, "finlandia_talo.py"))
