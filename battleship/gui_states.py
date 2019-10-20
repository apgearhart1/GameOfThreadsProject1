
from utils import colors, SCREEN_WIDTH, SCREEN_HEIGHT
from gui_functions import *
from gui_classes import State, Player, BoardSquare, Board, TextBox, Ship, Scoreboard
import sys
import pygame
from pygame.locals import *
from functools import reduce
import random
import operator

tripleShotP1 = False
tripleShotP2 = False

pygame.init()
pygame.display.set_caption("Battleship")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

imageBattleshipSurface = pygame.image.load('battleship-1200x900.jpg').convert()
blackBackground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

def playNavigate():
    """
    This plays the "navigate" sound effect for clicking boxes and pressing keys
    """
    navigate = pygame.mixer.Sound('../sounds/navigate.wav')
    navigate.play()

def playMiss():
    """
    This plays the "miss" sound effect for clicking on a square that does NOT contain a ship
    """
    miss = pygame.mixer.Sound('../sounds/miss.wav')
    miss.play()

def playHit():
    """
    This plays the "hit" sound effect for clicking on a square that DOES contain a ship
    """
    hit = pygame.mixer.Sound('../sounds/hit.wav')
    hit.play()

def playSink():
    """
    This plays the "explosion" sound effect for clicking on the final square of a ship (sinking the ship)
    """
    explosion = pygame.mixer.Sound('../sounds/explosion.wav')
    explosion.play()

def run_start():
    """
    This procedure draws the background battleship image and prompts the player to hit the space bar to play.
    :return: void
    """

    screen.blit(imageBattleshipSurface, (0, 0))

    battleshipTextBox = TextBox("Battleship!", (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 4), fontsize=96)
    screen.blit(battleshipTextBox.surface, battleshipTextBox.rect)
    pygame.mixer.music.load('../sounds/intro.mp3')
    pygame.mixer.music.play(-1)
    instructionsTextBox = TextBox("Press the SPACE bar to play", (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2), fontsize=48)
    screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                playNavigate()
                return

