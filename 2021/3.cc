#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>

int common(const std::vector<int>& numbers, int index)
{
    const int mask = 1 << index;
    int count = 0;
    for (int i : numbers)
    {
        if (i & mask) ++count;
    }
    return count;
}

std::vector<int> keep(const std::vector<int>& numbers, int index, bool set)
{
    std::vector<int> result;
    result.reserve(numbers.size());
    const int mask = 1 << index;
    for (auto i : numbers)
    {
        if (set == !!(i & mask))
        {
            result.push_back(i);
        }
    }
    return result;
}

const int width = 12;

int main()
{
    std::ifstream in("2021_3.txt", std::ifstream::in);
    std::vector<int> numbers;
    for (std::string line; std::getline(in, line); )
    {
        int acc = 0;
        for (int i = 0; i < width; ++i)
        {
            acc <<= 1;
            acc |= (line[i] - '0');
        }
        numbers.push_back(acc);
    }
    
    int gamma = 0, epsilon = 0;
    for (int i = width - 1; i >= 0; --i)
    {
        int x = common(numbers, i) > numbers.size() / 2;
        gamma <<= 1;
        gamma |= x;

        epsilon <<= 1;
        epsilon |= !x;
    }
    std::cout << gamma * epsilon << std::endl;

    std::vector<int> tmp(numbers);
    for (int i = width - 1; i >= 0; --i)
    {
        if (tmp.size() == 1) break;
        int x = common(tmp, i);
        int y = tmp.size() - x;
        tmp = keep(tmp, i, x >= y);
    }
    int ox = tmp[0];
    
    tmp = numbers;
    for (int i = width - 1; i >= 0; --i)
    {
        if (tmp.size() == 1) break;
        int x = common(tmp, i);
        int y = tmp.size() - x;
        tmp = keep(tmp, i, y > x);
    }
    int co = tmp[0];

    std::cout << ox * co << std::endl;
}