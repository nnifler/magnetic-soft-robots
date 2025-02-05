#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SoftRobots.Inverse" for configuration "MinSizeRel"
set_property(TARGET SoftRobots.Inverse APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SoftRobots.Inverse PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSoftRobots.Inverse.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libSoftRobots.Inverse.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS SoftRobots.Inverse )
list(APPEND _IMPORT_CHECK_FILES_FOR_SoftRobots.Inverse "${_IMPORT_PREFIX}/lib/libSoftRobots.Inverse.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
