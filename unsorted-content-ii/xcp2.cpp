#include <iostream>
using namespace std;
int main(){
    string num_list="11223344555666777888999000";
    string message="XM_023";
    for(int i=0; i<message.length(); i++){
        if(message[i]>='0'&&message[i]<='9')
            cout<<num_list[i]; 
        else if (message[i]>='A'&&message[i]<='Z')
            cout<<num_list[message[i]-'A'];
    }
    cout<<endl;
    return 0;
}