#include <iostream>
#include <vector>

using namespace std;

int dp(vector<int> dp_array, int index) {
    
}

void solve() {
    int n; cin>>n;
    vector<int> list(n+1, 0);
    for(int i=0; i<n; i++) cin>>list[i+1];
    vector<int> dp_array(n+1, 0);
}

int main() {
    cin.tie(0)->sync_with_stdio(0);
    
    int t;
    cin>>t;
    while(t--)solve();
    return 0;
}