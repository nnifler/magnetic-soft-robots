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

#include <sofa/component/solidmechanics/fem/hyperelastic/material/HyperelasticMaterial.h>
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
class NeoHookeanIsotropic : public HyperelasticMaterial<DataTypes>{

    typedef typename DataTypes::Coord::value_type Real;
    typedef typename DataTypes::Coord Coord;
    typedef type::Mat<3,3,Real> Matrix3;
    typedef type::Mat<6,6,Real> Matrix6;
    typedef type::MatSym<3,Real> MatrixSym;
    typedef typename fem::HyperelasticMaterial<DataTypes>::triplet triplet;
    typedef typename std::pair<Real,MatrixSym> MatrixCoeffPair;

  
	class Term1:public HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm {
	public:



		Term1():HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm(){

		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=false;
		this->numberExponentialTerm=0;
		}

		virtual Real MultiplyByCoeff(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *,const  typename HyperelasticMaterial<DataTypes>::MaterialParameters &){
			return 1;
		}

		virtual Real JFunction(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
		Real val=pow(sinfo->J,(Real)(-1.0/3.0));
		return val;
		}
		virtual Real JFunctionDerivative(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterial<DataTypes>::MaterialParameters &){
			Real val=(Real)(-1.0*pow(sinfo->J*sinfo->J,(Real)(-2.0/3.0))/3.0);
			return val;
		}
		virtual Real JFunctionSecondDerivative(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
			Real val=(Real)(4.0*pow(sinfo->J,(Real)(-7.0/3.0))/9.0);
			return val;
		}

		virtual Real InvariantFunction(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param){
				Real c3=param.parameterArray[2];
				//Real c5=param.parameterArray[4];
				Real c6=param.parameterArray[5];
				Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));

