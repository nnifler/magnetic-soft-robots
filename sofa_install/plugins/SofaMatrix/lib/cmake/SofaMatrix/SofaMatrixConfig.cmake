# CMake package configuration file for the plugin SofaMatrix

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was SofaMatrixConfig.cmake.in                            ########

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

set(SOFAMATRIX_HAVE_SOFA_GUI_QT 1)
set(SOFAMATRIX_HAVE_QT5CORE )
set(SOFAMATRIX_HAVE_QT6CORE )

find_package(Sofa.Core QUIET REQUIRED)
find_package(Sofa.Component.Constraint.Lagrangian.Solver QUIET REQUIRED)
find_package(Sofa.Component.LinearSolver.Direct QUIET REQUIRED)
find_package(Eigen3 QUIET REQUIRED)

if(SOFAMATRIX_HAVE_SOFA_GUI_QT )
    find_package(Sofa.GUI.Qt QUIET REQUIRED)
endif()
if(SOFAMATRIX_HAVE_QT5CORE)
    find_package(Qt5 COMPONENTS Core QUIET REQUIRED)
endif()
if(SOFAMATRIX_HAVE_QT6CORE)
    find_package(Qt6 COMPONENTS Core CoreTools QUIET)
endif()

if(NOT TARGET SofaMatrix)
    include("${CMAKE_CURRENT_LIST_DIR}/SofaMatrixTargets.cmake")
endif()

check_required_components(SofaMatrix)
