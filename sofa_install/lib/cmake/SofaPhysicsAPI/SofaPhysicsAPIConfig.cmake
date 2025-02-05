# CMake package configuration file for SofaPhysicsAPI


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was SofaPhysicsAPIConfig.cmake.in                            ########

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

set(SOFAPHYSICSAPI_HAVE_SOFAVALIDATION 1)

find_package(Sofa.Simulation.Graph QUIET REQUIRED)
find_package(Sofa.Component QUIET REQUIRED)
find_package(Sofa.GUI.Common QUIET REQUIRED)

if(SOFAPHYSICSAPI_HAVE_SOFAVALIDATION)
	find_package(SofaValidation QUIET REQUIRED)
endif()

if(NOT TARGET SofaPhysicsAPI)
	include("${CMAKE_CURRENT_LIST_DIR}/SofaPhysicsAPITargets.cmake")
endif()

check_required_components(SofaPhysicsAPI)
