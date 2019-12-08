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

    string target = images[0];

    for (string s : images) {
        for (int i = 0; i < target.length(); i++) {
            if (target[i] == '2') {
                target[i] = s[i];
            }
        }
    }

    for (int h = 0; h < HEIGHT; h++) {
        for (int w = 0; w < WIDTH; w++) {
            cout << target[h * WIDTH + w];
        }
        cout << endl;
    }
    
    return 0;
}
