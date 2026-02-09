#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<long long> a(n + 1);
        vector<long long> prefix(n + 1, 0);
        
        long long total_sum = 0;
        for (int i = 1; i <= n; i++) {
            cin >> a[i];
            total_sum += a[i];
            prefix[i] = prefix[i - 1] + a[i];
        }
        
        vector<long long> f(n + 1);
        for (int l = 1; l <= n; l++) {
            f[l] = -(long long)l * l + l + prefix[l - 1];
        }
        
        vector<long long> max_f(n + 1);
        max_f[1] = f[1];
        for (int r = 2; r <= n; r++) {
            max_f[r] = max(max_f[r - 1], f[r]);
        }
        
        long long max_delta = 0;
        for (int r = 1; r <= n; r++) {
            long long delta = max_f[r] + (long long)r * r + r - prefix[r];
            max_delta = max(max_delta, delta);
        }
        
        long long ans = total_sum + max_delta;
        cout << ans << "\n";
    }
    
    return 0;
}