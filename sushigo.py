# This is a command line interface for playing Sushi Go and logging gameplay data
# The resulting data will be used for training a machine learning model to play the game

import random
import math


output_filename = 'game_log.txt'


# define how many of each card there are 
sushi_go_cards = [
    {"count": 1, "name": ""},
]

# construct the deck
deck = []
for i in sushi_go_cards:
    for j in range(sushi_go_cards[i]["count"]):
        deck.append(sushi_go_cards[i]["name"])



def score_a_board(board, round):
    score = 0
    tempura_count = len([card for card in board if card == 'Tempura'])
    tempura_score = 5 * math.floor(tempura_count / 2.0)

    score = score + tempura_score


def player_takes_turn(player):
    print("It is " + player["name"] + "'s turn. " + player["name"] + " is holding these cards:")
    card_index = 0
    if len(player["hand"]) > 0:
        for card in player["hand"]:
            print(card_index + "    " + card)
            card_index = card_index + 1
            def play_a_card():
                playing_a_card = True
                while playing_a_card:
                    the_play = int(input(player["name"] + ", select a card to play by entering a number:"))
                    if the_play >=0 and the_play < len(player["hand"]):
                        card = player["hand"][the_play]
                        try:
                            player["hand"].remove(card)
                            player["board"].append(card)
                            playing_a_card = False
                            if card == "Chopsticks":
                                player["chopsticks_pending"] = player["chopsticks_pending"] + 1
                            if card == "Wasabi":
                                # TODO: add wasabi logic
                                print("Wasabi scoring logic has not yet been implemented")
                                player["wasabis_pending"] = player["wasabis_pending"] + 1
                        except:
                            print("Error occurred while removing the selected card from the player's hand")
                    else:
                        print("Invalid input")
            if player["chopsticks_pending"] > 0:
                play_a_card()
                try:
                    player["board"].remove("Chopsticks")
                    player["hand"].append("Chopsticks")
                    play_a_card
                except:
                    print("Error processing chopsticks: chopsticks card was not found in player's board")
                player["chopsticks_pending"] = player["chopsticks_pending"] - 1

                
 
    else:
        print("It is " + player["name"] + "'s turn. " + player["name"] + " has no cards in hand. Skipping turn.")

def print_boards(players):
    for player in players:
        print(player["name"] + "'s current board is ")
        for card in player["board"]:
            print(card)


def play_the_game(output_filename, players):

    # player_1 = {
    #     "order": 1,
    #     "name": "Player 1",
    #     "hand": [],
    #     "board": [],
    #     "score": 0
    # }

    # player_2 = {
    #     "order": 2,
    #     "name": "Player 2",
    #     "hand": [],
    #     "board": [],
    #     "score": 0
    # }

    # players = [player_1, player_2]

    def deal_cards():
        # deal 10 cards from the deck to each player
        for i in range(10):
            for player in players:
                n = random.randint(0, len(deck))
                player["hand"].append(deck[n])
                del deck[n]

    round = 1
    while round <=3:
        print("Beginning round " + round + "! ")

        # reset players' chopstick and wasabi statuses
        for player in players:
            player["chopsticks_pending"] = 0
            player["wasabis_pending"] = 0

        # shuffle the deck
        random.shuffle(deck)
        deal_cards()

        # start playing
        num_cards_remaining_in_hands = sum(len(player["hand"]) for player in players)
        while num_cards_remaining_in_hands > 0:
            for player in players:
                print_boards(players)
                player_takes_turn(player)
        
            # At the end of each turn, the players exchange hands
            dummyhand = player_1_hand
            player_1_hand = player_2_hand
            player_2_hand = dummyhand

            num_cards_remaining_in_hands = sum(len(player["hand"]) for player in players)

        # Score the players' boards. Puddings are scored only on round 3
        puddings = False
        if round >= 3:
            puddings = True
        for player in players:
            score = 0
            tempura_score = 5 * math.floor(len([card for card in player["hand"] if card is "Tempura"]) / 2.0)
            score = score + tempura_score
            print(player["name"] + "'s score for this round is " + score + " points. ")
            player["score"] = player["score"] + score
            

        


        # return all cards EXCEPT FOR PUDDINGS from the boards to the deck
        # Puddings stay on the board
        for player in players:
            deck.append([card for card in player["hand"]])
            deck.append([card for card in player["board"] if card is not "Pudding"])
            player["board"] = [card for card in player["board"] if card is "Pudding"]

        # The round is over
        if round < 3:
            print("Round " + round + " is over! The game ends after the third round.")
            round = round + 1
        else:
            print("Round " + round + " is over! The game is over.")
            print("The final scores are")
            for player in players:
                print(player["name"] + ": " + player["score"] + " points. ")
            largest_score = players[0]["score"]
            winner = players[0]["name"]
            for player in players:
                if player["score"] > largest_score:
                    largest_score = player["score"]
                    winner = player["name"]
            print("The winner is " + winner + "! ")


        
        






def start():
    print('Welcome to Sushi Go!')
    start_menu = True
    num_players = 0
    players = []
    while start_menu:
        start_menu_selection = input("Enter 'start' to start a new game, or enter 'quit' to quit:")
        match start_menu_selection:
            case 'start':
                # Number of players
                selecting_num_players = True
                while selecting_num_players:
                    num_players = int(input("Enter the number of players (2-5)"))
                    if 2 <= num_players <= 5:
                        selecting_num_players = False
                    else:
                        print("Invalid input.")
                # Names of players
                for i in range(num_players):
                    players.append({
                        "order": 1,
                        "name": "Player 1",
                        "hand": [],
                        "board": [],
                        "chopsticks_pending": 0,
                        "wasabis_pennding": 0,
                        "score": 0
                    })
                # Name of log file
                selecting_output_filename = True
                while selecting_output_filename:
                    print("The output filename will be " + output_filename)
                    overwrite_output_filename_selection = input("Do you want to choose a different filename? Y/N:")
                    match overwrite_output_filename_selection:
                        case 'Y' | 'y':
                            output_filename = input("Enter your desired output filename: ")
                        case 'N' | 'n':
                            selecting_output_filename = False
                        case _:
                            print('Invalid input')
                play_the_game(output_filename, players)
                starting_new_game = True
                while starting_new_game:
                    new_game = input("Start a new game?  Y/N")
                    match new_game:
                        case 'Y' | 'y':
                            starting_new_game = False
                            start()
                        case 'N' | 'n':
                            starting_new_game = False
                            print("Have a nice day!")
                        case _:
                            print('Invalid input')
            case 'quit':
                print('Have a nice day!')
                start_menu = False
            case _:
                print('Invalid input')

start()