import random as R
import os, sys, time, copy
from HumanAgent import Agent, HumanAgent
from AIagent import AI_agent

####################
# 顺牌
def card_sort(m_card_list):
    """ sort the cards from 3~ K~ X """
    card_value_dic = {'3':0,'4':1,'5':2,'6':3,'7':4,'8':5,'9':6,'10':7,'J':8,'Q':9,'K':10,'A':11,'2':12, "x":13, "X":14}
    def find_in_dic(ele):
        if ele[-1]=='0':
            ele="10"
        else:
            ele=ele[-1]
        if ele == "X" or ele == "x":
            return card_value_dic[ele]
        else:
            a = ele
            return card_value_dic[a]
    m_card_list.sort(key = find_in_dic)
    
class GameState():
    def __init__(self,player1,player2,player3):
        ###################
        # 分牌
        # 输入是玩家的名称，输出是一个dic    
        def random_card(player1, player2, player3):
            """ output a dictionary with sorted lists """
            numbers = [' A', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', ' 10', ' J', ' Q', ' K']
            colors = ['\u2660', '\u2663', '\u2665', '\u2666']
            kings = [' X',' x']

            # mix together
            for x in colors:
                for y in numbers:
                    s = x + y
                    kings.append(s)

            # shuffle
            R.shuffle(kings)
            m_list = [[],[],[]]

            # sample and sort 3 list and a base_cards
            for i in range(3):
                m_list[i] = R.sample(kings, 17)
                for x in m_list[i]:
                    kings.pop(kings.index(x))
                card_sort(m_list[i])
            card_sort(kings)

            card_dic = {player1:m_list[0], player2:m_list[1], player3:m_list[2], "base_cards":kings}
            
            return card_dic
        ##################################################### end of function
        # GameState attributes 
        """ 
        P1: the AI_agent
        P2, P3: the humanAgent 
        """
        self.whose_turn=1
        self.last_turn="Mr Master"
        self.is_active=True

        self.card_dic=random_card(player1, player2, player3)
        self.colored_card_dic=copy.deepcopy(self.card_dic)

        #delete the huase in `card_dic`
        for i in self.card_dic.keys():
            # self.colored_card_dic[i]=[]
            for j in range(len(self.card_dic[i])):
                # self.colored_card_dic[i].append(" ")
                self.card_dic[i][j]=self.card_dic[i][j][self.card_dic[i][j].find(" ")+1:]
        # self.card_dic, self.colored_card_dic = self.colored_card_dic, self.card_dic

        self.cards_out=None # cards of the current turn
        self.winner = None
        ##################
        #叫地主
        print("Mr Master is the landlord. The landlord's card are: ",self.colored_card_dic["base_cards"])
        print("let's begin the game.")
        self.card_dic[player1].extend(self.card_dic["base_cards"])
        self.colored_card_dic[player1].extend(self.colored_card_dic["base_cards"])


    ##################
    # 看牌
    # 输入是玩家名称和card_dic，print出玩家手中的牌
    def see_card(self, playerID):
        if playerID not in self.card_dic.keys():
            print("Wrong user name, please type in again: ")
        else:
            card_sort(self.colored_card_dic[playerID])
            print("Here are cards for %s:"%playerID, self.colored_card_dic[playerID])
            # os.system( 'pause' )
            #os.system('cls')

    def update_cards(self, playerID, newcards):
        """ internally update the cards of certain player in the current gamestate
        do **nothing** if no such player exists
        """
        if playerID not in self.card_dic.keys():
            return
        else:
            self.card_dic[playerID] = newcards
    
    def update_active(self, is_active):
        self.is_active = is_active

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

#更新card_dic
def update(state, player):
    """ 
    update the current gamestate after one player hand some cards out.
    """
    remaining_cards = player.takeAction(state)
    state.update_cards(player, remaining_cards)
    os.system( 'pause' )
