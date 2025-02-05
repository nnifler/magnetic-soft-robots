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

#include <sofa/component/linearsolver/iterative/MatrixLinearSolver.h>
#include <csparse.h>
#include <sofa/component/linearsolver/ordering/OrderingMethodAccessor.h>
#include <sofa/helper/OptionsGroup.h>

namespace csparsesolvers
{

//defaut structure for a LU factorization
template<class Real>
class SparseLUInvertData : public sofa::component::linearsolver::MatrixInvertData {
public :

    css *S; ///< store the permutations and the number of non null values by rows and by lines of the LU factorization
    csn *N; ///< store the partial pivot and the LU factorization
    cs A;
    cs* permuted_A;
    sofa::type::vector<int> perm,iperm; ///< fill reducing permutation
    sofa::type::vector<int> Previous_colptr,Previous_rowind; ///< shape of the matrix at the previous step
    sofa::type::vector<sofa::SignedIndex> A_i, A_p;
    sofa::type::vector<Real> A_x;
    Real * tmp;
    bool notSameShape;
    SparseLUInvertData()
    {
        S=nullptr; N=nullptr; tmp=nullptr;
    }

    ~SparseLUInvertData()
    {
        if (S) cs_sfree (S);
        if (N) cs_nfree (N);
        if (tmp) cs_free (tmp);
    }
};

// Direct linear solver based on Sparse LU factorization, implemented with the CSPARSE library
template<class TMatrix, class TVector, class TThreadManager= sofa::component::linearsolver::NoThreadManager>
class SparseLUSolver :
    public sofa::component::linearsolver::ordering::OrderingMethodAccessor<sofa::component::linearsolver::MatrixLinearSolver<TMatrix,TVector,TThreadManager> >
{
public:
    SOFA_CLASS(
        SOFA_TEMPLATE3(SparseLUSolver,TMatrix,TVector,TThreadManager),
        SOFA_TEMPLATE(sofa::component::linearsolver::ordering::OrderingMethodAccessor,
            SOFA_TEMPLATE3(sofa::component::linearsolver::MatrixLinearSolver,TMatrix,TVector,TThreadManager))
    );

    typedef TMatrix Matrix;
    typedef TVector Vector;
    typedef typename Matrix::Real Real;

    typedef sofa::component::linearsolver::MatrixLinearSolver<TMatrix,TVector,TThreadManager> Inherit;

    sofa::Data<double> f_tol; ///< tolerance of factorization

    void solve (Matrix& M, Vector& x, Vector& b) override;
    void invert(Matrix& M) override;

    SparseLUSolver();

    bool supportNonSymmetricSystem() const override { return true; }

    void parse(sofa::core::objectmodel::BaseObjectDescription *arg) override;

protected :

    sofa::core::objectmodel::lifecycle::DeprecatedData d_typePermutation{this, "v24.06", "v24.12", "applyPermutation", "Ordering method is now defined using ordering components"};
    sofa::Data<int> d_L_nnz; ///< Number of non-zero values in the lower triangular matrix of the factorization. The lower, the faster the system is solved.

    css* symbolic_LU(cs *A);

    sofa::component::linearsolver::MatrixInvertData * createInvertData() override {
        return new SparseLUInvertData<Real>();
    }

    std::unique_ptr<sofa::linearalgebra::CompressedRowSparseMatrix<Real> > Mfiltered;

};


#if !defined(CSPARSESOLVERS_SPARSELUSOLVER_CPP)
extern template class SOFA_CSPARSESOLVERS_API SparseLUSolver< sofa::linearalgebra::CompressedRowSparseMatrix< SReal>, sofa::linearalgebra::FullVector<SReal> >;
extern template class SOFA_CSPARSESOLVERS_API SparseLUSolver< sofa::linearalgebra::CompressedRowSparseMatrix<sofa::type::Mat<3,3,SReal>>, sofa::linearalgebra::FullVector<SReal> >;
#endif

} // namespace sofa::component::linearsolver::direct
