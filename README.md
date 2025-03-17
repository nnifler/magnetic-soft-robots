# Software Project: Magnetic Soft Robotics Simulation Software

## Project Description

The Magnetic Soft Robtics (MSR) Software is designed to provide a software solution for the modeling,
simulation and visualization of the deformation behavior of magnetic soft robots under the influence of magnetic forces.
It is specifically developed for Windows and focuses on a user-friedly interface as well as robust simulation tools.

The project is based on the [Simulation Open Framework Architecture (SOFA)](https://www.sofa-framework.org),
an open-source framework for interactive physics simulations using the finite element method (FEM).

MSR offers the following features:

- Graphical user interface (GUI) for configuring simulation parameters
- Support for simulating various models with adjustable parameters
- Material and model library with approximately 35 sample materials and five sample models
- Extensibility trough custom material and model definitions
- Detailed analysis of deformation behavior, including:
  - Display of maximum defirmation along all axes
  - Visualizsation of local stress distribution within the model
- Interactive simulation of magnetic forces, where the magnetic field affects material properties and consequently deformation

MSR enables precise testing of different materials and magnetic field strengths and their effects on the behavior of soft robots.

## Getting Started

To get started with the MSR software, the following guide describes the steps to install the project on a local computer.

### Install the Project

1. Create a folder where the repository will be stored if not already existing.
2. Clone the repository from GitHub.
   1. Download the ZIP file from the Releases tab.
   2. Extract the ZIP file to your desired destination folder.\
    Note: This folder cannot be changed later. To move the installation, you must download and extract the ZIP file again.
3. Installation
   1. Open PowerShell and navigate to the project folder.
   2. Execute the installation script **once** with `./Install.ps1`.\
    Note: Running it multiple times will result in error messages.
   3. The project is now cloned to your local machine.

## Start the Application

Start the application by opening Powershell, navigating to the project folder and running `./Run.ps1`.

## License

For licensing information, refer to the [LICENSE.md](./LICENSE.md) file included in this repository.

## Background

This project was developed as part of the ‘Teamprojekt Softwareentwicklung’ course at the Technical University of Darmstadt, under the supervision of Dr.-Ing. Ragnar Mogk, for the client Functional Materials at the Institute of Materials Science, Technical University of Darmstadt.
