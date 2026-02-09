#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
using namespace std;
 
int main() {
    int n, m, k;
    // should i input...
    cin >> n >> m >> k;
    vector<pair<int, int>> a(m);
    for (int i = 0; i < m; i++) {
        cin >> a[i].first;
        a[i].second = i + 1;
    }
 
    // impossible to ***
    sort(a.begin(), a.end(), greater<pair<int, int>>());
    int max_a = a[0].first;
    int blocks = (max_a + k - 1) / k;
    if (n < max_a + blocks - 1) {
        cout << -1 << endl;
        return 0;
    }
 
    priority_queue<pair<int, int>> pq;
    for (auto &p : a) pq.push(p);
 
    vector<int> result;
    int last_color = -1;
    int consec = 0;
 
    for (int i = 0; i < n; i++) {
        vector<pair<int, int>> temp;
        int chosen_color = -1;
        int chosen_count = -1;
 
        while (!pq.empty()) {
            auto top = pq.top();
            pq.pop();
            if (top.second == last_color && consec == k) {
                temp.push_back(top);
                continue;
            }
            chosen_color = top.second;
            chosen_count = top.first;
            break;
        }
 
        if (chosen_color == -1) {
            cout << -1 << endl;
            return 0;
        }
 
        for (auto &p : temp) pq.push(p);
 
        if (chosen_color == last_color) {
            consec++;
        } else {
            last_color = chosen_color;
            consec = 1;
        }
 
        result.push_back(chosen_color);
        if (chosen_count > 1) {
            pq.push({chosen_count - 1, chosen_color});
        }
    }
 
    // why do i need output!
    for (int x : result) cout << x << " ";
    cout << endl;
 
    return 0;
}