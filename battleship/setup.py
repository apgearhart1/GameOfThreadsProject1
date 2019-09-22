"""
Currently the game is fully implemented; however if a player tries,
    it will let them have two or more ships occupy the same space.

There may be other issues that I have yet to find
"""

import random
import game as G
import string


class Coordinates:
    # variables

    def __init__(self):
        """

        """
        self.ship_coordinates = [[], [], [], [], []]
        self.list = []

    def add_ship_coordinate(self, new_coordinate, ship_size):
        """

        :param new_coordinate: A string representing a coordinate, ex. "A1"
        :param ship_size: The size of the ship new_coordinate is a part of
        """
        self.list.append(new_coordinate)
        new_coord_tuple = convert_to_tuple(new_coordinate)
        if ship_size == 1:
            self.ship_coordinates[0].append(new_coord_tuple)
        elif ship_size == 2:
            self.ship_coordinates[1].append(new_coord_tuple)
        elif ship_size == 3:
            self.ship_coordinates[2].append(new_coord_tuple)
        elif ship_size == 4:
            self.ship_coordinates[3].append(new_coord_tuple)
        elif ship_size == 5:
            self.ship_coordinates[4].append(new_coord_tuple)

    def verify_not_a_duplicate(self, coordinate):
        """

        :param coordinate: A string representing a coordinate
        :return: False if a player has already placed a ship at the given coordinate, True otherwise
        """
        if coordinate not in self.list:
            return True
        else:
            return False

    def reset_everything(self):
        self.ship_coordinates = [[], [], [], [], []]


def startup():
    """

    """
    print("Welcome to Battleship!")
    plays_first()


def plays_first():
    """

    """
    coin_choice = input("Heads or tails?: ")
    coin_list = ["heads", "tails"]
    correct = random.choice(coin_list)
    if (coin_choice.lower() != "heads") & (coin_choice.lower() != "tails"):
        print("Well, since you were unable to enter heads or tails I will choose for you.")
        print("Person to the left is Player1 and person to the right is Player2.")
    elif coin_choice.lower() == correct:
        print("If you chose " + correct + " you are Player1")
        print("The other person is Player2")
    elif coin_choice.lower() != correct:
        print("If you chose " + correct + " you are Player2")
        print("The other person is Player1")


def convert_to_tuple(string_coord):
    """

    :param string_coord: A string representing a coordinate,  ex. "A1"
    :return: A 2-tuple representing the same coordinate, ex. (0, 0)
    """
    tuple_coord = (int(string_coord[1]) - 1, ord(string_coord[0].upper()) - 65)
    return tuple_coord


def get_num_of_ships():
    """

    :return: The number of ships in the range 1 to 5 that the user inputs
    """
    num_ships = input("How many ships should each player have: ")
    while not test_input(num_ships):
        num_ships = input("Please enter a valid input between 1 and 5: ")
    if test_input(num_ships):
        return int(num_ships)


def test_input(num_ships):
    """

    :param num_ships: Any input
    :return: True if the input is a number from 1 to 5, False otherwise
    """
    try:
        if int(num_ships) in range(1, 6):
            return True
    except ValueError:
        return False


def choose_ships(player, ship_num):
    """

    :param player: Coordinates object presenting one player's ship locations
    :param ship_num: The number of ships a player is to place
    """
    temp = 1
    while temp <= ship_num:
        add_ship(player, temp)
        temp = temp + 1