			/*	Coord fiber_a=param.anisotropyDirection[0];
				Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/

				Real lambda_star=param.parameterArray[6];
				Real val=0;
				if((LambdaJJ<lambda_star) && (LambdaJJ>1)) val += -c3*sinfo->lambda;
			//	if(lambda>lambda_star) val += -c5*lambda*lambda_star+c6*lambda;
				if(LambdaJJ>=lambda_star) val += c6*sinfo->lambda;
				return val;
		}
		virtual void InvariantFunctionSPKTensor(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo, 
			const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Real c3=param.parameterArray[2];
				//Real c5=param.parameterArray[4];
				Real c6=param.parameterArray[5];
				Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
				Coord fiber_a=param.anisotropyDirection[0];
			/*	Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/
				Real lambda_star=param.parameterArray[6];
				if((LambdaJJ<lambda_star) && (LambdaJJ>1)){
				MatrixSym dlambda;
				for (int m=0; m<3; m++){
					for (int n=m; n<3; n++){
						dlambda(m,n)=fiber_a[m]*fiber_a[n]/(2*sinfo->lambda);
					}
				}
				SPKTensor -= dlambda*2*c3;
				}
			
				if(LambdaJJ>=lambda_star){
					MatrixSym dlambda;
				for (int m=0; m<3; m++){
					for (int n=m; n<3; n++){
						dlambda(m,n)=fiber_a[m]*fiber_a[n]/(2*sinfo->lambda);
					}
				}
				SPKTensor +=dlambda*2*c6;	
				}
		}
		virtual void InvariantFunctionElasticityTensor(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo, const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param,
				std::vector<triplet> &firstPairMatrix,
				std::vector<MatrixCoeffPair> & ) {	

				Real c3=param.parameterArray[2];
			//	Real c5=param.parameterArray[4];
				Real c6=param.parameterArray[5];
				Coord fiber_a=param.anisotropyDirection[0];
				/*Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/
				Real lambda_star=param.parameterArray[6];
				firstPairMatrix.resize(1);
				Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
				if((LambdaJJ<lambda_star) && (LambdaJJ>1)){
				MatrixSym aCrossa;
				for (int m=0; m<3; m++){
					for (int n=m; n<3; n++){
						aCrossa(m,n)=fiber_a[m]*fiber_a[n];
					}
				}
				 firstPairMatrix[0]=triplet(c3/(2*sinfo->lambda*sinfo->lambda*sinfo->lambda),aCrossa,aCrossa);
				}
				//if(lambda>lambda_star) firstPairMatrix.push_back(pair<Matrix3,Matrix3>(aCrossa*(-c5*lambda_star+c6)/(2*lambda*lambda),aCrossa));	
				if(LambdaJJ>=lambda_star) {
					MatrixSym aCrossa;
				for (int m=0; m<3; m++){
					for (int n=m; n<3; n++){
						aCrossa(m,n)=fiber_a[m]*fiber_a[n];
					}
				}
				firstPairMatrix[0]=triplet(-c6*(Real)1.0/((Real)2.0*sinfo->lambda*sinfo->lambda*sinfo->lambda),aCrossa,aCrossa);	
				}
		}
	};

	class Term2:public HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm {
	public:



		Term2():HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm(){

		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=0;
		}

		virtual Real MultiplyByCoeff(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *,const  typename HyperelasticMaterial<DataTypes>::MaterialParameters &){
			return 1;
		}

		virtual Real JFunction(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
		Real val=pow(sinfo->J*sinfo->J,(Real)(-1.0/3.0));
		return val;
		}
		virtual Real JFunctionDerivative(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterial<DataTypes>::MaterialParameters &){
			Real val=(Real)(-2.0*pow(sinfo->J*sinfo->J,(Real)(-1.0/3.0))/sinfo->J/3.0);
			return val;
		}
		virtual Real JFunctionSecondDerivative(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
			Real val=(Real)(10.0*pow(sinfo->J*sinfo->J,(Real)(-4.0/3.0))/9.0);
			return val;
		}

		virtual Real InvariantFunction(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename   HyperelasticMaterial<DataTypes>::MaterialParameters &param){
				Real I1=sinfo->trC;
				Real c1=param.parameterArray[0];
				Real c5=param.parameterArray[4];
				/*Coord fiber_a=param.anisotropyDirection[0];
				Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/
				Real lambda_star=param.parameterArray[6];
				Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
				Real val=c1*I1;
				if(LambdaJJ>=lambda_star) val += c5*sinfo->lambda*sinfo->lambda/2;
				return val;
		}
		virtual void InvariantFunctionSPKTensor(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo, 
			const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param,MatrixSym &SPKTensor) {
				Real c1=param.parameterArray[0];
				Real c5=param.parameterArray[4];
				Coord fiber_a=param.anisotropyDirection[0];
			/*	Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/
				MatrixSym SPKID;
				SPKID.identity();
				SPKTensor=2*c1*SPKID;
				Real lambda_star=param.parameterArray[6];
				Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
				if(LambdaJJ>=lambda_star){
				MatrixSym aCrossa;
				for (int m=0; m<3; m++){
					for (int n=m; n<3; n++){
						aCrossa(m,n)=fiber_a[m]*fiber_a[n];
					}
				}
				
				SPKTensor += c5*aCrossa;
				}
		}
		virtual void InvariantFunctionElasticityTensor(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *, const typename   HyperelasticMaterial<DataTypes>::MaterialParameters &,
				std::vector<triplet> &,
				std::vector<MatrixCoeffPair> & ) {	
		}
	};

	class Term3:public HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm {
	public:

		Term3():HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm(){

		this->includeJFactor=true;
		this->includeInvariantFactor=true;
		this->hasConstantElasticityTensor=true;
		this->numberExponentialTerm=1;
		}

		virtual Real MultiplyByCoeff(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param){
			Real c3=param.parameterArray[2];
			Real c4=param.parameterArray[3];
		/*	Coord fiber_a=param.anisotropyDirection[0];
			Coord vectCa=sinfo->deformationTensor*fiber_a;
			Real aDotCDota=dot(fiber_a,vectCa);
			Real lambda=(Real)sqrt(aDotCDota);*/
			Real lambda_star=param.parameterArray[6];
			Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
			Real val=0;
			if((LambdaJJ<lambda_star)&&(LambdaJJ>1))val +=c3/c4*exp(-c4);
			return val;
		}
		virtual Real JFunction(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
			Real val=pow(sinfo->J,(Real)(-1.0/3.0));
			return val;
		}
		virtual Real JFunctionDerivative(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
			Real val=(Real)(-1.0*pow(sinfo->J*sinfo->J,(Real)(-2.0/3.0))/3.0);
			return val;
		}
		virtual Real JFunctionSecondDerivative(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
			Real val=(Real)(4.0*pow(sinfo->J,(Real)(-7.0/3.0))/9.0);
			return val;
		}

		virtual Real InvariantFunction(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,
			const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param){
			/*	Coord fiber_a=param.anisotropyDirection[0];
				Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/
				Real c4=param.parameterArray[3];

				return c4*sinfo->lambda;
		}

		virtual void InvariantFunctionSPKTensor(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,
			const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param, MatrixSym &SPKTensor) {
				Coord fiber_a=param.anisotropyDirection[0];
			/*	Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/
				Real c4=param.parameterArray[3];
				MatrixSym dlambda;
				for (int m=0; m<3; m++){
					for (int n=m; n<3; n++){
						dlambda(m,n)=fiber_a[m]*fiber_a[n]/(2*sinfo->lambda);
					}
				}
				SPKTensor=dlambda*2*c4;
		}

		virtual void InvariantFunctionElasticityTensor(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo, const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param,
				std::vector<triplet> &firstKindMatrixPairArray,
				std::vector<MatrixCoeffPair> &) {
				Real c4=param.parameterArray[3];
				Coord fiber_a=param.anisotropyDirection[0];
			/*	Coord vectCa=sinfo->deformationTensor*fiber_a;
				Real aDotCDota=dot(fiber_a,vectCa);
				Real lambda=(Real)sqrt(aDotCDota);*/
				MatrixSym aCrossa;
				for (int m=0; m<3; m++){
					for (int n=m; n<3; n++){
						aCrossa(m,n)=fiber_a[m]*fiber_a[n];
					}
				}
				firstKindMatrixPairArray.push_back(triplet((Real)(-c4*1.0/(2*sinfo->lambda*sinfo->lambda*sinfo->lambda)),aCrossa,aCrossa));
		}
	};

