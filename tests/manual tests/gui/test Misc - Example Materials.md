# Manual Test for the User Story 'Misc - Example Materials'

### Test Goal
Check whether the sample meshes are visible in the GUI. 

### User Story
As an engineer, I’d like to quickly assess with which material I’d like to realize my magnetic soft robot designs. For that, material property research would slow me down, so I want to see a list of predefined materials, which I can choose from.

## Prerequisites
Make sure that the project is installed according to [README.md]() and [Requirements.txt]().

## Test

1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Verify hardcoded material**
    1. Ensure that the simulation tab is selected
    2. Select Material *Neodymium Powder*
        1. Check Young's Modulus
        2. Check Poisson's Ratio
        3. Check Density
        4. Check Remanence
3. **Verify MatWeb materials**
    1. Select one material with a long name
    2. Use the search field on [MatWeb.com](https://www.matweb.com/index.aspx) and view Data Sheet
    3. Compare material values of the software with the datasheet


## Expected Result
1. 2.i.a. Young's Modulus equals to 16 GPa
2. 2.i.b. Poisson's Ratio equals to 0.3
3. 2.i.c. Density equals to 7500 kg/m^3
4. 2.i.d. Remanence equals to 1.508
5. 3.i. There are around 30 materials with a long name
6. 3.ii. The selected material is found on the website
7. 3.iii. The values in the software are equal to the values in the datasheet 
