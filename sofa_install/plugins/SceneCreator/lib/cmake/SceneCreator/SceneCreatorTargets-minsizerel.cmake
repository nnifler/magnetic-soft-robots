#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SceneCreator" for configuration "MinSizeRel"
set_property(TARGET SceneCreator APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SceneCreator PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSceneCreator.so.0.1"
  IMPORTED_SONAME_MINSIZEREL "libSceneCreator.so.0.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS SceneCreator )
list(APPEND _IMPORT_CHECK_FILES_FOR_SceneCreator "${_IMPORT_PREFIX}/lib/libSceneCreator.so.0.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
