# CMake package configuration file for Plugin

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was PluginConfig.cmake.in                            ########

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

set(SP3_BUILD_TEST ON)

find_package(pybind11 QUIET REQUIRED CONFIG)
find_package(Sofa.Simulation.Graph QUIET REQUIRED)

if(SP3_BUILD_TEST)
    find_package(Sofa.Testing QUIET REQUIRED)
endif()

# If we are importing this config file and the target is not yet there this is indicating that
# target is an imported one. So we include it
if(NOT TARGET Plugin)
    include("${CMAKE_CURRENT_LIST_DIR}/PluginTargets.cmake")
endif()

# Check that the component/target is there.
check_required_components(Plugin)
