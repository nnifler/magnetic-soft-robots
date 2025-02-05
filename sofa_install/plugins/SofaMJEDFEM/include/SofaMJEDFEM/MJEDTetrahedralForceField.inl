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

#include <sofa/gl/gl.h>
#include <SofaMJEDFEM/fem/material/BoyceAndArrudaMJED.h>
#include <SofaMJEDFEM/fem/material/VerondaWestmanMJED.h>
#include <SofaMJEDFEM/fem/material/NeoHookeanMJED.h>
#include <SofaMJEDFEM/fem/material/MooneyRivlinMJED.h>
#include <SofaMJEDFEM/fem/material/STVenantKirchhoffMJED.h>
#include <SofaMJEDFEM/fem/material/HyperelasticMaterialMJED.h>
#include <SofaMJEDFEM/fem/material/CostaMJED.h>
#include <SofaMJEDFEM/fem/material/OgdenMJED.h>
#include <SofaMJEDFEM/MJEDTetrahedralForceField.h>

#include <sofa/core/visual/VisualParams.h>
#include <sofa/defaulttype/VecTypes.h>
#include <sofa/component/statecontainer/MechanicalObject.h>
#include <sofa/core/ObjectFactory.h>
#include <fstream> // for reading the file
#include <iostream> //for debugging
#include <sofa/gl/template.h>
#include <sofa/core/behavior/ForceField.inl>
#include <sofa/core/topology/TopologyData.inl>
#include <algorithm>
#include <iterator>

