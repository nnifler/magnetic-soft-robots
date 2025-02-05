# CMake package configuration file for SofaMiscCollision

if(NOT "${CMAKE_PROJECT_NAME}" STREQUAL "Sofa" OR NOT "${PROJECT_SOURCE_DIR}" MATCHES "${CMAKE_SOURCE_DIR}/.*")
    # The project doing find_package is not a subproject of SOFA or is not located inside SOFA
    get_property(SofaMiscCollision_SENT_DEPRECATION_MESSAGE GLOBAL PROPERTY PROPERTY_SofaMiscCollision_SENT_DEPRECATION_MESSAGE SET)
    if(NOT SofaMiscCollision_SENT_DEPRECATION_MESSAGE)
        message(WARNING "SofaMiscCollision module is deprecated. It will be removed at v23.06. Use Sofa.Component.Collision.Geometry, Sofa.Component.Collision.Detection.Intersection and Sofa.Component.Collision.Response.Contact instead. Moreover, OBB and Capsule-related components have been moved into the external plugin CollisionOBBCapsule.")
    endif()
    set_property(GLOBAL PROPERTY PROPERTY_SofaMiscCollision_SENT_DEPRECATION_MESSAGE TRUE)
endif()

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was SofaMiscCollisionConfig.cmake.in                            ########

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

find_package(SofaBaseCollision QUIET REQUIRED)
find_package(SofaBaseTopology QUIET REQUIRED)
find_package(SofaGeneralMeshCollision QUIET REQUIRED)
find_package(SofaGeneralDeformable QUIET REQUIRED)
find_package(SofaConstraint QUIET REQUIRED)
find_package(SofaExplicitOdeSolver QUIET REQUIRED)
find_package(SofaGeneralExplicitOdeSolver QUIET REQUIRED)
find_package(SofaImplicitOdeSolver QUIET REQUIRED)

find_package(Sofa.Component.Collision.Geometry QUIET REQUIRED)
find_package(Sofa.Component.Collision.Detection.Intersection QUIET REQUIRED)
find_package(Sofa.Component.Collision.Response.Contact QUIET REQUIRED)

if(NOT TARGET SofaMiscCollision)
    include("${CMAKE_CURRENT_LIST_DIR}/SofaMiscCollisionTargets.cmake")
endif()

check_required_components(SofaMiscCollision)
set(SofaMiscCollision_LIBRARIES SOFAMISCCOLLISION)
set(SofaMiscCollision_INCLUDE_DIRS  ${SOFAMISCCOLLISION_INCLUDE_DIR})
