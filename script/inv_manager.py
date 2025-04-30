import json
import time
import os
VERSION = 1

def line(num : int = 1):
    for i in range(num):
        print("")


def inv_info():
    line(27)
    print("Welcome in the inv info program !")
    while True :
        print("Please, select a mode :")
        print("   [1] Simple mode. \n   [2] Advenced mode.")
        line()
        choise = input("Please, select a number [1-2] ")
    
        if choise == "1" or choise == "2" :
            choise = int(choise)
            break
        
        print("The number isn't right, please enter a number in range [1-2]")
        input("Press any key to go back to the menu.")
    
    if choise == 1 :
        line(27)
        total_user = 0
        total_size = 0
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_user += 1
                    total_size += os.path.getsize(fp)
        print("General info :")
        print(f"    Number of inventory file : [{total_user}] \n    Size of ./files/inventory : {total_size/1000}MB")
        
    line()
    input("End of the program, press any key to go back to the main menu.")





def key_manager():
    print("key manager")
    input("End of the program, press any key to go back to the main menu.")



func_list = {
    1 : "inv_info()",
    2 : "key_manager()"
}

line(27)
print("Starting the script...")
print(f"Welcome on script manager V{VERSION}")
line()
time.sleep(0.5)
while True :
    print("Choose something you want to do :")
    print("[1] Show the inv folder info.")
    print("[2] Key manager.")
    
    
    choise_range = "[1-2]"
    choise = input(f"Please select a number [{choise_range}] : ")

    try :
        exec(func_list[int(choise)])
    except KeyError :
        print(f"The number isn't right, please enter a number in range [{choise_range}]")
        input("Press any key to go back to the main menu.")
    line(27)
    