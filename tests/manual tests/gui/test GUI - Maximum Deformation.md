# Manual test for the user story 'GUI - Maximum Deformation'

### Test Goal
Check if there is a way to enable the maximum deformation analysis tool and change the parameters needed to perform the analysis.

### User Story
As a user, I want to be able to easily enable the maximum deformation analysis tool and choose the points I want to analyse.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]()

## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Open the analysis tab**
    1. Click on the tab `Analysis Settings`
    2. Check if a section named `Maximum Deformation Analysis` is present
3. **Check disabled status**
    1. Ensure that the checkbox `Enable Deformation Analysis` is not checked
    2. Check if all other radio buttons (`Indices`, `Coordinates`, `All Points`) do not react to interacting with them
    3. Check if all text fields (Under `Indices`, `Coordinates`, `X Axis`, `Y Axis`, `Z Axis`) are read only (nothing can be written inside them)
4. **Check enabled status**
    1. Click on the checkbox `Enable Deformation Analysis` and make sure it is enabled
    2. Check if all other radio buttons (`Indices`, `Coordinates`, `All Points`) are usable
    3. Check if clicking on one of these radio buttons deselects the other two radio buttons
    4. Check if the text fields under `Indices` and `Coordinates` are usable if the corresponding radio button is checked
    5. Check if the text fields under `Indices` and `Coordinates` are only usable if the corresponding radio button is checked
5. **Check correct indices input**
    1. Enable the radio button `Indices`
    2. Enter a valid sequence in the text field below (A valid sequence is an arbitrary, non zero amount of whole, finite numbers, seperated by commas with an arbitrary amount of whitespaces between the numbers and the commas)
    3. Click on the `Apply` button at the bottom of the GUI
6. **Check correct coordinates input**
    1. Close the whole program and repeat step 1 and 2
    2. Enable the checkbox `Enable Deformation Analysis` and the radio button `Coordinates`
    3. Enter a valid sequence in the text field below `Coordinates` (A valid sequence is an arbitrary, non zero amount of vectors seperated by commas followed by a new line. The vectors start with `[`, end with `]` and consist of both negative and positive  finite floating point numbers seperated by a comma)
    4. Click on the `Apply` button at the bottom of the GUI
7. **Check incorrect indices input**
    1. Close the whole program and repeat step 1 and 2
    2. Enable the checkbox `Enable Deformation Analysis` and the radio button `Indices`
    3. Enter an invalid sequence in the text field below `Indices`
    4. Click on the `Apply` button at the bottom of the GUI
8. **Check incorrect coordinates input**
    1. Enable the radio button `Coordinates`
    2. Enter an invalid sequence in the text field below
    4. Click on the `Apply` button a the bottom of the GUI

## Expected result
1. When clicking on `Apply` in step 5.3, the simulation should start and no errors should be displayed.
2. When clicking on `Apply` in step 6.4, the simulation should start and no errors should be displayed.
3. When clicking on `Apply` in step 7.4, the simulation should not start and an error should be displayed.
4. When clicking on `Apply` in step 8.3, the simulation should not start and an error should be displayed.
5. No unexpected errors or console ouputs should be displayed.
