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
    4. Select a random material from the Select Material field.
    5. If the text right of the selection states the material is custom redo step 4.4.
    6. Copy the text of your selection to the Material Name field. If you're unsure how to type the material name take a look in [the corresponding json file](../../../lib/materials/default.json).
    7. Click the save button.
5. Test Material Name functionality
    1. Input random accepted values in each text field except the name field in the material configuration widget.
    2. Input a unique text, that is not part of the Select Materials field yet, in the Material Name text field.
    3. Click the save button.
6. Select Material
    1. Look at the Select Material dropdown
    2. Look at the values
    3. Look at the text right of the dropdown
7. Test further exceptional behavior
    1. Copy the text out of the dropdown selection to the Material Name field.
    2. Input random accepted values in each text field except the name field in the material configuration widget.
    3. Click the Save button.
    4. In the error box click the Abort button.
    5. In the Select Material Dropdown select a random material.
    6. In the Select Material Dropdown select the material with the name you specified.
    7. Look at the values.
    8. Input random accepted values in each text field except the name field in the material configuration widget.
    9. Click the Save button.
    10. In the error box click the Save button.
    11. In the Select Material Dropdown select a random material.
    12. In the Select Material Dropdown select the material with the name you specified.
    13. Look at the values.
8. Restart Behavior
    1. Close the Soft Robotics Simulation window.
    2. Redo 1-2
    3. Select the material you defined in 5.2 in the Select Material selection.
    4. Look at the values.

## Expected Result

1. 3 There is an empty field with the placeholder text "Material Name".
2. 3 There is a button with the text "Save".
3. 4.1, 4.3 An error box appears with the text 'Please enter a material name'.
4. 4.7 An error box appears with the text 'Material name already exists in default materials.'
5. 5.3 An information box titled 'Material saved' appears with the text 'Material saved sucessfully.'
6. 6.1 The item with the name you specified is selected in the dropdown.
7. 6.2 The values you specified in 5.1 are equal to the values that are now shown.
8. 6.3 The text states the material is custom.
9. 7.3 An error box titled 'Replace Material?' with the text 'Material name already exists in custom materials.' and two buttons 'Save' and 'Abort' appears.
10. 7.7 The values you specified in 5.1 are equal to the values that are now shown.
11. 7.13 The values you specified in 7.2 are equal to the values that are now shown.
12. 8.3 There is a material with the name you specified in step 5.2 in the Select Material dropdown.
13. 8.4 The values you specified in 7.8 are equal to the values that are now shown.
