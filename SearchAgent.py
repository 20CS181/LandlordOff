from collections import Counter
from AIagent import *
from util import *
import copy
import random

class OneChoice:
    """
    One possible choice.
    a partition of a series of card types
    use a dictionary and a list to represent the card partitions and each num
    """
    def __init__(self):
        # 0~9:10 num_of_type
        """
        self.num_of_wangzha=0   # 0
        self.num_of_danzhang=0  # 1
        self.num_of_duizi=0     # 2
        self.num_of_sanzhang=0  # 3
        self.num_of_shunzi=0    # 4: dan_lian
        self.num_of_liandui=0   # 5: er_lian
        self.num_of_feiji=0     # 6: san_lian
        self.num_of_san_dai_yi=0# 7: 3+1
        self.num_of_san_dai_er=0# 8: 3+2
        self.num_of_bomb=0      # 9
        """
        self.list_num_of_types = [0, 0, 0, 0, 0, 0, 0, 0, 0,0]

        # 0~9: 10 list_of_type
        """
        self.list_of_wangzha=[] # 0
        self.list_of_danzhang=[]# 1
        self.list_of_duizi=[]   # 2
        self.list_of_sanzhang=[]# 3
        self.list_of_shunzi=[]  # 4
        self.list_of_liandui=[] # 5
        self.list_of_feiji=[]   # 6
        self.list_of_3_plus_1=[]# 7
        self.list_of_3_plus_2=[]# 8
        self.list_of_bomb=[]    # 9 
        """
        self.dic_list_of_types = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}

        # other attributes
        self.total_times=0 # total num of card choices
        self.value=0  # choose the action with largest remaining value
    
    def getTypesDic(self):
        """
        return  the deepcopy of the current type dictionary
        """
        return copy.deepcopy(self.dic_list_of_types)

    def update_types_with_dic(self, dic_of_type_list):
        """
        update `self.list_num_of_types`, `self.dic_list_of_types`
        they are changed only here
        """
        self.dic_list_of_types = dic_of_type_list
        for i in range(10):
            self.list_num_of_types[i] = len(self.dic_list_of_types[i])


# recursively 
def get_one_step_value(cards):
    #cards=pai_to_number(cards) # if need
    cards.sort()
    if is_danzhang(cards):
        cards=pai_to_number(cards)
        return cards[-1]  
    if is_duizi(cards):
        cards=pai_to_number(cards)
        return cards[-1]  
    if is_sanzhang(cards):
        cards=pai_to_number(cards)
        return cards[-1]
    if is_shunzi(cards):
        cards=pai_to_number(cards)
        return cards[-1]+1
    if is_liandui(cards):
        cards=pai_to_number(cards)
        return cards[-1]+1
    if is_feiji(cards):
        cards=pai_to_number(cards)
        return (cards[-1]+8)//2
    if is_sandaiyi(cards):
        cards=pai_to_number(cards)
        if cards[0]==cards[1]:
          return cards[0]+7
        else: 
          return cards[-1]+7
    if is_sandaier(cards):
        cards=pai_to_number(cards)
        if cards[0]==cards[2]:
          return cards[0]+7
        else: 
          return cards[-1]+7
    if is_bomb(cards):
        cards=pai_to_number(cards)
        return cards[-1]+14
    if is_wangzha(cards):
        return 30 
    return 0


def copy_OneChoice(choice):
    copy_choice = OneChoice()
    # updtae dic and list
    copy_choice.update_types_with_dic(choice.getTypesDic())
    # update other two attributes
    copy_choice.total_times = choice.total_times
    copy_choice.value = choice.value

    return copy_choice


