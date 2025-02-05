#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SofaCore" for configuration "MinSizeRel"
set_property(TARGET SofaCore APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaCore PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaCore.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofaCore.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaCore )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaCore "${_IMPORT_PREFIX}/lib/libSofaCore.so.24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
