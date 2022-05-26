import random
#------------------------------ Create Player with computer---------------------------------------#
class BattleshipGame:
    def __init__(self, num_of_players,name):
        
        if num_of_players == 1:
            
            self.players = [Human_Player(f"{name}"), Computer_Player("The Computer")]

        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

    
    def play(self):

        self.players[0].position_fleet()
        self.players[1].position_fleet()

        input("Both fleets are ready to play. Press enter to play... ")
        winner = False
        first_players_turn = True
        while not winner:
            if first_players_turn:
                winner = self.players[0].turn()
                if winner:
                    print("Game over!", self.players[0].player_name, "wins!")
                    input()
            else:
                winner = self.players[1].turn()
                if winner:
                    print("Game over!", self.players[1].player_name, "wins!")
                    input()
            first_players_turn = not first_players_turn


# ------------------------------------------- Board --------------------------------------------#
class Board:

    def __init__(self):
        
        self.grid = [[" _"]*10 for i in range(10)]
        
        self.hit_count = 0

    
    def __str__(self):
        str_val = "  0|1|2|3|4|5|6|7|8|9\n"
        for i in range(10):
            str_val += str(i)
            for j in range(10):
                str_val += self.grid[i][j]
            if i != 9:
                str_val += "\n"
        return str_val

    def public_view(self):
        str_val = "  0|1|2|3|4|5|6|7|8|9\n"
        for i in range(10):
            str_val += str(i)
            for j in range(10):
                if self.grid[i][j] == " B":
                    str_val += " _"
                else:
                    str_val += self.grid[i][j]
            if i != 9:
                str_val += "\n"
        return str_val

  
    def add_boat(self, boat):
        width = 1
        height = 1
        if boat.orientation == "v":
            height = boat.size
        else:
            width = boat.size

        if (boat.x < 0) or (boat.y < 0) or (boat.x+width > 10) or (boat.y+height > 10):
            return False


        for x in range(width):
            for y in range(height):
                if self.grid[boat.y + y][boat.x + x] != " _":
                    return False

        
        for x in range(width):
            for y in range(height):
                self.grid[boat.y + y][boat.x + x] = " B"
        return True

    def attack(self, x, y): # HIT the boat
        current_value = self.grid[y][x]
        if current_value == " B":
            self.grid[y][x] = " X"
            self.hit_count += 1
            return True
        elif current_value == " _":
            self.grid[y][x] = " O"
            return False
        
        else:
            return False

    def defeated(self):
        if self.hit_count == 17:
            return True
        else:
            return False

# -------------------------------------- BOAT --------------------------------------------------#
class Boat:
    
    def __init__(self, label, size):
        self.label = label
        self.size = size
        self.x = None
        self.y = None
        self.orientation = None

    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_orientation(self, orientation):
        self.orientation = orientation

# ------------------------------ HUMAN PLAYER --------------------------------------------#
class Human_Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = Board()
        self.fleet = [Boat("Aircraft Carrier", 5), Boat("Battleship", 4), Boat("Submarine", 3), Boat("Destroyer", 3), \
                      Boat("Patrol Boat", 2)]
        self.opponent = None
        self.log = [0,0,0]

    
    def set_opponent(self, opponent):
        self.opponent = opponent

    def position_fleet(self):
        input(self.player_name+": Are you ready to position your fleet?  Press enter to begin! ")

        for boat in self.fleet:
            self.position_boat(boat)

        print("Your fleet is ready to play.  Your board is positioned as follows:")
        print(self.board)

    def position_boat(self, boat):
        print(self.board)
        print("You need to position a", boat.label, "of length", boat.size, "on the board above.")
        orientation = None
        while orientation is None:
            orientation = input("Would you like to use a vertical or horizontal? (v/h) ")
            if (orientation != "v") and (orientation != "h"):
                print("You must enter a 'v' or a 'h'.  Please try again.")
                orientation = None
        position = None
        while position is None:
            try:
                position = input("Please enter the position for the top-left location of the boat. " + \
                                 " Use the form x = Top ,y = left  (example: 3,5): ")
                coords = position.split(",")
                x = int(coords[0])
                y = int(coords[1])
                boat.set_orientation(orientation)
                boat.set_position(x,y)
                if not self.board.add_boat(boat):
                    raise Exception
            except ValueError:
                print("You must a valid position for the boat.  Please try again.")
                position = None
            except:
                print("You must choose a position that is (a) on the board and (b) doesn't intersect" + \
                      "with any other boats.") 
                position = None

    def turn(self):
        print(self.player_name+"'s board:")
        print(self.board)
        print()
        print("Your view of "+self.opponent.player_name+"'s board:")
        print(self.opponent.board.public_view())
        print(self.player_name, "Statistics\nAttacks: ", self.log[0], "\tHits: ", self.log[1], "\tMisses: ", self.log[2])
        position = None
        while position is None:
            try:
                position = input("Please enter the position you would like to attack. Use the form x = Top ,y = left  (example: 3,5): ")
                coords = position.split(",")
                x = int(coords[0])
                y = int(coords[1])
                if (x < 0) or (x > 9) or (y < 0) or (y > 9):
                    raise Exception
                else:
                    break
            except:
                print("You must a valid position in the form x,y where both x and y are integers in the range of" + \
                      "0-9. Please try again.")
                position = None

        
        hit_flag = self.opponent.board.attack(x, y)
        self.log[0] += 1
        if hit_flag:
            self.log[1] += 1
            print("You hit a boat!")
        else:
            self.log[2] += 1
            print("You missed.")
        
        if self.opponent.board.defeated():
            return True
        else:
            return False

# ------------------------------------------ Computer ------------------------------------------------------#
class Computer_Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.board = Board()
        self.fleet = [Boat("Aircraft Carrier", 5), Boat("Battleship", 4), Boat("Submarine", 3), Boat("Destroyer", 3), \
                      Boat("Patrol Boat", 2)]
        self.opponent = None
        self.log = [0,0,0]

    def set_opponent(self, opponent):
        self.opponent = opponent

    def position_fleet(self):
        for boat in self.fleet:
            self.position_boat(boat)

        input("The Computer's fleet is ready to play.  Press enter to continue...")

    def position_boat(self, boat):
        position = False
        while position == False:
            o = random.randint(0, 1)
            if o == 0:
                orientation = "v"
            else:
                orientation = "h"

            x = random.randint(1, 10) - 1
            y = random.randint(1, 10) - 1

            boat.set_orientation(orientation)
            boat.set_position(x,y)

            result = self.board.add_boat(boat)
            if result == True:
                position = True

    def turn(self):
        x = random.randint(1, 10) - 1
        y = random.randint(1, 10) - 1

        print(self.player_name, "Statistics\nAttacks: ", self.log[0], "\tHits: ", self.log[1], "\tMisses: ",
              self.log[2])

        hit_flag = self.opponent.board.attack(x, y)
        self.log[0] += 1
        if hit_flag:
            self.log[1] += 1
            print("\nThe Computer hit a boat!")
        else:
            self.log[2] += 1
            print("\nThe Computer missed.")

        if self.opponent.board.defeated():
            return True
        else:
            return False
