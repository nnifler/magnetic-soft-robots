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
#include <string>


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
class NeoHookeanMJED : public HyperelasticMaterialMJED<DataTypes>{

  typedef typename DataTypes::Coord::value_type Real;
  typedef type::Mat<3,3,Real> Matrix3;
  typedef type::Mat<6,6,Real> Matrix6;
  typedef type::MatSym<3,Real> MatrixSym;

	class Term1:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:
	
		Term1():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){
		this->includeJFactor=false;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=0;
		}

		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *){}

		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return 1;
		}

		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
		return 1;
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){

			return 0;
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){

			return 0;
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				return mu*I1/2;
		}
		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Real mu=param.parameterArray[0];
				SPKTensor[0]=SPKTensor[2]=SPKTensor[5]=mu;
				SPKTensor[1]=SPKTensor[4]=SPKTensor[3]=0;
		}
		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &,
				std::vector<MatrixSym> & ) {	
		}
		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
			std::vector<Real> &,std::vector<Real> &){
		}
		
	};

	class Term2:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:

		Term2():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){
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
		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			Real mu=param.parameterArray[0];
			//return k0*(J-1)*(J-1)/2-mu*3/2;
			//return k0*(J-1)*(J-1)/2-mu*3/2
			return sinfo->logJ*(k0*sinfo->logJ/2)-mu*3/2-mu*sinfo->logJ;
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			Real mu=param.parameterArray[0];
			//return k0*(J-1);
			return (k0*sinfo->logJ- mu)/sinfo->J;
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			Real mu=param.parameterArray[0];
			//return k0;
			return (k0*(1-sinfo->logJ)+mu)/(sinfo->J*sinfo->J);
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
	NeoHookeanMJED (){
	this->materialTermArray.push_back(new Term1() );
	this->materialTermArray.push_back(new Term2());
	}
	
};


} // namespace sofa::component::fem
