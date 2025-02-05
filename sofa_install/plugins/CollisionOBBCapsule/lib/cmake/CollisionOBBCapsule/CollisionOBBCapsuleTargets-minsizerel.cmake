#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "CollisionOBBCapsule" for configuration "MinSizeRel"
set_property(TARGET CollisionOBBCapsule APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(CollisionOBBCapsule PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libCollisionOBBCapsule.so.1.0"
  IMPORTED_SONAME_MINSIZEREL "libCollisionOBBCapsule.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS CollisionOBBCapsule )
list(APPEND _IMPORT_CHECK_FILES_FOR_CollisionOBBCapsule "${_IMPORT_PREFIX}/lib/libCollisionOBBCapsule.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
