# Manual Test for the User Story 'LINK - SOFA Interface'

### Test Goal
Check whether the user inputs via the GUI get processed correctly, are added to the config class and the Sofa simulation can be started from the GUI.

### User Story
As any user, I’d like to see the changes I set in the GUI take effect on the simulation.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().

## Test

1. **Activate debug mode**
    1. Locate the file [$ magnetic-soft-robots/src/sofa_instantiator.py](../../../src/sofa_instantiator.py)
    2. Change the variable `debug` in the `main`-Method to `True`

2. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)

3. **Input values**
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

5. **Verify Config Class**
    1. Look into the console and verify if the values in the output are the same as the ones you put into the GUI

6. **Deactivate debug mode**
    1. Locate the file [$ magnetic-soft-robots/src/sofa_instantiator.py](../../../src/sofa_instantiator.py)
    2. Change the variable `debug` in the `main`-Method to `False`

7. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)

8. **Verify if the simulation starts**

## Expected Result
1. `Young's modulus` is found in `Material parameters` and is displayed in the console in `Pa`
2. `Poisson Ratio` is found in `Material parameters`
3. `Density` is found in `Material parameters` and is displayed in the console in `kg/m^3`
4. `Remanence` is found in `Material parameters`
5. `Magnetic Field Strength` is found in `External forces` as `magnetic_force`
6. `Direction` is found in `External forces` as an array
7. The simulation starts after pressing the `Apply` button without debug mode
8. No unexpected errors appear in the console
