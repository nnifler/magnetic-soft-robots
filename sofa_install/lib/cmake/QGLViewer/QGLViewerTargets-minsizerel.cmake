#----------------------------------------------------------------
# Generated CMake target import file for configuration "MinSizeRel".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "QGLViewer" for configuration "MinSizeRel"
set_property(TARGET QGLViewer APPEND PROPERTY IMPORTED_CONFIGURATIONS MINSIZEREL)
set_target_properties(QGLViewer PROPERTIES
  IMPORTED_LOCATION_MINSIZEREL "${_IMPORT_PREFIX}/lib/libQGLViewer.so"
  IMPORTED_SONAME_MINSIZEREL "libQGLViewer.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS QGLViewer )
list(APPEND _IMPORT_CHECK_FILES_FOR_QGLViewer "${_IMPORT_PREFIX}/lib/libQGLViewer.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
