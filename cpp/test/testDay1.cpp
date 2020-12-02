#include <catch2/catch.hpp>
#include <iostream>
#include <fstream>
#include <vector>

#include "aoc2020/day1.hpp"

TEST_CASE("Part 1 Example","day1")
{
    std::vector<int> array = {1721, 979, 366, 299, 675, 1456};
    auto pickAmount = 2;
    auto result = balanceExpenses(array,2,2020);
    REQUIRE(result==514579);

    result = balanceExpenses(array,3,2020);
    REQUIRE(result==241861950);
}

TEST_CASE("Test File Import","[day1]"){
    auto inputFile = "../inputs/day1.txt";
    std::ifstream inStream(inputFile);
    auto inputVector = loadFile(inStream);
    REQUIRE(inputVector.size()==200);
}
