#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "PluginExample" for configuration "MinSizeRel"
set_property(TARGET PluginExample APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(PluginExample PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libPluginExample.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libPluginExample.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS PluginExample )
list(APPEND _IMPORT_CHECK_FILES_FOR_PluginExample "${_IMPORT_PREFIX}/lib/libPluginExample.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
