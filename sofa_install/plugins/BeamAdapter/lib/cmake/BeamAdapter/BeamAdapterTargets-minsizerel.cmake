#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "BeamAdapter" for configuration "MinSizeRel"
set_property(TARGET BeamAdapter APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(BeamAdapter PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libBeamAdapter.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libBeamAdapter.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS BeamAdapter )
list(APPEND _IMPORT_CHECK_FILES_FOR_BeamAdapter "${_IMPORT_PREFIX}/lib/libBeamAdapter.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
