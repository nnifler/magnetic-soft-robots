# Manual Test for the User Story 'Sofa - Implement Magnetic Force'

### Test Goal
Verify whether the simulation behaves realistically and the model deforms according to the specified magnetic field.

### User Story
As an engineer, I'd like to simulate my models in software that implements magnetism, as little to no 3D-simulation for that exists. It needs to implement accurate physical behavior, so that I can see how the model would behave under the magnetic field.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().

## Test
1. **Enable show force**
    1. Locate the file [$ magnetic-soft-robots/gui/main_window.py](../../gui/main_window.py)
    2. Ensure that the function `Config.set_show_force()` is given `True` as a parameter in `apply_parameters()`

2. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../main.py)

3. **Set parameters**
    1. Ensure that the simulation tab is selected
    2. Input a random valid value in the number field `Young's Modulus`
    3. Choose a random option in the unit selector next to the number field `Young's Modulus`
    4. Input a random valid value in the number field `Poisson Ratio`
    5. Input a random valid value in the number field `Density`
    6. Choose a random option in the unit selector next to the number field `Density`
    7. Input a random valid value in the number field `Remanence`
    8. Put the slider `Magnetic Field Strength` on a random position
    9. Input a random valid vector in the `Direction` field 

4. **Click Apply Button**
    1. Click the `Apply` button at the bottom of the GUI

5. **Start the animation**
    1. In the simulation window, click the button `Animate`
    2. Observe the behavior of the model
    3. If the model does not deform, repeat step 2-5 and choose a lower `Young's Modulus`, a higher `Magnetic Field Strength` or change the `Direction`

6. **Stop the simulation**
    1. When the model does not deform any further, you can close the simulation window

## Expected Result

1. The model deforms
2. The forces acting on the object (green arrows) should not be fixed and change during the simulation
3. The deformation shown in the simulation is an expected outcome according to the parameters set in step 1
4. The simulation does not unexpectedly stop and no errors are shown in the console
