# Manual Test for the User Story 'GUI - Export to lib'

### Test Goal
Check whether saving material properties works.

### User Story
As a material scientist, I work on new materials for magnetic soft robots, so I'd like to add my own defined materials to the library in order to use them for simulations and thus test them.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().


## Test
1. Start of the application
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. Check the behaviour of the application: Check whether a sub widget with the name "Material Configuration" opens in the interface at start.
3. Test Material Name functionality
    1. Input random accepted values in each text field in the material configuration widget.
    2. Click save button
    3. Close the dialog window
    4. Close the main window
4. Redo step 1
5. Select Material
   1. Open Select Material Dropdown
   2. Select the material with the name you specified
   3. Look at the values

## Expected Result
1. 3.2 A dialog box appears that confirms your addition.
2. 5.1 The item with the specified name appears in the dropdown
3. 5.3 The values you specified are equal to the values that are now shown
