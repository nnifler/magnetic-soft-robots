# Software Project: Magnetic Soft Robotics Simulation Software

## Project Description

The Magnetic Soft Robotics (MSR) Software is designed to provide a software solution for the modeling,
simulation and visualization of the deformation behavior of magnetic soft robots under the influence of magnetic forces.
It is specifically developed for Windows and focuses on a user-friendly interface as well as robust simulation tools.

The project is based on the [Simulation Open Framework Architecture (SOFA)](https://www.sofa-framework.org),
an open-source framework for interactive physics simulations using the finite element method (FEM).

MSR offers the following features:

- Graphical user interface (GUI) for configuring simulation parameters
- Support for simulating various models with adjustable parameters
- Material and model library with approximately 35 sample materials and five sample models
- Extensibility through custom material and model definitions
- Detailed analysis of deformation behavior, including:
  - Display of maximum deformation along all axes
  - Visualization of local stress distribution within the model
- Interactive simulation of magnetic forces, where the magnetic field affects material properties and consequently deformation

MSR enables precise testing of different materials and magnetic field strengths and their effects on the behavior of soft robots.

## Getting Started

To get started with the MSR software, the following guide describes the steps to install the project on a local computer.

### Install the Project

1. Create a folder where the repository will be stored, if it does not already exist.
2. Clone the repository from GitHub.
   1. Download the ZIP file from the Releases tab.
   2. Extract the ZIP file to your desired destination folder.\
    Note: This folder cannot be changed later. To move the installation, you must download and extract the ZIP file again.
3. Installation
   1. Execute the installation script `Install.ps1`\
      This can be done by right clicking on it and selecting `Run with PowerShell` or by executing it in `PowerShell`.
   3. The project is now installed on your local machine.

### Possible Complications
**Windows prevents execution of the installation script**\
This could happen because the PowerShell execution policy is not configured correctly. To execute the installation script, set the execution policy to `Bypass` by executing the command `Set-ExecutionPolicy -ExecutionPolicy Bypass` in an administrator PowerShell.\
More information: [about_execution_policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)

**The installation script fails while downloading python or SOFA**\
This could happen because the path to the location of the project folder is too long. Try extracting the project folder to a location with a shorter path.

## Start the Application

Start the application by executing `Run.ps1` by right clicking on it and selecting `Run with PowerShell` or by executing it in `PowerShell`.

## How to get a volumetric mesh

To import a custom model you need both a surface mesh and a volumetric mesh. Most mesh files for 3D Models found on the internet are surface meshes. These meshes can be converted to volumetric meshes using various programs.

An easy to use program to convert `.stl`-files is [Gmsh](https://gmsh.info/). The steps to to create a volumetric mesh are as follows:
1. Open the `stl`-file using `File > Open`
2. Add a volume using `Modules > Geometry > Elementary entities > Add > Volume` and clicking on the model. If prompted to create a `.geo`-file, do so. Then press `e` to cancel the selection of hole boundaries.
3. Create the volumetric mesh using `Modules > Mesh > 3D`
4. Save the volumetric mesh using `Modules > Mesh > Save`

## License

For licensing information, refer to the [LICENSE.md](./LICENSE.md) file included in this repository.

## Background

This project was developed as part of the ‘Teamprojekt Softwareentwicklung’ course at the Technical University of Darmstadt, under the supervision of Dr.-Ing. Ragnar Mogk, for the client Functional Materials at the Institute of Materials Science, Technical University of Darmstadt.
