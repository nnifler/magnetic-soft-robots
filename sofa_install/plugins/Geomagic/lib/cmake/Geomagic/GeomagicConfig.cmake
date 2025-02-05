# CMake package configuration file for the plugin 'Geomagic'

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was GeomagicConfig.cmake.in                            ########

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

set(GEOMAGIC_HAVE_OPENHAPTICS "0")

find_package(Sofa.Config QUIET REQUIRED)
find_package(Sofa.Component.Controller QUIET REQUIRED)
find_package(Sofa.Component.IO.Mesh QUIET REQUIRED)
find_package(Sofa.Component.StateContainer QUIET REQUIRED)
find_package(Sofa.Component.Mapping.NonLinear QUIET REQUIRED)
find_package(Sofa.GL.Component.Rendering3D QUIET REQUIRED)
find_package(Sofa.Component.Haptics REQUIRED)

if(GEOMAGIC_HAVE_OPENHAPTICS)
    find_package(OpenHaptics QUIET REQUIRED)
endif()

if(NOT TARGET Geomagic)
    include("${CMAKE_CURRENT_LIST_DIR}/GeomagicTargets.cmake")
endif()

set(Geomagic_INCLUDE_DIRS  /builds/workspace/sofa-custom/refs/heads/v24.06/ubuntu_gcc_release_full_python3.10/src/applications/plugins/Geomagic/../
                                 OPENHAPTICS_INCLUDE_DIR-NOTFOUND)

check_required_components(Geomagic)
