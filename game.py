import random as R
import os, sys, time, copy
from HumanAgent import Agent, HumanAgent
from AIagent import AI_agent
from util import raiseNotDefined

####################
# 顺牌
def card_sort(m_card_list):
    """ sort the cards from 3~ K~ X """
    card_value_dic = { '3':0,'4':1,'5':2,'6':3,'7':4,'8':5,'9':6,'10':7,'J':8,'Q':9,'K':10,'A':11,'2':12, "x":13, "X":14 }
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
    
class GameState:
    def __init__(self, player1, player2, player3):
        # GameState attributes 
        # print("……………………………initializing……………………………")
        """ 
        P1: the AI_agent
        P2, P3: the humanAgent 
        """
        self.players = [player1, player2, player3]
        self.whose_turn=1 # current_turn

        # updated by the player class
        self.last_turn="Mr Master"
        self.cards_out=None # cards of the last turn

        self.card_dic={}
        self.colored_card_dic={}
        self.winner = None
        
    def begin(self, player1, player2, player3):
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

            card_dic = {player1: m_list[0], player2: m_list[1], player3: m_list[2], "base_cards":kings}
            
            return card_dic
        ##################################################### end of function
        self.card_dic=random_card(player1, player2, player3)
        ##################
        #叫地主
        print("Mr Master is the landlord. The landlord's card are: ", self.card_dic["base_cards"])
        self.card_dic[player1].extend(self.card_dic["base_cards"])
        card_sort(self.card_dic[player1])
        del self.card_dic["base_cards"]
        self.colored_card_dic=copy.deepcopy(self.card_dic)

        #delete the huase in `card_dic`
        for i in self.card_dic.keys():
            for j in range(len(self.card_dic[i])):
                self.card_dic[i][j]=self.card_dic[i][j][self.card_dic[i][j].find(" ")+1:]
        print("card_dic:", self.card_dic)
        print("colored_card_dic:", self.colored_card_dic)
        print("let's begin the game.")

    def copy(self, stateClass):
        p1, p2, p3 = self.players
        state = stateClass(p1,p2,p3)

        state.whose_turn = self.whose_turn
        state.last_turn = self.last_turn
        state.players = self.players.copy()
        state.cards_out = self.cards_out

        

        state.card_dic = copy.deepcopy(self.card_dic)
        state.colored_card_dic = copy.deepcopy(self.colored_card_dic)
        state.winner = self.winner

        return state

    def next_turn(self):
        """ return the next player number """
        if self.whose_turn == 3:
            return 1
        else:
            return (self.whose_turn + 1)

    def farmerWin(self):
        for key in self.players[1:]:
            if len(self.colored_card_dic[key]) == 0:
                return True
        return False

    def lordWin(self):
        return len(self.colored_card_dic['Mr Master'])==0
    ##################
    # 看牌
    # 输入是玩家名称和card_dic，print出玩家手中的牌
    def see_card(self, playerID):
        if playerID not in self.card_dic.keys():
            print("Wrong user name, please type in again: ")
        else:
            card_sort(self.colored_card_dic[playerID])
            print("………………………let's…see…cards…………………………………")
            print("Here are cards for %s:"%playerID, self.card_dic[playerID])
            print("The numbre of remaining cards:")
            for player in self.card_dic.keys():
                print("%s: "%player, len(self.card_dic[player]))

    def update_cards_and_turn(self, playerID, newcards):
        """ internally update the cards of certain player in the current gamestate
        do **nothing** if no such player exists
        """
        if playerID not in self.card_dic.keys():
            return
        else:
            self.card_dic[playerID] = newcards
        self.whose_turn = self.next_turn()
        # print("updated! next_turen: ", self.whose_turn)

    
    def finish(self, P1, P2, P3):
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
    
    def getLegalActions(self, playerNum):
        raiseNotDefined()
    def generateSuccessor(self, playerNum, action):
        raiseNotDefined()

#更新card_dic
def update(state, player):
    """ 
    update the current gamestate after one player hand some cards out.
    """
    print("………………choose…your…cards…out………………………")
    remaining_cards = player.takeAction(state)
    state.update_cards_and_turn(player.getName(), remaining_cards)

    os.system( 'pause' )

#更新card_dic
def update_with_action(state, player, action):
    """ 
    update the one gamestate after one player hand some cards out.
    """
    remaining_cards = player.takeCertainAction(state, action)
    state.update_cards_and_turn(player, remaining_cards)
