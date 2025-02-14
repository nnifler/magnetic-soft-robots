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
2. Selected Tab
    1. Make sure you selected the default tab simulation settings.
3. Check the behaviour of the application: Check whether a sub widget with the name "Material Configuration" opens in the interface at start.
4. Test exceptional Material Name functionality
    1. Click the save button without specifing a name in the Material Name field.
    2. Input random text only from whitespace and punctuation characters in the Material Name field.
    3. Click the save button.
    4. Close the dialog box.
    5. Select a random on your keyboard typable material from the Select Material field.
    6. Copy the name to the Material Name field.
    7. Click the save button.
    8. Close the dialog box.
5. Test Material Name functionality
    1. Input random accepted values in each text except the name field in the material configuration widget.
    2. Click the save button.
    3. Close the dialog box.
6. Select Material
    1. Open Select Material Dropdown
    2. Select the material with the name you specified
    3. Look at the values
    4. Copy the name to the Material Name field.
    5. Click the save button.
    6. Close the dialog box.
7. Restart Behavior
    1. Close the Soft Robotics Simulation window.
    2. Redo 1-2
    3. Redo 6.1-6.3

## Expected Result

1. 3 There is an empty field with the placeholder text "Material Name".
2. 3 There is a button with the text "Save".
3. 4.1, 4.3 An error box appears with the text 'Please enter a metrial name'.
4. 4.7 An error box appears with the text 'Material name already exists in default materials.'
5. 5.2 An information box titled 'Material saved' appears with the text 'Material saved sucessfully.'
6. 6.1 The item with the specified name appears in the dropdown.
7. 6.3 The values you specified are equal to the values that are now shown.
8. 6.5 An error box appears with the text 'Material name already exists in custom materials.'
