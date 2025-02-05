#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Bindings_SofaGLFW" for configuration "MinSizeRel"
set_property(TARGET Bindings_SofaGLFW APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(Bindings_SofaGLFW PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_MINSIZEREL "Python::Python"
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/python3/site-packages/./SofaGLFW.cpython-310-x86_64-linux-gnu.so"
  IMPORTED_SONAME_MINSIZEREL "SofaGLFW.cpython-310-x86_64-linux-gnu.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS Bindings_SofaGLFW )
list(APPEND _IMPORT_CHECK_FILES_FOR_Bindings_SofaGLFW "${_IMPORT_PREFIX}/lib/python3/site-packages/./SofaGLFW.cpython-310-x86_64-linux-gnu.so" )

# Import target "SofaGLFW" for configuration "MinSizeRel"
set_property(TARGET SofaGLFW APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(SofaGLFW PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_MINSIZEREL "glfw"
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libSofaGLFW.so.24.06.00"
  IMPORTED_SONAME_MINSIZEREL "libSofaGLFW.so.24.06.00"
  )

list(APPEND _IMPORT_CHECK_TARGETS SofaGLFW )
list(APPEND _IMPORT_CHECK_FILES_FOR_SofaGLFW "${_IMPORT_PREFIX}/lib/libSofaGLFW.so.24.06.00" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
