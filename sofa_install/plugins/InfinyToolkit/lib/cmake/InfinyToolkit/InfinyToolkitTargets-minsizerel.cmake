#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "InfinyToolkit" for configuration "MinSizeRel"
set_property(TARGET InfinyToolkit APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(InfinyToolkit PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libInfinyToolkit.so.0.1"
  IMPORTED_SONAME_MINSIZEREL "libInfinyToolkit.so.0.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS InfinyToolkit )
list(APPEND _IMPORT_CHECK_FILES_FOR_InfinyToolkit "${_IMPORT_PREFIX}/lib/libInfinyToolkit.so.0.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
