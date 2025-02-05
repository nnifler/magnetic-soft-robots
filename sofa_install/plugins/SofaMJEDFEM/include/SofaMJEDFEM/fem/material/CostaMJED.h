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
class CostaMJED: public HyperelasticMaterialMJED<DataTypes>{

    typedef typename DataTypes::Coord::value_type Real;
    typedef type::Mat<3,3,Real> Matrix3;
    typedef type::Mat<6,6,Real> Matrix6;
    typedef type::MatSym<3,Real> MatrixSym;


  public:

	class Term1:public HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm {
	public:
	
		Real bff,bfs,bss,bfn,bsn,bnn;
		MatrixSym D1,D2,D3;
		Real beta,gamma;
		Term1(const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param):HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm(){
		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=1;

		this->bff=param.parameterArray[2];
		this->bfs=param.parameterArray[3];
		this->bss=param.parameterArray[4];
		this->bfn=param.parameterArray[5];
		this->bsn=param.parameterArray[6];
		this->bnn=param.parameterArray[7];

		Real d1=sqrt(bff);
		Real d2=bfs/d1;
		Real d3=bfn/d1;
		if(bss-d2*d2>0) this->beta=(Real)1;
		else this->beta=(Real)(-1);
		Real d2prime=sqrt(this->beta*(bss-d2*d2));
		Real d3prime=(bsn-d2*d3)/(this->beta*d2prime);
		if(bnn-this->beta*d3prime*d3prime-d3*d3>0) this->gamma=(Real)1;
		else this->gamma=(Real)(-1);
		Real d3snde=sqrt(this->gamma*(bnn-this->beta*d3prime*d3prime-d3*d3));
		this->D1=MatrixSym(d1,0,d2,0,0,d3);
		this->D2=MatrixSym(0,0,d2prime,0,0,d3prime);
		this->D3=MatrixSym(0,0,0,0,0,d3snde);
		

		}

		virtual void CalculFunction(typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo){
				MatrixSym Id;
				Id.identity();
				sinfo->E=(sinfo->deformationTensor-Id)/2.0;
		}
		virtual Real MultiplyByCoeff(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
				Real a=param.parameterArray[0];
				return (Real)(1.0/2.0*a);
		}

		virtual Real JFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
				return (Real)(pow(sinfo->J,(Real)(-4.0/3.0)));
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
				return (Real)(-4.0*pow(sinfo->J,(Real)(-7.0/3.0))/3.0);
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
                                return (Real)(28.0*pow(sinfo->J,(Real)(-10.0/3.0))/9.0);
		}

		virtual Real InvariantFunction(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &){
				Real val=bff*sinfo->E[0]*sinfo->E[0]+2*bfs*sinfo->E[1]*sinfo->E[1]+bss*sinfo->E[2]*sinfo->E[2]+2*bfn*sinfo->E[3]*sinfo->E[3]+2*bsn*sinfo->E[4]*sinfo->E[4]+bnn*sinfo->E[5]*sinfo->E[5];
				return val;
		}
		virtual void InvariantFunctionSPKTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &, MatrixSym &SPKTensor) {
				SPKTensor=MatrixSym((Real)2.0*bff*sinfo->E[0],(Real)2.0*bfs*sinfo->E[1],(Real)2.0*bss*sinfo->E[2],(Real)2.0*bfn*sinfo->E[3],(Real)2.0*bsn*sinfo->E[4],(Real)2.0*bnn*sinfo->E[5]);
		}
		virtual void InvariantMatricesElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
				std::vector<MatrixSym> &,
				std::vector<MatrixSym> &matrixsecond ) {	
				matrixsecond.push_back(this->D1);
				matrixsecond.push_back(this->D2);
				matrixsecond.push_back(this->D3); 
		}

		virtual void InvariantScalarFactorElasticityTensor(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *, const  typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &,
			std::vector<Real> &,std::vector<Real> &coeffSecond){
				coeffSecond.push_back(1);
				coeffSecond.push_back(this->beta);
				coeffSecond.push_back(this->gamma);

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
			Real a=param.parameterArray[0];
			return (Real)(k0*(sinfo->J*sinfo->logJ-sinfo->J-1)-a/2.0);
		}
		virtual Real JFunctionDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			return k0*sinfo->logJ;
		}
		virtual Real JFunctionSecondDerivative(const typename HyperelasticMaterialMJED<DataTypes>::StrainInformation *sinfo,const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			return k0/sinfo->J;
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
	CostaMJED (const typename HyperelasticMaterialMJED<DataTypes>::MaterialParameters &param){
	this->materialTermArray.push_back(new Term2() );
	this->materialTermArray.push_back(new Term1(param));
	}
	

};


} // namespace sofa::component::fem
