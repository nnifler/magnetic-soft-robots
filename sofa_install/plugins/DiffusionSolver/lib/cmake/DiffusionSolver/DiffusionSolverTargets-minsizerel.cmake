#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "DiffusionSolver" for configuration "MinSizeRel"
set_property(TARGET DiffusionSolver APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(DiffusionSolver PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libDiffusionSolver.so.0.1"
  IMPORTED_SONAME_MINSIZEREL "libDiffusionSolver.so.0.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS DiffusionSolver )
list(APPEND _IMPORT_CHECK_FILES_FOR_DiffusionSolver "${_IMPORT_PREFIX}/lib/libDiffusionSolver.so.0.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
