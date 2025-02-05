# CSparseSolvers

## Overview


CSparseSolvers is SOFA plugin containing a collection of linear solver components.
These components are built on top of the CSparse library, providing you with the tools you need to solve sparse linear systems rising in SOFA simulations.

## Included Solvers

### SparseLUSolver
`SparseLUSolver` solves sparse linear systems using the LU (Lower-Upper) factorization method.

Key Features:

- LU decomposition-based solution
- Suitable for solving both symmetric and non-symmetric matrices

### SparseCholeskySolver
`SparseCholeskySolver` is designed to efficiently tackle symmetric positive-definite matrices using the Cholesky factorization method. By utilizing the CSparse library as its backbone, it ensures accuracy and speed when solving systems of equations with such matrices.

Key Features:

- Cholesky decomposition-based solution
- Optimized for symmetric positive-definite matrices

## Getting Started

Follow the instruction on [the SOFA documentation website](https://www.sofa-framework.org/community/doc/plugins/build-a-plugin-from-sources/) to build this plugin from sources.
