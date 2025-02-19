# Manual Test for the User Story 'GUI - Select Meshes'

### Test Goal
Check whether the import of models in the Models interface gets progressed properly so it is visible in the SOFA simulation.

### User Story
As a soft robot engineer, I'd like to try new structures besides new materials for my robots, so that I can test different robot designs.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().


## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Click Models button**
    1. Click the `Models` button at the top right corner.
    2. In the opening menu, select the QAction Import.
3. **Import Models Popup - regular**
    1. Check which Widgets appear in the Popup
    2. Define a name in the box for that, include spaces.
    3. Select a random .stl as a surface mesh, for instance from the provided examples
    4. Select a random .msh as a volumetric mesh, for instance from the provided examples
    5. Press the Import button.
    6. Check for success popup and close it.
4. **Provoke Errors**
    0. For each of the following points, repeat the previous instructions for the regular case (see point 1-3), except...
    1. Press import with nothing specified.
    2. Press import with no paths but valid name specified.
    3. Press import with either path unspecified.
    4. Try selecting a file with invalid format in the dialog.
    5. Press import with no name but valid paths specified.
## Expected Result
1. Our main window is started.
2. 
    1. A QMenu should open.
    2. A popup window titled "Import Models" should appear.
3. 
    1. Box to define models, which holds lables for declaring the model name, and both paths. Furthermore this box includes 2 buttons for selecting paths, and there is one big button to import the mesh below the box.
    2. name appears as it is typed
    3. A file dialog opens, allowing to select a file. Only .stl files should be shown. Upon selection, the path pointing to the selected file should appear in the label beside the button.
    4. A file dialog opens, allowing to select a file. Only .msh files should be shown. Upon selection, the path pointing to the selected file should appear in the label beside the button.
    5. After the button push, a pair consisting of a .stl and .msh file should appear in the folder lib/imported_models. Both files should have the specified name. Furthermore, they should appear in the Open Models Popup in the field Custom Models.
    Spaces before and after the specified 
    6. A popup indicating import success should open. Upon acknowledging that, both the popup and import window should close
4. 
    1. Warning popup indicating the missing name should appear. Import does not go through.
    2. Warning popup indicating a missing mesh path should appear. Import does not go through.
    3. Warning popup indicating a missing mesh path should appear. Import does not go through.
    4. Should not be possible.
    5. Warning popup indicating the missing name should appear. Import does not go through.