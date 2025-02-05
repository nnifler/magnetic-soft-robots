# CMake package configuration file for the image plugin

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was imageConfig.cmake.in                            ########

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

set(IMAGE_HAVE_SOFA_GL 1)
set(IMAGE_HAVE_SOFA_GUI_QT 1)
set(IMAGE_HAVE_SOFAPYTHON 0)
set(IMAGE_HAVE_MULTITHREADING 1)
set(IMAGE_HAVE_ZLIB 1)
set(IMAGE_HAVE_FREENECT 0)

find_package(Sofa.Core QUIET REQUIRED)
find_package(Sofa.Component.Visual QUIET REQUIRED)
find_package(CImgPlugin QUIET REQUIRED)


if(IMAGE_HAVE_SOFA_GL)
    find_package(Sofa.GL QUIET REQUIRED)
endif()
if(IMAGE_HAVE_SOFAGUIQT)
    find_package(Sofa.GUI.Qt QUIET REQUIRED)
endif()
if(IMAGE_HAVE_SOFAPYTHON)
    find_package(SofaPython QUIET REQUIRED)
endif()
if(IMAGE_HAVE_MULTITHREADING)
    find_package(MultiThreading QUIET REQUIRED)
endif()
if(IMAGE_HAVE_ZLIB)
    find_package(ZLIB QUIET REQUIRED)
endif()
if(IMAGE_HAVE_FREENECT)
    find_package(Freenect QUIET REQUIRED)
endif()

if(NOT TARGET image)
	include("${CMAKE_CURRENT_LIST_DIR}/imageTargets.cmake")
endif()

check_required_components(image)
