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
2. Select the tab in the sidebar of the interface.  
    1. Make sure you selected the default tab `Simulation Settings`.
3. Check the behaviour of the application: 
    1. Check whether a sub widget with the name `Material Configuration` opens in the interface at start.
4. Test the exceptional behaviour of the save material functionality.
    1. Click the save button without specifing a name in the `Material Name` field.
    2. Enter a random text only from whitespace and punctuation characters in the `Material Name` field.
    3. Click the `Save` button.
    4. Select a random material from the `Select Material` field.
    5. If the text right of the selected material states that the material is custom redo step 4.4.
    6. Copy the text of your previous selected material to the `Material Name` field. If you're unsure how to type the material name take a look in [the corresponding json file](../../../lib/materials/default.json).
    7. Click the `Save` button.
5. Test `Material Name` functionality
    1. Enter random accepted values in each text field except the name field in the `Material Configuration` widget.
    2. Enter a unique text, that is not yet part of the database shown under the `Select Materials` field, in the `Material Name` text field.
    3. Click the `Save` button.
6. Select Material
    1. Check the current selected material name shown in the `Select Material` dropdown and compare it to the material name specified in 5.2
    2. Check if the shown values are as specified in 5.1
    3. Check which mode the text right of the dropdown shows
7. Test further exceptional behavior
    1. Copy the current text from the `Select material` dropdown into the `Material Name` field.
    2. Enter random valid values in each text field except the `Material Name` field in the `Material Configuration` widget.
    3. Click the `Save` button.
    4. If an error box is shown click the `Abort` button.
    5. In the `Select Material` dropdown select a random material.
    6. Now select the material with the name you specified in 5.2 from the `Select Material` dropdown.
    7. Check the displayed values.
    8. Enter random valid values in each text field in the `Material Configuration` except the `Material Name` field, which should stay the same. 
    9. Click the `Save` button.
    10. If an error box appears, click the `Save` button in the error box.
    11. Select a random material from the `Select Material` dropdown.
    12. From the `Select Material` dropdown select the material with the name you specified in 5.2.
    13. Check the displayed values.
8. Restart Behavior
    1. Close the `Soft Robotics Simulation` window.
    2. Redo the steps 1 and 2. 
    3. Select the material you defined in 5.2 in the `Select Material` dropdown menu.
    4. Check the displayed values.

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