class Term4:public HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm {
	public:




		Term4():HyperelasticMaterial<DataTypes>::HyperelasticMaterialTerm(){

		this->includeJFactor=true;
		this->includeInvariantFactor=false;
		this->hasConstantElasticityTensor=false;
		this->numberExponentialTerm=0;
		}

		virtual Real MultiplyByCoeff(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *,const  typename HyperelasticMaterial<DataTypes>::MaterialParameters &){
			return 1;
		}
		virtual Real JFunction(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			Real mu=param.parameterArray[0];
			Real c3=param.parameterArray[2];
			Real c4=param.parameterArray[3];
			Real c5=param.parameterArray[4];
			Real c6=param.parameterArray[5];
		/*	Coord fiber_a=param.anisotropyDirection[0];
			Coord vectCa=sinfo->deformationTensor*fiber_a;
			Real aDotCDota=dot(fiber_a,vectCa);
			Real lambda=(Real)sqrt(aDotCDota);*/
			Real lambda_star=param.parameterArray[6];
			Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
			Real val=k0*log(sinfo->J)*log(sinfo->J)/2-3*mu;
			if((LambdaJJ<lambda_star)&&(LambdaJJ>1))val +=c3-c3/c4;
			if((LambdaJJ>=lambda_star))val +=c3/c4*(exp(c4*(lambda_star-1))-1)-c3*(lambda_star-1)-c5/2*lambda_star*lambda_star-c6*lambda_star;
			return val;
		}
		virtual Real JFunctionDerivative(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			return k0*log(sinfo->J)/sinfo->J;
		}
		virtual Real JFunctionSecondDerivative(const typename  HyperelasticMaterial<DataTypes>::StrainInformation *sinfo,const  typename HyperelasticMaterial<DataTypes>::MaterialParameters &param){
			Real k0=param.parameterArray[1];
			return k0*(1-log(sinfo->J))/(sinfo->J*sinfo->J);
		}

		virtual Real InvariantFunction(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *,const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &){
				return 1;
		}
		virtual void InvariantFunctionSPKTensor(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *, 
			const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &, MatrixSym &SPKTensor) {
				SPKTensor.clear();
		}
		virtual void InvariantFunctionElasticityTensor(const  typename HyperelasticMaterial<DataTypes>::StrainInformation *, const  typename  HyperelasticMaterial<DataTypes>::MaterialParameters &,
				std::vector<triplet> &,
				std::vector<MatrixCoeffPair> & ) {	
		}
	};
	
