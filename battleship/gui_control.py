import gui_states
from gui_classes import Scoreboard

# Global scoreboard object
score_tracker = Scoreboard()

# File I/O object for reading/writing player and ai score to file to store between game instances
s_file = open('score_file.txt', 'r+')
s_file_contents = s_file.readlines()
p1_data = int(s_file_contents[0])
p2_data = int(s_file_contents[1])
ai_data = int(s_file_contents[2])
score_tracker.set_scores_from_file(p1_data, p2_data, ai_data)

# Overwrite existing score file with updated scores
def write_scores(score_file):
    score_file.seek(0)
    score_file.write(str(score_tracker.get_p1_wins) + "\n")
    score_file.write(str(score_tracker.get_p2_wins) + "\n")
    score_file.write(str(score_tracker.get_ai_wins) + "\n")

# Set scores in file to 0s
def reset_file(score_file):
    score_file.seek(0)
    score_file.write("0\n")
    score_file.write("0\n")
    score_file.write("0\n")


def run():
    """
    The executive procedure that defines the control flow between all the sub-procedures.
    :return: void
    """
    play_again = True
    gui_states.screen.fill((0, 0, 0))
    while play_again:
        gui_states.run_start()
        num = gui_states.run_get_number_ships()
        numOfPlayers = gui_states.run_get_num_players()
        if(numOfPlayers == 1):
            aiDifficulty = gui_states.run_get_ai_difficulty_level()
            aiShips = gui_states.run_place_ai_ships(num)
            print("aiShips", aiShips)
            player1ships = gui_states.run_place_ships(num, "Player 1")

            
            winnerName = gui_states.run_ai_game_loop(player1ships, aiShips, aiDifficulty)
            score_tracker.update_win_score(winnerName)
            play_again = gui_states.winner_screen_prompt_replay(winnerName)
            if (play_again):
                write_scores(s_file)
            else:
                reset_file(s_file)

        else:
            player1ships = gui_states.run_place_ships(num, "Player 1")
            player2ships = gui_states.run_place_ships(num, "Player 2")
            winnerName = gui_states.run_game_loop(player1ships, player2ships)
            score_tracker.update_win_score(winnerName)
            play_again = gui_states.winner_screen_prompt_replay(winnerName)
            if (play_again):
                write_scores(s_file)
            else:
                reset_file(s_file)
            # test scoreboard by printing to terminal
            score_tracker.print_pvp_score()

run()
s_file.close()