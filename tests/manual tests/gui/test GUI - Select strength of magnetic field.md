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
        1. Verify an input field with the label `Magnetic Field Strength` is shown.
        2. Invalid input is restricted to ensure only values between 0 and 5.0000 are allowed (excluding negative numbers, non-numeric characters, except comma or dot).
        3. Verify the unit `T` is shown after the input field
        4. Verify a slider from `0 T` to `5 T` is shown.
        5. The sliders are adjustable to various positions within its range.
        6. Ensure that the minimum and maximum values of the slider are correct zero and 5 T.
        7. Insert a random number from 0.0000 to 5.0000 with up to 4 decimal places in the spinbox.
        8. Check the selected value in the slider.
        9. Input a random number in the slider.
        10. Check the selected value in the spinbox
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
10. 3.1.8 The slider shows the value entered in 3.1.7.
11. 3.1.10 The slider shows the value entered in 3.1.9.