public:
	NeoHookeanIsotropic (){
	this->materialTermArray.push_back(new Term1());
	this->materialTermArray.push_back(new Term2());
	this->materialTermArray.push_back(new Term4());
	this->materialTermArray.push_back(new Term3());
	}

#if 0
	virtual void deriveSPKTensor(  typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo, const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param,MatrixSym &SPKTensorGeneral){
		MatrixSym inversematrix;
		MatrixSym C=sinfo->deformationTensor;
		invertMatrix(inversematrix,C);
		Real I1=sinfo->trC;
		Real mu=param.parameterArray[0];
		Real k0=param.parameterArray[1];
		Real c3=param.parameterArray[2];
		Real c4=param.parameterArray[3];
		Real c5=param.parameterArray[4];
		Real c6=param.parameterArray[5];
		Real lambda_star=param.parameterArray[6];
		Coord fiber_a=param.anisotropyDirection[0];
		Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
		MatrixSym ID;
		ID.identity();
		SPKTensorGeneral=(Real)2.0*mu*pow(sinfo->J,(Real)(-2.0/3.0))*((Real)(-1.0)*I1*inversematrix/(Real)3.0+ID)+k0*log(sinfo->J)*inversematrix;
		if((LambdaJJ<lambda_star) && (LambdaJJ>1)){
			MatrixSym dlambda;
			for (int m=0; m<3; m++){
				for (int n=m; n<3; n++){
					dlambda(m,n)=fiber_a[m]*fiber_a[n]/(2*sinfo->lambda);
				}
			}
			SPKTensorGeneral += (Real)2.0*c3*(exp(c4*(LambdaJJ-1))-(Real)1)*pow(sinfo->J,(Real)(-1.0/3.0))*(dlambda-inversematrix*sinfo->lambda/(Real)6.0);
		}

		if(LambdaJJ>=lambda_star){
			MatrixSym dlambda;
			for (int m=0; m<3; m++){
				for (int n=m; n<3; n++){
					dlambda(m,n)=fiber_a[m]*fiber_a[n]/((Real)2.0*sinfo->lambda);
				}
			}
			SPKTensorGeneral +=(Real)2.0*(c5*LambdaJJ+c6)*pow(sinfo->J,(Real)(-1.0/3.0))*(dlambda-inversematrix*sinfo->lambda/(Real)6.0);
		}
		
	}
	

	virtual void applyElasticityTensor( typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo, const typename  HyperelasticMaterial<DataTypes>::MaterialParameters &param,const MatrixSym inputTensor, MatrixSym &outputTensor)  {
		MatrixSym inversematrix;
		MatrixSym C=sinfo->deformationTensor;
		invertMatrix(inversematrix,C);
		Real I1=sinfo->trC;
		Real mu=param.parameterArray[0];
		Real k0=param.parameterArray[1];
		Real c3=param.parameterArray[2];
		Real c4=param.parameterArray[3];
		Real c5=param.parameterArray[4];
		Real c6=param.parameterArray[5];
		Real lambda_star=param.parameterArray[6];
		Coord fiber_a=param.anisotropyDirection[0];
		Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
		MatrixSym ID;
		ID.identity();
		
		// C-1:H
		Real _trHC=inputTensor[0]*inversematrix[0]+inputTensor[2]*inversematrix[2]+inputTensor[5]*inversematrix[5]
		+2*inputTensor[1]*inversematrix[1]+2*inputTensor[3]*inversematrix[3]+2*inputTensor[4]*inversematrix[4];
		MatrixSym Firstmatrix;
		//C-1HC-1 convert to sym matrix
		Firstmatrix.Mat2Sym(inversematrix.SymMatMultiply(inputTensor.SymSymMultiply(inversematrix)),Firstmatrix);	
		//trH
		Real trH=inputTensor[0]+inputTensor[2]+inputTensor[5];

		outputTensor=(Real)2.0*mu*pow(sinfo->J,(Real)(-2.0/3.0))*((Real)(-1.0/3.0)*_trHC*((Real)(-1.0/3.0)*I1*inversematrix+ID)-(Real)(1.0/3.0)*trH*inversematrix+(Real)(1.0/3.0)*I1*Firstmatrix)+k0/(Real)2.0*_trHC*inversematrix-k0*log(sinfo->J)*Firstmatrix;
		if((LambdaJJ<lambda_star) && (LambdaJJ>1)){
			MatrixSym acrossa;
			for (int m=0; m<3; m++){
				for (int n=m; n<3; n++){
					acrossa(m,n)=fiber_a[m]*fiber_a[n];
				}
			}
		
		//axa:H
		Real Snd=inputTensor[0]*acrossa[0]+inputTensor[2]*acrossa[2]+inputTensor[5]*acrossa[5]+2*inputTensor[1]*acrossa[1]+2*inputTensor[3]*acrossa[3]+2*inputTensor[4]*acrossa[4];
		
		
		outputTensor +=(Real)2.0*c3*(exp(c4*(LambdaJJ-(Real)1))-(Real)1)*pow(sinfo->J,(Real)(-1.0/3.0))*(_trHC*(inversematrix*sinfo->lambda/(Real)36.0-acrossa*(Real)1.0/((Real)12.0*sinfo->lambda))+Firstmatrix*sinfo->lambda/(Real)6.0
			-Snd*inversematrix/((Real)12.0*sinfo->lambda)-Snd*acrossa/((Real)4.0*sinfo->lambda*sinfo->lambda*sinfo->lambda))+
			(Real)2.0*c3*c4*exp(c4*(LambdaJJ-1))*pow(sinfo->J,(Real)(-2.0/3.0))*(acrossa/((Real)2.0*sinfo->lambda)-sinfo->lambda*inversematrix/(Real)6.0)*(Snd/((Real)2.0*sinfo->lambda)-sinfo->lambda*_trHC/(Real)6.0);
		}

		if(LambdaJJ>=lambda_star){
		MatrixSym acrossa;
			for (int m=0; m<3; m++){
				for (int n=m; n<3; n++){
					acrossa(m,n)=fiber_a[m]*fiber_a[n];
				}
			}
	
		//axa:H
		Real Snd=inputTensor[0]*acrossa[0]+inputTensor[2]*acrossa[2]+inputTensor[5]*acrossa[5]+2*inputTensor[1]*acrossa[1]+2*inputTensor[3]*acrossa[3]+2*inputTensor[4]*acrossa[4];
		
		outputTensor +=(Real)2.0*(c5*LambdaJJ+c6)*pow(sinfo->J,(Real)(-1.0/3.0))*(_trHC*(inversematrix*sinfo->lambda/(Real)36.0-acrossa*(Real)1.0/((Real)12.0*sinfo->lambda))+Firstmatrix*sinfo->lambda/(Real)6.0
			-Snd*inversematrix/((Real)12.0*sinfo->lambda)-Snd*acrossa*(Real)1.0/((Real)4.0*sinfo->lambda*sinfo->lambda*sinfo->lambda))+
			(Real)2.0*c5*pow(sinfo->J,(Real)(-2.0/3.0))*(acrossa*(Real)1.0/((Real)2.0*sinfo->lambda)-sinfo->lambda*inversematrix*(Real)(1.0/6.0))*(Snd/((Real)2.0*sinfo->lambda)-sinfo->lambda*_trHC/(Real)6.0);
		}

		
	
	}

	virtual void ElasticityTensor( typename HyperelasticMaterial<DataTypes>::StrainInformation *sinfo, const typename HyperelasticMaterial<DataTypes>::MaterialParameters &param,Matrix6 &outputTensor)  {
		Matrix6 inter;
		Real I1=sinfo->trC;
		Real mu=param.parameterArray[0];
		Real k0=param.parameterArray[1];
		Real c3=param.parameterArray[2];
		Real c4=param.parameterArray[3];
		Real c5=param.parameterArray[4];
		Real c6=param.parameterArray[5];
		Real lambda_star=param.parameterArray[6];
		Coord fiber_a=param.anisotropyDirection[0];
		Real LambdaJJ=sinfo->lambda*pow(sinfo->J,(Real)(-1.0/3.0));
		MatrixSym ID;
		ID.identity();
		MatrixSym _C;
		invertMatrix(_C,sinfo->deformationTensor);
		Matrix6 C_H_C;
		C_H_C[0][0]=_C[0]*_C[0]; C_H_C[1][1]=_C[1]*_C[1]+_C[0]*_C[2]; C_H_C[2][2]=_C[2]*_C[2]; C_H_C[3][3]=_C[3]*_C[3]+_C[0]*_C[5]; C_H_C[4][4]=_C[4]*_C[4]+_C[2]*_C[5];
		C_H_C[5][5]=_C[5]*_C[5];
		C_H_C[1][0]=_C[0]*_C[1];C_H_C[0][1]=2*C_H_C[1][0]; 
		C_H_C[2][0]=C_H_C[0][2]=_C[1]*_C[1]; C_H_C[5][0]=C_H_C[0][5]=_C[4]*_C[4];
		C_H_C[3][0]=_C[0]*_C[3];C_H_C[0][3]=2*C_H_C[3][0]; C_H_C[4][0]=_C[1]*_C[3];C_H_C[0][4]=2*C_H_C[4][0];
		C_H_C[1][2]=_C[2]*_C[1];C_H_C[2][1]=2*C_H_C[1][2]; C_H_C[1][5]=_C[3]*_C[4];C_H_C[5][1]=2*C_H_C[1][5];
		C_H_C[3][1]=C_H_C[1][3]=_C[0]*_C[4]+_C[1]*_C[3]; C_H_C[1][4]=C_H_C[4][1]=_C[1]*_C[4]+_C[2]*_C[3];
		C_H_C[3][2]=_C[4]*_C[1];C_H_C[2][3]=2*C_H_C[3][2]; C_H_C[4][2]=_C[4]*_C[2];C_H_C[2][4]=2*C_H_C[4][2];
		C_H_C[2][5]=C_H_C[5][2]=_C[4]*_C[4];
		C_H_C[3][5]=_C[3]*_C[5];C_H_C[5][3]=2*C_H_C[3][5];
		C_H_C[4][3]=C_H_C[3][4]=_C[3]*_C[4]+_C[5]*_C[1];
		C_H_C[4][5]=_C[4]*_C[5];C_H_C[5][4]=2*C_H_C[4][5];
		Matrix6 trC_HC_;
		trC_HC_[0]=_C[0]*_C;
		trC_HC_[1]=_C[1]*_C;
		trC_HC_[2]=_C[2]*_C;
		trC_HC_[3]=_C[3]*_C;
		trC_HC_[4]=_C[4]*_C;
		trC_HC_[5]=_C[5]*_C;
		Matrix6 trID_HC_;
		trID_HC_[0]=ID[0]*_C;
		trID_HC_[1]=ID[1]*_C;
		trID_HC_[2]=ID[2]*_C;
		trID_HC_[3]=ID[3]*_C;
		trID_HC_[4]=ID[4]*_C;
		trID_HC_[5]=ID[5]*_C;
		Matrix6 trC_HID=trID_HC_.transposed();
		// C-1:H
		/*	Real _trHC=inputTensor[0]*inversematrix[0]+inputTensor[2]*inversematrix[2]+inputTensor[5]*inversematrix[5]
		+2*inputTensor[1]*inversematrix[1]+2*inputTensor[3]*inversematrix[3]+2*inputTensor[4]*inversematrix[4];
		MatrixSym Firstmatrix;
		//C-1HC-1 convert to sym matrix
		Firstmatrix.Mat2Sym(inversematrix.SymMatMultiply(inputTensor.SymSymMultiply(inversematrix)),Firstmatrix);	
		//trH
		Real trH=inputTensor[0]+inputTensor[2]+inputTensor[5];*/

	/*	inter=(Real)2.0*mu*pow(sinfo->J,(Real)(-2.0/3.0))*((Real)(1.0/3.0)*((Real)(1.0/3.0)*I1*trC_HC_-trID_HC_)-(Real)(1.0/3.0)*trC_HID+(Real)(1.0/3.0)*I1*C_H_C)+k0/(Real)2.0*trC_HC_-k0*log(sinfo->J)*C_H_C; */

		if((LambdaJJ<lambda_star) && (LambdaJJ>1)){
			MatrixSym acrossa;
			for (int m=0; m<3; m++){
				for (int n=m; n<3; n++){
					acrossa(m,n)=fiber_a[m]*fiber_a[n];
				}
			}

			//axa:H

			Matrix6 trA_A;
			trA_A[0]=acrossa[0]*acrossa;
			trA_A[1]=acrossa[1]*acrossa;
			trA_A[2]=acrossa[2]*acrossa;
			trA_A[3]=acrossa[3]*acrossa;
			trA_A[4]=acrossa[4]*acrossa;
			trA_A[5]=acrossa[5]*acrossa;
			Matrix6 trC_A;
			trC_A[0]=_C[0]*acrossa;
			trC_A[1]=_C[1]*acrossa;
			trC_A[2]=_C[2]*acrossa;
			trC_A[3]=_C[3]*acrossa;
			trC_A[4]=_C[4]*acrossa;
			trC_A[5]=_C[5]*acrossa;
			Matrix6 trA_C=trC_A.transposed();

			//	Real Snd=inputTensor[0]*acrossa[0]+inputTensor[2]*acrossa[2]+inputTensor[5]*acrossa[5]+2*inputTensor[1]*acrossa[1]+2*inputTensor[3]*acrossa[3]+2*inputTensor[4]*acrossa[4];

			inter +=(Real)2.0*c3*(exp(c4*(LambdaJJ-(Real)1.0))-(Real)1.0)*pow(sinfo->J,(Real)(-1.0/3.0))*(trC_HC_*sinfo->lambda/(Real)36.0-trA_C/((Real)12.0*sinfo->lambda)+C_H_C*sinfo->lambda/(Real)6.0
				-trC_A/((Real)12.0*sinfo->lambda)-trA_A/((Real)4.0*sinfo->lambda*sinfo->lambda*sinfo->lambda))+
				(Real)2.0*c3*c4*exp(c4*(LambdaJJ-(Real)1.0))*pow(sinfo->J,(Real)(-2.0/3.0))*(trA_A/((Real)4.0*sinfo->lambda*sinfo->lambda)-trC_A/(Real)12.0-trA_C/(Real)12.0+sinfo->lambda*sinfo->lambda*trC_HC_/(Real)36.0);
		}

		if(LambdaJJ>=lambda_star){
			MatrixSym acrossa;
			for (int m=0; m<3; m++){
				for (int n=m; n<3; n++){
					acrossa(m,n)=fiber_a[m]*fiber_a[n];
				}
			}

			//axa:H
			Matrix6 trA_A;
			trA_A[0]=acrossa[0]*acrossa;
			trA_A[1]=acrossa[1]*acrossa;
			trA_A[2]=acrossa[2]*acrossa;
			trA_A[3]=acrossa[3]*acrossa;
			trA_A[4]=acrossa[4]*acrossa;
			trA_A[5]=acrossa[5]*acrossa;
			Matrix6 trC_A;
			trC_A[0]=_C[0]*acrossa;
			trC_A[1]=_C[1]*acrossa;
			trC_A[2]=_C[2]*acrossa;
			trC_A[3]=_C[3]*acrossa;
			trC_A[4]=_C[4]*acrossa;
			trC_A[5]=_C[5]*acrossa;
			Matrix6 trA_C=trC_A.transposed();

			//Real Snd=inputTensor[0]*acrossa[0]+inputTensor[2]*acrossa[2]+inputTensor[5]*acrossa[5]+2*inputTensor[1]*acrossa[1]+2*inputTensor[3]*acrossa[3]+2*inputTensor[4]*acrossa[4];


			inter +=(Real)2.0*(c5*LambdaJJ+c6)*pow(sinfo->J,(Real)(-1.0/3.0))*(trC_HC_*sinfo->lambda/(Real)36.0-trA_C/((Real)12.0*sinfo->lambda)+C_H_C*sinfo->lambda/(Real)6.0
				-trC_A/((Real)12.0*sinfo->lambda)-trA_A/((Real)4.0*sinfo->lambda*sinfo->lambda*sinfo->lambda))+
				(Real)2.0*c5*pow(sinfo->J,(Real)(-2.0/3.0))*(trA_A/((Real)4.0*sinfo->lambda*sinfo->lambda)-trC_A/(Real)12.0-trA_C/(Real)12.0+sinfo->lambda*sinfo->lambda*trC_HC_/(Real)36.0);
		}
		outputTensor=2.0*inter;

	}
#endif

};


} // namespace sofa::component::fem
