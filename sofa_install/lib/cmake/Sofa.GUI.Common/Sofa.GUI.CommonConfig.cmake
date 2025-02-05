# CMake package configuration file for the Sofa.GUI.Common module

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was Sofa.GUI.CommonConfig.cmake.in                            ########

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

set(SOFA_GUI_COMMON_HAVE_SOFA_GL 1)

find_package(Sofa.Simulation.Common REQUIRED)
find_package(Sofa.Component.Setting QUIET REQUIRED)
find_package(Sofa.Component.Collision.Response.Contact QUIET REQUIRED)
find_package(Sofa.GUI.Component QUIET REQUIRED)
if(NOT TARGET cxxopts)
    find_package(cxxopts QUIET REQUIRED)
endif()

if(SOFA_GUI_COMMON_HAVE_SOFA_GL)
    find_package(Sofa.GL QUIET REQUIRED)
endif()

if(NOT TARGET Sofa.GUI.Common)
    include("${CMAKE_CURRENT_LIST_DIR}/Sofa.GUI.CommonTargets.cmake")
endif()

check_required_components(Sofa.GUI.Common)
