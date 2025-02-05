# InvertibleFVM

Implementation of the article entitled " [_Invertible finite elements for robust simulation of large deformation_](https://naml.us/paper/irving2004_invertible.pdf) "
from Irving, G., Teran, J., and Fedkiw, R., SCA 2004.

The paper introduced an algorithm for the finite element simulation of elastoplastic solids which is capable of robustly and efficiently handling arbitrarily large deformation.
This so-called Invertible Finite element Model (FVM) remains valid even when large parts of the mesh are inverted.
This SOFA implementation only addresses volumetric purely-elastic solids, but not that it can be extended to plasticity and cloth simulation.