def get_value(cards, possible_choices_list):
    """
    input: list of cards,  
    output:value 
    """
    flag=True
    possible_choices=[]
    all_possible_dic = get_legal_choices(cards)
    #print("all:",all_possible_dic)
    order=[4,5,6,7,8,2,3,1,9]
    for card_type in order:#all_possible_dic.keys():
        for cards_out in all_possible_dic[card_type]:
            # make 2 copies
            # card = deepcopy of cards
            if card_type==2:
                cards_out=[cards_out,cards_out]
            if card_type==3:
                cards_out=[cards_out,cards_out,cards_out]
            if type(cards_out)==str:
                l=[]
                l.append(cards_out)
                cards_out=l
            card = copy.deepcopy(cards)
            #print("before",card)
            #print("cards_out",cards_out)
            for one_card in cards_out:
               card.remove(one_card)
            # choices_list = deepcopy of possible_choices_list
            choices_list = []
            for i in possible_choices_list:
                choices_list.append(copy_OneChoice(i))
            # first turn
            if possible_choices_list == []:
                ch = OneChoice()
                ch.list_num_of_types[card_type]=1
                ch.dic_list_of_types[card_type].append(cards_out)
                ch.total_times = 1
                ch.value = get_one_step_value(cards_out)

                choices_list.append(ch)
            else:   
            # traverse choices_list
                for possible_choice in choices_list:
                    possible_choice.list_num_of_types[card_type]=possible_choice.list_num_of_types[card_type]+1
                    possible_choice.dic_list_of_types[card_type].append(cards_out)
                    possible_choice.value=possible_choice.value+get_one_step_value(cards_out)
                    possible_choice.total_times=possible_choice.total_times+1
                    if  possible_choice.total_times>2: return []
            if card !=[]:# and flag: 
                possible_choices=choices_list+get_value(card,choices_list)
    return  possible_choices

def get_tvTuple_from_list(possible_choice_list):
    # min times
    times = 20
    for choice in possible_choice_list:
        if choice.total_times < times:
            times = choice.total_times
    mint_list = []
    for choice in possible_choice_list:
        if choice.total_times == times:
            mint_list.append(choice)
    # max value
    value = 0
    for choice in mint_list:
        if choice.value > value:
            value = choice.value
    return (times, value)

        
