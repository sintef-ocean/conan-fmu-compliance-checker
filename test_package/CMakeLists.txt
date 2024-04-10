cmake_minimum_required(VERSION 3.15)

project(test_package C)

find_package(FMUComplianceChecker REQUIRED CONFIG)

if(NOT TARGET FMUComplianceChecker::executable)
  message(FATAL_ERROR "Executable target not defined")
endif()

get_target_property(_fmuchk FMUComplianceChecker::executable IMPORTED_LOCATION)

file(WRITE ${CMAKE_BINARY_DIR}/fmuchk ${_fmuchk})
