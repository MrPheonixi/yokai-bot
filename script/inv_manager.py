import json
import time
import os
VERSION = 1

def line(num : int = 1):
    for i in range(num):
        print(" ")
        
        
        
#Get inv func
def get_inv(id : str):
    if os.path.exists(f"./files/inventory/{id}.json"):
        with open(f"./files/inventory/{id}.json") as f:
            data = json.load(f)
    else :
        #retrun nothing if there's nothing to :/
        data = {}
       
    return data



#save inv func
def save_inv(data : dict, id : int):
    with open(f"./files/inventory/{str(id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def classid_to_class(id, reverse : bool = False):
    if reverse == False :
        return yokai_data[id]["class_name"]
    else :
        for classes in yokai_data :
            if yokai_data[classes]["class_name"] == id :
                return classes
        
    #return nothing if the id or the name was not fund    
    return ""


#Get Yo-kai lists :
with open("./files/yokai_list.json") as yokai_list:
    yokai_data = json.load(yokai_list)
    list_len = {
        "E" : len(yokai_data["E"]["yokai_list"]),
        "D" : len(yokai_data["D"]["yokai_list"]),
        "C" : len(yokai_data["C"]["yokai_list"]),
        "B" : len(yokai_data["B"]["yokai_list"]),
        "A" : len(yokai_data["A"]["yokai_list"]),
        "S" : len(yokai_data["S"]["yokai_list"]),
        "LegendaryS" : len(yokai_data["LegendaryS"]["yokai_list"]),
        "treasureS" : len(yokai_data["treasureS"]["yokai_list"]),
        "DivinityS" : len(yokai_data["DivinityS"]["yokai_list"]),
        "SpecialS" : len(yokai_data["SpecialS"]["yokai_list"]),
        "Boss" : len(yokai_data["Boss"]["yokai_list"])
    }
#Make the class list and the proba    
Class_list = ['E', 'D', 'C', 'B', 'A', 'S', 'LegendaryS', "treasureS", "SpecialS", 'DivinityS', "Boss"]
Proba_list = [0.4175, 0.2, 0.12, 0.12, 0.08, 0.04, 0.0075, 0.0075, 0.0075, 0.005, 0.0025]   
        
        
        


def inv_info():
    line(35)
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
    
    #if they chose the simple mode
    if choise == 1 :
        line(35)
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
        print(f"    Number of inventory file : {total_user} \n    Size of ./files/inventory : {total_size/1000}MB")
        
    #if they chose the advenced mode
    if choise == 2 :
         #first, get the basic info
        line(35)
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
        print(f"    Number of inventory file : {total_user} \n    Size of ./files/inventory : {total_size/1000}MB")
        line()
        
        #get the number of yokai per class
        yokai_per_class = {
            "E" : 0,
            "D" : 0,
            "C" : 0,
            "B" : 0,
            "A" : 0,
            "S" : 0,
            "LegendaryS" : 0,
            "treasureS" : 0,
            "SpecialS" : 0,
            "DivinityS" : 0,
            "Boss" : 0
        }
        
        yokai_per_class_total = {
            "E" : 0,
            "D" : 0,
            "C" : 0,
            "B" : 0,
            "A" : 0,
            "S" : 0,
            "LegendaryS" : 0,
            "treasureS" : 0,
            "SpecialS" : 0,
            "DivinityS" : 0,
            "Boss" : 0
        }
        
        for dirpath, dirnames, filenames in os.walk("./files/inventory"):
            for file in filenames :
                current_inv = get_inv(file.strip(".json"))
                for yokai in current_inv :
                    #check if the yokai is part of the inv system
                    if yokai in ["E", "D", "C", "B", "A", "S", "LegendaryS", "treasureS", "SpecialS", "DivinityS", "Boss", "last_claim", "", "claim"] :
                        pass
                    
                    else :
                        yokai_class = current_inv[yokai][0]
                        
                        #else, add his rank to the total
                        try :
                            for i in range(current_inv[yokai][1]) :
                                yokai_per_class_total[yokai_class] += 1
                        except :
                            yokai_per_class_total[yokai_class] += 1
                        yokai_per_class[yokai_class] += 1
                
        print("Specific infos :")
        print("    Yokai per class :")
        
        for classes in yokai_per_class:
            print(f"    - {classid_to_class(classes)} : {yokai_per_class[classes]}")
            
        line()
        print("    Yokai per class in total :")
        for classes in yokai_per_class_total:
            print(f"    - {classid_to_class(classes)} : {yokai_per_class_total[classes]}")
    
        
    line()
    input("End of the program, press any key to go back to the main menu.")





def key_manager():
    print("key manager")
    input("End of the program, press any key to go back to the main menu.")



func_list = {
    1 : "inv_info()",
    2 : "key_manager()"
}

line(35)
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

    if int(choise) in [1, 2] :
        exec(func_list[int(choise)])
    else :
        print(f"The number isn't right, please enter a number in range [{choise_range}]")
        input("Press any key to go back to the main menu.")
    line(35)
    