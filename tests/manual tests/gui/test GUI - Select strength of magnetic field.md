# Manual test for the user story ‘GUI - Select strength of magnetic field’

### Test Goal
Check adjustable mechanism for modifying the magnetic field, including a slider for strength adjustment next to the force size and a widget with a field for precise vector input for the magnetic direction. These widgets should be in the previously defined simulation settings widget.

### User Story
As a student of material sciences, I’d like to experiment with different magnetic fields, so that I can see how the behaviour of my models changes and thus develop an intuition for the interaction between (different components of a) magnetic field and responsive material.

## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Check the behaviour of the application**
    1. Check whether a sub widget with the name "Magnetic Field Settings" is visible in the simulation tab upon application start.
3. **Window check**
    1. Slider for Strength Adjustment
        1. Verify that it contains a slider with the label `Magnetic Field Strength`.
        2. Slider is adjustable to various positions within its range.
        3. Ensure that the minimum and maximum values of the slider are correct zero and 100 T.
        4. Check that changes in the slider position update the `Magnetic Field Strength` output in the `Magnetic Field Setting` widget in real time and match the expected values in Tesla.
    2. Vector Input Field
        1. Verify the presence of the input field with the label `Direction (Vector)`.
        2. Allowed: Numbers in the format [x, y, z], with optional spaces and decimal places.
        3. Invalid input is restricted: Anything that does not adhere to the format [x, y, z] with exactly three valid numbers and separators.
        4. The text field contains a description of the correct input format when empty. 
    3. Apply Function 
        1. Verify that the current slider value is applied to the magnetic field strength by checking the console output.
        2. Verify that the vector value from the input field is parsed correctly by checking the console output.
        3. Confirm that invalid vector inputs trigger a warning dialog box ad prevent the application of values. 
4. **Check the console output**
    1. Ensure that no unexpected errors or warnings occur in the integrated terminal.

## Expected result
1. Sub-widget appears correctly.
2. Labels are correct and complete.
3. Magnetic Field Strength input via the slider is possible.
4. The limit values of the slider are correct.
5. Vector direction value input is possible.
6. Invalid input is restricted and triggers a clear warning message.
7. Description of the correct entry is shown if the field is empty.
8. The console output for magnettic field strength and direction vector matches the input in the GUI .
9. No errors or warnings in the console.