class SearchAgent(AI_agent):
    def get_action(self, gamestate):
        """ judge the cards of others
        imput `choice`: class `OneChoice` of my current cards

        for active: random choose an available one
        for passive: try to follow the others under the rule
        if quit, return None.

        use `choices`: class `OneChoice`
        after kicking off the `cards_out`,
        we want the remaining as a `choice` with the largest value
        """
        '''def wang_zha():
            return (self.other_cards == ['x', 'X'])

        # 单牌
        def dan_pai():
            return len(self.other_cards)==1
        # duizi
        def two():
            if len(self.other_cards)==2:
                return self.other_cards[0]==self.other_cards[1]
            return False
        # three same
        def three():
            if len(self.other_cards)==3:
                return self.other_cards[0]==self.other_cards[1]==self.other_cards[2]
            return False
        # 3,4,5,...
        def dan_lian():
            other_cards=pai_to_number(self.other_cards)
            other_cards.sort()
            if all([other_cards[i]+1 == other_cards[i+1] for i in range(len(other_cards)-1)]) :
                choices=self.possible_choice[4]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==len(other_cards) and len(choices)>2 :
                        choices[i]=pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >other_cards[0] :
                            act=choices[i]
                            act=number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                            
                            return act
                return None
        #33,44,55,...
        def er_lian():
            other_cards=pai_to_number(self.other_cards)
            other_cards.sort()
            length_other=len(other_cards)
            #每个值频率为2
            if length_other <6 :return None
            dict = {}
            for key in other_cards:
                dict[key] = dict.get(key, 0) + 1
            a=[]
            a=dict.values()
            for i in range(len(a)):
                if a[i]!=2 :
                    return None

            #去重，再排序
            sorted(set(other_cards), key = other_cards.index)
            if all([other_cards[i]+1 == other_cards[i+1] for i in range(len(other_cards)-1)]) :
                choices=self.possible_choice[5]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==length_other and len(choices)>4 :
                        choices[i]=pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >other_cards[0] :
                            act=choices[i]
                            act=number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                                    
                            return act
                return None
        #333,444,555,...
        def san_lian():
            other_cards=pai_to_number(self.other_cards)
            other_cards.sort()
            length_other=len(other_cards)
            if length_other <6 :return None
            # 每个值频率为3
            dict = {}
            for key in other_cards:
                dict[key] = dict.get(key, 0) + 1
            a=[]
            a=dict.values()
            for i in range(len(a)):
                if a[i]!=3 :
                    return None

            #去重，再排序
            sorted(set(other_cards), key = other_cards.index)
            if all([other_cards[i]+1 == other_cards[i+1] for i in range(len(other_cards)-1)]) :
                choices=self.possible_choice[6]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==length_other and len(choices)>3 :
                        choices[i]=pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >other_cards[0] :
                            act=choices[i]
                            act=number_to_pai(act)

                            #delete
                            for j in range(len(act)) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            
                            return act
                return None
        
        def bomb():
            if len(self.other_cards)==4:
                return all(item ==self.other_cards[0] for item in self.other_cards)
            return False'''
        def wang_zha():
            return (self.other_cards == ['x', 'X'])

        # 单牌
        def dan_pai():
            if  len(self.other_cards)==1:
                choices=self.possible_choice[1] 
                if choices==[]:return None
                
                choices=pai_to_number(choices)

                if self.other_cards != [-1]:
                   other_cards=pai_to_number(self.other_cards)
                else:
                   other_cards=[-1]
                choices.sort()
                for i in range(len(choices)):
                    if choices[i] > other_cards[0] :
                        choices=number_to_pai(choices)
                        act=[choices[i]]
                        #delete
                        self.mycards.remove(choices[i])
                        self.possible_choice=get_legal_choices(self.mycards)
                        return act
                return None
        # duizi
        def two():
            if len(self.other_cards)==2:
                if self.other_cards[0]==self.other_cards[1]:
                    choices=self.possible_choice[2]
                    if choices==[]:return None
                    
                    choices=pai_to_number(choices)
                    other_cards=pai_to_number(self.other_cards)
                    choices.sort()
                    for i in range(len(choices)):
                        if choices[i] > other_cards[0] :
                            choices=number_to_pai(choices)
                            act=[choices[i],choices[i]]
                            #delete
                            for j in range(2) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                            return act
                    return None
        # three same
        def three():
            if len(self.other_cards)==3:
                if self.other_cards[0]==self.other_cards[1] and self.other_cards[0]==self.other_cards[2]:
                    choices=self.possible_choice[3]
                    if choices==[]:return None
                    
                    choices=pai_to_number(choices)
                    other_cards=pai_to_number(self.other_cards)
                    choices.sort()
                    for i in range(len(choices)):
                        if choices[i] > other_cards[0] :
                            choices=number_to_pai(choices)
                            act=[choices[i],choices[i],choices[i]]
                            for j in range(3) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                            return act
                    return None
                
        # 3,4,5,...
        def dan_lian():
            other_cards=pai_to_number(self.other_cards)
            other_cards.sort()
            if all([other_cards[i]+1 == other_cards[i+1] for i in range(len(other_cards)-1)]) :
                choices=self.possible_choice[4]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==len(other_cards) and len(choices)>2 :
                        choices[i]=pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >other_cards[0] :
                            act=choices[i]
                            act=number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                            
                            return act
                return None

        #33,44,55,...
        def er_lian():
            other_cards=pai_to_number(self.other_cards)
            other_cards.sort()
            length_other=len(other_cards)
            #每个值频率为2
            if length_other <6 :return None
            dic = {}
            for key in other_cards:
                dic[key] = dic.get(key, 0) + 1
           
            for i in dic.values():
                if i!=2 :
                    return None

            #去重，再排序
            sorted(set(other_cards), key = other_cards.index)
            if all([other_cards[i]+1 == other_cards[i+1] for i in range(len(other_cards)-1)]) :
                choices=self.possible_choice[5]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==length_other and len(choices)>4 :
                        choices[i]=pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >other_cards[0] :
                            act=choices[i]
                            act=number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                                    
                            return act
                return None

        #333,444,555,...
        def san_lian():
            other_cards=pai_to_number(self.other_cards)
            other_cards.sort()
            length_other=len(other_cards)
            if length_other <6 :return None
            #每个值频率为3
            dict = {}
            for key in other_cards:
                dict[key] = dict.get(key, 0) + 1
            a=[]
            a=dict.values()
            for i in range(len(a)):
                if a[i]!=3 :
                    return None

            #去重，再排序
            sorted(set(other_cards), key = other_cards.index)
            if all([other_cards[i]+1 == other_cards[i+1] for i in range(len(other_cards)-1)]) :
                choices=self.possible_choice[6]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==length_other and len(choices)>3 :
                        choices[i]=pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >other_cards[0] :
                            act=choices[i]
                            act=number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            
                            return act
                return None
        
        # 3+1
        def three_plus_one():
            if len(self.other_cards)==4:
                other_cards=pai_to_number(self.other_cards)
                #出现频率最高的一个数的频率为3
                if  Counter(other_cards).most_common(1)[0][1]==3 :
                    choices=self.possible_choice[7]
                    if choices==[]:return None

                    for i in range(len(choices)):
                        choices[i]=pai_to_number(choices[i])
                        three=Counter(choices[i]).most_common(1)[0][0]
                        if three > Counter(other_cards).most_common(1)[0][0] :
                            choices[i]=number_to_pai(choices[i])
                            act=choices[i]
                            #delete
                            for j in range(4) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            return act
                    return None
        
        # 3+2
        def three_plus_two():
            if len(self.other_cards)==5:
                other_cards=pai_to_number(self.other_cards)
                #出现频率最高的一个数的频率为3，次高为2
                max_f=Counter(other_cards).most_common(1)[0][1]
                most_number=Counter(other_cards).most_common(1)[0][0]
                while most_number in other_cards:
                    other_cards.remove(most_number)
                min_f=Counter(other_cards).most_common(1)[0][1]
                if  max_f==3 and min_f==2 :
                    choices=self.possible_choice[8]
                    if choices==[]:return None

                    for i in range(len(choices)):
                        choices[i]=pai_to_number(choices[i])
                        three=Counter(choices[i]).most_common(1)[0][0]
                        if three > most_number :
                            choices[i]=number_to_pai(choices[i])
                            act=choices[i]
                            #delete
                            for j in range(5) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            return act
                    return None

        
        def bomb():
            if len(self.other_cards)==4:
                if all(item ==self.other_cards[0] for item in self.other_cards):
                    choices=self.possible_choice[9]
                    if choices==[]:return None
                    
                    choices=pai_to_number(choices)
                    other_cards=pai_to_number(self.other_cards)
                    choices.sort()
                    for i in range(len(choices)):
                        if choices[i] > other_cards[0] :
                            choices=number_to_pai(choices)
                            act=[choices[i],choices[i],choices[i],choices[i]]
                            #delete
                            for j in range(4) :
                                self.mycards.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            return act
                    return None

        # the avialable types of your cards_out
        available_types =[4,5,6,7,8,2,3,1,9]  # [i for i in range(10)]
       
    

        # if passive, the only available type is the last person
        if (self.name!=gamestate.last_turn):
            '''
            if  wang_zha():                        return None
            def passive_type():
                if is_danzhang(self.other_cards) :                     return [1]
                if is_duizi(self.other_cards):                         return [2]
                if is_sanzhang(self.other_cards):                      return [3]
                if is_shunzi(self.other_cards):                        return [4]
                if is_liandui(self.other_cards):                       return [5]
                if is_feiji(self.other_cards):                         return [6]
                if is_sandaiyi(self.other_cards):           return [7]
                if is_sandaier(self.other_cards):           return [8]
                if bomb():                                  return [9]
                return None
            available_types = passive_type()'''
            if  wang_zha(): return None
            
            we_action=dan_pai()
            if  we_action is not None: return we_action
            
            we_action=two()
            if  we_action is not None: return we_action
            
            we_action=three()
            if  we_action is not None: return we_action
            
            we_action=dan_lian()
            if  we_action is not None: return we_action
            
            we_action=er_lian()
            if  we_action is not None: return we_action
            
            we_action=san_lian()
            if  we_action is not None: return we_action
            
            we_action=three_plus_one()
            if  we_action is not None: return we_action
            
            we_action=three_plus_two()
            if  we_action is not None: return we_action
            
            we_action=bomb()
            if  we_action is not None: return we_action
            return None
        
        # traverse all actions and compute the remaining value
        tv_pairs = []          # (action, remain_min_times, remain_max_value)
        for i in available_types:
            # i: index
            if len(self.possible_choice[i])!=0:
                
                for action in self.possible_choice[i]:
                    # the remaining
                    #if action[0]=='1':
                    #    action=[action]
                    if i==2:
                        action=[action,action]
                    if i==3:
                        action=[action,action,action]
                    #print("action",action)
                    rem_cards = copy.deepcopy(self.cards)
                    if type(action) is list:
                        for one_card in action:
                           rem_cards.remove(one_card)
                    else:
                        rem_cards.remove(action)
                    
                    tep=get_value(rem_cards, [])
                    min_times, max_value = get_tvTuple_from_list(tep)
                    #print("Here",min_times,max_value)
                    #input("stop")
                   
                    tv_pair = (action, min_times, max_value)
                    tv_pairs.append(tv_pair)
        # return the action
        # min times
        times = 20
        for atv in tv_pairs:
            if  atv[1] < times:
                times =  atv[1]
        mint_list = []
        for atv in tv_pairs:
            if  atv[1] == times:
                mint_list.append(atv)
        # max value
        value = 0
        for atv in mint_list:
            if atv[2] > value:
                value = atv[2]
        for atv in mint_list:
            if atv[2] == value:
                if type(atv[0]) is list:
                    for one_card in atv[0]:
                        self.mycards.remove(one_card)
                else:
                    self.mycards.remove(atv[0])
    
                return atv[0]


