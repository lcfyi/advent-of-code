#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

int count(string s, char t) {
    int count = 0;
    for (char c : s) {
        if (c == t) {
            count++;
        }
    }
    return count;
}

int main() {
    ifstream file;
    file.open("input.txt");

    // Read entire file
    string data;
    if (file.is_open()) {
    	char a;
    	while (file.get(a)) {
    		data += a;
    	}
    }
    file.close();

    const int HEIGHT = 6;
    const int WIDTH = 25;

    vector<string> images;

    for (int i = 0; i < data.length() / (HEIGHT * WIDTH); i++) {
        string temp;
        for (int j = 0; j < HEIGHT * WIDTH; j++) {
            temp += data[i * HEIGHT * WIDTH + j];
        }
        images.push_back(temp);
    }

    string target;
    int min;

    for (string s : images) {
        int curCount = count(s, '0');
        if (target.length() == 0 || curCount < min) {
            min = curCount;
            target = s;
        }
    }

    cout << count(target, '1') * count(target, '2') << endl;

    return 0;
}
