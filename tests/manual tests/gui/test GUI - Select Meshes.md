# Manual Test for the User Story 'LINK - SOFA Interface'

### Test Goal
Check whether the user inputs via the GUI get processed correctly, are added to the config class and the Sofa simulation can be started from the GUI.

### User Story
As any user, I’d like to see the changes I set in the GUI take effect on the simulation.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().


## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Click library button**
    1. Click the `Models` button at the top right corner.
    2. Select a random model in the list.
    3. Close the popup window.
3. **Click Apply Button**
    1. Click the `Apply` button at the bottom of the GUI.

## Expected Result
The in step 2.2 selected model is shown in the SOFA GUI.