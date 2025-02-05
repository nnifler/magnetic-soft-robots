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
#ifndef SOFA_COMPONENT_FORCEFIELD_InvertibleFVMForceField_H
#define SOFA_COMPONENT_FORCEFIELD_InvertibleFVMForceField_H

#include <InvertibleFVM/config.h>
#include <sofa/core/behavior/ForceField.h>
#include <sofa/core/topology/BaseMeshTopology.h>
#include <sofa/type/vector.h>
#include <sofa/defaulttype/VecTypes.h>
#include <sofa/type/Mat.h>
#include <sofa/type/Vec.h>

namespace sofa
{

namespace component
{

namespace forcefield
{

template<class DataTypes>
class InvertibleFVMForceField;

/// This class can be overridden if needed for additionnal storage within template specializations.
template<class DataTypes>
class InvertibleFVMForceFieldInternalData
{
public:
};


/** Compute Finite Volume forces based on tetrahedral and hexahedral elements.
 * implementation of "invertible FEM..."
*/
template<class DataTypes>
class InvertibleFVMForceField : virtual public core::behavior::ForceField<DataTypes>
{
public:
    SOFA_CLASS(SOFA_TEMPLATE(InvertibleFVMForceField, DataTypes), SOFA_TEMPLATE(core::behavior::ForceField, DataTypes));

    typedef typename DataTypes::VecCoord VecCoord;
    typedef typename DataTypes::VecDeriv VecDeriv;
    typedef typename DataTypes::VecReal VecReal;
    typedef VecCoord Vector;
    typedef typename DataTypes::Coord Coord;
    typedef typename DataTypes::Deriv Deriv;
    typedef typename Coord::value_type Real;

    typedef core::objectmodel::Data<VecDeriv>    DataVecDeriv;
    typedef core::objectmodel::Data<VecCoord>    DataVecCoord;

    typedef sofa::Index Index;
    typedef core::topology::BaseMeshTopology::Tetra Tetra;
    typedef core::topology::BaseMeshTopology::SeqTetrahedra VecTetra;



protected:

    /// @name Per tetrahedron data
    /// @{

    /// Displacement vector (deformation of the 4 corners of a tetrahedron)
    typedef type::VecNoInit<12, Real> Displacement;

    /// Rigid transformation (rotation) matrix
    typedef type::MatNoInit<3, 3, Real> Transformation;

    /// @}

    type::vector<Transformation> _rotationsU;
    type::vector<Transformation> _rotationsV;

    core::topology::BaseMeshTopology* _mesh;
    const VecTetra *_indexedTetra;

    type::vector<Transformation> _initialTransformation;
    type::vector<Transformation> _initialRotation;

    type::vector<Transformation> _U;
    type::vector<Transformation> _V;
    type::vector<type::Vec<3,Coord> > _b;

    InvertibleFVMForceFieldInternalData<DataTypes> data;
    friend class InvertibleFVMForceFieldInternalData<DataTypes>;

public:


    Data< VecCoord > _initialPoints; ///< the intial positions of the points

    Data<Real> _poissonRatio; ///< FEM Poisson Ratio [0,0.5[
    Data<VecReal > _youngModulus; ///< FEM Young Modulus
    Data<VecReal> _localStiffnessFactor; ///< Allow specification of different stiffness per element. If there are N element and M values are specified, the youngModulus factor for element i would be localStiffnessFactor[i*M/N]


    Data< bool > drawHeterogeneousTetra; ///< Draw Heterogeneous Tetra in different color
    Data< bool > drawAsEdges; ///< Draw as edges instead of tetrahedra

    Data< bool > _verbose; ///< Print debug stuff

    Real minYoung;
    Real maxYoung;
protected:
    InvertibleFVMForceField() ;
    virtual ~InvertibleFVMForceField() ;

public:
    void setPoissonRatio(Real val) ;
    void setYoungModulus(Real val) ;

    void reset() override ;
    void init() override ;
    void reinit()override ;

    void addForce(const core::MechanicalParams* mparams,
                          DataVecDeriv& d_f, const DataVecCoord& d_x, const DataVecDeriv& d_v) override ;

    void addDForce(const core::MechanicalParams* mparams,
                           DataVecDeriv& , const DataVecDeriv& ) override ;

    void addKToMatrix(sofa::linearalgebra::BaseMatrix *m, SReal kFactor, unsigned int &offset) override ;

    SReal getPotentialEnergy(const core::MechanicalParams* mparams,
                                     const DataVecCoord&  x) const override ;

    void draw(const core::visual::VisualParams* vparams) override;
};

#if  !defined(SOFA_COMPONENT_FORCEFIELD_InvertibleFVMForceField_CPP)
extern template class SOFA_InvertibleFVM_API InvertibleFVMForceField<defaulttype::Vec3Types>;

#endif

} // namespace forcefield

} // namespace component

} // namespace sofa

#endif
