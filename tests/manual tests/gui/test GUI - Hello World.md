# Manual test for the user story ‘GUI - Hello World’

### Test Goal
Check whether an external window is opened when the application is started

### User Story
As a user of the simulation framework, I'd like to run it in a window, so that I don't have to use non-intuitive console interfaces or code files for running my simulations.

## Prerequisites 
Make sure that the project is installed according to [README.md]() and [Requirements.txt]()

## Test
1. **Start of the application**
    1. Run the file [$ magnetic-soft-robots/main.py](../../../main.py)
2. **Check the behaviour of the application**
    1. Check whether a window with the name "Magnetic Soft Robotic Simulation" opens within 2 seconds
3. **Logo check**
    1. Check whether a logo appears in top left-hand corner of the "Magnetic Soft Robotic Simulation" widget. 
    2. Check whether the logo is proportionally scaled and not distorted or cut off.
4. **Window check**
    1. Maximise and minimise the window.
    2. Moving the window.
    3. Closing the window.
4. **Check the console output**
    1. Ensure that no unexpected errors or warnings occur in the integrated terminal.

## Expected result
1. After starting the main.py file, a separate window with the title ‘Magnetic Soft Robotic Simulation’ appears.
2. The window can be maximised, minimised, moved and closed.
3. The logo is displayed in the top left-hand corner, the aspect ratio is retained and therefore the logo does not appear distorted and the size of the logo matches the height of the header bar, i.e. it is not cut off. 
3. No unexpected errors or console output.
