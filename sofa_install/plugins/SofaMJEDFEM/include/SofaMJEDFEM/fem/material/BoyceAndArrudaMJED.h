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
class BoyceAndArrudaMJED : public HyperelasticMaterialMJED<DataTypes>{

    typedef typename DataTypes::Coord::value_type Real;
    typedef type::Mat<3,3,Real> Matrix3;
    typedef type::Mat<6,6,Real> Matrix6;
    typedef type::MatSym<3,Real> MatrixSym;


  class Term1:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:
    
     
		Term1():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){
		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=0;

		}

		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *){}

		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return 1;
		}

		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
		return pow(sinfo->J*sinfo->J,(Real)(-1.0/3.0));
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(-2.0*pow(sinfo->J*sinfo->J,(Real)(-1.0/3.0))/sinfo->J/3.0);
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(10.0*pow(sinfo->J*sinfo->J,(Real)(-4.0/3.0))/9.0);
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				return mu*I1/2;
		}
		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Real mu=param.parameterArray[0];
				MatrixSym Id;
				Id.identity();
				SPKTensor=mu*Id;
		}
		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &,	std::vector<MatrixSym> & ) {	
		}

		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
			std::vector<Real> &,std::vector<Real> &){
		}
	};

	class Term2:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:
    

		Term2():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){
		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=0;
		}

		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *){}

		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return 1;
		}
		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return pow(sinfo->J*sinfo->J,(Real)(-2.0/3.0));
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(-4.0*pow(sinfo->J*sinfo->J,(Real)(-2.0/3.0))/sinfo->J/3.0);
			
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(28.0*pow(sinfo->J*sinfo->J,(Real)(-5.0/3.0))/9.0);
		
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				return mu*I1*I1/160;
		}

		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				MatrixSym Id;
				Id.identity();
				SPKTensor=Id*mu/40*I1;

		}

		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &firstKindMatrixArray,	std::vector<MatrixSym> &) {	
			MatrixSym ID;
			ID.identity();	
			firstKindMatrixArray.push_back(ID);
		}

		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param,
			std::vector<Real> &FirstCoeffArray,std::vector<Real> &){
			Real mu=param.parameterArray[0];
			FirstCoeffArray.push_back(mu/40);
		}
	};

	class Term3:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:



		Term3():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){

		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=0;
		}
		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *){}

		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return 1;
		}
		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)pow(sinfo->J,(Real)-2.0);
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(-2.0*pow(sinfo->J,(Real)-3.0));
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(6.0*pow(sinfo->J,(Real)-4.0));
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				return (Real)(11.0*mu*pow(I1,3)/(64.0*1050.0));
		}

		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				MatrixSym Id;
				Id.identity();
				SPKTensor=Id*(Real)(66.0*mu*pow(I1,2)/(64.0*1050.0));
		}

		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &firstKindMatrixArray,	std::vector<MatrixSym> &) {	
			MatrixSym ID;
			ID.identity();	
			firstKindMatrixArray.push_back(ID);
		}

		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param,
			std::vector<Real> &FirstCoeffArray,std::vector<Real> &){
			Real mu=param.parameterArray[0];
			Real I1=sinfo->trC;
			FirstCoeffArray.push_back((Real)(mu*I1*33.0/(16.0*1050)));
		}
	};

	class Term4:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:



		Term4():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){

		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=0;
		}
		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *){}

		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return 1;
		}
		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)pow(sinfo->J,(Real)(-8.0/3.0));
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(-8.0*pow(sinfo->J,(Real)(-11.0/3.0))/3.0);
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(88.0*pow(sinfo->J,(Real)(-14.0/3.0))/9.0);
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				return (Real)(19.0*mu*pow(I1,(Real)4.0)/(7000*8*8*8));
		}

		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				MatrixSym Id;
				Id.identity();
				SPKTensor=Id*(Real)(2.0*19.0*4.0*mu*pow(I1,(Real)3.0)/(7000.0*8.0*8.0*8.0));
		}

		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &firstKindMatrixArray,	std::vector<MatrixSym> &) {	
			MatrixSym ID;
			ID.identity();	
			firstKindMatrixArray.push_back(ID);
		}

		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param,
			std::vector<Real> &FirstCoeffArray,std::vector<Real> &){
			Real mu=param.parameterArray[0];
			Real I1=sinfo->trC;
			FirstCoeffArray.push_back((Real)(mu*I1*I1*8.0*19.0*3.0/(7000.0*8.0*8.0*8.0)));
		}
		
	};

	class Term5:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:



		Term5():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){

		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=0;
		}
		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *){}

		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return 1;
		}
		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)pow(sinfo->J,(Real)(-10.0/3.0));
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(-10.0*pow(sinfo->J,(Real)(-13.0/3.0))/3.0);
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
			return (Real)(130.0*pow(sinfo->J,(Real)(-16.0/3.0))/9.0);
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				return (Real)(519.0*mu*pow(I1,(Real)5.0)/(64.0*64*673750));
		}

		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,
			const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Real I1=sinfo->trC;
				Real mu=param.parameterArray[0];
				MatrixSym Id;
				Id.identity();
				SPKTensor=Id*(Real)(2.0*5.0*519.0*mu*pow(I1,(Real)4.0)/(64.0*64.0*673750.0));
		}

		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &firstKindMatrixArray,	std::vector<MatrixSym> &) {	
			MatrixSym ID;
			ID.identity();	
			firstKindMatrixArray.push_back(ID);
		}

		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param,
			std::vector<Real> &FirstCoeffArray,std::vector<Real> &){
			Real mu=param.parameterArray[0];
			Real I1=sinfo->trC;
			FirstCoeffArray.push_back((Real)(mu*pow(I1,(Real)3.0)*40.0*519.0/(64.0*64.0*673750.0)));
		}
	};

	class Term6:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:



		Term6():HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){

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
			return (Real)(k0*sinfo->logJ*sinfo->logJ/2.0-mu*(3.0/2.0+9.0/(20.0*8.0)+11.0*27.0/(1050.0*64.0)+pow(3.0,4.0)*19.0/(7000*pow(8.0,3.0))+pow(3.0,5.0)*519.0/(673750.0*64.0*64.0)));
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			return k0*sinfo->logJ/sinfo->J;
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			return k0*(1-sinfo->logJ)/(sinfo->J*sinfo->J);
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
				return 1;
		}
		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &, MatrixSym &SPKTensor) {
				SPKTensor.clear();
		}

		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &,	std::vector<MatrixSym> & ) {
		}
		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<Real> &,std::vector<Real> &){
		}
	};
public:
  BoyceAndArrudaMJED () {
	this->materialTermArray.push_back(new Term1() );
	this->materialTermArray.push_back(new Term2());
	this->materialTermArray.push_back(new Term3() );
	this->materialTermArray.push_back(new Term4());
	this->materialTermArray.push_back(new Term5()); 
	this->materialTermArray.push_back(new Term6()); 
  }

  


};
  	
	


} // namespace sofa::component::fem
