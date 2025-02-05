#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "STLIB" for configuration "MinSizeRel"
set_property(TARGET STLIB APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(STLIB PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSTLIB.so.3.0"
  IMPORTED_SONAME_MINSIZEREL "libSTLIB.so.3.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS STLIB )
list(APPEND _IMPORT_CHECK_FILES_FOR_STLIB "${_IMPORT_PREFIX}/lib/libSTLIB.so.3.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
