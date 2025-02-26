# Manual Test for the User Story 'GUI - Select Meshes'

### Test Goal
Check whether the input in the Models interface gets progressed properly so it is visible in the SOFA simulation.

### User Story
As a material science engineer, I’d like to switch between several meshes to compare my material’s behaviour on different geometries, so that I can evaluate material properties on different test subjects.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().


## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Open Popup Menu**
    1. Click the `Models` button at the top right corner.
    2. Click the `Open` button that appeared after clicking the `Models` button.
3. **Select Model**
    1. Select a random model out of the default or custom models.
    2. Click the `Close` button in the bottom of the popup window.
4. **Validate selected model**
    1. Click the `Apply` button at the bottom of the GUI.


## Expected Result
1. 2.1 A popup window titled `Models` appears.
2. 2.1 The popup window contains the following default models listed under 'Default Models:'
   - `gripper_4_arm`
   - `beam`
   - `simple_buttefly`
   - `butterfly`
   - `gripper_3_arm`
3. 2.1 The popup window can also contain models listed under 'Custom Models'.
4. 4.1 The selected model is applied in the GUI. 
