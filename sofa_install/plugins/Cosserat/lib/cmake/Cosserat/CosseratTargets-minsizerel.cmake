#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "CosseratBindings" for configuration "MinSizeRel"
set_property(TARGET CosseratBindings APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(CosseratBindings PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_MINSIZEREL "Python::Python"
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/python3/site-packages/Cosserat.cpython-310-x86_64-linux-gnu.so"
  IMPORTED_SONAME_MINSIZEREL "Cosserat.cpython-310-x86_64-linux-gnu.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS CosseratBindings )
list(APPEND _IMPORT_CHECK_FILES_FOR_CosseratBindings "${_IMPORT_PREFIX}/lib/python3/site-packages/Cosserat.cpython-310-x86_64-linux-gnu.so" )

# Import target "Cosserat" for configuration "MinSizeRel"
set_property(TARGET Cosserat APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(Cosserat PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libCosserat.so.21.12.0"
  IMPORTED_SONAME_MINSIZEREL "libCosserat.so.21.12.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS Cosserat )
list(APPEND _IMPORT_CHECK_FILES_FOR_Cosserat "${_IMPORT_PREFIX}/lib/libCosserat.so.21.12.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
