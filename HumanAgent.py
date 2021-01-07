from collections import Counter
from util import raiseNotDefined

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, name, cards, isLord):
        self.name = name
        self.cards = cards
        self.isLord = isLord

    def getName(self):
        return self.name

    def isWinner(self):
        return True if self.cards==[] else False

    def takeAction(self, state):
        """
        The Agent will receive a GameState,
        it must take an action 
        and return the remaining cards
        """
        raiseNotDefined()
    
    def getAction(self, state):
        raiseNotDefined()


class HumanAgent(Agent):
    def takeAction(self, state):
        # active
        # to make sure you have the cards you hand out
        while True:
            choice = input("player %s: \nplease enter your card choices in ONE LINE:"%(self.name))
            cards_out = choice.split()
            # if pass
            if cards_out == []:
                return self.cards
            if cards_out == ['x', 'X']:
                break

            # check if input valid
            # if not, recurse
            cur_cards = self.cards.copy()
            print("Your choice: ", cards_out)

            # check if the chosen cards exist
            for card_out in cards_out:
                find = False
                for card in cur_cards :
                    if (card[1:] == card_out) or (card == card_out):
                        cur_cards.remove(card)
                        find = True
                        break
                if not find:
                    print("invalid card choice!! no card `%s` available!! Please enter again!!"%card_out) 
                    print("available cards: ", state.colored_card_dic[self.name])
                    break

            # check if the action is leagal
            # legal = True
            is_active = state.last_turn==self.name
            legal = self.checkAction(state.cards_out, cards_out, is_active)
            if not legal:
                print("invalid card choice!! make sure you follow the rules!!") 
                last_turn = "you" if(state.last_turn==self.name)else state.last_turn
                print("In last turn, %s puts out \n"%(last_turn), (state.cards_out))
            
            if find and legal:
                state.cards_out=cards_out

                #remove the cards in huase
                for card_out in cards_out:
                    for card in state.colored_card_dic[self.name]:
                        if card[-1] == card_out[-1]:
                            state.colored_card_dic[self.name].remove(card)
                            break

                #print("this round player %s take out"%(self.name),cards_out)
                state.last_turn=self.name
                self.cards = cur_cards
                return self.cards

    def checkAction(self, last_cards, my_cards, is_active):
        """ given `last_cards` from the other, check if `my_cards` are leagal 
        first try to find a legal format,
        if failed, return False. """
        # wang_zha
        if last_cards==['x', 'X']: return False
        if my_cards==['x', 'X']: return True

        
        # others: 10 -> 0
        priority = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, '0':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, "x":13, "X":14}
        def find_prior(ele):
            return priority[ele]

        cards_last=[card[-1] for card in last_cards]
        cards_last.sort(key=find_prior)
        cards_mine=[card[-1] for card in my_cards]
        cards_mine.sort(key=find_prior)
        # print("before set, cards_mine:", cards_mine, "\ncards_last: ", cards_last)

        
        # func=[dan_pai,two,three,three_plus_one, three_plus_two, dan_lian, er_lian,san_lian]
        otherCardsCounter = Counter() 
        for card in cards_last:
            otherCardsCounter[card]+=1

        myCardsCounter = Counter()
        for card in cards_mine:
            myCardsCounter[card]+=1

        # bomb
        if len(cards_mine)==4:
            if myCardsCounter.most_common(1)[0][1]==4:
                return not(cards_mine==['x', 'X']) and \
                 not(len(cards_last)==4 and otherCardsCounter.most_common(1)[0][1]==4 and priority[cards_mine[0]] < priority[cards_last[0]])
        
        # dan_pai
        if len(cards_mine)==1:
            # act freely as long as following the rule
            if is_active: 
                return True
            # follow the previous player, same bellow
            elif len(cards_last)==1 and priority[cards_mine[0]] > priority[cards_last[0]]: 
                return True
            else: 
                return False
        
        # two same
        if len(cards_mine)==2:
            if (cards_mine[0]==cards_mine[1]):
                if is_active: 
                    return True
                elif len(cards_last)==2 and (cards_last[0]==cards_last[1]) and priority[cards_mine[0]] > priority[cards_last[0]]: 
                    return True
                else: 
                    return False

        # three same
        if len(cards_mine)==3:
            if (cards_mine[0]==cards_mine[1]==cards_mine[2]):
                if is_active: 
                    return True
                elif len(cards_last)==3 and (cards_last[0]==cards_last[1]==cards_last[2]) and priority[cards_mine[0]] > priority[cards_last[0]]: 
                    return True
                else: 
                    return False


        # three_plus_one
        my_most_card = myCardsCounter.most_common(1)[0][0]
        if myCardsCounter[my_most_card]==3:
            if len(cards_mine)==4:
                if is_active: 
                    return True
                elif len(cards_last)==4 and (otherCardsCounter.most_common(1)[0][1]==3):
                    my_three = my_most_card
                    other_three = otherCardsCounter.most_common(1)[0][0]
                    return True if priority[my_three] > priority[other_three] else False 
                else: 
                    return False

            # three_plus_two
            if len(cards_mine)==5:
                myCardsCounter[my_most_card]=0
                my_least_card = myCardsCounter.most_common(1)[0][0]
                if myCardsCounter[my_least_card]!=2:
                    return False
                elif is_active: 
                    return True
                elif len(cards_last)==5 and (otherCardsCounter.most_common(1)[0][1]==3):
                    my_three=my_most_card
                    other_three = otherCardsCounter.most_common(1)[0][0]
                    return True if priority[my_three] > priority[other_three] else False 
                else: 
                    return False

        # lian shun_zi
        # remove redundency
        same_frequent = myCardsCounter.most_common(1)[0][1]
        if same_frequent == 1: return True
        for key in myCardsCounter.keys():
            if myCardsCounter[key]!=same_frequent:
                return False
        cards_mine=list(set(cards_mine))
        # dan_lian, er_lian, san_lian
        # for i in range(len(cards_mine)-1):
            # if (priority[cards_mine[i+1]]!=priority[cards_mine[i]]+1):
                # return False
        
        print ("nice!\nyou put `shun_zi`!")
        # return True
        if is_active:
            return True
        else:
            # other is shunzi with same length, same freq
            other_freq = otherCardsCounter.most_common(1)[0][1]
            for key in otherCardsCounter.keys():
                if otherCardsCounter[key]!=other_freq:
                    return False # last is not shunzi
                if other_freq!=same_frequent: return False # diff freq
                
            # same length 
            cards_last = list(set(cards_last))
            if len(cards_last)!=len(cards_mine): return False # diff len
            # print("cards_mine:", cards_mine, "\ncards_last: ", cards_last)
            
            return True

        #     if all([ (priority[cards_last[i+1]]==priority[cards_last[i]]+1) for i in range(len(cards_mine)-1)]) \
        #          and priority[cards_mine[0]] > priority[cards_last[0]]:
        #         return True
        # # invalid format
        # return False






