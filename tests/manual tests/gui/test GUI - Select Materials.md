# Manual test for the user story ‘GUI - Select Materials’

### Test Goal
Check whether a sub-widget appears in the simulation settings widget that contains a selectable unit for the selection of materials with a corresponding label. Upon selection, the different parameters of the selected material should be displayed in the previously defined parameter screen.

### User Story
As a student of material sciences, I'd like to easily select different materials for a given model, so that I can easily switch between and experiment with them, in order to get a better feel for their behaviour. I'd also like to see the properties of each material when I select them, so that I can see what I am working with.

## Prerequisites 
Make sure that the project is installed according to [README.md]() and [Requirements.txt]()


## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Check the behaviour of the application**
    1. Check whether a sub widget with the name "Material Configuration" opens in the simulation tab at start including a field with the name "Select Materials:"
3. **Window check**
    1. Selecting materials
    2. Switching between different materials 
        1. Switching between different materials is possible
    3. Displays the parameters of the selected material.
        1. The parameters of the selected material are displayed in the parameter fields.
        2. The values change correctly when changing between materials
4. **Check the console output**
    1. Ensure that no unexpected errors or warnings occur in the integrated terminal.

## Expected result
1. Sub-widget appears correctly.
2. Label is correct and complete.
3. Drop-down menu for material selection is available and working.
4. No errors or warnings in the console.
