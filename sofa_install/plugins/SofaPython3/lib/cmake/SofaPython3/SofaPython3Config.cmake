# CMake package configuration file for SofaPython3


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was SofaPython3Config.cmake.in                            ########

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

set(SP3_WITH_SOFAEXPORTER ON)
set(SP3_PYTHON_PACKAGES_DIRECTORY python3/site-packages)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
include(SofaPython3Tools)

# Find Python3
if(NOT Python_FOUND)
    find_package(Python 3.10 EXACT QUIET REQUIRED COMPONENTS Interpreter Development)
endif()

# Find pybind11
if(NOT pybind11_FOUND)
    # Save PYTHON_* vars
    set(PYTHON_VERSION_RESET "${PYTHON_VERSION}")
    set(PYTHON_EXECUTABLE_RESET "${PYTHON_EXECUTABLE}")
    set(PYTHON_LIBRARIES_RESET "${PYTHON_LIBRARIES}")
    set(PYTHON_INCLUDE_DIRS_RESET "${PYTHON_INCLUDE_DIRS}")
    set(PYTHON_LIBRARY_RESET "${PYTHON_LIBRARY}")
    set(PYTHON_INCLUDE_DIR_RESET "${PYTHON_INCLUDE_DIR}")

    # Change PYTHON_* vars before pybind11 find_package
    # to be sure that pybind11 relies on the right Python version
    set(PYTHON_VERSION "${Python_VERSION}" CACHE STRING "" FORCE)
    set(PYTHON_EXECUTABLE "${Python_EXECUTABLE}" CACHE FILEPATH "" FORCE)
    set(PYTHON_LIBRARIES "${Python_LIBRARIES}" CACHE STRING "" FORCE)
    set(PYTHON_INCLUDE_DIRS "${Python_INCLUDE_DIRS}" CACHE STRING "" FORCE)
    if(EXISTS "${Python_LIBRARY}")
        set(PYTHON_LIBRARY "${Python_LIBRARY}" CACHE INTERNAL "" FORCE)
    elseif(EXISTS "${Python_LIBRARIES}")
        set(PYTHON_LIBRARY "${Python_LIBRARIES}" CACHE INTERNAL "" FORCE)
    endif()
    if(EXISTS "${Python_INCLUDE_DIR}")
        set(PYTHON_INCLUDE_DIR "${Python_INCLUDE_DIR}" CACHE INTERNAL "" FORCE)
    elseif(EXISTS "${Python_INCLUDE_DIRS}")
        set(PYTHON_INCLUDE_DIR "${Python_INCLUDE_DIRS}" CACHE INTERNAL "" FORCE)
    endif()

    find_package(pybind11 2.9.1 QUIET REQUIRED CONFIG)

    # Reset PYTHON_* vars
    set(PYTHON_VERSION "${PYTHON_VERSION_RESET}" CACHE STRING "" FORCE)
    set(PYTHON_EXECUTABLE "${PYTHON_EXECUTABLE_RESET}" CACHE FILEPATH "" FORCE)
    set(PYTHON_LIBRARIES "${PYTHON_LIBRARIES_RESET}" CACHE STRING "" FORCE)
    set(PYTHON_INCLUDE_DIRS "${PYTHON_INCLUDE_DIRS_RESET}" CACHE STRING "" FORCE)
    set(PYTHON_LIBRARY "${PYTHON_LIBRARY_RESET}" CACHE INTERNAL "" FORCE)
    set(PYTHON_INCLUDE_DIR "${PYTHON_INCLUDE_DIR_RESET}" CACHE INTERNAL "" FORCE)
endif()

# Find SofaPython3::XXXXX
if(NOT SofaPython3_FIND_COMPONENTS)
    set(SofaPython3_FIND_COMPONENTS Plugin Bindings)
endif()
foreach(component ${SofaPython3_FIND_COMPONENTS})
    if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/${component}Config.cmake")
        # For requested component, execute its "config" script
        set_and_check(config_file ${CMAKE_CURRENT_LIST_DIR}/${component}Config.cmake)
        include(${config_file})
        set(SofaPython3_${component}_FOUND True)
    else()
        set(SofaPython3_FOUND False)
        set(SofaPython3_NOT_FOUND_MESSAGE "Unsupported component: ${component}.")
    endif()
endforeach()

# Check that the component/target is there.
check_required_components(SofaPython3)
