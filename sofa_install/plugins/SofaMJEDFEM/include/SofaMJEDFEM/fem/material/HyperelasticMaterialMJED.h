/******************************************************************************
*                             SOFA MJED FEM plugin                            *
*                                (c) 2006 Inria                               *
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
* Authors: see Authors.md                                                     *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/
#pragma once

#include <sofa/core/topology/BaseMeshTopology.h>
#include <sofa/core/topology/TopologyData.h>
#include <sofa/type/Vec.h>
#include <sofa/type/Mat.h>
#include <sofa/type/MatSym.h>
#include <string>

#ifdef SOFA_HAVE_EIGEN2
//#include <Eigen/Core>
#include <Eigen/QR>
#include <Eigen/Eigenvalues>
#endif
namespace sofa::component::fem
{
using namespace std;
using namespace sofa::defaulttype;
using namespace sofa::core::topology;

/** a Class that describe a generic hyperelastic material .
The material is described based on continuum mechanics and the description is independent
to any discretization method like the finite element method.
A material is generically described by a strain energy function and its first and second derivatives.
In practice the energy is the sum of several energy terms which depends on 2 quantities :
the determinant of the deformation gradient J and the right Cauchy Green deformation tensor */


template<class DataTypes>
class HyperelasticMaterialMJED
{
public:
    typedef typename DataTypes::Coord Coord;
    typedef typename Coord::value_type Real;
        typedef typename type::MatSym<3,Real> MatrixSym;
        typedef typename type::Mat<3,3,Real> Matrix3;
        typedef typename type::Mat<6,6,Real> Matrix6;

         #ifdef SOFA_HAVE_EIGEN2
    typedef typename Eigen::SelfAdjointEigenSolver<Eigen::Matrix<Real,3,3> >::MatrixType EigenMatrix;
  typedef typename Eigen::SelfAdjointEigenSolver<Eigen::Matrix<Real,3,3> >::RealVectorType CoordEigen;
  #endif
   virtual ~HyperelasticMaterialMJED(){}

        /** structure that store the parameters required to that are necessary to compute the strain energy
        The material parameters might be constant in space (homogeneous material) or not */
        struct MaterialParameters {
                /** an array of Real values that correspond to the material parameters : the size depends on the material,
                e.g. 2 Lame coefficients for St-Venant Kirchhoff materials */
                vector<Real> parameterArray;
                /** the direction of anisotropy in the rest configuration  : the size of the array is 0 if the material is
                isotropic, 1 if it is transversely isotropic and 2 for orthotropic materials (assumed to be orthogonal to each other)*/
                vector<Coord> anisotropyDirection;
                /** for viscous part, give the real alphai and taui such as alpha(t)= alpha0+sum(1,N)alphaiexp(-t/taui)*/
                vector<Real> parameterAlpha;
                vector<Real> parameterTau;//starting with delta t the time step
        };

        /** Structure that stores the strain invariants and other information about the deformation.
        For instance one can store the eigenvalues and eigenvectors of C.
        This structure is set and modified by the 3 invariant functions in this order : InvariantFunctionSPKTensor,
        eventually InvariantFunction and InvariantFunctionElasticityTensor.
        It is therefore likely that InvariantFunctionSPKTensor will be the function which computes all required invariants.
        The boolean hasBeenInitialized is used to test if the invariants has been already computed */



public:
    class StrainInformation
        {
        public:

        std::vector<Real> summfg;
        std::vector<Real> coeffs;
        std::vector<bool> Exponential;
        std::vector<int> counters;
        std::vector<Real> numbers;
        std::vector<Real> functf;
        std::vector<Real> functg;
        std::vector<Real> summDfg;
        std::vector<Real> summD2fg;
        std::vector<Real> functDf;
        std::vector<Real> functD2f;
        std::vector<MatrixSym> summfS;
        std::vector<MatrixSym> SPK;
        std::vector<MatrixSym> summDfS;
        unsigned int taille;
          /// Trace of C = I1
      Real trC;
          Real J;
          Real lambda;
          /// Trace of C^2 : I2 = (trCSquare - trC^2)/2
      Real trCsquare;

          /// boolean indicating whether the invariants have been computed
          bool hasBeenInitialized;
        /// right Cauchy-Green deformation tensor C (gradPhi^T gradPhi)
          MatrixSym deformationTensor;
#ifdef SOFA_HAVE_EIGEN2
        EigenMatrix Evect;
        CoordEigen Evalue;
#endif
                Real logJ;
                MatrixSym E;

        public:
          StrainInformation() : hasBeenInitialized(false) {
          }

          virtual ~StrainInformation(){}
    };

        /** A term in the hyperelastic material : assumes that either includeJFactor or includeInvariantFactor is true */
        class HyperelasticMaterialTerm {
        protected:
                /// whether this term has a dependence on J = determinant of the deformation gradient
                bool includeJFactor;
                /** whether this term has a dependence on the invariants of C = right Cauchy Green deformation tensor */
                bool includeInvariantFactor;
                /// whether the elasticity tensor is constant (=independent of C ) of not
                bool hasConstantElasticityTensor;

                int numberExponentialTerm;
                /// if the term is in exp(sum fg ), 0 for no exp, 1 if it is in the first exp, 2 if exp (fg) +exp (fg)...
        public:


                /// whether this term is multiplied by a conastant(in case of exponential term it can't be included in functionJ nor functg)
                virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param)=0;
                /// whether this term has a dependence on J = determinant of the deformation gradient
                inline bool includeAJFactor() const {
                        return includeJFactor;
                }

