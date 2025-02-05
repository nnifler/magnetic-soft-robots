# CMake package configuration file for the SofaCUDA plugin

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was SofaCUDAConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

list(FIND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}" HAS_SOFACUDA_CMAKE_MODULE_PATH)
if(HAS_SOFACUDA_CMAKE_MODULE_PATH EQUAL -1)
    list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR})
endif()

set(SOFACUDA_ARCH )

find_package(Sofa.Component.Mass QUIET REQUIRED)
find_package(Sofa.Component.SolidMechanics.FEM.Elastic QUIET REQUIRED)
find_package(Sofa.Component.SolidMechanics.FEM.HyperElastic QUIET REQUIRED)
find_package(Sofa.Component.SolidMechanics.TensorMass QUIET REQUIRED)
find_package(Sofa.Component.Collision.Response.Contact QUIET REQUIRED)
find_package(Sofa.Component.Collision.Detection.Intersection QUIET REQUIRED)
find_package(Sofa.Component.StateContainer QUIET REQUIRED)
find_package(Sofa.Component.Constraint.Projective QUIET REQUIRED)
find_package(Sofa.Component.Mapping.Linear QUIET REQUIRED)
find_package(Sofa.Component.Mapping.NonLinear QUIET REQUIRED)
find_package(Sofa.Component.Engine.Select QUIET REQUIRED)
find_package(Sofa.Component.Engine.Transform QUIET REQUIRED)
find_package(Sofa.Component.MechanicalLoad QUIET REQUIRED)
find_package(CUDA QUIET REQUIRED)


set(SOFACUDA_HAVE_SOFA_GL 1)
if(SOFACUDA_HAVE_SOFA_GL)
	find_package(Sofa.GL QUIET REQUIRED)
endif()

set(SOFACUDA_HAVE_SOFA_GUI_QT 1)
if(SOFACUDA_HAVE_SOFA_GUI_QT)
	find_package(Sofa.GUI.Qt QUIET REQUIRED)
endif()

set(SOFACUDA_HAVE_SOFADISTANCEGRID )
set(SOFACUDA_HAVE_MINIFLOWVR 0)
if(SOFACUDA_HAVE_SOFADISTANCEGRID)
	find_package(SofaDistanceGrid QUIET REQUIRED)
	if(SOFACUDA_HAVE_MINIFLOWVR)
		find_package(miniFlowVR QUIET REQUIRED)
	endif()
endif()

set(SOFACUDA_HAVE_SOFASPHFLUID )
if(SOFACUDA_HAVE_SOFASPHFLUID)
	find_package(SofaSphFluid QUIET REQUIRED)
endif()

set(SOFACUDA_HAVE_SOFAVALIDATION 1)
if(SOFACUDA_HAVE_SOFAVALIDATION)
	find_package(SofaValidation QUIET REQUIRED)
endif()

if(NOT TARGET SofaCUDA)
	include("${CMAKE_CURRENT_LIST_DIR}/SofaCUDATargets.cmake")
endif()

check_required_components(SofaCUDA)

include(SofaCUDANvccFlags)
