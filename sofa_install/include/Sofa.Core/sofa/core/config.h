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
#pragma once

#include <sofa/config.h>

#define SOFA_CORE_ENABLE_CRSMULTIMATRIXACCESSOR 0

#ifdef SOFA_BUILD_SOFA_CORE
#  define SOFA_TARGET Sofa.Core
#  define SOFA_CORE_API SOFA_EXPORT_DYNAMIC_LIBRARY
#else
#  define SOFA_CORE_API SOFA_IMPORT_DYNAMIC_LIBRARY
#endif


#ifdef SOFA_CORE_TOPOLOGY_ENABLE_DEPRECATION_MESSAGE

#define SOFA_CORE_TOPOLOGY_ATTRIBUTE_DEPRECATED__ALIASES_INDEX() \
    SOFA_CORE_TOPOLOGY_ATTRIBUTE_DEPRECATED("Index aliases are deprecated, please use sofa::Index.")

#else

#define SOFA_CORE_TOPOLOGY_ATTRIBUTE_DEPRECATED(msg)
#define SOFA_CORE_TOPOLOGY_ATTRIBUTE_DEPRECATED__ALIASES_INDEX()

#endif // SOFA_CORE_TOPOLOGY_ENABLE_DEPRECATION_MESSAGE

#ifdef SOFA_BUILD_SOFA_CORE
#define SOFA_ATTRIBUTE_DISABLED__SYMMETRICMATRIX(msg)
#else

#define SOFA_ATTRIBUTE_DISABLED__SYMMETRICMATRIX(msg) \
    SOFA_ATTRIBUTE_DISABLED("v23.12 (PR#3861)", "v24.06", msg)

#endif

#ifdef SOFA_BUILD_SOFA_CORE
#define SOFA_ATTRIBUTE_DISABLED__CONSTORDER()
#else
#define SOFA_ATTRIBUTE_DISABLED__CONSTORDER() \
    SOFA_ATTRIBUTE_DISABLED("v23.12", "v24.06", "ConstOrder is now a scoped enumeration. It must be used to access the values.")
#endif

#ifdef SOFA_BUILD_SOFA_CORE
#define SOFA_ATTRIBUTE_DEPRECATED__CORE_INTERSECTION_AS_PARAMETER()
#else
#define SOFA_ATTRIBUTE_DEPRECATED__CORE_INTERSECTION_AS_PARAMETER() \
    SOFA_ATTRIBUTE_DEPRECATED("v24.06", "v24.12", "Intersection detection methods now needs the Intersection method as a parameter.")
#endif
