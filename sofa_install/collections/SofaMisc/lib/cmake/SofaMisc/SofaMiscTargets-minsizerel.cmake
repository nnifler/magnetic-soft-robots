#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SofaMisc" for configuration "MinSizeRel"
set_property(TARGET SofaMisc APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaMisc PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaMisc.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofaMisc.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaMisc )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaMisc "${_IMPORT_PREFIX}/lib/libSofaMisc.so.24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
