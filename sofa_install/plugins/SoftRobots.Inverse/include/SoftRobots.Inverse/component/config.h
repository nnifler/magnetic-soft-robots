/******************************************************************************
*       SOFA, Simulation Open-Framework Architecture, version 1.0 RC 1        *
*                (c) 2006-2011 MGH, INRIA, USTL, UJF, CNRS                    *
*                                                                             *
* This library is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This library is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this library; if not, write to the Free Software Foundation,     *
* Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.          *
*******************************************************************************
*                               SOFA :: Plugins                               *
*                                                                             *
* Authors: Christian Duriez                                                   *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/
#pragma once

#include <sofa/helper/config.h>

#ifdef SOFA_BUILD_SOFTROBOTS_INVERSE
#  define SOFA_TARGET SoftRobots.Inverse
#  define SOFA_SOFTROBOTS_INVERSE_API SOFA_EXPORT_DYNAMIC_LIBRARY
#  define SOFA_ATTRIBUTE_DEPRECATED__RENAME_NAMESPACE_SOFTROBOTS_INVERSE()
#else
#  define SOFA_SOFTROBOTS_INVERSE_API SOFA_IMPORT_DYNAMIC_LIBRARY
#  define SOFA_ATTRIBUTE_DEPRECATED__RENAME_NAMESPACE_SOFTROBOTS_INVERSE() \
    SOFA_ATTRIBUTE_DEPRECATED( \
        "v23.06", "v23.12", \
        "Namespace in the plugin SoftRobots.Inverse is now 'softrobotsinverse'.")
#endif

namespace softrobotsinverse
{
	constexpr const char* MODULE_NAME = "SoftRobots.Inverse";
	constexpr const char* MODULE_VERSION = "1.0";
}
