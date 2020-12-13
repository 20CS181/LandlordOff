import random as R
import sys
import time
import os
from agent import*

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
    m_card_list.sort(key = find_in_dic)
    
class gamestate():
    def __init__(self,player1,player2,player3): 
        ###################
        #分牌
        #输入是玩家的名称，输出是一个dic    
        def random_card(player1,player2,player3):
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
         
        self.card_dic=random_card(player1,player2,player3)
        ##################
        #叫地主
        print("Mr Master is the landlord. The landlord's card are: ",self.card_dic["base_cards"])
        print("let's begin the game.")
        self.card_dic[player1].extend(self.card_dic["base_cards"])
        
        self.winner = None
    ##################
    #看牌
    #输入是玩家名称和card_dic，print出玩家手中的牌
    def see_card(self,playerID):
        if playerID not in self.card_dic.keys():
            print("Wrong user name, please type in again: ")
        else:
            card_sort(self.card_dic[playerID])
            print(self.card_dic[playerID])
            os.system( 'pause' )
            os.system('cls')

    def finish(self,P1,P2,P3):
        if P1.isWinner() == True:
            self.winner = P1.getName()
            return True
        if P2.isWinner() == True:
            self.winner = P2.getName()
            return True
        if P3.isWinner() == True:
            self.winner = P3.getName()
            return True
        return False

    #更新card_dic
    def update(self,num,P1,P2,P3):
        if num == 1:
            a = P1.takeAction(self)
            self.card_dic[P1.getName()] = a
        if num == 2:
            a = P2.takeAction(self)
            self.card_dic[P2.getName()] = a
        if num == 3:
            a = P3.takeAction(self)
            self.card_dic[P3.getName()] = a

    #返回谁是winner，返回玩家输入的名字
    def Winner(self):
        #地主获胜
        if self.winner:
            return self.winner
        else:
            return None

    #返回card_dic
    def Card_dic(self):
        return self.card_dic
# main process:
###############################################################################
#type in the user name
player1 = "Mr Master"
print("Hi, this is "+player1+". Are you ready to play with me?")
os.system( 'pause' )
print("Now please create your name!")
player2 = input("Your are player 1, please type in your player name: ")
player3 = input("Your are player 2, please type in your player name: ")

game=gamestate(player1,player2,player3)
card_dic = game.Card_dic()
P1 = AIagent(player1,card_dic[player1],True)
P2 = HumanAgent(player2,card_dic[player2],False)
P3 = HumanAgent(player3,card_dic[player2],False)

whose_turn = 1
while game.finish(P1,P2,P3) !=True:
    if whose_turn == 1:
        print(player1+"! Is your turn to release cards.")
        os.system( 'pause' )
        game.see_card(player1)
        game.update(1,P1,P2,P3)
        whose_turn = 2

    elif whose_turn == 2:
        print(player2+"! Is your turn to release cards.")
        os.system( 'pause' )
        game.see_card(player2)
        game.update(2,P1,P2,P3)
        whose_turn = 3
    
    else:
        print(player3+"! Is your turn to release cards.")
        os.system( 'pause' )
        game.see_card(player3)
        game.update(3,P1,P2,P3)
        whose_turn = 1

winner = game.Winner()
if winner == "Mr Master":
    print("The landlord wins!")
else:
    print("The landlord has been defeated. congratulations!")
