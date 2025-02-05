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

#include <sofa/core/behavior/ForceField.h>
#include <sofa/component/statecontainer/MechanicalObject.h>
#include <sofa/type/Vec.h>
#include <sofa/type/Mat.h>
#include <sofa/type/MatSym.h>
#include <sofa/core/topology/BaseMeshTopology.h>
#include <sofa/core/topology/TopologyData.h>
#include <string>
#include <map>

namespace sofa::component::forcefield
{

using namespace std;
using namespace sofa::defaulttype;
using namespace sofa::core::topology;



//***************** Tetrahedron FEM code for several elastic models: Multiplicative Jacobian Energy Decomposition Method ***************************************
//****************** Based on strain enrergy W=sum f(J)G(I), then automatic caluclus are made to obtain Fi=-dW/dQi and Bij=d2W/dQidQj ***************************
//******************* It is dependant on the description of material following the model of sofa::component::fem::HyperelasticMaterial.h ************************
//***************************** more explication on MJED explication.pdf****************************

/** Compute Finite Element forces based on tetrahedral elements.*/
template<class DataTypes>
class MJEDTetrahedralForceField : public core::behavior::ForceField<DataTypes>
{
public:
    SOFA_CLASS(SOFA_TEMPLATE(MJEDTetrahedralForceField, DataTypes), SOFA_TEMPLATE(core::behavior::ForceField, DataTypes));

    typedef core::behavior::ForceField<DataTypes> Inherited;
    typedef typename DataTypes::VecCoord VecCoord;
    typedef typename DataTypes::VecDeriv VecDeriv;
    typedef typename DataTypes::Coord Coord;
    typedef typename DataTypes::Deriv Deriv;
    typedef typename Coord::value_type Real;

    typedef core::objectmodel::Data<VecDeriv>    DataVecDeriv;
    typedef core::objectmodel::Data<VecCoord>    DataVecCoord;

    typedef typename type::MatSym<3,Real> MatrixSym;
    typedef typename type::Mat<3,3,Real> Matrix3;


    typedef type::vector<Real> SetParameterArray; //necessary to store hyperelastic parameters (mu, lambda ...)
    typedef type::vector<Real> SetParameterAlpha; // necessary to store viscous parameter of Prony series (alpha infinity, alpha1, alpha2...)
    typedef type::vector<Real> SetParameterTau; // necessary to store viscous parameter (time ) of Prony series (deltaT, tau1,tau2..)
    typedef type::vector<Coord> SetAnisotropyDirectionArray; // When the model is anisotropic, for instance in invariant I4


    typedef sofa::Index Index;
    typedef core::topology::BaseMeshTopology::Tetra Element;
    typedef core::topology::BaseMeshTopology::SeqTetrahedra VecElement;


public :
    typedef typename sofa::component::fem::HyperelasticMaterialMJED<DataTypes>::HyperelasticMaterialTerm HyperelasticMatTerm;
    typename sofa::component::fem::HyperelasticMaterialMJED<DataTypes>::MaterialParameters globalParameters;


    class MatrixList
    {
    public:
        Matrix3 data[6];
        void clear(){
            this->data[0].clear();
            this->data[1].clear();
            this->data[2].clear();
            this->data[3].clear();
            this->data[4].clear();
            this->data[5].clear();
        }

    };


    /// data structure stored for each tetrahedron
    class TetrahedronRestInformation : public fem::HyperelasticMaterialMJED<DataTypes>::StrainInformation // inherit from HyperelasticMaterial.h where more data are stored
    {
    public:
        //vector of matrixlist to store precomputed linear Lij used in the second derivative of SPK tensor
        typedef std::vector< std::vector<MatrixList> > MatrixListMap;
        MatrixListMap Lij_first_k;
        MatrixListMap Lij_second_k;
        /// shape vector at the rest configuration
        Coord shapeVector[4];
        /// position points at the rest configuration
        Coord pointP[4];
        //precomputed Di cross Dj;
        Matrix3 DicrossDj[6];
        /// fiber direction in rest configuration
        Coord fiberDirection;
        /// rest volume
        Real restVolume;
        /// current tetrahedron volume
        Real volScale;
        /// derivatives of J
        Coord dJ[4];
        /// deformation gradient = gradPhi
        Matrix3 deformationGradient;
        /// current (=deformed) tetrahedron position eventually corrected for inverted tetrahedron
        Coord currentPos[4];
        /// area vector at the deformed configuration
        Coord areaVector[4];

        //For Prony series, tensor GammaOLd and New are registered
        std::vector<MatrixSym> GammaOld;
        std::vector<MatrixSym> GammaNew;
        // For Prony series , sum bi*gammai is stored
        MatrixSym sumBgamma;
        //First Piola Kirchhoff Tensor
        Matrix3 FPK;


        Real strainEnergy;//total strain energy

        /// use this vector to store values needed in AddForce and AddDforce
        std::vector<Real> strainEnergies;
        std::vector<MatrixSym> sumfS;
        std::vector<Real> sumDfg;
        std::vector<Real> functionf;
        std::vector<Real> functiong;
        std::vector<Real> functionDf;
        std::vector<Real> functionD2f;
        std::vector<MatrixSym> SPKTensor;
        std::vector<std::vector<Real> > coeffFirstpair;
        std::vector<std::vector<Real> > coeffSecondpair;
        std::vector<Real> coeff;

