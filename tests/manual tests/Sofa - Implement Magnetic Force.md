# Manual Test for the User Story 'Sofa - Implement Magnetic Force'

### Test Goal
Verify whether the simulation behaves realistically and the model deforms according to the specified magnetic field.

### User Story
As an engineer, I'd like to simulate my models in software that implements magnetism, as little to no 3D-simulation for that exists. It needs to implement accurate physical behavior, so that I can see how the model would behave under the magnetic field.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().

## Test
<span style='color:red'> ---------------------------------------------------------------------\
<span style='color:red'> Old version, remove as soon as GUI branch is merged\
<span style='color:red'> ---------------------------------------------------------------------

1. **Set parameters**
    1. Locate the file [$ magnetic-soft-robots/src/config.py](../../src/config.py)
    2. Change the value of `POISSON_RATIO` to a random value between 0 and 0.499
    3. Change the value of `YOUNGS_MODULUS` to a random valid value (use the YoungsModulus class)
    4. Change the value of `DENSITY` to a random valid value (use the Density class)
    5. Change the value of `MAGNETIC_FORCE` to a random valid value (use the Tesla class)
    6. Change the value of `REMANENCE` to a random valid value (use the Tesla class)
    7. Change the value of `MAGNETIC_DIR` to a random `np.array` with length 1
    8. Ensure that the value of `SHOW_FORCE` is set to `True`

2. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/sofa_instantiator.py](../../sofa_instantiator.py)

<span style='color:red'> ---------------------------------------------------------------------\
<span style='color:red'> End of old version\
<span style='color:red'> ---------------------------------------------------------------------

<span style='color:green'> ---------------------------------------------------------------------\
<span style='color:green'> New version, replaces old version when GUI branch is merged\
<span style='color:green'> ---------------------------------------------------------------------

1. **Enable show force**
    1. Locate the file [$ magnetic-soft-robots/gui/mainWindow.py](../../gui/mainWindow.py)
    2. Ensure that the function `Config.set_show_force()` is given `True` as a parameter in `apply_parameters()`

2. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../main.py)

3. **Set parameters**
    1. Input a random valid value in the number field `Young's Modulus`
    2. Choose a random option in the unit selector next to the number field `Young's Modulus`
    3. Input a random valid value in the number field `Poisson Ratio`
    4. Input a random valid value in the number field `Density`
    5. Choose a random option in the unit selector next to the number field `Density`
    6. Input a random valid value in the number field `Remanence`
    7. Put the slider `Magnetic Field Strength` on a random position
    8. Input a random valid vector in the `Direction` field 

4. **Click Apply Button**
    1. Click the `Apply` button at the bottom of the GUI

<span style='color:green'> ---------------------------------------------------------------------\
<span style='color:green'> End of new version\
<span style='color:green'> ---------------------------------------------------------------------

3. **Start the animation**
    1. In the simulation window, click the button `Animate`
    2. Observe the behavior of the model
    3. If the model does not deform, lower the `YOUNGS_MODULUS` or raise the `MAGNETIC_FORCE` in the file [$ magnetic-soft-robots/src/config.py](../../src/config.py) and repeat step 3

4. **Stop the simulation**
    1. When the model does not deform any further, you can close the simulation window

## Expected Result

1. The model deforms
2. The forces acting on the object (green arrows) should not be fixed and change during the simulation
3. The deformation shown in the simulation is an expected outcome according to the parameters set in step 1
4. The simulation does not unexpectedly stop and no errors are shown in the console
