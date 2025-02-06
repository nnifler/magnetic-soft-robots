# Manual test for the user story ‘GUI - Library Interface’

### Test Goal
Check if there is a special section in the GUI for simulation settings, where all sections for the definition of different properties (e.g. material definition, magnetic force, ...) can be easily added.

### User Story
As a user, I’d like to see a clearly defined section in the window, where I can define all the details for my simulation, so that I don’t have to write them into a messy configuration file making assumptions about everything.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]()

## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Check the behaviour of the application**
	1. Check whether a widget with the tab "Simulation Settings" opens in the interface at start 
3. **Check the console output**
	1. Ensure that no unexpected errors or warnings occur in the integrated terminal.

## Expected result
1. After starting the mainWindow.py file, a separate window with the title ‘Soft Robotic Simulation’ appears.
2. No unexpected errors or console output.
