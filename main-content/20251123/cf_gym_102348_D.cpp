#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    string s;
    cin >> n >> s;
    
    int sumL = 0, sumR = 0;
    int qL = 0, qR = 0;
    
    for (int i = 0; i < n/2; i++) {
        if (s[i] == '?') qL++;
        else sumL += s[i] - '0';
    }
    for (int i = n/2; i < n; i++) {
        if (s[i] == '?') qR++;
        else sumR += s[i] - '0';
    }
    
    int diff = sumL - sumR;
    int qDiff = qR - qL;
    
    if (diff == qDiff * 9 / 2) {
        cout << "Bicarp" << endl;
    } else {
        cout << "Monocarp" << endl;
    }
    
    return 0;
}