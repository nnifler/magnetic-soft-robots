# Manual Test for the User Story 'GUI - Select Meshes'

### Test Goal
Check whether the input in the models interface gets progressed properly so it is visible in the SOFA simulation.

### User Story
As a material science engineer, I’d like to switch between several meshes to compare my material’s behaviour on different geometries, so that I can evaluate material properties on different test subjects.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().


## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Click library button**
    1. Click the `Models` button at the top right corner.
    2. Click the `Open` button that appeared after clicking the `Models` button.
    3. Select a random model from the displayed lists.
    4. Close the popup window.
3. **Click Apply Button**
    1. Click the `Apply` button at the bottom of the GUI.

## Expected Result
The in step 2.ii selected model is shown in the SOFA GUI.
