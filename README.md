# Software Project: Magnetic Soft Robotics Simulation Software

## Project Description
The Magnetic Soft Robtics (MSR) Software is designed to provide a software solution for the modeling, 
simulation and visualization of the deformation behavior of magnetic soft robots under the influence of magnetic forces. 
It is specifically developed for Windows and focuses on a user-friedly interface as well as robust simulation tools. 

The project is based on the [Simulation Open Framework Architecture (SOFA)](https://www.sofa-framework.org), an open-source framework for interactive 
physics simulations using the finite element method (FEM).

MSR offers the following features: 
- Graphical user interface (GUI) for configuring simulation parameters
- Support for simulating various models with adjustable parameters
- Material and model library with approximately 35 sample materials and five sample models. 
- Extensibility trough custom material and model definitions 
- Detailed analysis of deformation behavior, including: 
    - Display of maximum defirmation along all axes
    - Visualizsation of local stress distribution within the model 
- Interactive simulation of magnetic forces, where the magnetic field affects material properties and consequently deformation. 

MSR enables precise testing of different materials and magnetic field strengths and their effects on the behavior of soft robots. 

## Getting Started
Before getting started, please read the Requirements document.

To get started with the MSR software, the following guide describes the steps to install the project on a local computer after successfully setting up the required dependencies. 

### Clone the Repository 
1. Create a folder where the repository will be stored and navigate to this folder. 
2. Open a terminal window and run the following command to clone the repository from GitHub to the local directory on your computer: 
    ```git clone https://github.com/nnifler/magnetic-soft-robots.git```
3. Now the project is cloned to the local computer and can be opened in an IDE (e.g. Visual Studio).

### Start the Software 
Open the MSR software in a suitable IDE and start the software by opening the repository and running the file main.py.
Or start the MSR software in a terminal window by navigation to the repository and running ```python main.py```

## License
For licensing information, refer to the LICENSE file included in this repository.

## Background 
The project is devolped as part of the ’Teamprojekt Softwareentwicklung’ course at the Technical University of Darmstadt, overseen by Dr.-Ing. Ragnar Mogk. 


