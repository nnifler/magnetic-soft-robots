#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SofaPython3::Plugin" for configuration "MinSizeRel"
set_property(TARGET SofaPython3::Plugin APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaPython3::Plugin PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaPython3.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libSofaPython3.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaPython3::Plugin )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaPython3::Plugin "${_IMPORT_PREFIX}/lib/libSofaPython3.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
