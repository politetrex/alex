#include <iostream>
using namespace std;
int main() {
    int A[8][10]={0};
    cout<<"Start index: "<<&A[0][0]<<endl;
    cout<<"Requested index: "<<&A[5][8]<<endl;
    cout<<"Indented: "<<&A[5][8]-&A[0][0]<<endl;
    return 0;
}