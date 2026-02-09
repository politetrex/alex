#include <iostream>
using namespace std;
const int NUM = 5;
void indent(int idt){
    for(int i=0; i<idt; i++)cout<<"| ";
}
int fun(int n, int idt=0){
    indent(idt);
    cout<<"fun("<<n<<")\n";
    if(n<=NUM){
        indent(idt);
        cout<<"returning "<<n<<endl;
        return n;
    }
    for(int i=1; i<=NUM; i++){
        indent(idt);
        cout<<"i="<<i<<endl;
        if(fun(n-i, idt+1)<0){
            indent(idt);
            cout<<"returning "<<i<<endl;
            return i;
        }
    }
    indent(idt);
    cout<<"returning "<<-1<<endl;
    return -1;
}
int main(){
    int n;
    cin>>n;
    cout<<fun(n)<<endl;
    return 0;
}