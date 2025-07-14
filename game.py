import random
from colorama import init,Fore,Style,Back
init()
items={1:"Cigarette", 2:"Beer", 3:"Magnifying Glass", 4:"Saw", 5:"Handcuffs"}
player1={"name":"Asif","health":4,"items":[],"handcuffed":False,"turn":True,"sawed":False,"buff":[]}
player2={"name":"Rasgreen","health":4,"items":[],"handcuffed":False,"turn":False,"sawed":False,"buff":[]}
gun=[]
turn=1

def load_gun():
    if not gun:
        live=0
        blanks=0
        reel=[1]*2+[0]*3
        for _ in range(5):
            bullet=random.choice(reel)
            reel.remove(bullet)
            gun.append(bullet)
            if bullet:
                live+=1
            else:
                blanks+=1
        print(Fore.CYAN+f"\nThe gun has been reloaded.\nLIVE BULLETS : {live}\nBLANK BULLETS : {blanks}")
    else:
        print(Fore.MAGENTA+f"\nThe gun is not empty yet!")
          

def use_item(current,opponent,item):

    if item==0:
        print(Fore.BLUE+"\nYou did not use any item.")
    elif item==1:
        print(Fore.BLUE+f"\nYou smoked a cigarette. Your health increased by 1")
        current["health"]+=1
        current["items"].remove(item)
    elif item==2:
        bullet="LIVE" if gun.pop() else "BLANK"
        print(Fore.BLUE+f"\nYou drank a beer and popped a shell off the shotgun. It was a {bullet} one.")
        current["items"].remove(item)
    elif item==3:
        bullet="LIVE" if gun[-1] else "BLANK"
        print(Fore.BLUE+f"\nYou used a magnifying glass to look into the shotgun. The next bullet is a {bullet} one.")
        current["items"].remove(item)
    elif item==4:
        print(Fore.BLUE+f"\nYou used a saw to cut the barrel of the shotgun. Your next shot would do TWICE the damage")
        current["sawed"]=True
        current["buff"].append("Double Damage")
        current["items"].remove(item)
    elif item==5:
        if not opponent["handcuffed"]:
            print(Fore.BLUE+f"\nYou put your opponent in handcuffs. They can't shoot this round.")
            opponent["handcuffed"]=True
            opponent["buff"].append("Handcuffed")
            current["items"].remove(item)
        else:
            print(Fore.MAGENTA+f"\nOpponent is already in handcuffs.")   
    else:
        print(Fore.MAGENTA+f"\nInvalid item")
        
    
        

def shoot(current, opponent, choice, gun):
    if not gun:
        print(Fore.BLUE+f"The gun was empty! Reloading gun...")
        return
    bullet=gun.pop()
    if choice==1:
        if bullet:
            print(Fore.RED+f"\nYou shot a LIVE bullet at yourself! Ouch. You did {2 if current["sawed"] else 1} damage")
            current["health"]-=2 if current["sawed"] else 1
            current["turn"] = False
            opponent["turn"] = True
        elif not bullet:
            print(Fore.RED+f"\nYou shot a BLANK bullet at yourself! It is your turn again.")
    elif choice==2:
        if bullet:
            print(Fore.RED+f"\nYou shot a LIVE bullet at {opponent["name"]}! Nice job. You did {2 if current["sawed"] else 1} damage")
            opponent["health"]-=2 if current["sawed"] else 1
            current["turn"] = False
            opponent["turn"] = True
        elif not bullet:
            print(Fore.RED+f"\nYou shot a BLANK bullet at {opponent["name"]}! Oops.")
            current["turn"] = False
            opponent["turn"] = True
    
    if current["sawed"]:
        if "Double Damage" in current["buff"]:
            current["buff"].remove("Double Damage")  
            current["sawed"]=False      
      
def status(current, opponent):
    print(Fore.GREEN+f"\n{current["name"]}:\nHealth : {current["health"]}\nItems : {[items[x] for x in current["items"]]}\nCurrent effect(s) : {current["buff"]}\n")
    print(Fore.RED+f"\n{opponent["name"]}:\nHealth : {opponent["health"]}\nItems : {[items[x] for x in opponent["items"]]}\nCurrent effect(s) : {opponent["buff"]}\n")
    

def give_items(player):
    for _ in range(5):
        player["items"].append(random.choice([1,2,3,4,5]))

def gameover(player1, player2):
    if player1["health"] <=0 or player2["health"] <=0:
        return True
    else:
        return False

def game(player1, player2):
    load_gun()
    give_items(player1)
    give_items(player2)

    while not gameover(player1,player2):
        if not gun:
            load_gun()
        if player1["turn"]:
            current, opponent = player1, player2
        else:
            current, opponent = player2, player1

        if current["handcuffed"]:
            print(Fore.BLUE+f"\n\n{current["name"]} was in handcuffs. Skipping turn...")
            current["handcuffed"]=False
            current["buff"].remove("Handcuffed")
            current, opponent = opponent, current
            current["turn"]=True
            opponent["turn"]=False

        print(Fore.MAGENTA+f"\n\nIt is {current["name"]}'s turn")

        item_choice=-1
        item_choice_bool = True
        while item_choice_bool:
            status(current,opponent)
            item_choice = int(input(Fore.BLUE+"\nUse an item if you want to [ 0:None 1:Cigarette, 2:Beer, 3:Magnifying Glass, 4:Saw, 5:Handcuffs ]  :  "))

            if item_choice not in [0,1,2,3,4,5]:
                print(Fore.RED+"\nInvalid choice\n")
                continue
            elif item_choice not in current["items"] and item_choice!=0:
                print(Fore.MAGENTA+"\nYou don't have that item!\n")
                continue

            use_item(current,opponent,item_choice)
            item_choice_bool=False

        status(current,opponent)

        shoot_choice = int(input(Fore.RED+"\nWhom do you want to shoot? [ 1:Yourself 2:Opponent ]  :  "))
        shoot(current,opponent,shoot_choice, gun)
      

    if player1["health"]<=0:
        print(Style.BRIGHT+Fore.GREEN+f"{player2["name"]} WINS!")
    else:
        print(Style.BRIGHT+Fore.GREEN+f"{player1["name"]} WINS!")

game(player1,player2)












