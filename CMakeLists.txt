cmake_minimum_required (VERSION 3.10)
project ("aoc_2020")

# Project Settings
#-----------------------------------------------
# set to cpp 11 standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find the Catch2 Library used for Unittests
# If not found on system, can be installed from source at https://github.com/catchorg/Catch2
find_package(Catch2 REQUIRED)

# include necessary directories
include_directories("${PROJECT_SOURCE_DIR}/cpp/inc/")
include_directories("${PROJECT_SOURCE_DIR}/cpp/")

# Executables should be created in the build.cmake file
INCLUDE("cmake/build.cmake")

# All tests should be defined in the tests.cmake file
INCLUDE("cmake/tests.cmake")