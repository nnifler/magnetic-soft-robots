#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Sofa.Component.LinearSolver.Direct" for configuration "MinSizeRel"
set_property(TARGET Sofa.Component.LinearSolver.Direct APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(Sofa.Component.LinearSolver.Direct PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofa.Component.LinearSolver.Direct.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofa.Component.LinearSolver.Direct.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS Sofa.Component.LinearSolver.Direct )
list(APPEND _IMPORT_CHECK_FILES_FOR_Sofa.Component.LinearSolver.Direct "${_IMPORT_PREFIX}/lib/libSofa.Component.LinearSolver.Direct.so.24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
