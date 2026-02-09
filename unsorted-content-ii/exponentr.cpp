#include <iostream>
using namespace std;
union TestUnion{
    int small;
    unsigned int big;
};
int main(){
    TestUnion a;
    a.big=2150000025;
    cout<<a.small;
    return 0;
}