def run_get_num_players():
    """
    This will display a screen where users can select if they want to play with one or two players.
    """
    # define background, instruction, box for each number of ships
    def create_number_boxes():
        def create_number_box(j):
            x = SCREEN_WIDTH / 2
            y = SCREEN_HEIGHT - (SCREEN_HEIGHT / 3)
            return TextBox("{}".format(j), ((x * j) - 300, y), fontsize=128)
        return reduce(lambda others, j: others + [create_number_box(j)], [1, 2], [])


    instructionsTextBox = TextBox("Do you want to play with one or two players?", (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 3), fontsize=64)
    numberBoxes = create_number_boxes()

    # draw background
    screen.blit(imageBattleshipSurface, (0, 0))

    # draw instruction
    screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

    # draw number boxes
    for box in numberBoxes:
        screen.blit(box.surface, box.rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in [1, 2]:
                    if numberBoxes[i - 1].rect.collidepoint(event.pos):
                        playNavigate()
                        return i

def run_get_ai_difficulty_level():
    """
    This will display a screen where users can select the difficulty of the AI to play agianst in one player mode
    """
    # define background, instruction, box for each number of ships
    def create_number_boxes():
        def create_number_box(j):
            x = SCREEN_WIDTH / 3
            y = SCREEN_HEIGHT - (SCREEN_HEIGHT / 3)
            return TextBox("{}".format(j), ((x * j) - 200, y), fontsize=128)
        return reduce(lambda others, j: others + [create_number_box(j)], [1, 2, 3], [])


    instructionsTextBox = TextBox("Select AI diffiuclty: 1) Easy, 2) Medium, 3) Hard", (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 3), fontsize=64)
    numberBoxes = create_number_boxes()

    # draw background
    screen.blit(imageBattleshipSurface, (0, 0))

    # draw instruction
    screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

    # draw number boxes
    for box in numberBoxes:
        screen.blit(box.surface, box.rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in [1, 2, 3]:
                    if numberBoxes[i - 1].rect.collidepoint(event.pos):
                        playNavigate()
                        return i

# returns the number of ships
def run_get_number_ships():
    """
    This prompts the user to select a number box. It returns an integer value for the number of ships that the game will be played with.
    :return: int from 1-5 representing the number of ships to play with
    """
    # define background, instruction, box for each number of ships
    def create_number_boxes():
        def create_number_box(j):
            x = SCREEN_WIDTH / 5
            y = SCREEN_HEIGHT - (SCREEN_HEIGHT / 3)
            return TextBox("{}".format(j), ((x * j) - 128, y), fontsize=128)
        return reduce(lambda others, j: others + [create_number_box(j)], [1, 2, 3, 4, 5], [])


    instructionsTextBox = TextBox("Click the number of ships to play with:", (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 3), fontsize=64)
    numberBoxes = create_number_boxes()

    # draw background
    screen.blit(imageBattleshipSurface, (0, 0))

    # draw instruction
    screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

    # draw number boxes
    for box in numberBoxes:
        screen.blit(box.surface, box.rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in [1, 2, 3, 4, 5]:
                    if numberBoxes[i - 1].rect.collidepoint(event.pos):
                        playNavigate()
                        return i

def run_place_ai_ships(numShips):
    """ This method will randomly create the coordinates for the AI's ships
    :param numShips: int - represents the number of placeable ships
    :return: a list of list of coordinates (row, col). Each sub list represents the grouping of a ship.

    TODO make sure ships can't be placed on top of eachother. Right now, they could be placed on top of
         eachother if the random numbers work out that way
    """

    coordinates = []
    shipToPlace = numShips

    for index in range(0, numShips):

        individualCoordinates = []
        isBadPlacement = True

        while isBadPlacement:

            startX = random.randint(1, 8 - shipToPlace)
            startY = random.randint(1, 8 - shipToPlace)

            verticalOrHorizontal = random.randint(1, 2) # 1 -> vertical, 2 -> horizontal

            if verticalOrHorizontal == 1:
                for i in range(0, shipToPlace):
                    individualCoordinates.append((startY + i, startX))
            else:
                for i in range(0, shipToPlace):
                    individualCoordinates.append((startY, startX + i))

            isBadPlacement = False

            for i in individualCoordinates:
                if i in flatten(coordinates):
                    isBadPlacement = True

        coordinates.append(individualCoordinates)
        shipToPlace = shipToPlace - 1

    return coordinates

# Returns a list of lists of (row, col) coordinates. Example: [[(1,1), (1,2), (1,3)], [(3,3), (4,3)], [(8,8)]]
def run_place_ships(numShips, playerName):
    """
    This is a procedure that allows the user to interactively place their ships on a placement board. It iterates until all ships are placed.
    :param numShips: int - represents the number of placeable ships
    :param playerName: string - used to display the message prompting the user to place their ships
    :return: a list of list of coordinates. Each sub list represents the grouping of a ship.
    """

    # define the board to place on
    placeBoard = Board(((SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 6)), (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * (2 / 3)))

    instructionsTextBox1 = TextBox("Click a blue ship on the left to select it for placement.", (48, 48))

    instructionsTextBoxEscape = TextBox("Press the ESC button to cancel placing this ship.", (96, 102), fontsize=36)

    instructionsTextBoxClick = TextBox("Click an anchor box on the grid. You will then be able to rotate your ship.",(48, 48))

    def ship_size_to_coord(size):
        queueWidth = SCREEN_WIDTH / 3
        queueHeight = SCREEN_HEIGHT * (2 / 3)
        queueX = SCREEN_WIDTH / 8
        queueY = SCREEN_HEIGHT / 4

        firstColX = queueX
        firstRowY = queueY

        secondColX = queueX + (queueWidth * (1 / 3))

        switch = {
            1: (firstColX,  firstRowY),
            2: (firstColX,  firstRowY + (placeBoard.squareHeight * 2)),
            3: (firstColX,  firstRowY + (placeBoard.squareHeight * 5)),
            4: (secondColX, firstRowY),
            5: (secondColX, firstRowY + (placeBoard.squareHeight * 5))
        }
        return switch[size]

    # define ship surfaces based on numShips - they sit to the left of the board

    def create_ship_queue(n):
        return reduce(lambda prevs, i: prevs + [Ship(i, placeBoard.squareWidth - 1, placeBoard.squareHeight - 1, ship_size_to_coord(i))], range(1, n+1), [])

    shipQueue = create_ship_queue(numShips)

    # black the screen
    screen.fill(colors['BLACK'])
    pygame.display.flip()
    # blit_objects(screen, placeBoard.squares + placeBoard.rowLabels + placeBoard.colLabels)
    # blit_objects(screen, shipQueue)
    # screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)

    def get_clicked_ship(pos):
        return get_intersect_object_from_list(pos, shipQueue)

    # Display the welcome message
    welcomeBox = TextBox("{}, place your ships!".format(playerName), (130, SCREEN_HEIGHT / 3), fontsize=96, textcolor=colors['GREEN'])
    screen.blit(welcomeBox.surface, welcomeBox.rect)
    pygame.display.update(welcomeBox.rect)
    pygame.time.delay(2000)
    screen.fill(colors['BLACK'])

    # event loop
    shipCoordsList = []

    while True:
        if not shipQueue:
            screen.fill((0, 0, 0))
            pygame.display.flip()
            return list(filter(lambda e: not isinstance(e, tuple), shipCoordsList))
        screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
        blit_objects(screen, shipQueue)
        blit_board(screen, generate_placement_board(encode_placement_board([], flatten(shipCoordsList))))
        screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
        pygame.display.flip()
        if playerName != "AI":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clickedShip = get_clicked_ship(event.pos)
                    if clickedShip is not None:
                        playNavigate()
                        # highlight ship in the queue
                        highlight(screen, clickedShip, colors['GREEN'])
                        chosenLocation = run_choose_board_location(clickedShip, shipCoordsList, playerName)
                        if chosenLocation is None:
                            cover_instructions(screen, instructionsTextBoxEscape)
                            cover_instructions(screen, instructionsTextBoxClick)
                            highlight(screen, clickedShip, colors['BLUE'])
                        else:
                            shipCoordsList += [chosenLocation]
                            shipQueue.remove(clickedShip)
                            highlight(screen, clickedShip, colors['BLACK'])
                            # blit_objects(screen, shipQueue)


        screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
        pygame.display.flip()
        pygame.time.delay(200)


def run_choose_board_location(ship, otherShipCoords, playerName):
    """
    This is a sub-procedure to the procedure 'run_placed_ships'. Logically, this represents the state for the player to place an already selected ship.
    :param ship: a Ship object that holds the information about its length and other properties
    :param otherShipCoords: a list of all the other previously-placed coordinates. Used prevent invalid placement.
    :return: a list of coordinates corresponding to where the ship was placed or None if the user escapes the transaction
    """
    instructionsTextBoxClick = TextBox("Click an anchor box on the grid. You will then be able to rotate your ship.",
                                       (48, 48))
    instructionsTextBoxEscape = TextBox("Press the ESC button to cancel placing this ship.", (96, 102), fontsize=36)

    otherCoordsPairsList = list(map(lambda coord: (coord, 2), otherShipCoords))

    ## display a board with the other placed ships' coordinates filled in
    initialBoard = generate_placement_board(otherCoordsPairsList)

    def escape_placement():
        blit_board(screen, initialBoard)
        pygame.display.flip()


    # highlight the updateBoard squares that correspond to each coordinate in the passed in list of coordinates
    # just display a new board?
    def display_suggestion_placement_board(coordList):
        codePairs = encode_placement_board(coordList, otherCoordsPairsList)
        blit_board(screen, generate_placement_board(codePairs))


    def wait_for_click_display(board, square):
        while True:
            blit_board(screen, board)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and square.rect.collidepoint(event.pos):
                    playNavigate()
                    return True
                elif event.type == pygame.MOUSEMOTION and not square.rect.collidepoint(event.pos):
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    playNavigate()
                    cover_instructions(screen, instructionsTextBoxEscape)
                    cover_instructions(screen, instructionsTextBoxClick)
                    return None
            pygame.time.delay(100)

    def ai_place_anchor(row, col):
        anchor = [row, col]
        if anchor in otherShipCoords:
            return False
        else:
            return True

    #def ai_place_ship(anchor, shiplength, otherShipCoords):




    def run_rotate_ship(shipLength, anchorCoord, firstOrientation):
        """
        This is a sub-procedure to the 'run_choose_board_location' procedure and corresponds to the state where the player rotates their "anchored" ship.
        :param shipLength: int - the placement ship's length
        :param anchorCoord: coordinate (row, col) - the pivot coordinate of the ship's rotation
        :param firstOrientation: int - an orientation code (0-3) representing the initial orientation of the ship
        :return: a list of coordinates representing the placed coordinates of the ship or None if the user escapes
        """
        instructionsTextBoxRotate = TextBox("Use the UP (counter-clockwise) and DOWN (clockwise) arrow keys to rotate your ship.", (96, 10), fontsize=36)
        instructionsTextBoxEnter = TextBox("Press SPACE when you are satisfied with the orientation.", (96, 56), fontsize=36)

        screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.surface.fill(colors['BLACK']).move(instructionsTextBoxClick.window_coord))

        blit_objects(screen, [instructionsTextBoxEnter, instructionsTextBoxRotate, instructionsTextBoxEscape])
        pygame.display.flip()

        placeList = orientation_to_coord_list(anchorCoord, shipLength, firstOrientation)
        orientation = firstOrientation

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    playNavigate()
                    if event.key == pygame.K_ESCAPE:
                        cover_instructions(screen, instructionsTextBoxRotate)
                        cover_instructions(screen, instructionsTextBoxEnter)
                        cover_instructions(screen, instructionsTextBoxEscape)
                        cover_instructions(screen, instructionsTextBoxClick)
                        escape_placement()
                        return None
                    elif event.key == pygame.K_UP and is_possible_orientation(anchorCoord, shipLength, orientation + 1, otherShipCoords):
                        orientation = (orientation + 1) % 4
                    elif event.key == pygame.K_DOWN and is_possible_orientation(anchorCoord, shipLength, orientation - 1, otherShipCoords):
                        orientation = (orientation - 1) % 4
                    elif event.key == pygame.K_SPACE:
                        cover_instructions(screen, instructionsTextBoxRotate)
                        cover_instructions(screen, instructionsTextBoxEnter)
                        cover_instructions(screen, instructionsTextBoxEscape)
                        cover_instructions(screen, instructionsTextBoxClick)
                        escape_placement()
                        pygame.display.flip()
                        return placeList
            placeList = orientation_to_coord_list(anchorCoord, shipLength, orientation)
            blit_board(screen, generate_placement_board(encode_placement_board(placeList, otherShipCoords)))
            pygame.display.flip()
            pygame.time.delay(100)

    blit_board(screen, initialBoard)
    # screen.blit(ship.surface, ship.rect)
    # screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.rect)
    # screen.blit(instructionsTextBoxEscape.surface, instructionsTextBoxEscape.rect)
    pygame.display.flip()
    if playerName != "AI":
        while True:
            screen.blit(ship.surface, ship.rect)
            screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.rect)
            screen.blit(instructionsTextBoxEscape.surface, instructionsTextBoxEscape.rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    playNavigate()
                    return None
                elif event.type == MOUSEMOTION:
                    hoveredSquare = get_hovered_square(event.pos, initialBoard)
                    if hoveredSquare is not None:
                        firstOrientation = first_possible_orientation(hoveredSquare.grid_coord, ship.length, otherShipCoords)
                        if firstOrientation is not None:
                            suggestionCoords = orientation_to_coord_list(hoveredSquare.grid_coord, ship.length, firstOrientation)
                            displayBoard = generate_placement_board(encode_placement_board(suggestionCoords, otherShipCoords))
                            didClick = wait_for_click_display(displayBoard, hoveredSquare)
                            if didClick:
                                placed = run_rotate_ship(ship.length, hoveredSquare.grid_coord, firstOrientation)
                                if placed is not None:
                                    otherShipCoords += placed
                                    return placed
                                else:
                                    escape_placement()
                                    cover_instructions(screen, instructionsTextBoxEscape)
                                    cover_instructions(screen, instructionsTextBoxClick)
                                    return None
                            elif didClick is None:
                                escape_placement()
                                cover_instructions(screen, instructionsTextBoxClick)
                                return None
            pygame.display.flip()
            pygame.time.delay(50)


def run_ai_game_loop(shipCoords1, shipCoords2, aiDifficulty):
    """
    This is the main game loop for battleship. It consists of a loop the allows one player to guess, stores that guess, updates the current player, and then switches the turn.
    :param shipCoords1: a list of lists of coordinates corresponding to the first player's chosen ship locations.
    :param shipCoords2: a list of lists of coordinates corresponding to the second player's chosen ship locations.
    :return: string - the name of the player who won (either "Player 1" or "Player 2")
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load('../sounds/gameplay.mp3')
    pygame.mixer.music.play(-1)

    switchTurnsInstructionsBox = TextBox("Press the SPACE key to switch turns.", (240, 48))
    switchTurnsInstructionsBox2 = TextBox("Please switch spots with your playing partner. Press any key to continue.", (35, SCREEN_HEIGHT / 2), fontsize=44)
    guessBoardLabel = TextBox("Attack Board", (200, SCREEN_HEIGHT / 5), textcolor=colors['RED'])
    myBoardLabel = TextBox("My Board", (SCREEN_WIDTH - 370, SCREEN_HEIGHT / 5), textcolor=colors['GREEN'])
    hitTextBox = TextBox("Hit!", ((SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT * (8 / 10)), textcolor=colors['GREEN'], fontsize=96)
    missTextBox = TextBox("Miss.", ((SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT * (8 / 10)), textcolor=colors['RED'], fontsize=96)

    player1 = Player(shipCoords1, "Player 1")
    player2 = Player(shipCoords2, "AI")
    state = State(player1, player2)

    hits = []

    spotsToHit = shipCoords1

    def generate_sunk_ship_alert(shipLength):
        #PLAY SUNK SHIP EXPLOSION SOUND
        playSink()
        return TextBox("You sunk the other player's {}".format(ship_length_to_name(shipLength)), (SCREEN_WIDTH / 4, SCREEN_HEIGHT * (9 / 10)), textcolor=colors['GREEN'])

    def produce_guess_board():
        return generate_guess_board(encode_guess_board(state.player1.guesses, state.player2.ships))

    def produce_guessed_at_board():
        return generate_guessed_at_board(encode_guessed_at_board(state.player2.guesses, state.player1.ships))

    def wait_for_click_guess(square):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and square.rect.collidepoint(event.pos):
                    playNavigate()
                    return square.grid_coord
                elif event.type == pygame.MOUSEMOTION and not square.rect.collidepoint(event.pos):
                    return None
            pygame.time.delay(30)

    def med_ai_traverse(ax, ay, shipCoords1, arr):
        if ay+1 < 9 and ax+1 < 9 and ay-1 > 0 and ax-1 > 0:
            if (ay+1, ax) not in shipCoords1 and (ay-1, ax) not in shipCoords1 and (ay, ax+1) not in shipCoords1 and (ay, ax-1) not in shipCoords1:
                return arr
            if (ay+1, ax) in shipCoords1:
                arr.append((ay+1, ax))
                med_ai_traverse(ax, ay+1, shipCoords1, arr)

            if (ay, ax+1) in shipCoords1:
                arr.append((ay, ax+1))
                med_ai_traverse(ax+1, ay, shipCoords1, arr)

            if (ay-1, ax) in shipCoords1:
                arr.append((ay-1, ax))
                med_ai_traverse(ax, ay-1, shipCoords1, arr)

            if (ay, ax-1) in shipCoords1:
                arr.append((ay, ax-1))
                med_ai_traverse(ax-1, ay, shipCoords1, arr)
            else:
                return



    def run_switch_turns():
        # display switch turns instruction message
        screen.blit(switchTurnsInstructionsBox.surface, switchTurnsInstructionsBox.rect)
        pygame.display.flip()
        # wait till they hit SPACE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    playNavigate()
                    # black the screen
                    screen.fill((0, 0, 0))
                    # display the instructions to switch turns
                    screen.blit(switchTurnsInstructionsBox2.surface, switchTurnsInstructionsBox2.rect)
                    pygame.display.flip()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                                playNavigate()
                                screen.fill(colors['BLACK'])
                                return True
            pygame.time.delay(50)
        return False

    while True:
        if state.player1.name == "Player 1":
            whosTurnTextBox = TextBox("{}'s Turn".format(state.player1.name), (SCREEN_WIDTH * (3 / 8), 40), fontsize=64, textcolor=colors['GREEN'])
            guessInstructionsTextBox = TextBox("Click a coordinate on the Attack Board to fire a missile!", (110, 96))
            initialGuessBoard = produce_guess_board()
            blit_board(screen, initialGuessBoard)
            blit_board(screen, produce_guessed_at_board())
            blit_objects(screen, [guessBoardLabel, myBoardLabel, guessInstructionsTextBox, whosTurnTextBox])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    hoveredSquare = get_hovered_square(event.pos, initialGuessBoard)
                    if (hoveredSquare is not None) and (hoveredSquare.grid_coord not in state.player1.guesses):
                        highlight(screen, hoveredSquare, colors['YELLOW'])
                        guess = wait_for_click_guess(hoveredSquare)
                        if guess is not None:
                            print("Human Guess:", guess)
                            pygame.draw.rect(screen, colors['BLACK'], guessInstructionsTextBox.rect)
                            pygame.draw.rect(screen, colors['BLACK'], whosTurnTextBox.rect)
                            if hit(guess, state.player2.ships):
                                #PLAY HIT SOUND
                                playHit()
                                highlight(screen, hoveredSquare, colors['GREEN'])
                                screen.blit(hitTextBox.surface, hitTextBox.rect)
                                sunkenShipLength = which_sunk(guess, state.player1.guesses, state.player2.ships)
                                state.update(guess)
                                if sunkenShipLength is not None:
                                    sunkAlertBox = generate_sunk_ship_alert(sunkenShipLength)
                                    screen.blit(sunkAlertBox.surface, sunkAlertBox.rect)
                                    pygame.display.flip()
                                    if state.is_game_over():
                                        pygame.display.flip()
                                        pygame.time.delay(2000)
                                        screen.fill(colors['BLACK'])
                                        return state.player2.name
                            else:
                                #PLAY MISS SOUND
                                playMiss()
                                highlight(screen, hoveredSquare, colors['RED'])
                                screen.blit(missTextBox.surface, missTextBox.rect)
                                state.update(guess)
                            pygame.display.flip()
                            pygame.time.delay(1500)
                            if run_switch_turns():
                                screen.fill(colors['BLACK'])
                                break
            pygame.display.flip()
            pygame.time.delay(30)
        else:
            guess = 0
            if aiDifficulty == 1:
                x = random.randint(1, 8)
                y = random.randint(1, 8)
                guess = (y, x)
                print("AI Guess:", guess)
                #state.update((y, x))
                if guess in flatten(state.player2.ships):
                    print("in hit")
                    sunkenShipLength = which_sunk(guess, state.player1.guesses, state.player2.ships)
                    state.update(guess)
                    if sunkenShipLength is not None:
                        sunkAlertBox = generate_sunk_ship_alert(sunkenShipLength)
                        screen.blit(sunkAlertBox.surface, sunkAlertBox.rect)
                        pygame.display.flip()
                        if state.is_game_over():
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            screen.fill(colors['BLACK'])
                            return state.player2.name
                else:
                    state.update(guess)

            elif aiDifficulty == 2:
                x = random.randint(1, 8)
                y = random.randint(1, 8)
                print("AI Guess:", (y, x))
                print(state.player1.name)
                if (y,x) in flatten(state.player2.ships) and (y,x) not in hits:
                    ax = x
                    ay = y
                    ct = 1
                    arr = [(ay,ax)]
                    listOfHitsInTurn = med_ai_traverse(ax, ay, flatten(state.player2.ships), arr)
                    hits.append(listOfHitsInTurn)
                    state.update(listOfHitsInTurn)
                else:
                    state.update((y,x))
                aiGuessedText = TextBox("Guess: {}".format((y,x)))
                #pygame.display.flip()
                pygame.time.delay(1500)

            else:
                randShipNum = random.randint(0, len(spotsToHit) - 1)
                singleShip = spotsToHit[randShipNum]
                randSpotNum = random.randint(0, len(singleShip) - 1)
                singleSpot = singleShip[randSpotNum]
                guess = singleSpot
                #print("AI Guess:", (y, x))
                state.update(spotsToHit)
                print()
                print(randShipNum)
                print(singleShip)
                print(randSpotNum)
                print(singleSpot)
                print(guess)
                print(spotsToHit)
                spotsToHit[randShipNum].remove(singleSpot)
                if len(spotsToHit[randShipNum]) == 0:
                    spotsToHit.remove([])
                print(spotsToHit)

                if len(flatten(spotsToHit)) == 0:
                    screen.fill(colors['BLACK'])
                    return state.player2.name

# the main game loop
# takes 2 args: player1 and player2
def run_game_loop(shipCoords1, shipCoords2):
    """
    This is the main game loop for battleship. It consists of a loop the allows one player to guess, stores that guess, updates the current player, and then switches the turn.
    :param shipCoords1: a list of lists of coordinates corresponding to the first player's chosen ship locations.
    :param shipCoords2: a list of lists of coordinates corresponding to the second player's chosen ship locations.
    :return: string - the name of the player who won (either "Player 1" or "Player 2")
    """
    tripleShotP1 = False
    tripleShotP2 = False
    p1 = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('../sounds/gameplay.mp3')
    pygame.mixer.music.play(-1)

    switchTurnsInstructionsBox = TextBox("Press the SPACE key to switch turns.", (240, 48))
    switchTurnsInstructionsBox2 = TextBox("Please switch spots with your playing partner. Press any key to continue.", (35, SCREEN_HEIGHT / 2), fontsize=44)
    guessBoardLabel = TextBox("Attack Board", (200, SCREEN_HEIGHT / 5), textcolor=colors['RED'])
    myBoardLabel = TextBox("My Board", (SCREEN_WIDTH - 370, SCREEN_HEIGHT / 5), textcolor=colors['GREEN'])
    hitTextBox = TextBox("Hit!", ((SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT * (8 / 10)), textcolor=colors['GREEN'], fontsize=96)
    missTextBox = TextBox("Miss.", ((SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT * (8 / 10)), textcolor=colors['RED'], fontsize=96)

    player1 = Player(shipCoords1, "Player 1")
    player2 = Player(shipCoords2, "Player 2")
    state = State(player1, player2)


    def generate_sunk_ship_alert(shipLength):
        return TextBox("You sunk the other player's {}".format(ship_length_to_name(shipLength)), (SCREEN_WIDTH / 4, SCREEN_HEIGHT * (9 / 10)), textcolor=colors['GREEN'])

    def produce_guess_board():
        return generate_guess_board(encode_guess_board(state.player1.guesses, state.player2.ships))

    def produce_guessed_at_board():
        return generate_guessed_at_board(encode_guessed_at_board(state.player2.guesses, state.player1.ships))

    def wait_for_click_guess(square):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and square.rect.collidepoint(event.pos):
                    playNavigate()
                    return square.grid_coord
                elif event.type == pygame.MOUSEMOTION and not square.rect.collidepoint(event.pos):
                    return None
            pygame.time.delay(30)

    def run_switch_turns():
        # display switch turns instruction message
        screen.blit(switchTurnsInstructionsBox.surface, switchTurnsInstructionsBox.rect)
        pygame.display.flip()
        # wait till they hit SPACE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    playNavigate()
                    # black the screen
                    screen.fill((0, 0, 0))
                    # display the instructions to switch turns
                    screen.blit(switchTurnsInstructionsBox2.surface, switchTurnsInstructionsBox2.rect)
                    pygame.display.flip()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                                playNavigate()
                                screen.fill(colors['BLACK'])
                                return True
            pygame.time.delay(50)
        return False

    while True:
        whosTurnTextBox = TextBox("{}'s Turn".format(state.player1.name), (SCREEN_WIDTH * (3 / 8), 40), fontsize=64, textcolor=colors['GREEN'])
        guessInstructionsTextBox = TextBox("Click a coordinate on the Attack Board to fire a missile!", (110, 96))
        initialGuessBoard = produce_guess_board()
        blit_board(screen, initialGuessBoard)
        blit_board(screen, produce_guessed_at_board())
        blit_objects(screen, [guessBoardLabel, myBoardLabel, guessInstructionsTextBox, whosTurnTextBox])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                if((tripleShotP1 and p1) or (tripleShotP2 and not p1)):
                    hoveredSquare = get_hovered_square(event.pos, initialGuessBoard)
                    hoveredSquare2 = get_hovered_square((event.pos[0] - 60, event.pos[1]), initialGuessBoard)
                    hoveredSquare3 = get_hovered_square((event.pos[0] + 60, event.pos[1]), initialGuessBoard)
                    if (hoveredSquare2 is not None) and (hoveredSquare2.grid_coord not in state.player1.guesses):
                            highlight(screen, hoveredSquare2, colors['YELLOW'])
                    if (hoveredSquare3 is not None) and (hoveredSquare3.grid_coord not in state.player1.guesses):
                            highlight(screen, hoveredSquare3, colors['YELLOW'])
                    if (hoveredSquare is not None) and (hoveredSquare.grid_coord not in state.player1.guesses):
                        highlight(screen, hoveredSquare, colors['YELLOW'])
                        guess = wait_for_click_guess(hoveredSquare)
                        if guess is not None:
                            pygame.draw.rect(screen, colors['BLACK'], guessInstructionsTextBox.rect)
                            pygame.draw.rect(screen, colors['BLACK'], whosTurnTextBox.rect)
                            if hit(guess, state.player2.ships):
                                highlight(screen, hoveredSquare, colors['GREEN'])
                                screen.blit(hitTextBox.surface, hitTextBox.rect)
                                sunkenShipLength = which_sunk(guess, state.player1.guesses, state.player2.ships)
                                state.update(guess, False)
                                if sunkenShipLength is not None:
                                    sunkAlertBox = generate_sunk_ship_alert(sunkenShipLength)
                                    screen.blit(sunkAlertBox.surface, sunkAlertBox.rect)
                                    pygame.display.flip()
                                    if state.is_game_over():
                                        pygame.display.flip()
                                        pygame.time.delay(2000)
                                        screen.fill(colors['BLACK'])
                                        return state.player2.name
                            else:
                                highlight(screen, hoveredSquare, colors['RED'])
                                screen.blit(missTextBox.surface, missTextBox.rect)
                                state.update(guess, False)
                            if hit(tuple(map(operator.add, guess, (0, -1))), state.player2.ships):
                                highlight(screen, hoveredSquare2, colors['GREEN'])
                                screen.blit(hitTextBox.surface, hitTextBox.rect)
                                sunkenShipLength = which_sunk(tuple(map(operator.add, guess, (0, -1))), state.player1.guesses, state.player2.ships)
                                state.update(tuple(map(operator.add, guess, (0, -1))), False)
                                if sunkenShipLength is not None:
                                    sunkAlertBox = generate_sunk_ship_alert(sunkenShipLength)
                                    screen.blit(sunkAlertBox.surface, sunkAlertBox.rect)
                                    pygame.display.flip()
                                    if state.is_game_over():
                                        pygame.display.flip()
                                        pygame.time.delay(2000)
                                        screen.fill(colors['BLACK'])
                                        return state.player2.name
                            else:
                                highlight(screen, hoveredSquare2, colors['RED'])
                                screen.blit(missTextBox.surface, missTextBox.rect)
                                state.update(tuple(map(operator.add, guess, (0, -1))), False)
                            if hit(tuple(map(operator.add, guess, (0, 1))), state.player2.ships):
                                highlight(screen, hoveredSquare3, colors['GREEN'])
                                screen.blit(hitTextBox.surface, hitTextBox.rect)
                                sunkenShipLength = which_sunk(tuple(map(operator.add, guess, (0, 1))), state.player1.guesses, state.player2.ships)
                                state.update(tuple(map(operator.add, guess, (0, 1))), True)
                                if sunkenShipLength is not None:
                                    sunkAlertBox = generate_sunk_ship_alert(sunkenShipLength)
                                    screen.blit(sunkAlertBox.surface, sunkAlertBox.rect)
                                    pygame.display.flip()
                                    if state.is_game_over():
                                        pygame.display.flip()
                                        pygame.time.delay(2000)
                                        screen.fill(colors['BLACK'])
                                        return state.player2.name
                            else:
                                highlight(screen, hoveredSquare3, colors['RED'])
                                screen.blit(missTextBox.surface, missTextBox.rect)
                                state.update(tuple(map(operator.add, guess, (0, 1))), True)
                            pygame.display.flip()
                            pygame.time.delay(1500)
                            if run_switch_turns():
                                screen.fill(colors['BLACK'])
                                break
                else:
                    hoveredSquare = get_hovered_square(event.pos, initialGuessBoard)
                    if (hoveredSquare is not None) and (hoveredSquare.grid_coord not in state.player1.guesses):
                        highlight(screen, hoveredSquare, colors['YELLOW'])
                        guess = wait_for_click_guess(hoveredSquare)
                        if guess is not None:
                            pygame.draw.rect(screen, colors['BLACK'], guessInstructionsTextBox.rect)
                            pygame.draw.rect(screen, colors['BLACK'], whosTurnTextBox.rect)
                            if hit(guess, state.player2.ships):
                                #PLAY HIT SOUND
                                playHit()
                                highlight(screen, hoveredSquare, colors['GREEN'])
                                screen.blit(hitTextBox.surface, hitTextBox.rect)
                                sunkenShipLength = which_sunk(guess, state.player1.guesses, state.player2.ships)
                                state.update(guess)
                                if sunkenShipLength is not None:
                                    sunkAlertBox = generate_sunk_ship_alert(sunkenShipLength)
                                    screen.blit(sunkAlertBox.surface, sunkAlertBox.rect)
                                    pygame.display.flip()
                                    if(sunkenShipLength == 1):
                                    if(not p1):
                                        tripleShotP1 = True
                                    else:
                                        tripleShotP2 = True
                                    if state.is_game_over():
                                        pygame.display.flip()
                                        pygame.time.delay(2000)
                                        screen.fill(colors['BLACK'])
                                        return state.player2.name
                            else:
                                #PLAY MISS SOUND
                                playMiss()
                                highlight(screen, hoveredSquare, colors['RED'])
                                screen.blit(missTextBox.surface, missTextBox.rect)
                                state.update(guess)
                            pygame.display.flip()
                            pygame.time.delay(1500)
                            if run_switch_turns():
                                screen.fill(colors['BLACK'])
                                break
        pygame.display.flip()
        pygame.time.delay(30)


# returns a boolean indicating whether or not to play again
def winner_screen_prompt_replay(winnerName, isAI, win_score):
    """
    This is a display screen procedure that displays the game's winner and prompts the user to click whether or not to play again.
    :param winnerName: string - the name of the game's winner
    :param isAI: bool - true if game is player vs ai, false when game is player vs player
    :param win_score: Scoreboard - the scoreboard for the game
    :return: bool - represents whether or not to play again
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load('../sounds/win.mp3')
    pygame.mixer.music.play(0)
    screen.fill(colors['BLACK'])
    # display the winner text box
    winnerTextBox = TextBox("{} has won the game!".format(winnerName), (130, 48), fontsize=96, textcolor=colors['GREEN'])
    # display the play again prompt
    playAgainTextBox = TextBox("Would you like to play again? Click either 'YES' or 'NO'.", (90, SCREEN_HEIGHT * (3 / 8)), fontsize=56)
    # display the 'Yes' and 'No' boxes
    yesBox = TextBox("YES", ((SCREEN_WIDTH / 3) - (128 * (2 / 3)), SCREEN_HEIGHT * (3 / 4)), fontsize=128, textcolor=colors['GREEN'])
    noBox = TextBox("NO", ((SCREEN_WIDTH * (2 / 3)) - (128 * (2 / 3)), SCREEN_HEIGHT * (3 / 4)), fontsize=128, textcolor=colors['RED'])

    if isAI:
        scoreBox = TextBox("Player 1 Score: " + str(win_score.get_p1_wins()) + "    AI Score: " + str(win_score.get_ai_wins()),
                            (45, 150), fontsize=90, textcolor=colors['BLUE'])
    else:
        scoreBox = TextBox("Player 1 Score: " + str(win_score.get_p1_wins()) + "    Player 2 Score: " + str(win_score.get_p2_wins()),
                            (45, 150), fontsize=90, textcolor=colors['BLUE'])

    blit_objects(screen, [winnerTextBox, playAgainTextBox, yesBox, noBox, scoreBox])
    pygame.display.flip()
    # wait for click

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                clickedOnBox = get_intersect_object_from_list(event.pos, [yesBox, noBox])
                if clickedOnBox is not None:
                    playNavigate()
                    screen.fill(colors['BLACK'])
                    pygame.display.flip()
                    if clickedOnBox is yesBox:
                        return True
                    return False
        pygame.time.delay(200)
