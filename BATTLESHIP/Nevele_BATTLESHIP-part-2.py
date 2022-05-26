import os
def main():
    os.system('cls')
    print("*************** Welcome to BATTLESHIP! ***************")
    print("1.) Start - Player vs Computer!")
    print("2.) Exit ")
    print("******************************************************")
    choice = input("Choice: ")
    choice = int(choice)
    if choice == 1:
         os.system('cls')
         create()
    elif choice == 2:
        os.system('cls')
        print("thank you for playing")
        input()
        exit()
    else:
        input("You must Enter 1 to 3, Press Enter please try again.")
        main()

def create():
    from Nevele_BATTLESHIP_part_1 import BattleshipGame
    num_of_players = None
    
    while num_of_players == None:
        try:
            name = input("Enter Your name player: ")
            num_of_players = int(input(f"Would you like to {name} vs computer? (Enter 1): "))
            if (num_of_players != 1):
             raise Exception()
        except:
            print("You must enter either 1.  Please try again.")
            num_of_players = None
    game = BattleshipGame(num_of_players,name)
    game.play()        

main()   
