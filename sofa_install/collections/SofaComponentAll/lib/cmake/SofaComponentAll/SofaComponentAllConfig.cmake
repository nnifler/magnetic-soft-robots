# CMake package configuration file for SofaComponentAll

if(NOT "${CMAKE_PROJECT_NAME}" STREQUAL "Sofa" OR NOT "${PROJECT_SOURCE_DIR}" MATCHES "${CMAKE_SOURCE_DIR}/.*")
    # The project doing find_package is not a subproject of SOFA or is not located inside SOFA
    get_property(SofaComponentAll_SENT_DEPRECATION_MESSAGE GLOBAL PROPERTY PROPERTY_SofaComponentAll_SENT_DEPRECATION_MESSAGE SET)
    if(NOT SofaComponentAll_SENT_DEPRECATION_MESSAGE)
        message(WARNING "SofaComponentAll is deprecated and will be removed at v23.06. Use Sofa.Component instead.")
    endif()
    set_property(GLOBAL PROPERTY PROPERTY_SofaComponentAll_SENT_DEPRECATION_MESSAGE TRUE)
endif()

### Expanded from @PACKAGE_GUARD@ by SofaMacrosInstall.cmake ###
include_guard()
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../bin")
list(APPEND CMAKE_LIBRARY_PATH "${CMAKE_CURRENT_LIST_DIR}/../../../lib")
################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was SofaComponentAllConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

set(SOFACOMPONENTALL_MODULES SofaBaseCollision;SofaBaseLinearSolver;SofaBaseMechanics;SofaBaseTopology;SofaBaseUtils;SofaBaseVisual;SofaSimulationCommon;SofaSimulationGraph;SofaDeformable;SofaEngine;SofaExplicitOdeSolver;SofaImplicitOdeSolver;SofaLoader;SofaMeshCollision;SofaObjectInteraction;SofaRigid;SofaSimpleFem;SofaBoundaryCondition;SofaConstraint;SofaGeneralAnimationLoop;SofaGeneralDeformable;SofaGeneralEngine;SofaGeneralExplicitOdeSolver;SofaGeneralImplicitOdeSolver;SofaGeneralLinearSolver;SofaGeneralLoader;SofaGeneralMeshCollision;SofaGeneralObjectInteraction;SofaGeneralRigid;SofaGeneralTopology;SofaGeneralVisual;SofaGraphComponent;SofaTopologyMapping;SofaUserInteraction;SofaNonUniformFem;SofaMiscCollision;SofaMiscEngine;SofaMiscExtra;SofaMiscFem;SofaMiscForceField;SofaMiscMapping;SofaMiscSolver;SofaMiscTopology;SofaDenseSolver;SofaExporter;SofaHaptics;SofaOpenglVisual;SofaPreconditioner;SofaSparseSolver;SofaValidation)


set(SOFACOMPONENTALL_HAVE_SOFABASECOLLISION 1)
set(SOFACOMPONENTALL_HAVE_SOFABASELINEARSOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFABASEMECHANICS 1)
set(SOFACOMPONENTALL_HAVE_SOFABASETOPOLOGY 1)
set(SOFACOMPONENTALL_HAVE_SOFABASEUTILS 1)
set(SOFACOMPONENTALL_HAVE_SOFABASEVISUAL 1)
set(SOFACOMPONENTALL_HAVE_SOFASIMULATIONCOMMON 0)
set(SOFACOMPONENTALL_HAVE_SOFASIMULATIONGRAPH 0)
set(SOFACOMPONENTALL_HAVE_SOFADEFORMABLE 1)
set(SOFACOMPONENTALL_HAVE_SOFAENGINE 1)
set(SOFACOMPONENTALL_HAVE_SOFAEXPLICITODESOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFAIMPLICITODESOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFALOADER 1)
set(SOFACOMPONENTALL_HAVE_SOFAMESHCOLLISION 0)
set(SOFACOMPONENTALL_HAVE_SOFAOBJECTINTERACTION 1)
set(SOFACOMPONENTALL_HAVE_SOFARIGID 1)
set(SOFACOMPONENTALL_HAVE_SOFASIMPLEFEM 1)
set(SOFACOMPONENTALL_HAVE_SOFABOUNDARYCONDITION 1)
set(SOFACOMPONENTALL_HAVE_SOFACONSTRAINT 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALANIMATIONLOOP 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALDEFORMABLE 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALENGINE 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALEXPLICITODESOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALIMPLICITODESOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALLINEARSOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALLOADER 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALMESHCOLLISION 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALOBJECTINTERACTION 0)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALRIGID 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALTOPOLOGY 1)
set(SOFACOMPONENTALL_HAVE_SOFAGENERALVISUAL 1)
set(SOFACOMPONENTALL_HAVE_SOFAGRAPHCOMPONENT 1)
set(SOFACOMPONENTALL_HAVE_SOFATOPOLOGYMAPPING 1)
set(SOFACOMPONENTALL_HAVE_SOFAUSERINTERACTION 1)
set(SOFACOMPONENTALL_HAVE_SOFANONUNIFORMFEM 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCCOLLISION 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCENGINE 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCEXTRA 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCFEM 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCFORCEFIELD 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCMAPPING 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCSOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFAMISCTOPOLOGY 1)
set(SOFACOMPONENTALL_HAVE_SOFADENSESOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFAEXPORTER 1)
set(SOFACOMPONENTALL_HAVE_SOFAHAPTICS 1)
set(SOFACOMPONENTALL_HAVE_SOFAOPENGLVISUAL 1)
set(SOFACOMPONENTALL_HAVE_SOFAPRECONDITIONER 1)
set(SOFACOMPONENTALL_HAVE_SOFASPARSESOLVER 1)
set(SOFACOMPONENTALL_HAVE_SOFAVALIDATION 1)

foreach(module ${SOFACOMPONENTALL_MODULES})
    string(TOUPPER "${module}" module_upper)
    if(SOFACOMPONENTALL_HAVE_${module_upper})
        find_package(${module} QUIET REQUIRED)
    endif()
endforeach()

if(NOT TARGET SofaComponentAll)
    include("${CMAKE_CURRENT_LIST_DIR}/SofaComponentAllTargets.cmake")
endif()

check_required_components(SofaComponentAll)
