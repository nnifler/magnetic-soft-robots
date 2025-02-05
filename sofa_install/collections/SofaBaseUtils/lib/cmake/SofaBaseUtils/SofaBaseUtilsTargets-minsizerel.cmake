#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SofaBaseUtils" for configuration "MinSizeRel"
set_property(TARGET SofaBaseUtils APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaBaseUtils PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaBaseUtils.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofaBaseUtils.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaBaseUtils )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaBaseUtils "${_IMPORT_PREFIX}/lib/libSofaBaseUtils.so.24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
