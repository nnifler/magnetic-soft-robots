#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Geomagic" for configuration "MinSizeRel"
set_property(TARGET Geomagic APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(Geomagic PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libGeomagic.so.0.1"
  IMPORTED_SONAME_MINSIZEREL "libGeomagic.so.0.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS Geomagic )
list(APPEND _IMPORT_CHECK_FILES_FOR_Geomagic "${_IMPORT_PREFIX}/lib/libGeomagic.so.0.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
