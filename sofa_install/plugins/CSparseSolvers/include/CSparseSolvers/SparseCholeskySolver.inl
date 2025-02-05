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

#include <CSparseSolvers/SparseCholeskySolver.h>
#include <sofa/component/linearsolver/direct/SparseCommon.h>
#include <sofa/helper/ScopedAdvancedTimer.h>

namespace csparsesolvers
{

template<class TMatrix, class TVector>
SparseCholeskySolver<TMatrix,TVector>::SparseCholeskySolver()
    : m_symbolicFactorization(nullptr), m_numericFactorization(nullptr)
{}

template<class TMatrix, class TVector>
SparseCholeskySolver<TMatrix,TVector>::~SparseCholeskySolver()
{
    if (m_symbolicFactorization) cs_sfree (m_symbolicFactorization);

    if (m_numericFactorization)
    {
        cs_nfree (m_numericFactorization);
    }
}

template<class TMatrix, class TVector>
void SparseCholeskySolver<TMatrix,TVector>::solve (Matrix& /*M*/, Vector& x, Vector& b)
{
    const int n = m_matrixToInvert.n;

    SCOPED_TIMER_VARNAME(solveTimer, "solve");

    if (m_numericFactorization)
    {
        cs_ipvec (n, perm.data(),  (double*)b.ptr() , tmp.data() );	//x = P*b , permutation on rows
        cs_lsolve (m_numericFactorization->L, tmp.data() );			//x = L\x
        cs_ltsolve (m_numericFactorization->L, tmp.data() );			//x = L'\x/
        cs_pvec (n, perm.data() , tmp.data() , (double*)x.ptr() );	 //x = P'*x , permutation on columns
    }
    else
    {
        msg_error() << "Cannot solve system due to invalid factorization";
    }
}

template<class TMatrix, class TVector>
void SparseCholeskySolver<TMatrix,TVector>::invert(Matrix& M)
{
    if (m_numericFactorization)
    {
        cs_nfree(m_numericFactorization);
    }

    M.compress();

    m_matrixToInvert.nzmax = M.getColsValue().size();	// maximum number of entries
    A_p = (int *) &(M.getRowBegin()[0]);
    A_i = (int *) &(M.getColsIndex()[0]);
    A_x.resize(m_matrixToInvert.nzmax);
    for (int i = 0; i < m_matrixToInvert.nzmax; ++i)
    {
        A_x[i] = (double)M.getColsValue()[i];
    }

    // build A with M
    m_matrixToInvert.m = M.rowBSize();					// number of rows
    m_matrixToInvert.n = M.colBSize();					// number of columns
    m_matrixToInvert.p = A_p;							// column pointers (size n+1) or col indices (size nzmax)
    m_matrixToInvert.i = A_i;							// row indices, size nzmax
    m_matrixToInvert.x = &(A_x[0]);				// numerical values, size nzmax
    m_matrixToInvert.nz = -1;							// # of entries in triplet matrix, -1 for compressed-col
    cs_dropzeros( &m_matrixToInvert );
    tmp.resize(m_matrixToInvert.n);

    {
        SCOPED_TIMER_VARNAME(factorization_permTimer, "factorization_perm");

        notSameShape = sofa::component::linearsolver::direct::compareMatrixShape( m_matrixToInvert.n , m_matrixToInvert.p , m_matrixToInvert.i, Previous_colptr.size()-1 , Previous_colptr.data() , Previous_rowind.data() );

        if( notSameShape )
        {
            perm.resize(m_matrixToInvert.n);
            iperm.resize(m_matrixToInvert.n);

            sofa::core::behavior::BaseOrderingMethod::SparseMatrixPattern pattern;
            pattern.matrixSize = m_matrixToInvert.n;
            pattern.numberOfNonZeros = m_matrixToInvert.nzmax;
            pattern.rowBegin = m_matrixToInvert.p;
            pattern.colsIndex = m_matrixToInvert.i;

            this->l_orderingMethod->computePermutation(pattern, perm.data(), iperm.data());
        }

        permuted_A = cs_permute( &m_matrixToInvert , perm.data() , iperm.data() , 1);

        if ( notSameShape )
        {
            if (m_symbolicFactorization)
            {
                cs_sfree(m_symbolicFactorization);
            }
            m_symbolicFactorization = symbolic_Chol( permuted_A );
        } // symbolic analysis

        m_numericFactorization = cs_chol (permuted_A, m_symbolicFactorization) ;		// numeric Cholesky factorization
        assert(m_numericFactorization);

        cs_free(permuted_A);
    }

    // store the shape of the matrix
    if ( notSameShape )
    {
        Previous_rowind.clear();
        Previous_colptr.resize(m_matrixToInvert.n +1);
        for (int i = 0; i < m_matrixToInvert.n; i++)
        {
            Previous_colptr[i+1] = m_matrixToInvert.p[i+1];

            for( int j=m_matrixToInvert.p[i] ; j < m_matrixToInvert.p[i+1] ; j++)
            {
                Previous_rowind.push_back(m_matrixToInvert.i[j]);
            }
        }
    }

}

template<class TMatrix, class TVector>
css* SparseCholeskySolver<TMatrix,TVector>::symbolic_Chol(cs *A)
{ //based on cs_schol
    int n, *c, *post;
    cs *C ;
    css *S ;
    if (!A) return (NULL) ;		    // check inputs
    n = A->n ;
    S = (css*)cs_calloc (1, sizeof (css)) ;	    // allocate symbolic analysis
    if (!S) return (NULL) ;		    // out of memory
    C = cs_symperm (A, S->Pinv, 0) ;	    // C = spones(triu(A(P,P)))
    S->parent = cs_etree (C, 0) ;	    // find etree of C
    post = cs_post (n, S->parent) ;	    // postorder the etree
    c = cs_counts (C, S->parent, post, 0) ; // find column counts of chol(C)
    cs_free (post) ;
    cs_spfree (C) ;
    S->cp = (int*)cs_malloc (n+1, sizeof (int)) ; // find column pointers for L
    S->unz = S->lnz = cs_cumsum (S->cp, c, n) ;
    // we do not use the permutation of SuiteSparse
    S->Q = nullptr ; // permutation on columns set to identity
    S->Pinv = nullptr; // permutation on rows set to identity
    cs_free (c) ;
    return ((S->lnz >= 0) ? S : cs_sfree (S)) ;
}

} // namespace sofa::component::linearsolver::direct
