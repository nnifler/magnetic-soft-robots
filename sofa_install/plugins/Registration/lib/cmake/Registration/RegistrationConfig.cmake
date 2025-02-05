# CMake package configuration file for the Registration plugin


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was RegistrationConfig.cmake.in                            ########

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

set(REGISTRATION_HAVE_SOFADISTANCEGRID 1)
set(REGISTRATION_HAVE_IMAGE 1)

find_package(Sofa.GL QUIET REQUIRED)
find_package(Sofa.Component.IO.Mesh QUIET REQUIRED)
find_package(Sofa.Component.Engine.Generate QUIET REQUIRED)
find_package(Sofa.Component.Collision.Response.Mapper QUIET REQUIRED)

if(REGISTRATION_HAVE_SOFADISTANCEGRID)
    find_package(SofaDistanceGrid QUIET REQUIRED)
endif()
if(REGISTRATION_HAVE_IMAGE)
    find_package(Image QUIET REQUIRED)
endif()

if(NOT TARGET Registration)
	include("${CMAKE_CURRENT_LIST_DIR}/RegistrationTargets.cmake")
endif()

check_required_components(Registration)

set(Registration_LIBRARIES Registration)
set(Registration_INCLUDE_DIRS  ${REGISTRATION_INCLUDE_DIR})
