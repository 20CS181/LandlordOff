from gameData import *
# from game import *
from SearchAgent import *
from MultiAgent import *
from HumanAgent import HumanAgent

# main process:
###############################################################################
#type in the user name
player1 = "Mr Master"
print("Hi, this is "+player1+". Are you ready to play with me?")
os.system( 'pause' )
print("Now please create your name!")
player2 = input("Your are player 1, please type in your player name: ")
player3 = input("Your are player 2, please type in your player name: ")

# init three players
game=GameStateData(player1, player2, player3)
game.begin(player1, player2, player3)
card_dic = game.Card_dic()
P1 = MinimaxAgent(player1, card_dic[player1], True)
P2 = AI_agent(player2, card_dic[player2], False)
P3 = AI_agent(player3, card_dic[player3], False)
playerAgents.extend([P1, P2, P3])

""" 
play the game, whose_turn indicates the player to play:
"""
# Mr. Master goes first
update(game, P1)
os.system('cls')
# game.whose_turn=2

while game.finish(P1, P2, P3) !=True:
    print("card_dic:", game.card_dic)
    print("colored_card_dic:", game.colored_card_dic)
    print("P1: ", P1.cards)
    print("P2: ", P2.cards)
    print("P3: ", P3.cards)
    if game.whose_turn == 1:

        print(player1 + "!\nIs your turn to release cards.")
        os.system( 'pause' )
        if (game.last_turn==player1):
            print("last_turn is you and you put out:", game.cards_out)
        else:
            print("last_turn is %s and puts out:"%(game.last_turn), game.cards_out)
        # game.see_card(player1)
        update(game, P1)
        os.system('cls')

    elif game.whose_turn == 2:

        print(player2 + "!\nIs your turn to release cards.")
        os.system( 'pause' )
        if (game.last_turn==player2):
            print("last_turn is you and you put out:", game.cards_out)
        else:
            print("last_turn is %s and puts out:"%(game.last_turn), game.cards_out)
        game.see_card(player2)
        update(game, P2)
        os.system('cls')

    else:
        print(player3 + "!\nIs your turn to release cards.")
        os.system( 'pause' )
        if (game.last_turn==player3):
            print("last_turn is you and you put out:", game.cards_out)
        else:
            print("last_turn is %s and puts out:"%(game.last_turn), game.cards_out)
        game.see_card(player3)
        update(game, P3)
        os.system('cls')


winner = game.Winner()
if winner == "Mr Master":
    print("The landlord wins!")
else:
    print("The landlord has been defeated.\ncongratulations!!")