# CMake package configuration file for the plugin PluginExample

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was PluginExampleConfig.cmake.in                            ########

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

set(PLUGINEXAMPLE_HAVE_SOFA_GUI_QT 1)
set(PLUGINEXAMPLE_HAVE_QT5_CORE 1)

find_package(Sofa.Component.Visual QUIET REQUIRED)

if(PLUGINEXAMPLE_HAVE_SOFA_GUI_QT)
    find_package(Sofa.GUI.Qt QUIET REQUIRED)
endif()
if(PLUGINEXAMPLE_HAVE_QT5_CORE)
    find_package(Qt5 COMPONENTS Core QUIET REQUIRED)
endif()

if(NOT TARGET PluginExample)
    include("${CMAKE_CURRENT_LIST_DIR}/PluginExampleTargets.cmake")
endif()

check_required_components(PluginExample)
