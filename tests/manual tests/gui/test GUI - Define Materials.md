# Manual test for the user story ‘GUI - Define materials’

### Test Goal
Check whether a sub-widget appears in the simulation settings widget that contains labels for each property to explain the property name, a field for entering the value and a selectable unit

### User Story
As a material science engineer, I'd like to see how different materials change the behaviour of the models, so that I can pick the one best suited for my product. For that, I need to define different material properties.

## Prerequisites 
Make sure that the project is installed according to [README.md]() and [Requirements.txt]()

## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Check the behaviour of the application**
    1. Check whether a sub widget with the name "Material Configuration" opens in the simulation tab at start.
3. **Window check**
    1. Selecting materials
    2. Selecting material behavior
    3. Input field with label for Young modulus:
        1. Input of positive values with up to four decimal digits possible
        2. Input of invalid characters not possible (negative numbers, non-numeric characters except comma or dot for decimal separator)
    4. Input field with label for Poisson ratio:
        1. Input allowed: positive decimal values between 0 and 0.4999 with up to four decimal places.
        2. Invalid input is restricted to ensure only values between 0 and 0.4999 are allowed (excluding negative numbers, non-numeric characters, except comma or dot).
    5. Input field with label for density:
        1. Input allowed: positive numbers between 0 and 30000 with up to two decimal places.
        2. Invalid input is restricted to ensure only values between 0 and 30000 are allowed (excluding negative numbers, non-numeric characters, except comma or dot).
    6. Input field with label for remanence:
        1. Input allowed: numbers between -2.0 and 2.0 with up to three decimal places.
        2. Invalid input is restricted to ensure only values between -2.0 and 2.0 are allowed (excluding non-numeric characters, except comma or dot).
    7. Displays the parameters of the selected material.
        1. The parameters of the selected material are displayed in the parameter fields.
        2. The values change correctly when changing between materials
    8. Selection of different unit sizes
        1. Selection between different sizes for Youngs Modulus
        2. Selection between different sizes for Density
        3. The values change correctly when changing between unit sizes
        4. No selection with one choice appears
4. **Check the console output**
    1. Ensure that no unexpected errors or warnings occur in the integrated terminal.

## Expected result
1. Sub-widget appears correctly.
2. Labels are correct and complete.
3. Value input is possible
4. Invalid input is restricted
5. Drop-down menus for unit sizes for Youngs Modulus and Density are available and working.
6. Drop-down menus for material selection and behavior are available and working.
7. No errors or warnings in the console.
