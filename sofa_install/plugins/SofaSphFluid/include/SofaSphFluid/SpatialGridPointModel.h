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
#ifndef SOFA_COMPONENT_COLLISION_SPATIALGRIDPOINTMODEL_H
#define SOFA_COMPONENT_COLLISION_SPATIALGRIDPOINTMODEL_H
#include <SofaSphFluid/config.h>

#include <sofa/component/collision/geometry/PointModel.h>
#include <SofaSphFluid/SpatialGridContainer.h>
#include <sofa/defaulttype/VecTypes.h>
#include <vector>


namespace sofa::component::collision
{


class SOFA_SPH_FLUID_API SpatialGridPointModel : public geometry::PointCollisionModel<sofa::defaulttype::Vec3Types>
{
public:
    SOFA_CLASS(SpatialGridPointModel, geometry::PointCollisionModel<sofa::defaulttype::Vec3Types>);

    typedef container::SpatialGridContainer<defaulttype::Vec3Types> GridContainer;
    typedef GridContainer::Grid Grid;

    Data<int> d_leafScale; ///< at which level should the first cube layer be constructed. Note that this must not be greater than GRIDDIM_LOG2
protected:
    SpatialGridPointModel();
public:
    void init() override;

    // -- CollisionModel interface

    void computeBoundingTree(int maxDepth=0) override;

    Grid* getGrid() { return grid->getGrid(); }
protected:

    GridContainer* grid;
    class OctreeCell
    {
    public:
        Grid::Key k;
        int pfirst;
        int plast;
        OctreeCell( Grid::Key k = Grid::Key(), int pfirst = 0, int plast = -1)
            : k(k), pfirst(pfirst), plast(plast)
        {
        }
    };
    class OctreeSorter
    {
    public:
        int root_shift;
        OctreeSorter(int root_shift=8) : root_shift(root_shift) {}
        bool operator()(const Grid::Key& k1, const Grid::Key &k2);
        bool operator()(const OctreeCell& c1, const OctreeCell &c2)
        {
            return (*this)(c1.k,c2.k);
        }
    };
};

} // namespace sofa::component::collision


#endif
