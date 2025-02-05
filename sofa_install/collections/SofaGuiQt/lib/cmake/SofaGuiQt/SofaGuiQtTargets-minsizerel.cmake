#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SofaGuiQt" for configuration "MinSizeRel"
set_property(TARGET SofaGuiQt APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaGuiQt PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaGuiQt.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofaGuiQt.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaGuiQt )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaGuiQt "${_IMPORT_PREFIX}/lib/libSofaGuiQt.so.24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
