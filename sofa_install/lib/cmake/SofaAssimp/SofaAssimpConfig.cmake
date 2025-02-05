# CMake package configuration file for the plugin 'SofaAssimp'

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was SofaAssimpConfig.cmake.in                            ########

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

set(SOFAASSIMP_HAVE_IMAGE 1)
set(SOFAASSIMP_HAVE_FLEXIBLE 0)

find_package(Assimp REQUIRED)
find_package(SofaLoader REQUIRED)
find_package(SofaOpenglVisual REQUIRED)
find_package(SofaBoundaryCondition REQUIRED)
find_package(SofaGeneralRigid REQUIRED)
find_package(SofaMeshCollision REQUIRED)

if(SOFAASSIMP_HAVE_IMAGE)
    find_package(image QUIET REQUIRED)
endif()
if(SOFAASSIMP_HAVE_FLEXIBLE)
    find_package(Flexible QUIET REQUIRED)
endif()

if(NOT TARGET SofaAssimp)
    include("${CMAKE_CURRENT_LIST_DIR}/SofaAssimpTargets.cmake")
endif()

set(SofaAssimp_INCLUDE_DIRS  /builds/workspace/sofa-custom/refs/heads/v24.06/ubuntu_gcc_release_full_python3.10/src/applications/plugins/SofaAssimp/../
                                 )

check_required_components(SofaAssimp)
