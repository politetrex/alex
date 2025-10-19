#include <iostream>
#include <vector>

#define ll long long
using namespace std;

int main() {
    cin.tie(0)->sync_with_stdio(0);
    int n, q, shift=0;
    cin>>n>>q;
    vector<ll> array(n), pfx(n+1, 0);
    for(int i = 0; i < n; i++) {
        cin >> array[i];
        pfx[i+1]=pfx[i]+array[i];
    }
    for(int i = 0; i < q; i++){
        int k; cin>>k;
        if (!(k-1)) {
            int c; cin>>c;
            shift=(shift+c)%n;
        } else {
            int l, r; cin>>l>>r;
            l--; r--;
            l=(l+shift)%n;
            r=(r+shift)%n;
            if (l>r){
                cout<<pfx[n]-pfx[l]+pfx[r+1]<<char(10);
            } else {
                cout<<pfx[r+1]-pfx[l]<<char(10);
            }
        }
    }
    return 0;
}