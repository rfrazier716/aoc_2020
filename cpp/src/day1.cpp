#include "aoc2020/day1.hpp"
#include <vector> // the std vector library
#include <iostream>
#include <numeric>

#include <iterator>
#include <fstream>
#include <vector>
#include <algorithm> // for std::copy


//Debug code to print out the results
void print(std::vector <int> const &a) {
   std::cout << "The vector elements are : ";

   for(int i=0; i < a.size(); i++)
   std::cout << a.at(i) << ' ';
   std::cout << std::endl;
}

// function that loads the puzzle input into a vector of ints
std::vector<int> loadFile(std::ifstream & stream){
    std::istream_iterator<int> start(stream), end;
    std::vector<int> numbers(start, end);
    return numbers;
}

//the combination helper is a recursive function that generates combinations
// Somewhat annoying that there's no standard way to generate combinations
// Also would be great if there were generator functions so I could simply call the next permutation
void combinationHelper(std::vector<int>::iterator start, std::vector<int>::iterator end, std::vector<int> &dataArray, int depth, int targetSum, int & result, bool & exit){
    if(depth == 0){
        auto sumOfElements = std::accumulate(dataArray.begin(), dataArray.end(), 0);
        if(sumOfElements == targetSum)
        {
            result = std::accumulate(dataArray.begin(), dataArray.end(), 1, std::multiplies<int>()); //update the result flag
            exit = true; //set the exit flag so the recursive loop breaks
        }
    }
    else{
        for(auto it = start; it != end-(depth-1); it++)
        {
            dataArray[dataArray.size()-depth] = *it; //update the data array
            //recursively call the combination helper with a shrunk array
            combinationHelper(it+1,end,dataArray,depth-1,targetSum, result, exit); 
            if(exit) break; //break if the exit flag was set
        }
    }
}

//This is the main function to calculate the product if the sum of n numbers in the data equal the target sum
int balanceExpenses(std::vector<int> &inputArray, int combinationLength, int targetSum){
    std::vector<int> dataArray(combinationLength); //make a data array that's passed through the recursive function
    auto exit = false; //set the exit flag false
    int result; //this is where the result will be stored
    combinationHelper(inputArray.begin(), inputArray.end(), dataArray, combinationLength, targetSum, result, exit);
    return result;

}

int runDay(int *argc, char* argv[]){
    //load the puzzle input
    auto inputFile = "../inputs/day1.txt";
    std::ifstream inStream(inputFile);
    auto puzzleInput = loadFile(inStream);

    //get the result for a 2 number combination
    auto result = balanceExpenses(puzzleInput,2,2020);
    std::cout << "Result for 2 combinations is "<< result << std::endl;

    //get the result for a 3 number combination
    result = balanceExpenses(puzzleInput,3,2020);
    std::cout << "Result for 3 combinations is "<< result << std::endl;
}