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
    2. Assure that there are at least two custom models imported. 
        1. Should no such models be imported, import two by cloning the default meshes using the dialogue under `Models` > `Import`.
2. **Open Popup Menu**
    1. Click the `Models` button at the top right corner.
    2. Click the `Open` button that appeared after clicking the `Models` button.
3. **Provoke Erroneous Behaviour**
    1. Press the `Open Model` button at the bottom of the window without selecting anything.
4. **Select Model Regularly**
    1. Single click on a random model in either the list selection for default or custom models.
    2. Single click on a different model in the other widget.    
    3. Press the `Enter` key on your keyboard.
    4. Double click on a model from the other list selection.
    5. Press the `Open Model` button at the bottom of the window.
5. **Stop the Selection Process**
    1. Execute step 2 to open the `Models` window again.
    2. Select a model using double click so that its name is displayed under `Current Selection`.
    3. Close the window using the X in its corner.
6. **Validate selected model**
    1. Click the `Apply` button at the bottom of the GUI.


## Expected Result
2.  **Open Popup Menu**
    1. A popup window titled `Models` appears.
    The popup window contains the following default models listed under `Default Models`:
    - `gripper_4_arm`
    - `beam`
    - `simple_buttefly`
    - `butterfly`
    - `gripper_3_arm`
    The popup window also lists custom models under `Custom Models`.
    At the bottom of the window, there is space for displaying the selected models name captioned `Current Selection`.
    At the very bottom, there is a button called Open Model.
3. **Provoke Erroneous Behaviour**
    1. A warning box appears, telling you to select a model. 
    After closing it, you're still in the selection screen.
4. **Select Model Regularly**
    1. The model clicked is highlighted in the list. Its name is not displayed under `Current Selection`. Nothing else is highlihted.
    2. The model clicked is highlighted in the list. Its name is not displayed under `Current Selection`. Nothing else is highlihted, especially not the previously selected model.
    3. Now, the model previously highlighted in 4.2 has its name displayed under `Current Selection`.
    4. The model double clicked in this step has its name displayed under `Current Selection`. The previously selected model is not highlighted anymore.
    5. A popup indicating selection success opens.
5. **Stop the Selection Process**
    3. No change recognizable.
6. **Validate selected model**
    1. The selected model is applied in the GUI. 
