#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SofaImplicitField" for configuration "MinSizeRel"
set_property(TARGET SofaImplicitField APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaImplicitField PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_MINSIZEREL "SofaDistanceGrid"
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaImplicitField.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libSofaImplicitField.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaImplicitField )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaImplicitField "${_IMPORT_PREFIX}/lib/libSofaImplicitField.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