        /// Output stream
        inline friend ostream& operator<< ( ostream& os, const TetrahedronRestInformation& /*eri*/ ) {  return os;  }
        /// Input stream
        inline friend istream& operator>> ( istream& in, TetrahedronRestInformation& /*eri*/ ) { return in; }

        TetrahedronRestInformation() {}
    };

    /// data structure stored for each edge
    class EdgeInformation
    {
    public:
        /// store the stiffness edge matrix
        Matrix3 DfDx;

        /// Output stream
        inline friend ostream& operator<< ( ostream& os, const EdgeInformation& /*eri*/ ) {  return os;  }
        /// Input stream
        inline friend istream& operator>> ( istream& in, EdgeInformation& /*eri*/ ) { return in; }

        EdgeInformation() {}
    };

protected :
    core::topology::BaseMeshTopology* _topology;
    VecCoord  _initialPoints;	/// the intial positions of the points
    bool updateMatrix;
    bool  _meshSaved ;
    bool viscous;
    bool considerInversion;
    Data<bool> f_inversion;
    Data<bool> viscoelasticity; /// whether the material is viscous or not
    Data<bool> f_stiffnessMatrixRegularizationWeight; // if the regularization should be done
    bool stiffnessMatrixRegularizationWeight;
    Data<string> f_materialName; /// the name of the material
    Data<SetParameterArray> f_parameterSet;
    Data<SetParameterAlpha> f_parameterAlpha;
    Data<SetParameterTau> f_parameterTau;
    Data<SetAnisotropyDirectionArray> f_anisotropySet;
    Data<string> f_parameterFileName;
    vector<bool> isExponential; // To know if the strain energy is in exponential form or not, such as to adapt the calcul of force and stiffness
    vector<int> counter; // Used to know which term belongs to which exponential
    vector<Real> coeffA,coeffB; // For prony series, it calcules Ai =delatT alphai/(deltaT+taui) and Bi= taui/(deltaT+taui)
    Real sumA;

public:

    void setMaterialName(const string name)     { f_materialName.setValue(name); }
    void setparameter(const vector<Real> param) { f_parameterSet.setValue(param); }
    void setdirection(const vector<Coord> direction) { f_anisotropySet.setValue(direction); }
    void setalpha(const vector<Real> alpha)     { f_parameterAlpha.setValue(alpha); }
    void settau(const vector<Real> tau)         { f_parameterTau.setValue(tau); }
    void setviscous (const bool viscous)        { viscoelasticity.setValue(viscous); }

protected:

    MJEDTetrahedralForceField();

    virtual   ~MJEDTetrahedralForceField();

public:

    void init() override;

    void addForce(const core::MechanicalParams* mparams /* PARAMS FIRST */, DataVecDeriv& d_f, const DataVecCoord& d_x, const DataVecDeriv& d_v) override;
    void addDForce(const core::MechanicalParams* mparams /* PARAMS FIRST */, DataVecDeriv& d_df, const DataVecDeriv& d_dx) override;

    void addKToMatrix(sofa::linearalgebra::BaseMatrix *m, SReal kFactor, unsigned int &offset) override;
    virtual void updateMatrixData();

    SReal getPotentialEnergy(const core::MechanicalParams* /*mparams*/, const DataVecCoord& /*x*/) const override
    {
        return (SReal)0.0;
    }

    void draw(const core::visual::VisualParams* vparams) override;


    /** Method to initialize @sa TetrahedronRestInformation when a new Tetrahedron is created.
    * Will be set as creation callback in the TetrahedronData @sa tetrahedronInfo
    */
    void createTetrahedronRestInformation(Index, TetrahedronRestInformation& t,
        const core::topology::BaseMeshTopology::Tetrahedron&,
        const sofa::type::vector<Index>&,
        const sofa::type::vector<double>&);

    type::Mat<3,3,double> getPhi( int tetrahedronIndex);
    type::Mat<3,3,double> getForce( int tetrahedronIndex);
    TetrahedronData<sofa::type::vector<TetrahedronRestInformation> > tetrahedronInfo;
    EdgeData<sofa::type::vector<EdgeInformation> > edgeInfo;

protected:

    /// the array that describes the complete material energy and its derivatives
    std::vector<HyperelasticMatTerm *> materialTermArray;

    fem::HyperelasticMaterialMJED<DataTypes> *myMaterial;

    void testDerivatives();// a test to check the accuracy of Addforce and AddDforce, it needs the calculus of the total strain energy
    void saveMesh( const char *filename );

    VecCoord myposition;

};

using sofa::defaulttype::Vec3Types;

#if !defined(SOFA_COMPONENT_FORCEFIELD_MJEDTETRAHEDRALFORCEFIELD_CPP)
extern template class SOFA_MJED_FEM_API MJEDTetrahedralForceField<Vec3Types>;
#endif //!defined(SOFA_COMPONENT_FORCEFIELD_MJEDTETRAHEDRALFORCEFIELD_CPP)

} // namespace sofa::component::forcefield
