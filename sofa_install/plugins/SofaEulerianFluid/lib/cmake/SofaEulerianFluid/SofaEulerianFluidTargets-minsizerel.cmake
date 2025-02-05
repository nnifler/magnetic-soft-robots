#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SofaEulerianFluid" for configuration "MinSizeRel"
set_property(TARGET SofaEulerianFluid APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaEulerianFluid PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaEulerianFluid.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libSofaEulerianFluid.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaEulerianFluid )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaEulerianFluid "${_IMPORT_PREFIX}/lib/libSofaEulerianFluid.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
