#pragma once
#include <vector>
#include <iostream>

void print(std::vector<int> const &);
std::vector<int> loadFile(std::ifstream & stream);

int balanceExpenses(std::vector<int> &inputArray, int combinationLength, int targetSum);
void combinationHelper(std::vector<int>::iterator start, std::vector<int>::iterator end, std::vector<int> &dataArray, int depth);