add_library(catchMain cpp/test/testMain.cpp)

add_executable(testDay1 
    "cpp/test/testDay1.cpp"
    "cpp/src/day1.cpp")

target_link_libraries(testDay1 Catch2::Catch2)
target_link_libraries(testDay1 catchMain)