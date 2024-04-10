if(NOT TARGET FMUComplianceChecker::executable)
  if("${CMAKE_SYSTEM_NAME}" MATCHES "Darwin")
    set(_os "darwin")
  elseif("${CMAKE_SYSTEM_NAME}" MATCHES "Linux")
    set(_os "linux")
  elseif(WIN32)
    set(_os "win")
  else()
    message(FATAL_ERROR "Unknown or unsupported platform: ${CMAKE_SYSTEM_NAME}")
  endif()
  math(EXPR _wordSize 8*${CMAKE_SIZEOF_VOID_P})
  add_executable(FMUComplianceChecker::executable IMPORTED GLOBAL)
  set_target_properties(FMUComplianceChecker::executable
    PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_LIST_DIR}/../bin/fmuCheck.${_os}${_wordSize}")
endif()

message(STATUS "Add macro 'add_fmu_compliance_check'")
macro(add_fmu_compliance_check testName fmuPath)
  add_test(
    NAME "${testName}"
    COMMAND FMUComplianceChecker::executable "${fmuPath}"
    WORKING_DIRECTORY "${CMAKE_BINARY_DIR}")
endmacro()
