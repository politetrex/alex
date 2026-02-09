import os

def link_to_filename(link):
    splitted_link = link.split("/")
    if(splitted_link[0]!="https:" or splitted_link[1]!=""):
        raise ValueError("Invalid link")
    else:
        if splitted_link[2]=="codeforces.com":
            if (splitted_link[3]=="contest") & (splitted_link[5]=="problem") & (len(splitted_link)==7):
                return "cf_contest"+splitted_link[4]+"_"+splitted_link[6]
            elif (splitted_link[3]=="problemset") & (splitted_link[4]=="problem") & (len(splitted_link)==7):
                return "cf_pbset_"+splitted_link[5]+"_"+splitted_link[6]
            if (splitted_link[3]=="gym") & (splitted_link[5]=="problem") & (len(splitted_link)==7):
                return "cf_gym_"+splitted_link[4]+"_"+splitted_link[6]
            else:
                raise ValueError("Invalid Codeforces link")
        elif splitted_link[2]=="atcoder.jp":
            if (splitted_link[3]=="contests") & (splitted_link[5]=="tasks") & (len(splitted_link)==7):
                return "at_"+splitted_link[6]
            else:
                raise ValueError("Invalid AtCoder link")
        else:
            raise ValueError("Unknown OJ")

print("C++ file template creator on the command line")

def askdir():
    base_dir=("Enter a directory path: ")
    if os.path.isdir(base_dir):
        print(f"You entered: {base_dir}")
    else:
        print("Invalid directory path.")
        askdir()
    return base_dir

while True:
    try:
        print(link_to_filename(input("Enter a link: ")))
    except ValueError as e:
        print(e)