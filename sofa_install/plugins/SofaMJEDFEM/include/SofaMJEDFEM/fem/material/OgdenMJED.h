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

#include <SofaMJEDFEM/fem/material/HyperelasticMaterialMJED.h>
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

/** a Class that describe a generic hyperelastic material : exemple of Boyce and Arruda
The material is described based on continuum mechanics and the description is independent
to any discretization method like the finite element method. 
A material is generically described by a strain energy function and its first and second derivatives.
In practice the energy is the sum of several energy terms which depends on 2 quantities :
the determinant of the deformation gradient J and the right Cauchy Green deformation tensor */



template<class DataTypes>
class OgdenMJED: public HyperelasticMaterialMJED<DataTypes>{

    typedef typename DataTypes::Coord::value_type Real;
    typedef type::Mat<3,3,Real> Matrix3;
    typedef type::Mat<6,6,Real> Matrix6;
    typedef type::MatSym<3,Real> MatrixSym;
    typedef type::Vec<3,Real> Vect;
   #ifdef SOFA_HAVE_EIGEN2
    typedef typename Eigen::SelfAdjointEigenSolver<Eigen::Matrix<Real,3,3> >::MatrixType EigenMatrix;
    typedef typename Eigen::SelfAdjointEigenSolver<Eigen::Matrix<Real,3,3> >::RealVectorType CoordEigen;
  #endif


  public:

	  class Term1:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm{

		  Real alpha1,mu1;
	  

	public:
	
		Term1(const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param):HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){
		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=false;
		this->numberExponentialTerm=0;
		this->mu1=param.parameterArray[1];
		this->alpha1=param.parameterArray[2];
		}

		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo){
#ifdef SOFA_HAVE_EIGEN2	
                MatrixSym C=sinfo->deformationTensor;
                EigenMatrix CEigen;
		CEigen(0,0)=C[0];CEigen(0,1)=C[1];CEigen(1,0)=C[1];CEigen(1,1)=C[2];
		CEigen(1,2)=C[4];CEigen(2,1)=C[4];CEigen(2,0)=C[3];CEigen(0,2)=C[3];CEigen(2,2)=C[5];
		Eigen::SelfAdjointEigenSolver<EigenMatrix> Vect(CEigen,true);
		sinfo->Evalue=Vect.eigenvalues();
		sinfo->Evect=Vect.eigenvectors();
#else
                SOFA_UNUSED(sinfo);
#endif
		}

		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
				return 1;
		}

		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){	
			return (Real)(pow(sinfo->J,(Real)(-alpha1/3.0)));
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(-alpha1*pow(sinfo->J,(Real)((-alpha1-3.0)/3.0))/3.0);
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){	
			return (Real)(alpha1*(alpha1+3.0)*pow(sinfo->J,(Real)((-alpha1-6.0)/3.0))/9.0);
		}

#ifdef SOFA_HAVE_EIGEN2								
		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
				Real val=pow(sinfo->Evalue[0],alpha1/(Real)2)+pow(sinfo->Evalue[1],alpha1/(Real)2)+pow(sinfo->Evalue[2],alpha1/(Real)2);			
				return val*mu1/(alpha1*alpha1);
		}
#else
		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
      return 1; // function must return a value!
		}
#endif
#ifdef SOFA_HAVE_EIGEN2	
		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &, MatrixSym &SPKTensor) {
				Matrix3 Pinverse;
				Pinverse(0,0)=sinfo->Evect(0,0);Pinverse(1,1)=sinfo->Evect(1,1);Pinverse(2,2)=sinfo->Evect(2,2);Pinverse(0,1)=sinfo->Evect(1,0);
				Pinverse(1,0)=sinfo->Evect(0,1);Pinverse(2,0)=sinfo->Evect(0,2);
				Pinverse(0,2)=sinfo->Evect(2,0);Pinverse(2,1)=sinfo->Evect(1,2);Pinverse(1,2)=sinfo->Evect(2,1);
				MatrixSym Dalpha_1=MatrixSym(pow(sinfo->Evalue[0],(Real)(alpha1/2.0-1.0)),0,pow(sinfo->Evalue[1],(Real)(alpha1/2.0-1)),0,0,pow(sinfo->Evalue[2],(Real)(alpha1/2.0-1.0)));
				MatrixSym Calpha_1;Matrix3 Ca;
				Ca=Pinverse.transposed()*Dalpha_1.SymMatMultiply(Pinverse);
				Calpha_1.Mat2Sym(Ca,Calpha_1);
				SPKTensor=mu1/alpha1*Calpha_1;
		}
#else
		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &, MatrixSym &) {
		}
#endif



#ifdef SOFA_HAVE_EIGEN2
		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &,	std::vector<MatrixSym> &secondKindMatrixArray) {	
				Matrix3 Pinverse;
				Pinverse(0,0)=sinfo->Evect(0,0);Pinverse(1,1)=sinfo->Evect(1,1);Pinverse(2,2)=sinfo->Evect(2,2);
				Pinverse(0,1)=sinfo->Evect(1,0);Pinverse(1,0)=sinfo->Evect(0,1);Pinverse(2,0)=sinfo->Evect(0,2);
				Pinverse(0,2)=sinfo->Evect(2,0);Pinverse(2,1)=sinfo->Evect(1,2);Pinverse(1,2)=sinfo->Evect(2,1);
				MatrixSym Dalpha_2=MatrixSym(pow(sinfo->Evalue[0],alpha1/(Real)4.0-(Real)1.0),0,pow(sinfo->Evalue[1],alpha1/(Real)4.0-(Real)1.0),0,0,pow(sinfo->Evalue[2],alpha1/(Real)4.0-(Real)1.0));
				MatrixSym Calpha_2;Matrix3 Ca;
				Ca=Pinverse.transposed()*Dalpha_2.SymMatMultiply(Pinverse);
				Calpha_2.Mat2Sym(Ca,Calpha_2);
				secondKindMatrixArray.push_back(Calpha_2);
		}
#else
		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &,	std::vector<MatrixSym> &) {	
		}
#endif

		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
			std::vector<Real> &,std::vector<Real> &secondCoeffArray){
			secondCoeffArray.push_back(mu1*(alpha1/(Real)2.0-(Real)1.0)/alpha1);
		}
	};

	class Term2:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:

		Real k0,mu1,alpha1;

		Term2(const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param):HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){
		this->k0=param.parameterArray[0];
		this->mu1=param.parameterArray[1];
		this->alpha1=param.parameterArray[2];
		this->includeJFactor=true;
		this->includeInvariantFactor=false;
		this->hasConstantElasticityTensor=false;
		this->numberExponentialTerm=0;
		}

		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo){
			sinfo->logJ=log(sinfo->J);
		}
		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return 1;
		}
		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return k0*sinfo->logJ*sinfo->logJ/(Real)2.0-(Real)3.0*mu1/(alpha1*alpha1);
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return k0*sinfo->logJ/sinfo->J;
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return k0*(1-sinfo->logJ)/(sinfo->J*sinfo->J);
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
				return 1;
		}
		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &, MatrixSym &SPKTensor) {
				SPKTensor.clear();
		}

		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &,
				std::vector<MatrixSym> & ) {	
		}
		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
			std::vector<Real> &,std::vector<Real> &){
		}
		
	};

	
public:
	OgdenMJED (const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
	this->materialTermArray.push_back(new Term1(param));
	this->materialTermArray.push_back(new Term2(param));
	}
};


} // namespace sofa::component::fem
