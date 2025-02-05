#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Tearing" for configuration "MinSizeRel"
set_property(TARGET Tearing APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(Tearing PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libTearing.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libTearing.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS Tearing )
list(APPEND _IMPORT_CHECK_FILES_FOR_Tearing "${_IMPORT_PREFIX}/lib/libTearing.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
