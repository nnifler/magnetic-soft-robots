/******************************************************************************
*                 SOFA, Simulation Open-Framework Architecture                *
*                    (c) 2006 INRIA, USTL, UJF, CNRS, MGH                     *
*                                                                             *
* This program is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This program is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this program. If not, see <http://www.gnu.org/licenses/>.        *
*******************************************************************************
* Authors: The SOFA Team and external contributors (see Authors.txt)          *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/
#pragma once

#include <CSparseSolvers/config.h>

#include <sofa/core/behavior/LinearSolver.h>
#include <sofa/component/linearsolver/iterative/MatrixLinearSolver.h>
#include <sofa/simulation/MechanicalVisitor.h>
#include <sofa/helper/OptionsGroup.h>
#include <csparse.h>
#include <sofa/component/linearsolver/ordering/OrderingMethodAccessor.h>


namespace csparsesolvers
{

// Direct linear solver based on Sparse Cholesky factorization, implemented with the CSPARSE library
template<class TMatrix, class TVector>
class SparseCholeskySolver :
    public sofa::component::linearsolver::ordering::OrderingMethodAccessor<sofa::component::linearsolver::MatrixLinearSolver<TMatrix,TVector> >
{
public:
    SOFA_CLASS(
        SOFA_TEMPLATE2(SparseCholeskySolver,TMatrix,TVector),
        SOFA_TEMPLATE(sofa::component::linearsolver::ordering::OrderingMethodAccessor, SOFA_TEMPLATE2(sofa::component::linearsolver::MatrixLinearSolver,TMatrix,TVector))
    );

    typedef TMatrix Matrix;
    typedef TVector Vector;

    SparseCholeskySolver();
    ~SparseCholeskySolver() override;

    void solve (Matrix& M, Vector& x, Vector& b) override;
    void invert(Matrix& M) override;

protected:

    cs m_matrixToInvert;
    cs* permuted_A;
    css *m_symbolicFactorization { nullptr };
    csn* m_numericFactorization { nullptr };
    int * A_i; ///< row indices, size nzmax
    int * A_p; ///< column pointers (size n+1) or col indices (size nzmax)
    sofa::type::vector<int> Previous_colptr,Previous_rowind; ///<  shape of the matrix at the previous step
    sofa::type::vector<int> perm,iperm; ///< fill reducing permutation
    sofa::type::vector<double> A_x,z_tmp,r_tmp,tmp;
    bool notSameShape;

    sofa::core::objectmodel::lifecycle::DeprecatedData d_typePermutation{this, "v24.06", "v24.12", "applyPermutation", "Ordering method is now defined using ordering components"};
    css* symbolic_Chol(cs *A);
};

#if !defined(CSPARSESOLVERS_SPARSECHOLESKYSOLVER_CPP)
extern template class SOFA_CSPARSESOLVERS_API SparseCholeskySolver< sofa::linearalgebra::CompressedRowSparseMatrix<SReal>, sofa::linearalgebra::FullVector<SReal> >;
#endif

} // namespace sofa::component::linearsolver::direct
