from game import *
from util import *

playerAgents = list()

def item2list(item, freq):
    items = []
    for _ in range(freq):
        items.append(item)
    return items

class GameStateData(GameState):
    def generateSuccessor(self, playerNum, action):
        """ playerNum in range(3), action is cards_out """
        next_s = self.copy(GameStateData)
        player = playerAgents[playerNum]

        # print("With ", self.card_dic[player.getName()])
        # print(player.getName(),"try action", action)
        update_with_action(next_s, player, action)

        return next_s

    def getLegalActions(self, playerNum):
        """
        return leagal actoins concerning active carding or not
        """
        actions = []
        priority = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, '10':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, "x":13, "X":14}
        # not your turn
        # if self.whose_turn != playerNum+1:
        #     return []
        player = playerAgents[playerNum]

        # Collect legal moves and successor states
        all_choices = get_legal_choices(self.card_dic[player.getName()])
        # print(all_choices)

        # if passive, the only available type is the last person
        if (player.getName()!=self.last_turn):

            last_cards = self.cards_out
            last_min = self.cards_out[0]
            if  is_wangzha(last_cards):
                return []
    
            def passive_type():
                if is_danzhang(last_cards) :
                    return 1
                if is_duizi(last_cards) :
                    return 2
                if is_sanzhang(last_cards) :
                    return 3
                if is_shunzi(last_cards):         
                    return 4
                if is_liandui(last_cards):          
                    return 5
                if is_feiji(last_cards):         
                    return 6
                if is_sandaiyi(last_cards):  
                    return 7
                if is_sandaier(last_cards):  
                    return 8
                if is_bomb(last_cards):         
                    return 9
            available_type = passive_type()
            if all_choices[available_type]==[]:
                return []

            for item in all_choices[available_type]:
                # 1/2/3 same
                if available_type in [1, 2, 3]:
                    if priority[item] > priority [last_min]:
                        cards = item2list(item, available_type)
                        actions.append(cards)
                # bomb
                elif available_type == 9:
                    if priority[item] > priority [last_min]:
                        cards = item2list(item, 4)
                        actions.append(cards)
                elif priority[item[0]] > priority[last_min]:
                    actions.append(item)


        
        else:
            # passive carding
            singles=list(set(all_choices[1]))
            for item in singles:
                singles.append([item])
                singles.remove(item)
            
            # the avialable types of your cards_out
            available_types = [i for i in range(10)]

            # merge all available action
            for i in available_types:
                if all_choices[i]!=[]:
                    if i in [1,2,3]:
                        for item in all_choices[i]:
                            actions.append(item2list(item, i))
                    else:
                        actions.extend(all_choices[i])

        # print("legalMoves for %s: "%self.players[playerNum], actions)
        
        return actions
