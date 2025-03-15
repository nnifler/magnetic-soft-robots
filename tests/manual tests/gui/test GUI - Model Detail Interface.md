# Manual Test for the User Story 'GUI - Model Detail Interface'

### Test Goal

Check whether model properties and selections are shown correctly.
Check if the following criteria are met: 
To define the bounding box inside of which all vertices are fixed, two (diagonally opposing) points need to be specified in the GUI. Each point should be represented as a vector, allowing float values for each of its three places. For that, an own widget should be defined dedicated to the definition of model parameters.
In the same widget, the name of the currently selected mesh should be displayed in a label, so that it is clear for which model the fixation is defined. For further information, the number of nodes in the specified mesh should be displayed.


### User Story

As a user, I want to see which mesh is to be loaded and define the fixation points of the model, so that I can simulate its behaviour under different circumstances. As the models change, so do the points where they are fixed to the environment. Even in the same model, different behaviours might be caused by different environmental fixations. A butterfly model for example curls differently when attached on its wing than it would attached on its torso.

## Prerequisites

Make sure that the project is installed according to [README.md]() and [Requirements.txt]().

## Test

1. Start of the application:
    1. Run the file ∼/magnetic-soft-robots/main.py
2. Check the behaviour of the application
    1. Check whether a sub widget with the name "Model Configuration" opens in the interface at start including a field with the name "Selected Model:"
3. Select a mesh
    1. Upper Right Button "Models"
    2. Select "Open"
    3. Select a random default model
4. Window check
    1. "Selected Model" displays the name of the selected model
    2. "Number of Nodes" displays the number of nodes.
    3. "Number of Tetrahedra" displays the number of tetrahedra
    4. Bounding Boxes: --> see [LINK - SOFA Interface 3.9-10](test LINK - SOFA Interface.md)

## Expected Result

1. 2.1: The widget appears.
2. 4.1: The model name equals the model name you selected in 3.3
3. 4.2-3: The model nodes count equals the following values for default models:
    1. `beam`: 306 Nodes, 807 Tetrahedra
    2. `butterfly`: 423 Nodes, 1094 Tetrahedra
    3. `gripper_3_arm`: 466 Nodes, 1131 Tetrahedra
    4. `gripper_4_arm`: 1679 Nodes, 4912 Tetrahedra
    5. `simple_butterly`: 260 Nodes, 624 Tetrahedra