namespace sofa::component::forcefield
{

using namespace sofa::defaulttype;
using namespace core::topology;

template< class DataTypes>
void MJEDTetrahedralForceField<DataTypes>::createTetrahedronRestInformation(unsigned int tetrahedronIndex,
                                                                            TetrahedronRestInformation &tinfo,
                                                                            const Tetrahedron &,
                                                                            const sofa::type::vector<unsigned int> &,
                                                                            const sofa::type::vector<double> &)
{
    const vector< Tetrahedron > &tetrahedronArray=_topology->getTetrahedra() ;
    const std::vector< Edge> &edgeArray=_topology->getEdges() ;
    unsigned int j,m,n;
    int k,l;
    typename DataTypes::Real volume;
    //	typename DataTypes::Coord point[4];



    const typename DataTypes::VecCoord& restPosition=this->mstate->read(sofa::core::ConstVecCoordId::restPosition())->getValue();

    ///describe the indices of the 4 tetrahedron vertices
    const Tetrahedron &t= tetrahedronArray[tetrahedronIndex];
    BaseMeshTopology::EdgesInTetrahedron te=_topology->getEdgesInTetrahedron(tetrahedronIndex);

    // store the point position

    for(j=0;j<4;++j)
      tinfo.pointP[j]=restPosition[t[j]];
    /// compute 6 times the rest volume
    volume=dot(cross(tinfo.pointP[2]-tinfo.pointP[0],tinfo.pointP[3]-tinfo.pointP[0]),tinfo.pointP[1]-tinfo.pointP[0]);
    /// store the rest volume
    tinfo.volScale =(Real)(1.0/volume);
    tinfo.restVolume = fabs(volume/6);
    // store shape vectors at the rest configuration
    for(j=0;j<4;++j) {
      if (!(j%2))
        tinfo.shapeVector[j]=-cross(tinfo.pointP[(j+2)%4] - tinfo.pointP[(j+1)%4],tinfo.pointP[(j+3)%4] -tinfo.pointP[(j+1)%4])/ volume;
      else
        tinfo.shapeVector[j]=cross(tinfo.pointP[(j+2)%4] - tinfo.pointP[(j+1)%4],tinfo.pointP[(j+3)%4] - tinfo.pointP[(j+1)%4])/ volume;;
    }

    // precompute Di cross Dj needed for the second derivative of the SPK tensor
    for(j=0;j<6;++j) {
      Edge e=_topology->getLocalEdgesInTetrahedron(j);
      k=e[0];
      l=e[1];
      if (edgeArray[te[j]][0]!=t[k]) {
        k=e[1];
        l=e[0];
      }
      for(m=0;m<3;++m){
        for(n=0;n<3;++n){
          tinfo.DicrossDj[j][m][n]=tinfo.shapeVector[k][m]*tinfo.shapeVector[l][n];
        }
      }

    }


    //we want to precomput Lij=2BDicrossDjA or Lij=C(DicrossDj^TC^T+DjdotCDi)
    // we also strore functions that need a call to the material and won't change

    //typename vector<HyperelasticMatTerm *> materialTermArray;
    materialTermArray = myMaterial->getMaterialTermArray();
    typename vector<HyperelasticMatTerm *>::iterator it;
    it=materialTermArray.begin();
    int id=0;
    std::vector<Real> number;
    Real coefficient=0;
    tinfo.coeff.resize(0);
    MatrixSym SPK;
    for(;it<materialTermArray.end();++it) {
      number.push_back((*it)->MultiplyByCoeff(&tinfo,globalParameters));
      std::vector<MatrixList> Lijfirst;
      std::vector<MatrixList> Lijsecond;
      if((*it)->hasAConstantElasticityTensor()){

        vector<MatrixSym> vectorMatrixFirstPair;
        vector<MatrixSym> vectorMatrixSecondPair;
        (*it)->InvariantMatricesElasticityTensor(&tinfo,globalParameters,vectorMatrixFirstPair,vectorMatrixSecondPair);
        unsigned int sizeFirst=vectorMatrixFirstPair.size();
        unsigned int sizeSecond=vectorMatrixSecondPair.size();

        if(sizeFirst>=1){
          for(m=0;m<sizeFirst;++m){
            MatrixList Lijf;
            for(j=0;j<6;++j) {
              Edge e=_topology->getLocalEdgesInTetrahedron(j);
              k=e[0];
              l=e[1];
              if (edgeArray[te[j]][0]!=t[k]) {
                k=e[1];
                l=e[0];
              }
              Lijf.data[j]=vectorMatrixFirstPair[m].MatSymMultiply(vectorMatrixFirstPair[m].SymMatMultiply(tinfo.DicrossDj[j]))*2;
            }
            Lijfirst.push_back(Lijf);

          }
        }

        if(sizeSecond>=1){
          for(m=0;m<sizeSecond;++m){
            MatrixList Lijs;
            for(j=0;j<6;++j) {

              Edge e=_topology->getLocalEdgesInTetrahedron(j);
              k=e[0];
              l=e[1];
              if (edgeArray[te[j]][0]!=t[k]) {
                k=e[1];
                l=e[0];
              }

              Coord temp=vectorMatrixSecondPair[m]*tinfo.shapeVector[k];
              Lijs.data[j]=vectorMatrixSecondPair[m]*dot(tinfo.shapeVector[l],temp)+
                  vectorMatrixSecondPair[m].MatSymMultiply(vectorMatrixSecondPair[m].SymMatMultiply(tinfo.DicrossDj[j].transposed()));
            }
            Lijsecond.push_back(Lijs);
          }
        }

        tinfo.Lij_first_k.push_back(Lijfirst );
        tinfo.Lij_second_k.push_back( Lijsecond );
        Lijfirst.clear();
        Lijsecond.clear();
      }//end of if constant
      else{

        tinfo.Lij_first_k.push_back( Lijfirst);
        tinfo.Lij_second_k.push_back(  Lijsecond );
      }

      id++;
      tinfo.functionf.push_back(1);
      tinfo.functiong.push_back(1);
      tinfo.functionDf.push_back(0);
      tinfo.functionD2f.push_back(0);
      tinfo.SPKTensor.push_back(SPK);


    }// end of for it

    coefficient=number[0];
    for(unsigned int m=1; m<counter.size();++m){
      if(counter[m]!=counter[m-1]){
        tinfo.coeff.push_back(coefficient);
        coefficient=number[m];
      }
    }//end of for m
    tinfo.coeff.push_back(coefficient);
}

template <class DataTypes> MJEDTetrahedralForceField<DataTypes>::MJEDTetrahedralForceField() 
    : _topology(0)
    , _initialPoints(0)
    , updateMatrix(true)
    , _meshSaved( false)
    , viscous(false)
    , considerInversion(false)
    , f_inversion(initData(&f_inversion,false,"considerInversion","if inverted tetrahedra should be considered"))
    , viscoelasticity(initData(&viscoelasticity,false,"viscous","If the material is also viscous"))
    , f_stiffnessMatrixRegularizationWeight(initData(&f_stiffnessMatrixRegularizationWeight,false,"matrixRegularization","Regularization of the Stiffness Matrix (true or false)"))
    , f_materialName(initData(&f_materialName,std::string("ArrudaBoyce"),"materialName","the name of the material to be used"))
    , f_parameterSet(initData(&f_parameterSet,"ParameterSet","The global parameters specifying the material"))
    , f_parameterAlpha(initData(&f_parameterAlpha,"ParameterAlpha","The parameters alpha to describe viscous part"))
    , f_parameterTau(initData(&f_parameterTau,"ParameterTau","The parameters tau to describe viscous part"))
    , f_anisotropySet(initData(&f_anisotropySet,"AnisotropyDirections","The global directions of anisotropy of the material"))
    , f_parameterFileName(initData(&f_parameterFileName,std::string("myFile.param"),"ParameterFile","the name of the file describing the material parameters for all tetrahedra"))
    , tetrahedronInfo(initData(&tetrahedronInfo, "tetrahedronInfo", "Internal tetrahedron data"))
    , edgeInfo(initData(&edgeInfo, "edgeInfo", "Internal edge data"))
    , myMaterial(0)
{
}

template <class DataTypes> MJEDTetrahedralForceField<DataTypes>::~MJEDTetrahedralForceField()
{
	if (myMaterial)
	{
		/// destroy elements in the material term array
		//typename vector<HyperelasticMatTerm *> materialTermArray;
		materialTermArray = myMaterial->getMaterialTermArray();
		typename  vector<HyperelasticMatTerm *>::iterator it;                				
		for (it=materialTermArray.begin();it!=materialTermArray.end();++it)
		{
			if (*it) delete *it;
		}
	}
}


template <class DataTypes> void MJEDTetrahedralForceField<DataTypes>::init()
{
	cerr << "initializing MJEDTetrahedralForceField" <<endl;
	this->Inherited::init();
	_topology = this->getContext()->getMeshTopology();
	/** parse the parameter set */
	SetParameterArray paramSet=f_parameterSet.getValue();
	if (paramSet.size()>0) {
		globalParameters.parameterArray.resize(paramSet.size());
		copy(paramSet.begin(), paramSet.end(),globalParameters.parameterArray.begin());
	}
	/** parse the anisotropy Direction set */
	SetAnisotropyDirectionArray anisotropySet=f_anisotropySet.getValue();
	if (anisotropySet.size()>0) {
		globalParameters.anisotropyDirection.resize(anisotropySet.size());
		copy(anisotropySet.begin(), anisotropySet.end(),globalParameters.anisotropyDirection.begin());
	}
	viscous=viscoelasticity.getValue();
        considerInversion=f_inversion.getValue();
	stiffnessMatrixRegularizationWeight=f_stiffnessMatrixRegularizationWeight.getValue();

	if(viscous){
		/** parse the parameter alpha */
		SetParameterAlpha Alpha=f_parameterAlpha.getValue();
		if (Alpha.size()>0) {
			globalParameters.parameterAlpha.resize(Alpha.size());
			copy(Alpha.begin(), Alpha.end(),globalParameters.parameterAlpha.begin());
		}
		/** parse the parameter set */
		SetParameterTau Tau=f_parameterTau.getValue();
		if (Tau.size()>0) {
			globalParameters.parameterTau.resize(Tau.size());
			copy(Tau.begin(), Tau.end(),globalParameters.parameterTau.begin());
		}
	}

	//	typename vector<HyperelasticMatTerm *> materialTermArray;
	/** parse the input material name */
        string material = f_materialName.getValue();
	if (material=="ArrudaBoyce") {
            fem::BoyceAndArrudaMJED<DataTypes> *BoyceAndArrudaMaterial = new fem::BoyceAndArrudaMJED<DataTypes>;
            myMaterial = BoyceAndArrudaMaterial;
            cout<<"The model is "<<material<<endl;
            materialTermArray =  myMaterial->getMaterialTermArray();
	} 
	else if (material=="StVenantKirchhoff"){
            fem::STVenantKirchhoffMJED<DataTypes> *STVenantKirchhoffMaterial = new fem::STVenantKirchhoffMJED<DataTypes>;
            myMaterial = STVenantKirchhoffMaterial;
            cout<<"The model is "<<material<<endl;
            materialTermArray =  myMaterial->getMaterialTermArray();
        }
	else if (material=="NeoHookean"){
            fem::NeoHookeanMJED<DataTypes> *NeoHookeanMaterial = new fem::NeoHookeanMJED<DataTypes>;
            myMaterial = NeoHookeanMaterial;
            cout<<"The model is "<<material<<endl;
            materialTermArray =  myMaterial->getMaterialTermArray();
	}
	else if (material=="MooneyRivlin"){
            fem::MooneyRivlinMJED<DataTypes> *MooneyRivlinMaterial = new fem::MooneyRivlinMJED<DataTypes>;
            myMaterial = MooneyRivlinMaterial;
            cout<<"The model is "<<material<<endl;
            materialTermArray =  myMaterial->getMaterialTermArray();
	}
	else if (material=="VerondaWestman"){
            fem::VerondaWestmanMJED<DataTypes> *VerondaWestmanMaterial = new fem::VerondaWestmanMJED<DataTypes>;
            myMaterial = VerondaWestmanMaterial;
            cout<<"The model is "<<material<<endl;
            materialTermArray =  myMaterial->getMaterialTermArray();
	}

	/*else if (material=="Isotropic_NeoHookean"){
	fem::NeoHookeanIsotropicMJED<DataTypes> *IsoNeoMaterial = new fem::NeoHookeanIsotropicMJED<DataTypes>;
	myMaterial =IsoNeoMaterial;
	cout<<"The model is "<<material<<endl;
	materialTermArray =  myMaterial->getMaterialTermArray();
	}*/
	else if (material=="Costa"){
            fem::CostaMJED<DataTypes> *CostaMaterial = new fem::CostaMJED<DataTypes>(globalParameters);
            myMaterial =CostaMaterial;
            cout<<"The model is "<<material<<endl;
            materialTermArray =  myMaterial->getMaterialTermArray();
	}
	else if (material=="Ogden"){
            fem::OgdenMJED<DataTypes> *OgdenMaterial = new fem::OgdenMJED<DataTypes>(globalParameters);
            myMaterial =OgdenMaterial;
            cout<<"The model is "<<material<<endl;
            materialTermArray =  myMaterial->getMaterialTermArray();
	}

	else {
            cerr << "material name " << material << " is not valid"<<endl;
	}



	if (!_topology->getNbTetrahedra())
	{
            cerr << "ERROR(MJEDForceField): object must have a Tetrahedral Set Topology.\n";
            return;
	}

        helper::WriteOnlyAccessor< Data<sofa::type::vector<TetrahedronRestInformation> > > tetrahedronInf = tetrahedronInfo;

	/// prepare to store info in the triangle array
	tetrahedronInf.resize(_topology->getNbTetrahedra());

        helper::WriteOnlyAccessor< Data<sofa::type::vector<EdgeInformation> > > edgeInf = edgeInfo;
        edgeInf.resize(_topology->getNbEdges());
        edgeInfo.createTopologyHandler(_topology);


	// get restPosition
	if (_initialPoints.size() == 0)
	{
            const VecCoord& p = this->mstate->read(core::ConstVecCoordId::restPosition())->getValue();
            _initialPoints=p;
	}

        // initialize data that are the same for all tetrahedrons
	typename vector<HyperelasticMatTerm *>::iterator it;
	for (it=materialTermArray.begin();it<materialTermArray.end();++it) {
            counter.push_back((*it)->getNumberOfExponential());
	}

	bool Expo;
	if(counter[0]==0) Expo=false;
	else Expo=true;

	for (unsigned int m=1; m < counter.size(); ++m){
            if (counter[m]==counter[m-1]){
                if(counter[m]==0) Expo=false;
                else Expo=true;
            }
            else{
                isExponential.push_back(Expo);
                if(counter[m]==0) Expo=false;
                else Expo=true;

            }
	}// end of for m
	isExponential.push_back(Expo);

	if(viscous){
            std::vector<Real> tauu=f_parameterTau.getValue();
            Real dt= (Real)this->getContext()->getDt();
            std::vector<Real> alphaa=f_parameterAlpha.getValue();
            coeffA.resize(tauu.size());
            coeffB.resize(tauu.size());
            sumA=0;
            for (unsigned int num=0; num<tauu.size();num++){
                coeffA[num]=dt*alphaa[num]/(dt+tauu[num]);
                coeffB[num]=tauu[num]/(dt+tauu[num]);
                sumA+=coeffA[num];
            }
	}



	/// initialize the data structure associated with each tetrahedron
        for (Index i=0;i<_topology->getNbTetrahedra();++i) {

            createTetrahedronRestInformation(i,tetrahedronInf[i],
                                             _topology->getTetrahedron(i),  (const vector< unsigned int > )0,
                                             (const vector< double >)0);
            if(viscous){
                    int size=coeffA.size();
                    tetrahedronInf[i].GammaOld.resize(size);
                    tetrahedronInf[i].GammaNew.resize(size);
            }
	}
	/// set the call back function upon creation of a tetrahedron
        tetrahedronInfo.createTopologyHandler(_topology);
        tetrahedronInfo.setCreationCallback([this](Index tetrahedronIndex, TetrahedronRestInformation& tetraInfo,
            const core::topology::BaseMeshTopology::Tetrahedron& tetra,
            const sofa::type::vector< Index >& ancestors,
            const sofa::type::vector< double >& coefs)
        {
            createTetrahedronRestInformation(tetrahedronIndex, tetraInfo, tetra, ancestors, coefs);
        });

}

template <class DataTypes> 
void MJEDTetrahedralForceField<DataTypes>::addForce(const core::MechanicalParams* /* mparams */ /* PARAMS FIRST */, DataVecDeriv& d_f, const DataVecCoord& d_x, const DataVecDeriv& /* d_v */)
{
        helper::WriteAccessor< Data< VecDeriv > > f = d_f;
        helper::ReadAccessor< Data< VecCoord > > x = d_x;
        unsigned int nbInverted=0;
        Real volume;

	// used to save the mesh at a certain time of the simulation
	const bool printLog = this->f_printLog.getValue();
	if (printLog && !_meshSaved) {
		saveMesh( "sofa-result.stl" );
		printf( "Mesh saved.\n" );
		_meshSaved = true;
	}
	unsigned int i=0,j=0,k=0,l=0;
	unsigned int nbTetrahedra=_topology->getNbTetrahedra();

        helper::WriteOnlyAccessor< Data<sofa::type::vector<TetrahedronRestInformation> > > tetrahedronInf = tetrahedronInfo;


	TetrahedronRestInformation *tetInfo;

	assert(this->mstate);

	Coord dp[3],x0,sv,pp[3],dj;
	//        myposition=x;  // to uncomment if the test derivative is performed


	for(i=0; i<nbTetrahedra; i++ )
	{
		tetInfo=&tetrahedronInf[i];
		const Tetrahedron &ta= _topology->getTetrahedron(i);


                //to compute J= currentvolume/restvolume

                volume= dot(cross(x[ta[1]]-x[ta[0]],x[ta[2]]-x[ta[0]]),x[ta[3]]-x[ta[0]])/6;

                tetInfo->J =volume/tetInfo->restVolume;
//                Real JJ=tetInfo->J-1;

                for(j=0;j<4;++j) {
                        tetInfo->currentPos[j]=x[ta[j]];
                }

                if(considerInversion){
                if (tetInfo->J< 0) {
                        nbInverted++;
                        std::cerr<<"Inverted Tetrahedron="<<i<<std::endl;

                        Real volSquare=volume*volume;
                        Real maxAltitude= -1;
                        unsigned int bestVertex = 0;

                        // store shape vectors
                        for(j=0;j<4;++j) {
                                if ((j%2)==0)
                                        tetInfo->areaVector[j]= -cross(tetInfo->currentPos[(j+2)%4] - tetInfo->currentPos[(j+1)%4],
                                        tetInfo->currentPos[(j+3)%4] - tetInfo->currentPos[(j+1)%4])/6;
                                else
                                        tetInfo->areaVector[j]= cross(tetInfo->currentPos[(j+2)%4] - tetInfo->currentPos[(j+1)%4],
                                        tetInfo->currentPos[(j+3)%4] - tetInfo->currentPos[(j+1)%4])/6;
                                Real altitude=tetInfo->areaVector[j].norm2()/volSquare;
                                if (altitude>maxAltitude) {
                                        maxAltitude=altitude;
                                        bestVertex=j;
                                }
                        }
                        Real targetJ=0.75;
                        tetInfo->currentPos[bestVertex]+=tetInfo->areaVector[bestVertex]*(1+ targetJ/fabs(tetInfo->J))*volume/(tetInfo->areaVector[bestVertex].norm2());
                        volume= dot(cross(tetInfo->currentPos[1]-tetInfo->currentPos[0],tetInfo->currentPos[2]-tetInfo->currentPos[0]),tetInfo->currentPos[3]-tetInfo->currentPos[0])/6;
//                        JJ=volume/tetInfo->restVolume-1;
                        tetInfo->J=volume/tetInfo->restVolume;
                }
            }

                x0=tetInfo->currentPos[0];

                dp[0]=tetInfo->currentPos[1]-x0;
                // compute the deformation gradient
                // deformation gradient = sum of tensor product between vertex position and shape vector
                // optimize by using displacement with first vertex

                sv=tetInfo->shapeVector[1];
                for (k=0;k<3;++k) {
                        for (l=0;l<3;++l) {
                                tetInfo->deformationGradient[k][l]=dp[0][k]*sv[l];
                        }
                }
                for (j=1;j<3;++j) {
                        dp[j]=tetInfo->currentPos[j+1]-x0;
                        sv=tetInfo->shapeVector[j+1];
                        for (k=0;k<3;++k) {
                                for (l=0;l<3;++l) {
                                        tetInfo->deformationGradient[k][l]+=dp[j][k]*sv[l];
                                }
                        }
                }








		/// compute the right Cauchy-Green deformation matrix
		for (k=0;k<3;++k) {
			for (l=k;l<3;++l) {
				//if (l>=k) {
				tetInfo->deformationTensor(k,l)=(tetInfo->deformationGradient(0,k)*tetInfo->deformationGradient(0,l)+
					tetInfo->deformationGradient(1,k)*tetInfo->deformationGradient(1,l)+
					tetInfo->deformationGradient(2,k)*tetInfo->deformationGradient(2,l));
				//	}
				//	else 
				//	tetInfo->deformationTensor[k][l]=tetInfo->deformationTensor[l][k];
			}
		}


		tetInfo->trC = (Real)( tetInfo->deformationTensor(0,0) + tetInfo->deformationTensor(1,1) + tetInfo->deformationTensor(2,2));

		// in case of transversaly isotropy
		if(globalParameters.anisotropyDirection.size()>0){
			tetInfo->fiberDirection=globalParameters.anisotropyDirection[0];
			Coord vectCa=tetInfo->deformationTensor*tetInfo->fiberDirection;
			Real aDotCDota=dot(tetInfo->fiberDirection,vectCa);
			tetInfo->lambda=(Real)sqrt(aDotCDota);
		}



                Coord areaVec = cross( dp[1], dp[2] );
		// we have to compute dJ 
                tetInfo->dJ[0] = cross( tetInfo->currentPos[3]-tetInfo->currentPos[1], tetInfo->currentPos[2]-tetInfo->currentPos[1] ) * tetInfo->volScale;
		tetInfo->dJ[1] = areaVec * tetInfo->volScale;
		tetInfo->dJ[2] = cross( dp[2], dp[0] ) * tetInfo->volScale;
		tetInfo->dJ[3] = cross( dp[0], dp[1] ) * tetInfo->volScale;


		MatrixSym SPK;

		// get the information for the material and store what is necessary
		//typename vector<HyperelasticMatTerm *> materialTermArray;
		materialTermArray = myMaterial->getMaterialTermArray();
		//tetInfo->strainEnergy=myMaterial->getStrainEnergy(tetInfo,globalParameters); // to uncomment for test derivatives

		typename vector<HyperelasticMatTerm *>::iterator it;
		it=materialTermArray.begin();
		//tetInfo->sumfS.clear();
		MatrixSym fS;
		Real Dfg=0;
		Real energy=0;
		tetInfo->strainEnergies.resize(0);
		tetInfo->sumfS.resize(0);
		tetInfo->sumDfg.resize(0);
		int id=0;
		tetInfo->FPK.clear();

		for(;it<materialTermArray.end();++it) {
			(*it)->CalculFunction(tetInfo);

			if((*it)->includeAJFactor() && (*it)->includeAnInvariantFactor() ){
				tetInfo->functionf[id]=(*it)->JFunction(tetInfo,globalParameters);
				tetInfo->functionDf[id]=(*it)->JFunctionDerivative(tetInfo,globalParameters);
				tetInfo->functionD2f[id]=(*it)->JFunctionSecondDerivative(tetInfo,globalParameters);
				(*it)->InvariantFunctionSPKTensor(tetInfo,globalParameters,SPK);
				tetInfo->SPKTensor[id]=SPK;
				tetInfo->functiong[id]=(*it)->InvariantFunction(tetInfo,globalParameters);
			}
			else if((*it)->includeAnInvariantFactor()){
				(*it)->InvariantFunctionSPKTensor(tetInfo,globalParameters,SPK);
				tetInfo->SPKTensor[id]=SPK;
				tetInfo->functiong[id]=(*it)->InvariantFunction(tetInfo,globalParameters);
			}
			else if((*it)->includeAJFactor()){
				tetInfo->functionf[id]=(*it)->JFunction(tetInfo,globalParameters);
				tetInfo->functionDf[id]=(*it)->JFunctionDerivative(tetInfo,globalParameters);
				tetInfo->functionD2f[id]=(*it)->JFunctionSecondDerivative(tetInfo,globalParameters);
			}
			id++;
		}
		if(isExponential.size()==1){
			for(unsigned int m=0; m<counter.size();++m){
				fS += tetInfo->SPKTensor[m]*tetInfo->functionf[m];
				Dfg += tetInfo->functionDf[m]*tetInfo->functiong[m];
				energy+=tetInfo->functiong[m]*tetInfo->functionf[m];
			}
			tetInfo->sumfS.push_back(fS);
			tetInfo->sumDfg.push_back(Dfg);
			tetInfo->strainEnergies.push_back(energy);	
		}
		else{
			fS=tetInfo->SPKTensor[0]*tetInfo->functionf[0];
			Dfg=tetInfo->functionDf[0]*tetInfo->functiong[0];
			energy=tetInfo->functiong[0]*tetInfo->functionf[0];
			for(unsigned int m=1; m<counter.size();++m){	
				if(counter[m]==counter[m-1]){
					fS += tetInfo->SPKTensor[m]*tetInfo->functionf[m];
					Dfg += tetInfo->functionDf[m]*tetInfo->functiong[m];
					energy+=tetInfo->functiong[m]*tetInfo->functionf[m];
				}
				else {
					tetInfo->sumfS.push_back(fS);
					tetInfo->sumDfg.push_back(Dfg);
					tetInfo->strainEnergies.push_back(energy);
					fS=tetInfo->SPKTensor[m]*tetInfo->functionf[m];
					Dfg=tetInfo->functionDf[m]*tetInfo->functiong[m];
					energy=tetInfo->functiong[m]*tetInfo->functionf[m];
				}

			}//end of for m
			tetInfo->sumfS.push_back(fS);
			tetInfo->sumDfg.push_back(Dfg);
			tetInfo->strainEnergies.push_back(energy);	
		}

		//general case (non viscous)
		if(!viscous){

			for(unsigned int w=0;w<isExponential.size();++w){
				if(!isExponential[w]){
					for(l=0;l<4;++l){
						f[ta[l]]-=(tetInfo->deformationGradient*(tetInfo->sumfS[w]*tetInfo->shapeVector[l])+tetInfo->dJ[l]*tetInfo->sumDfg[w])*tetInfo->restVolume*tetInfo->coeff[w];
					}

				}
				else {
					for(l=0;l<4;++l){
						f[ta[l]]-=(tetInfo->deformationGradient*(tetInfo->sumfS[w]*tetInfo->shapeVector[l])+tetInfo->dJ[l]*tetInfo->sumDfg[w])*tetInfo->restVolume*tetInfo->coeff[w]*exp(tetInfo->strainEnergies[w]);

					}

				}
			}//end of for w
		}

		//If viscous, by use of prony series
		else if(viscous){

			Matrix3 inverseDeformationGradient;
			// compute the inverse deformation gradient		
			pp[0]=tetInfo->pointP[1]-tetInfo->pointP[0];
			dj=tetInfo->dJ[1]/tetInfo->J;
			for (k=0;k<3;++k) {
				for (l=0;l<3;++l) {
					inverseDeformationGradient[k][l]=pp[0][k]*dj[l];
				}
			}
			for (j=1;j<3;++j) {
				pp[j]=tetInfo->pointP[j+1]-tetInfo->pointP[0];
				dj=tetInfo->dJ[j+1]/tetInfo->J;
				for (k=0;k<3;++k) {
					for (l=0;l<3;++l) {
						inverseDeformationGradient[k][l]+=pp[j][k]*dj[l];
					}
				}
			}


			for(unsigned int w=0;w<isExponential.size();++w){
				if(!isExponential[w]){
					tetInfo->FPK+=(tetInfo->sumfS[w].MatSymMultiply(tetInfo->deformationGradient)+inverseDeformationGradient.transposed()*tetInfo->sumDfg[w]*tetInfo->J)*tetInfo->coeff[w];
				}
				else {
					tetInfo->FPK+=(tetInfo->sumfS[w].MatSymMultiply(tetInfo->deformationGradient)+inverseDeformationGradient.transposed()*tetInfo->sumDfg[w]*tetInfo->J)*tetInfo->coeff[w]*exp(tetInfo->strainEnergies[w]);
				}
			}//end of for w
			tetInfo->sumBgamma.clear();
			MatrixSym sumBgam;
			sumBgam.clear();
			for(unsigned int num=0; num<coeffA.size();++num){
				tetInfo->sumBgamma+=coeffB[num]*tetInfo->GammaOld[num];
				MatrixSym Si;
				Si.Mat2Sym(coeffA[num]*inverseDeformationGradient*tetInfo->FPK,Si);
				tetInfo->GammaNew[num]=Si+coeffB[num]*tetInfo->GammaOld[num];
				sumBgam+=tetInfo->GammaNew[num];

			}
			for(l=0;l<4;++l){		
				f[ta[l]]-=(tetInfo->FPK*tetInfo->shapeVector[l])*tetInfo->restVolume;

			}
			for(l=0;l<4;++l){	
				f[ta[l]]=f[ta[l]]+tetInfo->deformationGradient*(sumBgam*tetInfo->shapeVector[l])*tetInfo->restVolume;
			}
		}


	}// end of for i
        if (nbInverted>0)
                std::cerr<< "nb inverted elements is " <<nbInverted<<std::endl;

	/// indicates that the next call to addDForce will need to update the stiffness matrix
	updateMatrix=true;
}


template <class DataTypes> 
void MJEDTetrahedralForceField<DataTypes>::updateMatrixData() 
{
	/// if the  matrix needs to be updated
	if (updateMatrix) {
		unsigned int l=0,i=0,j=0,k=0;
		unsigned int nbEdges=_topology->getNbEdges();
		const vector< Edge> &edgeArray=_topology->getEdges() ;


                helper::WriteOnlyAccessor< Data<sofa::type::vector<EdgeInformation> > > edgeInf = edgeInfo;
                helper::WriteOnlyAccessor< Data<sofa::type::vector<TetrahedronRestInformation> > > tetrahedronInf = tetrahedronInfo;

		// VecDeriv& x = myposition;  // to uncomment for test derivatives and comment next line
		const VecCoord& x = this->mstate->read(core::ConstVecCoordId::position())->getValue();
		EdgeInformation *einfo;

		unsigned int m,n;
		TetrahedronRestInformation *tetInfo;
		unsigned int nbTetrahedra=_topology->getNbTetrahedra();
		const std::vector< Tetrahedron> &tetrahedronArray=_topology->getTetrahedra() ;
		const unsigned int vertexVertexIndex[4][4][2]={{{5,5},{3,2},{1,3},{2,1}},{{2,3},{5,5},{3,0},{0,2}},
		{{3,1},{0,3},{5,5},{1,0}},{{1,2},{2,0},{0,1},{5,5}}};

		MatrixSym DfS;
		Real D2fg,varh;
		Coord dp;
		std::vector<Matrix3> matrixN;
		std::vector<MatrixSym> sumDfS;
		std::vector<Real> sumD2fg;
		Matrix3 LinearMatrix1,LinearMatrix2;
		Matrix3 Lam, M, Theta, Pi, R,  N;

		for(l=0; l<nbEdges; l++ ) {
			edgeInf[l].DfDx.clear();
		}
		for(i=0; i<nbTetrahedra; i++ )
		{
			std::vector<MatrixList> Nk;
			Nk.resize(counter.size());
			tetInfo=&tetrahedronInf[i];
			Matrix3 &df=tetInfo->deformationGradient;
			Matrix3 Tdf=df.transposed();
			BaseMeshTopology::EdgesInTetrahedron te=_topology->getEdgesInTetrahedron(i);

			if (f_stiffnessMatrixRegularizationWeight.getValue()) {
				if(tetInfo->J>=1) varh=0;
				else if (tetInfo->J <=0 ) varh=1;
				else varh=(1-tetInfo->J);
			}
			else varh=0;

			/// describe the jth vertex index of triangle no i 
			const Tetrahedron &ta= tetrahedronArray[i];


			int id=0;
			// use the precomputed linear matrices Lij to calculate the term with second derivative of SPK			
			//typename vector<HyperelasticMatTerm *> materialTermArray;
			materialTermArray = myMaterial->getMaterialTermArray();
			typename vector<HyperelasticMatTerm *>::iterator it;
			it=materialTermArray.begin();
			for(it=materialTermArray.begin();it<materialTermArray.end();++it) {
				Nk[id].clear();
				if((*it)->includeAnInvariantFactor()){
					vector<Real> coeffMatrixFirstPair;
					vector<Real> coeffMatrixSecondPair;
					(*it)->InvariantScalarFactorElasticityTensor(tetInfo,globalParameters,coeffMatrixFirstPair,coeffMatrixSecondPair);
					unsigned int sizeFirst=coeffMatrixFirstPair.size();
					unsigned int sizeSecond=coeffMatrixSecondPair.size();
					if((sizeFirst>0) ||(sizeSecond>0)){
						if((*it)->hasAConstantElasticityTensor()){								

							for(j=0;j<6;j++) {
								einfo= &edgeInf[te[j]];
								Edge e=_topology->getLocalEdgesInTetrahedron(j);

								k=e[0];
								l=e[1];
								if (edgeArray[te[j]][0]!=ta[k]) {
									k=e[1];
									l=e[0];
								}
								LinearMatrix1.clear();
								if(sizeFirst>0){
									for(m=0;m<sizeFirst;++m){
										LinearMatrix1+=tetInfo->Lij_first_k[id][m].data[j]*coeffMatrixFirstPair[m];
									}
								}
								if(sizeSecond>0){
									for(m=0;m<sizeSecond;++m){
										LinearMatrix1+=tetInfo->Lij_second_k[id][m].data[j]*coeffMatrixSecondPair[m];
									}
								}
								Nk[id].data[j]+=(df*LinearMatrix1*Tdf).transposed()*tetInfo->functionf[id];
							}
						}
						else if (!(*it)->hasAConstantElasticityTensor()){
							std::vector<MatrixSym> vectorMatrixFirstPair,vectorMatrixSecondPair;
							(*it)->InvariantMatricesElasticityTensor(tetInfo,globalParameters,vectorMatrixFirstPair,vectorMatrixSecondPair);
							for(j=0;j<6;j++) {
								einfo= &edgeInf[te[j]];
								Edge e=_topology->getLocalEdgesInTetrahedron(j);

								k=e[0];
								l=e[1];
								if (edgeArray[te[j]][0]!=ta[k]) {
									k=e[1];
									l=e[0];
								}
								LinearMatrix2.clear();
								if(sizeFirst>0){
									for(m=0;m<sizeFirst;++m){
										LinearMatrix2+=vectorMatrixFirstPair[m].MatSymMultiply(vectorMatrixFirstPair[m].SymMatMultiply(tetInfo->DicrossDj[j]))*2*coeffMatrixFirstPair[m];
									}
								}
								if(sizeSecond>0){
									for(m=0;m<sizeSecond;++m){
										Coord temp=vectorMatrixSecondPair[m]*tetInfo->shapeVector[k];
										LinearMatrix2+=(vectorMatrixSecondPair[m]*dot(tetInfo->shapeVector[l],temp)+
											vectorMatrixSecondPair[m].MatSymMultiply(vectorMatrixSecondPair[m].SymMatMultiply(tetInfo->DicrossDj[j].transposed())))*coeffMatrixSecondPair[m];
									}
								}
								Nk[id].data[j]+=(df*LinearMatrix2*Tdf).transposed()*tetInfo->functionf[id];
							}
						}
					}

				}
				id++;
			}// end of for it

			for(j=0;j<6;j++) {
				einfo= &edgeInf[te[j]];
				Edge e=_topology->getLocalEdgesInTetrahedron(j);

				k=e[0];
				l=e[1];
				if (edgeArray[te[j]][0]!=ta[k]) {
					k=e[1];
					l=e[0];
				}
				Matrix3 &edgeDfDx = einfo->DfDx;


				//second derivative of J:
                                type::MatNoInit<3,3,Real> d2J;
				dp = (x[ta[vertexVertexIndex[k][l][0]]] - x[ta[vertexVertexIndex[k][l][1]]])  * tetInfo->volScale;

				d2J[0][0] = 0;
				d2J[0][1] = -dp[2];
				d2J[0][2] = dp[1];
				d2J[1][0] = dp[2];
				d2J[1][1] = 0;
				d2J[1][2] = -dp[0];
				d2J[2][0] = -dp[1];
				d2J[2][1] = dp[0];
				d2J[2][2] = 0;


				Coord dJl=tetInfo->dJ[l];
				Coord dJk=tetInfo->dJ[k];
				Coord svl=tetInfo->shapeVector[l];
				Coord svk=tetInfo->shapeVector[k];



				sumD2fg.resize(0);
				matrixN.resize(0);
				sumDfS.resize(0);

				if(isExponential.size()==1){
					DfS.clear();
					D2fg=0;
					N.clear();
					for(m=0; m<counter.size();++m){	
						DfS += tetInfo->SPKTensor[m]*tetInfo->functionDf[m];
						D2fg += tetInfo->functionD2f[m]*tetInfo->functiong[m];
						N+=Nk[m].data[j];
					}
					sumDfS.push_back(DfS);
					sumD2fg.push_back(D2fg);
					matrixN.push_back(N);
				}
				else{
					DfS=tetInfo->SPKTensor[0]*tetInfo->functionDf[0];
					D2fg=tetInfo->functionD2f[0]*tetInfo->functiong[0];
					N=Nk[0].data[j];
					for(m=1; m<counter.size();++m){	
						if(counter[m]==counter[m-1]){
							DfS += tetInfo->SPKTensor[m]*tetInfo->functionDf[m];
							D2fg += tetInfo->functionD2f[m]*tetInfo->functiong[m];
							N+=Nk[m].data[j];
						}
						else {
							sumDfS.push_back(DfS);
							sumD2fg.push_back(D2fg);
							matrixN.push_back(N);
							DfS=tetInfo->SPKTensor[m]*tetInfo->functionDf[m];
							D2fg=tetInfo->functionD2f[m]*tetInfo->functiong[m];
							N=Nk[m].data[j];
						}

					}//end of for m
					sumDfS.push_back(DfS);
					sumD2fg.push_back(D2fg);
					matrixN.push_back(N);
				}

				Matrix3 Bij;
				for(unsigned int w=0;w<isExponential.size();++w){
					if(!isExponential[w]){
						Coord FF[4];
						for(m=0;m<4;++m) FF[m]=df*(sumDfS[w]*tetInfo->shapeVector[m]);	
						//Now M
						Real productDfSD;
						Coord vectSD=tetInfo->sumfS[w]*svk;
						productDfSD=dot(vectSD,svl);
						//M[0][1]=M[0][2]=M[1][0]=M[1][2]=M[2][0]=M[2][1]=0;
						M[0][0]=M[1][1]=M[2][2]=(Real)productDfSD;

						///Then R Lambda et Theta
						R.clear();
						for(m=0;m<3;++m){
							for(n=0;n<3;++n){
								R[m][n]=dJl[m]*dJk[n]*(1-varh)*sumD2fg[w];
								if(m==n) R[m][n]+=dot(dJl,dJk)*sumD2fg[w]*varh;
								Lam[m][n]=dJl[m]*FF[k][n];
								Theta[m][n]=dJk[n]*FF[l][m];
							}
						}

						///Then Pi
						Pi=d2J*tetInfo->sumDfg[w];
						Bij += (Lam+M+matrixN[w]+R+Pi+Theta)*tetInfo->restVolume*tetInfo->coeff[w];
					}
					else {
						R.clear();
						//edgeDfDx.clear();
						Coord FF[4];
						for(m=0;m<4;++m) FF[m]=df*(sumDfS[w]*tetInfo->shapeVector[m]);	
						//Now M
						Real productDfSD;
						Coord vectSD=tetInfo->sumfS[w]*svk;
						productDfSD=dot(vectSD,svl);
						//M[0][1]=M[0][2]=M[1][0]=M[1][2]=M[2][0]=M[2][1]=0;
						M[0][0]=M[1][1]=M[2][2]=(Real)productDfSD;

						///Then R Lambda et Theta
						for(m=0;m<3;++m){
							for(n=0;n<3;++n){
								R[m][n]=dJl[m]*dJk[n]*(1-varh)*sumD2fg[w];
								if(m==n) R[m][n]+=dot(dJl,dJk)*sumD2fg[w]*varh;
								Lam[m][n]=dJl[m]*FF[k][n];
								Theta[m][n]=dJk[n]*FF[l][m];
							}
						}

						///Then Pi
						Pi=d2J*tetInfo->sumDfg[w];
						Matrix3 inter;
						Coord dWi,dWj;
						dWj=df*(tetInfo->sumfS[w]*svl)+dJl*tetInfo->sumDfg[w];
						dWi=df*(tetInfo->sumfS[w]*svk)+dJk*tetInfo->sumDfg[w];

						for(m=0;m<3;++m){
							for(n=0;n<3;++n){
								inter[m][n]=dWj[m]*dWi[n]*(1-varh);
								if(m==n) inter[m][n]+=dot(dWj,dWi)*varh;
							}
						}
						Bij += (Lam+M+matrixN[w]+R+Pi+Theta+inter)*tetInfo->restVolume*tetInfo->coeff[w]*exp(tetInfo->strainEnergies[w]);
					}//end of else
				}//end of for w
				if (viscous){					
					Real productDgammaD;
					Coord vectGD=tetInfo->sumBgamma*svk;
					productDgammaD=dot(vectGD,svl);
					Matrix3 G;
					//G[0][1]=G[0][2]=G[1][0]=G[1][2]=G[2][0]=G[2][1]=0;
					G[0][0]=G[1][1]=G[2][2]=productDgammaD;
					Bij *= ((Real)1.0-sumA);
					Bij-=G*tetInfo->restVolume;	
				}
				edgeDfDx+=Bij;
			}// end of for j
			if(viscous) tetInfo->GammaOld=tetInfo->GammaNew;
		}//end of for i
		updateMatrix=false;

	}// end of if
}

template <class DataTypes> 
void MJEDTetrahedralForceField<DataTypes>::addDForce(const core::MechanicalParams* mparams /* PARAMS FIRST */, DataVecDeriv& d_df, const DataVecDeriv& d_dx)
{
        helper::WriteAccessor< Data< VecDeriv > > df = d_df;
        helper::ReadAccessor< Data< VecDeriv > > dx = d_dx;
        Real kFactor = (Real)mparams->kFactorIncludingRayleighDamping(this->rayleighStiffness.getValue());

	unsigned int l=0;
	unsigned int nbEdges=_topology->getNbEdges();
	const vector< Edge> &edgeArray=_topology->getEdges();

        helper::WriteAccessor< Data<sofa::type::vector<EdgeInformation> > > edgeInf = edgeInfo;
        EdgeInformation *einfo;

	this->updateMatrixData();			

	/// performs matrix vector computation
	unsigned int v0,v1;
	Deriv deltax;	Deriv dv0,dv1;

	for(l=0; l<nbEdges; l++ )
	{
		einfo=&edgeInf[l];
		v0=edgeArray[l][0];
		v1=edgeArray[l][1];

		deltax= dx[v0] - dx[v1];
		dv0 = einfo->DfDx * deltax;
		// do the transpose multiply:
		dv1[0] = (Real)(deltax[0]*einfo->DfDx[0][0] + deltax[1]*einfo->DfDx[1][0] + deltax[2]*einfo->DfDx[2][0]);
		dv1[1] = (Real)(deltax[0]*einfo->DfDx[0][1] + deltax[1]*einfo->DfDx[1][1] + deltax[2]*einfo->DfDx[2][1]);
		dv1[2] = (Real)(deltax[0]*einfo->DfDx[0][2] + deltax[1]*einfo->DfDx[1][2] + deltax[2]*einfo->DfDx[2][2]);
		// add forces
		df[v0] += dv1 * kFactor;
		df[v1] -= dv0 * kFactor;
	}
}

template <class DataTypes> 
void MJEDTetrahedralForceField<DataTypes>::addKToMatrix(sofa::linearalgebra::BaseMatrix *m, SReal kFactor, unsigned int &offset) {
	unsigned int l=0;
	unsigned int nbEdges=_topology->getNbEdges();
	const vector< Edge> &edgeArray=_topology->getEdges();

        helper::WriteAccessor< Data<sofa::type::vector<EdgeInformation> > > edgeInf = edgeInfo;
        EdgeInformation *einfo;

	this->updateMatrixData();

	/// performs matrix vector computation
	unsigned int v0,v1;

	for(l=0; l<nbEdges; l++ )
	{
		einfo=&edgeInf[l];
		v0=offset + edgeArray[l][0]*3;
		v1=offset + edgeArray[l][1]*3;

		for (int L=0;L<3;L++) {
			for (int C=0;C<3;C++) {
				double v = einfo->DfDx[L][C] * kFactor;
				m->add(v0+C,v0+L, v);
				m->add(v0+C,v1+L,-v);
				m->add(v1+L,v0+C,-v);
				m->add(v1+L,v1+C, v);
			}
		}
	}

}

template<class DataTypes>
void MJEDTetrahedralForceField<DataTypes>::draw(const core::visual::VisualParams* vparams)
{
	//	unsigned int i;
	if (!vparams->displayFlags().getShowForceFields()) return;
	if (!this->mstate) return;

	if (vparams->displayFlags().getShowWireFrame())
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

	if (vparams->displayFlags().getShowWireFrame())
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

}

template<class DataTypes>
type::Mat<3,3,double> MJEDTetrahedralForceField<DataTypes>::getPhi(int TetrahedronIndex)
{
        helper::WriteOnlyAccessor< Data<sofa::type::vector<TetrahedronRestInformation> > > tetrahedronInf = tetrahedronInfo;
        TetrahedronRestInformation *tetInfo;
	tetInfo=&tetrahedronInf[TetrahedronIndex];
	return tetInfo->deformationGradient;

}
template<class DataTypes>
type::Mat<3,3,double> MJEDTetrahedralForceField<DataTypes>::getForce(int TetrahedronIndex)
{
        helper::WriteOnlyAccessor< Data<sofa::type::vector<TetrahedronRestInformation> > > tetrahedronInf = tetrahedronInfo;
        TetrahedronRestInformation *tetInfo;
	tetInfo=&tetrahedronInf[TetrahedronIndex];
        type::Mat<3,3,double> force,inverseDeformationGradient;
	force.clear();
    const bool canInvert = inverseDeformationGradient.invert(tetInfo->deformationGradient);
    assert(canInvert);
    SOFA_UNUSED(canInvert);
	for(unsigned int w=0;w<isExponential.size();++w){
		if(!isExponential[w]){
			force+=(tetInfo->sumfS[w].MatSymMultiply(tetInfo->deformationGradient)+inverseDeformationGradient.transposed()*tetInfo->sumDfg[w]*tetInfo->J)*tetInfo->coeff[w];
		}
		else {
			force+=(tetInfo->sumfS[w].MatSymMultiply(tetInfo->deformationGradient)+inverseDeformationGradient.transposed()*tetInfo->sumDfg[w]*tetInfo->J)*tetInfo->coeff[w]*exp(tetInfo->strainEnergies[w]);
		}
	}//end of for w

	return force;
}

template<class DataTypes>
void MJEDTetrahedralForceField<DataTypes>::testDerivatives()
{
        DataVecCoord d_pos;
        VecCoord &pos = *d_pos.beginEdit();
        pos =  this->mstate->read(sofa::core::ConstVecCoordId::position())->getValue();

	// perturbate original state:
	srand( 0 );
	for (unsigned int idx=0; idx<pos.size(); idx++) {
		for (unsigned int d=0; d<3; d++) pos[idx][d] += (Real)0.01 * ((Real)rand()/(Real)(RAND_MAX - 0.5));
	}


	DataVecDeriv d_force1;
        helper::WriteAccessor< Data<VecDeriv > > force1 = d_force1;
	force1.resize( pos.size() );

	DataVecDeriv d_deltaPos;
        helper::WriteAccessor< Data<VecDeriv > > deltaPos = d_deltaPos;
	deltaPos.resize( pos.size() );

	DataVecDeriv d_deltaForceCalculated;
        helper::WriteAccessor< Data<VecDeriv > > deltaForceCalculated = d_deltaForceCalculated;
	deltaForceCalculated.resize( pos.size() );

	DataVecDeriv d_force2;
        helper::WriteAccessor< Data<VecDeriv > > force2 = d_force2;
	force2.resize( pos.size() );

	Coord epsilon, zero;
	Real cs = (Real)0.00001;
	Real errorThresh = (Real)200.0*cs*cs;
	Real errorNorm;
	Real avgError=0.0;
	int count=0;

        helper::WriteOnlyAccessor< Data<sofa::type::vector<TetrahedronRestInformation> > > tetrahedronInf = tetrahedronInfo;

	for (unsigned int moveIdx=0; moveIdx<pos.size(); moveIdx++)
	{
		for (unsigned int i=0; i<pos.size(); i++) {
			deltaForceCalculated[i] = zero;
			force1[i] = zero;
			force2[i] = zero;
		}
		//this->addForce( force1, pos, force1 );
		this->addForce( core::MechanicalParams::defaultInstance() /* PARAMS FIRST */, d_force1, d_pos, d_force1 );

		// get current energy around
		Real energy1 = 0;
		BaseMeshTopology::TetrahedraAroundVertex vTetras = _topology->getTetrahedraAroundVertex( moveIdx );
		for(unsigned int i = 0; i < vTetras.size(); ++i)
		{
			energy1 += tetrahedronInf[vTetras[i]].strainEnergy * tetrahedronInf[vTetras[i]].restVolume;
		}
		// generate random delta
		epsilon[0]= cs * ((Real)rand()/(Real)(RAND_MAX - 0.5));
		epsilon[1]= cs * ((Real)rand()/(Real)(RAND_MAX - 0.5));
		epsilon[2]= cs * ((Real)rand()/(Real)(RAND_MAX - 0.5));
		deltaPos[moveIdx] = epsilon;
		// calc derivative
		//this->addDForce( deltaForceCalculated, deltaPos);
		this->addDForce( core::MechanicalParams::defaultInstance() /* PARAMS FIRST */, d_deltaForceCalculated, d_deltaPos );

		deltaPos[moveIdx] = zero;
		// calc factual change
		pos[moveIdx] = pos[moveIdx] + epsilon;

		//this->addForce( force2, pos, force2 );
		this->addForce( core::MechanicalParams::defaultInstance() /* PARAMS FIRST */, d_force2, d_pos, d_force2 );

		pos[moveIdx] = pos[moveIdx] - epsilon;
		// check first derivative:
		Real energy2 = 0;
		for(unsigned int i = 0; i < vTetras.size(); ++i)
		{
			energy2 += tetrahedronInf[vTetras[i]].strainEnergy * tetrahedronInf[vTetras[i]].restVolume;
		}
		Coord forceAtMI = force1[moveIdx];
		Real deltaEnergyPredicted = -dot( forceAtMI, epsilon );
		Real deltaEnergyFactual = (energy2 - energy1);
		Real energyError = fabs( deltaEnergyPredicted - deltaEnergyFactual );
		if (energyError > 0.05*fabs(deltaEnergyFactual)) { // allow up to 5% error
			printf("Error energy %i = %f%%\n", moveIdx, 100.0*energyError/fabs(deltaEnergyFactual) );
		}

		// check 2nd derivative for off-diagonal elements:
		BaseMeshTopology::EdgesAroundVertex vEdges = _topology->getEdgesAroundVertex( moveIdx ); 
		for (unsigned int eIdx=0; eIdx<vEdges.size(); eIdx++)
		{
			BaseMeshTopology::Edge edge = _topology->getEdge( vEdges[eIdx] );
			unsigned int testIdx = edge[0];
			if (testIdx==moveIdx) testIdx = edge[1];
			Coord deltaForceFactual = force2[testIdx] - force1[testIdx];
			Coord deltaForcePredicted = deltaForceCalculated[testIdx];
			Coord error = deltaForcePredicted - deltaForceFactual;
			errorNorm = error.norm();
			errorThresh = (Real) 0.05 * deltaForceFactual.norm(); // allow up to 5% error
			if (deltaForceFactual.norm() > 0.0) {
				avgError += (Real)100.0*errorNorm/deltaForceFactual.norm();
				count++;
			}
			if (errorNorm > errorThresh) {
				printf("Error move %i test %i = %f%%\n", moveIdx, testIdx, 100.0*errorNorm/deltaForceFactual.norm() );
			}
		}
		// check 2nd derivative for diagonal elements:
		unsigned int testIdx = moveIdx;
		Coord deltaForceFactual = force2[testIdx] - force1[testIdx];
		Coord deltaForcePredicted = deltaForceCalculated[testIdx];
		Coord error = deltaForcePredicted - deltaForceFactual;
		errorNorm = error.norm();
		errorThresh = (Real)0.05 * deltaForceFactual.norm(); // allow up to 5% error
		if (errorNorm > errorThresh) {
			printf("Error move %i test %i = %f%%\n", moveIdx, testIdx, 100.0*errorNorm/deltaForceFactual.norm() );
		}
	}

	printf( "testDerivatives passed!\n" );
	avgError /= (Real)count;
        printf( "Average error = %.2f%%\n", avgError );
        d_pos.endEdit();
}

template<class DataTypes>
void MJEDTetrahedralForceField<DataTypes>::saveMesh( const char *filename )
{
	VecCoord pos(this->mstate->read(sofa::core::ConstVecCoordId::position())->getValue());
	core::topology::BaseMeshTopology::SeqTriangles triangles = _topology->getTriangles();
	FILE *file = fopen( filename, "wb" );
	if (!file) return;
	// write header
	char header[81];
    size_t errResult = 0;
	//strcpy( header, "STL generated by SOFA." );
        errResult = fwrite( (void*)&(header[0]),1, 80, file );
	unsigned int numTriangles = triangles.size();
        errResult = fwrite( &numTriangles, 4, 1, file );
	// write poly data
	float vertex[3][3];
	float normal[3] = { 1,0,0 };
	short stlSeperator = 0;

	for (unsigned int triangleId=0; triangleId<triangles.size(); triangleId++) {
		if (_topology->getTetrahedraAroundTriangle( triangleId ).size()==1) {
			// surface triangle, save it
			unsigned int p0 = _topology->getTriangle( triangleId )[0];
			unsigned int p1 = _topology->getTriangle( triangleId )[1];
			unsigned int p2 = _topology->getTriangle( triangleId )[2];
			for (int d=0; d<3; d++) {
				vertex[0][d] = (float)pos[p0][d];
				vertex[1][d] = (float)pos[p1][d];
				vertex[2][d] = (float)pos[p2][d];
			}
                        errResult = fwrite( (void*)&(normal[0]), sizeof(float), 3, file );
                        errResult = fwrite( (void*)&(vertex[0][0]), sizeof(float), 9, file );
                        errResult = fwrite( (void*)&(stlSeperator), 2, 1, file );
		}
	}

    errResult -= errResult; // ugly trick to avoid warnings

	fclose( file );
}


} // namespace sofa::component::forcefield