def add_ship(player, size):
    """

    :param player: Coordinates object presenting one player's ship locations
    :param size: The size of the ship being placed
    """
    if size == 1:
        valid_input = False
        new_coordinate = input("Enter the coordinate (for example, A1) where you would like to place your 1 ship: ")
        while not valid_input:
            if verify_ship_input(new_coordinate) & player.verify_not_a_duplicate(new_coordinate):
                player.add_ship_coordinate(new_coordinate, size)
                valid_input = True
            else:
                new_coordinate = input("Invalid Input. Please enter a valid coordinate: ")
    if size in range(2, 6):
        valid_input = False
        start_coordinate = input(f"Enter the START coordinate for your {size} ship: ")
        while not valid_input:
            if verify_ship_input(start_coordinate) & player.verify_not_a_duplicate(start_coordinate):
                player.add_ship_coordinate(start_coordinate, size)
                valid_input = True
            else:
                start_coordinate = input("Invalid Input. Please enter a valid coordinate: ")
        valid_input = False
        end_coordinate = input(f"Enter the END coordinate for your {size} ship: ")
        while not valid_input:
            if verify_ship_input(end_coordinate) & player.verify_not_a_duplicate(end_coordinate):
                if verify_ship_size(start_coordinate, end_coordinate, size):
                    player.add_ship_coordinate(end_coordinate, size)
                    valid_input = True
                else:
                    end_coordinate = input("Either END coordinate is not in the same row or col as START, "
                                           "or ship is the incorrect size. Try again: ")
            else:
                end_coordinate = input("Invalid Input. Please enter a valid coordinate: ")


def verify_ship_size(start, end, size):
    """

    :param start: string representing the coordinate for one end of a ship
    :param end: string representing the coordinate for the other end of the ship
    :param size: The length that the ship is supposed to be
    :return: True if a ship with the given start and end coordinates is the given length, False otherwise
    """
    start = convert_to_tuple(start)
    end = convert_to_tuple(end)
    if (start[0] == end[0]) & (abs(end[1] - start[1]) + 1 == size):
        return True
    elif (start[1] == end[1]) & (abs(end[0] - start[0]) + 1 == size):
        return True
    else:
        return False


def verify_ship_input(possible_coordinate):
    """

    :param possible_coordinate: Any input
    :return: True if the input is a string in the form of a valid coordinate, False otherwise
    """
    letters = string.ascii_uppercase[:8]
    if len(possible_coordinate) == 2:
        if (possible_coordinate[0].upper() in letters) & (int(possible_coordinate[1]) in range(1, 9)):
            return True
    else:
        return False


def play_again():
    correct_answers = ["Yes", "Y", "y", "yes", "YES"]
    wrong_answers = ["No", "N", "n", "no", "NO"]
    ans = input("Do you want to play again (Yes/No): ")
    if ans in correct_answers:
        return True
    if ans in wrong_answers:
        return False
    else:
        loop = True
    while loop:
        new_ans = input("Please enter a valid response (Yes/No): ")
        if new_ans in correct_answers:
            return True
        if new_ans in wrong_answers:
            return False


def main():
    """

    """
    startup()
    numOfShips = get_num_of_ships()
    p1_ships = Coordinates()
    p2_ships = Coordinates()
    print("Player 1's Turn: ")
    choose_ships(p1_ships, numOfShips)
    print('\n\n\n\n\n\n\n\n\n\n\n\n')
    print("Player 2's Turn: ")
    choose_ships(p2_ships, numOfShips)
    print('\n\n\n\n\n\n\n\n\n\n\n\n')
    game = G.Game(numOfShips)
    game.player1.placeShip(p1_ships.ship_coordinates[0][0], p1_ships.ship_coordinates[0][0])
    game.player2.placeShip(p2_ships.ship_coordinates[0][0], p2_ships.ship_coordinates[0][0])
    for i in range(1, numOfShips):
        game.player1.placeShip(p1_ships.ship_coordinates[i][0], p1_ships.ship_coordinates[i][1])
        game.player2.placeShip(p2_ships.ship_coordinates[i][0], p2_ships.ship_coordinates[i][1])
    while not game.win:
        game.currentPlayer.displayGrids()
        valid_guess = False
        current_guess = input("Enter coordinate to fire: ")
        while not valid_guess:
            if verify_ship_input(current_guess):
                valid_guess = True
                current_guess = convert_to_tuple(current_guess)
                game.turn(current_guess)
            else:
                current_guess = input("Please enter a valid guess: ")
    game.printWinner()
    p1_ships.reset_everything()
    p2_ships.reset_everything()
    if play_again():
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        main()
    if not play_again():
        print("Thanks for Playing")

main()
