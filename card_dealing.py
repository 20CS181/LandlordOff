import random as R
import sys
import time
import os

#from game import*


class Game:
    ###################
    #分牌
    #输入是玩家的名称，输出是一个dic
    def random_card(player1, player2, player3):
        L = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', ' 10', ' J', ' Q', ' K']
        H = ['\u2660', '\u2663', '\u2665', '\u2666']

        P = [' X',' x']
        for x in H:
            for y in L:
                s = x + y
                P.append(s)

        R.shuffle(P)
        m_list = [[],[],[]]

        for i in range(3):
            m_list[i] = R.sample(P, 17)
            for x in m_list[i]:
                P.pop(P.index(x))

        card_dic = {player1:m_list[0],player2:m_list[1],player3:m_list[2],"base_cards":P}
        return card_dic

    ####################
    #顺牌
    def card_sort(m_card_list):
        card_value_dic = {'3':0,'4':1,'5':2,'6':3,'7':4,'8':5,'9':6,'10':7,'J':8,'Q':9,'K':10,'A':11,'2':12, " x":13, " X":14}
        def find_in_dic(ele):
            if ele == " X" or ele == " x":
                return card_value_dic[ele]
            else:
                a = ele[2:]
                return card_value_dic[a]
        m_carpyd_list.sort(key = find_in_dic)
        # print("hhhhhhh",m_card_list)

    ##################
    #看牌
    #输入是玩家名称和card_dic，print出玩家手中的牌
    def see_card(playerID,card_dic)
        if playerID not in card_dic.keys():
            print("Wrong user name, please type in again: ")
        else:
            card_sort(card_dic[playerID])
            print(card_dic[playerID])
            os.system( 'pause' )
            os.system('cls')
        
    ####################
    #出牌
    def release_card(playerID):

    ###############################################################################
    # main process:
    
    #type in the user name
    player1 = "Mr Master"
    print("Hi, this is "+player1+". Are you ready to play with me?")
    os.system( 'pause' )
    print("Now please create your name!")
    player2 = input("Your are player 1, please type in your player name: ")
    player3 = input("Your are player 2, please type in your player name: ")

    #################
    #洗牌
    card_dic = random_card(player1,player2,player3)

    ##################
    #叫地主
    print("Mr Master is the landlord. The landlord's card are: ",card_dic["base_cards"])
    print("let's begin the game.")
    card_dic[player1].extend(card_dic["base_cards"])


    print(player1+"! Is your turn to release cards.")





