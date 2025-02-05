# CMake package configuration file for the ModelOderReduction plugin


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was ModelOrderReductionConfig.cmake.in                            ########

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

find_package(Sofa.Core REQUIRED)
find_package(Sofa.Component.Collision.Response.Contact REQUIRED)
find_package(Sofa.Component.Mapping.MappedMatrix REQUIRED)
find_package(Sofa.Component.SolidMechanics.FEM.HyperElastic REQUIRED)
find_package(Sofa.Component.SolidMechanics.FEM.Elastic REQUIRED)
find_package(Sofa.GL REQUIRED)
find_package(CollisionOBBCapsule QUIET)

if(NOT TARGET ModelOrderReduction)
    include("${CMAKE_CURRENT_LIST_DIR}/ModelOrderReductionTargets.cmake")
endif()

check_required_components(ModelOrderReduction)
