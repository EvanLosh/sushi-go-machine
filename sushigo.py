# This is a command line interface for playing Sushi Go and logging gameplay data
# The resulting data will be used for training a machine learning model to play the game

import random
import math


def score_a_board(board, round):
    score = 0
    tempura_count = len([card for card in board if card == 'Tempura'])
    tempura_score = 5 * math.floor(tempura_count / 2.0)

    score = score + tempura_score

def play_the_game(output_filename):

    deck = []
    player_1_hand = []
    player_2_hand = []
    player_1_board = []
    player_2_board = []
    player_1_score = 0
    player_2_score = 0

    round = 1
    while round <=3:


        def deal_cards():
            # deal 10 cards from the deck to each player
            for i in range(10):
                n = random.randint(0, len(deck))
                player_1_hand.append(deck[n])
                del deck[n]
                n = random.randint(0, len(deck))
                player_2_hand.append(deck[n])
                del deck[n]
    
        deal_cards()

        # start playing
        turn = 1
        #Player 1's turn
        while len(player_1_hand) > 0 or len(player_2_hand) > 0:
            print("It is round " + round + ", turn " + turn + ".")
            print("Player 1's board is:")
            for card in player_1_board:
                print(card)
            print("Player 2's board is:")
            for card in player_2_board:
                print(card)
            print("It is player 1's turn. Player 1 is holding these cards:")
            card_index = 0
            for card in player_1_hand:
                print(card_index + "    " + card)
                card_index = card_index + 1
            making_a_play = True
            while making_a_play:
                the_play = input("Player 1, select a card to play by entering a number:")
                the_play = int(the_play)
                if the_play >=0 and the_play < len(player_1_hand):
                    player_1_board.append(player_1_hand[the_play])
                    del player_1_hand[the_play]
                    making_a_play = False

            #player 2's turn
            print("Player 1's board is:")
            for card in player_1_board:
                print(card)
            print("Player 2's board is:")
            for card in player_2_board:
                print(card)
            print("It is player 2's turn. Player 2 is holding these cards:")
            card_index = 0
            for card in player_2_hand:
                print(card_index + "    " + card)
                card_index = card_index + 1
            making_a_play = True
            while making_a_play:
                the_play = input("Player 2, select a card to play by entering a number:")
                the_play = int(the_play)
                if the_play >=0 and the_play < len(player_2_hand):
                    player_2_board.append(player_2_hand[the_play])
                    del player_2_hand[the_play]
                    making_a_play = False
        
            # At the end of each turn, the players exchange hands
            dummyhand = player_1_hand
            player_1_hand = player_2_hand
            player_2_hand = dummyhand

        # Score the players' boards. Puddings are scored only on round 3
            
        player_1_score = player_1_score + score_a_board(player_1_board, round)
        player_2_score = player_2_score + score_a_board(player_2_board, round)
        
        # return all cards EXCEPT FOR PUDDINGS from the boards to the deck

        deck.append([card for card in player_1_board if card is not "Pudding"])
        deck.append([card for card in player_2_board if card is not "Pudding"])
        player_1_board = [card for card in player_1_board if card is "Pudding"]
        player_2_board = [card for card in player_2_board if card is "Pudding"]


        # The round is over
        round = round + 1

    # after 



output_filename = 'game_log.txt'

def start():
    print('Welcome to Sushi Go!')
    start_menu = True
    while start_menu:
        start_menu_selection = input("Enter 'start' to start a new game, or enter 'quit' to quit:")
        match start_menu_selection:
            case 'start':
                selecting_output_filename = True
                while selecting_output_filename:
                    print("The output filename will be " + output_filename)
                    overwrite_output_filename_selection = input("Do you want to choose a different filename? Y/N:")
                    match overwrite_output_filename_selection:
                        case 'Y' | 'y':
                            output_filename = input("Enter your desired output filename: ")
                        case 'N' | 'n':
                            selecting_output_filename = False
                play_the_game(output_filename)
            case 'quit':
                print('Goodbye')
                start_menu = False
            case _:
                print('Invalid input')

start()