                /** whether this term has a dependence on the invariants of C = right Cauchy Green deformation tensor */
                inline bool includeAnInvariantFactor() const {
                        return includeInvariantFactor;
                }

                /// whether the elasticity tensor is constant (=independent of C ) of not
                inline bool hasAConstantElasticityTensor() const {
                        return hasConstantElasticityTensor;
                }

                inline int getNumberOfExponential() const {
                        return numberExponentialTerm;
                }

                //calculates values that are needed for several functions
                virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo)=0;
                /// returns the JFunction value used in the strain energy
                virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param)=0;

                /// returns the derivative of the JFunction  used in the strain energy derivative
                virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param)=0;

                /// returns the second derivative of the JFunction  used in the strain energy second derivative
                virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param)=0;


                /** returns the InvariantFunction value used in the strain energy
                This function is called only if includeJFactor==true  and includeInvariantFactor==true */
                virtual Real InvariantFunction(	const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param)=0;

            /** sets the second Piola-Kirchhoff stress tensor corresponding to twice the derivative of
                the strain energy with respect to the rightCauchyGreen Deformation tensor.
                Note that this function is always called first but only if includeInvariantFactor==true */
                virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo, const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) =0;


            /** sets the Elasticity tensor corresponding to twice the second derivative of
                the strain energy with respect to the rightCauchyGreen Deformation tensor.
                The Elasticity tensor is described as 2 arrays of Matrices (see documentation) and two arrays of scalars
                These functions are called after InvariantFunctionSPKTensor if includeInvariantFactor==true */
                virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo, const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param,
                        std::vector<MatrixSym> &firstKindMatrixTripletArray,
                        std::vector<MatrixSym> &secondKindMatrixPairArray )=0;


                virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo, const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param,
                        std::vector<Real> &FirstCoeffArray,std::vector<Real> &SecondCoeffArray)=0;

                HyperelasticMaterialTerm() : includeJFactor(false), includeInvariantFactor(false),hasConstantElasticityTensor(false){
                }

                virtual ~HyperelasticMaterialTerm() {}

                friend class HyperelasticMaterialMJED<DataTypes>;
        };

protected:
        /// the hyperelastic material is discribed as a set of terms each one being a function of J and the invariants of C
         std::vector<HyperelasticMaterialTerm *> materialTermArray;
public:

        /** returns the array of Hyperelastic Material terms */
        const std::vector<HyperelasticMaterialTerm *> &getMaterialTermArray(){
                return materialTermArray;
        }

        /** returns the strain energy of the current configuration */
        virtual Real getStrainEnergy(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo, const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param) {
                        Real energy=(Real)0;
                        Real fg=0;
                        Real coefficient=1;
                        sinfo->summfg.resize(0);
                        sinfo->functf.resize(0);
                        sinfo->functg.resize(0);
                        sinfo->counters.resize(0);
                        sinfo->numbers.resize(0);
                        sinfo->Exponential.resize(0);
                        sinfo->coeffs.resize(0);

                        bool Expo=false;
                        typename std::vector<HyperelasticMaterialTerm *>::const_iterator  it;
                        it=this->materialTermArray.begin();
                        for (;it!=this->materialTermArray.end();it++) {
                                (*it)->CalculFunction(sinfo);
                                sinfo->counters.push_back((*it)->numberExponentialTerm);
                                sinfo->numbers.push_back((*it)->MultiplyByCoeff(sinfo,param));
                                if((*it)->includeJFactor && (*it)->includeInvariantFactor){
                                        sinfo->functf.push_back((*it)->JFunction(sinfo,param));
                                        sinfo->functg.push_back((*it)->InvariantFunction(sinfo,param));
                                }
                                else if((*it)->includeInvariantFactor){
                                        sinfo->functf.push_back(1);
                                        sinfo->functg.push_back((*it)->InvariantFunction(sinfo,param));
                                }
                                else if((*it)->includeJFactor){
                                        sinfo->functf.push_back((*it)->JFunction(sinfo,param));
                                        sinfo->functg.push_back(1);
                                }
                        }

                        fg=sinfo->functf[0]*sinfo->functg[0];
                        coefficient=sinfo->numbers[0];

                        if(sinfo->counters[0]==0) Expo=false;
                        else Expo=true;
                        for(unsigned int m=1; m<sinfo->counters.size();++m){
                                if (sinfo->counters[m]==sinfo->counters[m-1]){
                                        fg += sinfo->functf[m]*sinfo->functg[m];
                                        coefficient=sinfo->numbers[m];
                                        if(sinfo->counters[m]==0) Expo=false;
                                        else Expo=true;
                                }
                                else{
                                        sinfo->summfg.push_back(fg);
                                        sinfo->Exponential.push_back(Expo);
                                        sinfo->coeffs.push_back(coefficient);
                                        fg=sinfo->functf[m]*sinfo->functg[m];
                                        coefficient=sinfo->numbers[m];

                                }
                        }

                        sinfo->coeffs.push_back(coefficient);
                        sinfo->Exponential.push_back(Expo);
                        sinfo->summfg.push_back(fg);
                        sinfo->taille=sinfo->summfg.size();
                        for(unsigned int w=0;w<sinfo->taille;++w){
                                if(!sinfo->Exponential[w]){
                                        energy+=(Real)(sinfo->summfg[w]*sinfo->coeffs[w]);
                                }
                                else {
                                        energy+=(Real)(exp(sinfo->summfg[w])*sinfo->coeffs[w]);
                                }
                        }
                        return energy;
        }
        };


} // namespace sofa::component::fem
