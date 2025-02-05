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
#ifndef SOFA_COMPONENT_ENGINE_INERTIAALIGN_H
#define SOFA_COMPONENT_ENGINE_INERTIAALIGN_H

#include <sofa/core/objectmodel/BaseObject.h>
#include <sofa/defaulttype/VecTypes.h>
#include <sofa/type/vector.h>
#include <sofa/core/topology/Topology.h>
#include <sofa/type/Vec.h>
#include <sofa/type/Mat.h>
#include <Eigen/Dense>
#include <Eigen/Core>
#include <Eigen/Geometry>
#include <Eigen/LU>
namespace sofa
{

namespace component
{


class InertiaAlign: public sofa::core::objectmodel::BaseObject
{
public:
    SOFA_CLASS(InertiaAlign,core::objectmodel::BaseObject);

    InertiaAlign();
    ~InertiaAlign() override;
    typedef type::Mat<3,3> Mat3x3;

    /**
      * Data Fields
      */
    /// input
    Data <sofa::type::Vec3> targetC;
    Data <sofa::type::Vec3> sourceC; ///< input: the gravity center of the source mesh

    Data < Mat3x3 > targetInertiaMatrix; ///< input: the inertia matrix of the target mesh
    Data < Mat3x3 > sourceInertiaMatrix; ///< input: the inertia matrix of the source mesh

    /// input//output
    Data< type::vector<sofa::type::Vec<3,SReal> > > m_positiont;
    Data< type::vector<sofa::type::Vec<3,SReal> > > m_positions; ///< input: positions of the source vertices
    type::vector<sofa::type::Vec<3,SReal> > positionDistSource;

    /// Initialization method called at graph modification, during bottom-up traversal.
    void init() override;

protected:

    typedef type::Vec3 Vector3;
    typedef type::Matrix4 Matrix4;

    SReal computeDistances(type::vector<sofa::type::Vec<3,SReal> >, type::vector<sofa::type::Vec<3,SReal> >);
    SReal distance(sofa::type::Vec<3,SReal>, type::vector<sofa::type::Vec<3,SReal> >);
    SReal abs(SReal);

    Matrix4 inverseTransform(Matrix4);
    /**
      * Protected methods
      */
public:


};


} // namespace component

} // namespace sofa

#endif
