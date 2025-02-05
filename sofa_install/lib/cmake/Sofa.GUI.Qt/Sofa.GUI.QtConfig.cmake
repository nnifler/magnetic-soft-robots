# CMake package configuration file for the Sofa.GUI.Qt module

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was Sofa.GUI.QtConfig.cmake.in                            ########

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

set(SOFA_GUI_QT_HAVE_QT5 1)
set(SOFA_GUI_QT_HAVE_QT6 )

set(SOFA_GUI_QT_ENABLE_QTVIEWER ON)
set(SOFA_GUI_QT_ENABLE_QGLVIEWER ON)
set(SOFA_GUI_QT_ENABLE_NATIVE_MENU ON)
set(SOFA_GUI_QT_ENABLE_VSYNC OFF)

set(SOFA_GUI_QT_HAVE_QT5_CHARTS 1)
set(SOFA_GUI_QT_HAVE_QT5_WEBENGINE )
set(SOFA_GUI_QT_HAVE_NODEEDITOR )
set(SOFA_GUI_QT_HAVE_TINYXML )

set(SOFA_GUI_QT_HAVE_QT6_CHARTS )
set(SOFA_GUI_QT_HAVE_QT6_WEBENGINECORE )

# This is needed to be able to find plugins/SofaGuiQt/lib/cmake/QGLViewer
list(APPEND CMAKE_PREFIX_PATH "${CMAKE_CURRENT_LIST_DIR}/..")

find_package(Sofa.GUI.Common QUIET REQUIRED)
find_package(Sofa.Component.Visual QUIET REQUIRED)
find_package(Sofa.Component.SceneUtility QUIET REQUIRED)

if(SOFA_GUI_QT_HAVE_QT5)
    find_package(Qt5 QUIET REQUIRED Core Gui OpenGL)
    if(SOFA_GUI_QT_HAVE_QT5_CHARTS)
        find_package(Qt5 QUIET REQUIRED Charts)
    endif()
    if(SOFA_GUI_QT_HAVE_QT5_WEBENGINE)
        find_package(Qt5 QUIET REQUIRED WebEngine WebEngineWidgets)
    endif()
    if(SOFA_GUI_QT_ENABLE_QGLVIEWER)
        find_package(QGLViewer QUIET REQUIRED)
    endif()
elseif(SOFA_GUI_QT_HAVE_QT6)
    find_package(Qt6 COMPONENTS Widgets OpenGLWidgets QUIET REQUIRED)
    if(SOFA_GUI_QT_HAVE_QT6_CHARTS)
        find_package(Qt6 QUIET REQUIRED Charts)
    endif()
    if(SOFA_GUI_QT_HAVE_QT6_WEBENGINECORE)
        find_package(Qt6 QUIET REQUIRED Positioning WebChannel WebEngineCore WebEngineWidgets)
    endif()
    if(SOFA_GUI_QT_ENABLE_QGLVIEWER)
        find_package(QGLViewer QUIET REQUIRED)
    endif()
endif()

if(SOFA_GUI_QT_HAVE_NODEEDITOR)
    find_package(NodeEditor QUIET REQUIRED)
endif()


if(NOT TARGET Sofa.GUI.Qt)
    include("${CMAKE_CURRENT_LIST_DIR}/Sofa.GUI.QtTargets.cmake")
endif()

check_required_components(Sofa.GUI.Qt)
