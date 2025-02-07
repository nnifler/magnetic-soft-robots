# Manual Test for the User Story 'GUI - Model Detail Interface'

### Test Goal

Check whether model properties and selections are shown correctly.

### User Story

n/a

## Prerequisites

Make sure that the project is installed according to [README.md]() and [Requirements.txt]().

## Test

1. Start of the application:
    1. Run the file ∼/magnetic-soft-robots/main.py
2. Check the behaviour of the application
    1. Check whether a sub widget with the name "Material Configuration" opens in the interface at start including a field with the name "Constraint Box Lower Corner:"
3. Select a mesh
    1. Upper Right Button "Models"
    2. Select "Open"
    3. Select one of the default models
4. Window check
    1. "Model Name: " displays the name of your selected model
    2. "Model Nodes Count: " displays number of nodes.
    3. "Model Tetrahedra Count: " displays the number of tetrahedra
    4. Bounding Boxes: --> see [LINK - SOFA Interface 3.9-10](test LINK - SOFA Interface.md)

## Expected Result

1. 2.1: The widget appears.
2. 4.1: The model name equals the model name you selected in 3.3
3. 4.2-3: The model nodes count equals the following values for default models:
    1. `beam`: 306 Nodes, 807 Tetrahedra
    2. `butterfly`: 427 Nodes, 1159 Tetrahedra
    3. `gripper_3_arm`: 466 Nodes, 1131 Tetrahedra
    4. `gripper_4_arm`: 1679 Nodes, 4912 Tetrahedra
    5. `simple_butterly`: 225 Nodes, 527 Tetrahedra
