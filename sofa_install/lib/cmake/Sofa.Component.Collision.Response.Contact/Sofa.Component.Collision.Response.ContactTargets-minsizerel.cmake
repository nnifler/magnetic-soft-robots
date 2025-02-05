#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Sofa.Component.Collision.Response.Contact" for configuration "MinSizeRel"
set_property(TARGET Sofa.Component.Collision.Response.Contact APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(Sofa.Component.Collision.Response.Contact PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofa.Component.Collision.Response.Contact.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofa.Component.Collision.Response.Contact.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS Sofa.Component.Collision.Response.Contact )
list(APPEND _IMPORT_CHECK_FILES_FOR_Sofa.Component.Collision.Response.Contact "${_IMPORT_PREFIX}/lib/libSofa.Component.Collision.Response.Contact.so.24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
