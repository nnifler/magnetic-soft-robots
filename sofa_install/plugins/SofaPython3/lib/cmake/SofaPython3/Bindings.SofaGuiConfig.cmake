# CMake package configuration file for Bindings.SofaGui

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was Bindings.SofaGuiConfig.cmake.in                            ########

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

find_package(SofaPython3 QUIET REQUIRED COMPONENTS Plugin Bindings.Sofa)

find_package(Sofa.Core QUIET REQUIRED)
find_package(Sofa.GUI.Common QUIET REQUIRED)

if(Sofa.GUI.Batch_FOUND)
    find_package(Sofa.GUI.Batch QUIET REQUIRED)
endif()

if(Sofa.GUI.Qt_FOUND)
    find_package(Sofa.GUI.Qt QUIET REQUIRED)
endif()

if(Sofa.GUI.HeadlessRecorder_FOUND)
    find_package(Sofa.GUI.HeadlessRecorder QUIET REQUIRED)
endif()

# If we are importing this config file and the target is not yet there this is indicating that
# target is an imported one. So we include it
if(NOT TARGET Bindings.SofaGui)
    include("${CMAKE_CURRENT_LIST_DIR}/Bindings.SofaGuiTargets.cmake")
endif()

# Check that the component/target is there.
check_required_components(Bindings.SofaGui)
