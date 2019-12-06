#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

int main() {
    ifstream file;
    file.open("input.txt");

    // Read lines
    // vector<string> data;
    // if (file.is_open()) {
    // 	string line;
    // 	while (!file.eof()) {
    // 		getline(file, line);
    // 		data.push_back(line);
    // 	}
    // }
    // file.close();

    // Read entire file
    // string data;
    // if (file.is_open()) {
    // 	char a;
    // 	while (file.get(a)) {
    // 		data += a;
    // 	}
    // }
    // file.close();

    return 0;
}
