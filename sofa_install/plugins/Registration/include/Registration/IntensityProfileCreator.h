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
#ifndef SOFA_REGISTRATION_IntensityProfileCreator_H
#define SOFA_REGISTRATION_IntensityProfileCreator_H

#include <Registration/config.h>
#include <image/ImageTypes.h>

#include <sofa/core/DataEngine.h>
#include <sofa/core/objectmodel/BaseObject.h>
#include <sofa/type/Vec.h>


namespace sofa
{

namespace component
{

namespace engine
{


/**
 * Create reference intensity profiles from custom values
 */


template <class _ImageTypes>
class IntensityProfileCreator : public core::DataEngine
{
public:
    typedef core::DataEngine Inherited;
    SOFA_CLASS(SOFA_TEMPLATE(IntensityProfileCreator,_ImageTypes),Inherited);

    typedef _ImageTypes ImageTypes;
    typedef typename ImageTypes::T T;
    typedef typename ImageTypes::imCoord imCoord;
    typedef helper::ReadAccessor<Data< ImageTypes > > raImage;

    Data< ImageTypes > image;
    Data< type::vector<T> > values; ///< intensity values for each line

    IntensityProfileCreator()    :   Inherited()
      , image(initData(&image,ImageTypes(),"image",""))
      , values(initData(&values,"values","intensity values for each line"))
    {
    }

    ~IntensityProfileCreator() override {}

    void init() override
    {
        addInput(&values);
        addOutput(&image);
        setDirtyValue();
    }

    void reinit() override { update(); }

protected:

    void doUpdate() override
    {
        helper::ReadAccessor<Data< type::vector<T> > > val(this->values);

        helper::WriteOnlyAccessor<Data< ImageTypes > > out(this->image);
        imCoord dim(val.size(),1,1,1,1);
        out->setDimensions(dim);
        cimg_library::CImg<T>& outImg=out->getCImg();
        for(size_t i=0;i<val.size();++i) outImg(i,0,0,0)=val[i];
    }

};


} // namespace engine

} // namespace component

} // namespace sofa

#endif // SOFA_REGISTRATION_IntensityProfileCreator_H
