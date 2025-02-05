#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Sofa.GUI" for configuration "MinSizeRel"
set_property(TARGET Sofa.GUI APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(Sofa.GUI PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofa.GUI.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofa.GUI.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS Sofa.GUI )
list(APPEND _IMPORT_CHECK_FILES_FOR_Sofa.GUI "${_IMPORT_PREFIX}/lib/libSofa.GUI.so.24.06.00" )

# Import target "runSofa" for configuration "MinSizeRel"
set_property(TARGET runSofa APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(runSofa PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/bin/runSofa-24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS runSofa )
list(APPEND _IMPORT_CHECK_FILES_FOR_runSofa "${_IMPORT_PREFIX}/bin/runSofa-24.06.00" )

# Import target "runSofaGLFW" for configuration "MinSizeRel"
set_property(TARGET runSofaGLFW APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(runSofaGLFW PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/bin/runSofaGLFW-24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS runSofaGLFW )
list(APPEND _IMPORT_CHECK_FILES_FOR_runSofaGLFW "${_IMPORT_PREFIX}/bin/runSofaGLFW-24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
