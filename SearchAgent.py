from collections import Counter
from AIagent import *
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


def is_danzhang(cards):
    flag=False
    if len(cards)==1:
        flag=True
    return flag
def is_duizi(cards):
    flag=False
    if len(cards)==2:
        if cards[0]==cards[1]:
            flag=True
    return flag 
def is_sanzhang(cards):
    flag=False
    if len(cards)==3:
        if cards[0]==cards[1] and cards[0]==cards[2]:
            flag=True
    return flag
def is_shunzi(cards):
    flag=False
    cards=pai_to_number(cards)
    cards.sort()
    if all([cards[i]+1 == cards[i+1] for i in range(len(cards)-1)]):
        flag=True
    return flag
def is_bomb(cards):
    flag=False
    if len(cards)==4:
        if all(item ==cards[0] for item in cards):
            flag=True
    return flag
def is_feiji(cards):
    #e.g., 333444, 555777
    flag=False
    cards=pai_to_number(cards)
    cards.sort()
    length=len(cards)
    if length !=6 :return flag
    #每个值频率为3
    dict = {}
    for key in cards:
        dict[key] = dict.get(key, 0) + 1
    a=[]
    a=dict.values()
    for i in range(len(a)):
        if a[i]!=3 :
            return flag

    flag=True
    return flag
def is_wangzha(cards):
    flag=False
    if len(cards)==2:
        if 'x' in cards and 'X' in cards:
            flag=True
    return flag
def is_liandui(cards):
    flag=False
    cards=pai_to_number(cards)
    cards.sort()
    length=len(cards)
    #每个值频率为2
    if length <6 : return flag
    dict = {}
    for key in cards:
        dict[key] = dict.get(key, 0) + 1
    a=[]
    a=dict.values()
    for i in range(len(a)):
        if a[i]!=2 :
            return flag
    #去重，再排序
    sorted(set(cards), key = cards.index)
    if all([cards[i]+1 == cards[i+1] for i in range(len(cards)-1)]) :
        flag=True

    return flag
def is_sandaiyi(cards):
    if len(cards)==4:
        other_cards=pai_to_number(cards)
        #出现频率最高的一个数的频率为3，次高为2
        max_f=Counter(other_cards).most_common(1)[0][1]
        return  max_f==3
    return False
def is_sandaier(cards):
    if len(cards)==5:
        other_cards=pai_to_number(cards)
        #出现频率最高的一个数的频率为3，次高为2
        max_f=Counter(other_cards).most_common(1)[0][1]
        most_number=Counter(other_cards).most_common(1)[0][0]
        while most_number in other_cards:
            other_cards.remove(most_number)
        min_f=Counter(other_cards).most_common(1)[0][1]
        return  max_f==3 and min_f==2
    return False

def find_duizi(mycards) :
    mycards= tranf_from_list_to_dic(mycards)
    for i in mycards.keys():
        if mycards[i]>1:
            return i
    return False
def find_sanzhang(mycards) :
    mycards= tranf_from_list_to_dic(mycards)
    for i in mycards.keys():
        if mycards[i]>2:
            return i
    return False
#1
def find_shunzi(mycards) :
    mycards= tranf_from_list_to_dic(mycards)
    count=0
    ans=[]
    t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    for j in t:
        if mycards[j]>0:
            count=count+1
            if count >=5:
                for i in range(count-4):
                    ans=ans.append(t[(t.index(j)-count+1+i):(t.index(j)+1)])           
        else:   count=0
    return ans

def find_bomb(mycards) :
    mycards= tranf_from_list_to_dic(mycards)
    for i in mycards.keys():
        if mycards[i]>3:
            return i
    return False

def find_feiji(mycards):
    if find_sanzhang(mycards) :
        ans=[]
        i=find_sanzhang(mycards)
        ans=[i,i,i]
        mycards.remove(i)
        if find_sanzhang(mycards) :
            j=find_sanzhang(mycards)
            return ans.append([j,j,j])
    return False

def find_wangzha(mycards):
    return (mycards==['x','X'])

#2
def find_liandui(mycards):
    count=0
    t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    ans=[]
    for j in t:
        if mycards[j]>1:
            count=count+1
            if count >=3:
                for i in range(count-2):
                    tep=t[(t.index(j)-count+1+i):(t.index(j)+1)]
                    ans=ans.append(tep+tep)
        else:  count=0          
    return ans

# recursively 
def get_one_step_value(cards):
    cards=pai_to_number(cards) # if need
    cards.sort()
    if is_danzhang(cards):
        return cards[-1]  
    if is_duizi(cards):
        return cards[-1]  
    if is_sanzhang(cards):
        return cards[-1]
    if is_shunzi(cards):
        return cards[-1]+1
    if is_liandui(cards):
        return cards[-1]+1
    if is_feiji(cards):
        return (cards[-1]+8)//2
    if is_sandaiyi(cards):
        if cards[0]==cards[1]:
          return cards[0]+7
        else: 
          return cards[-1]+7
    if is_sandaier(cards):
        if cards[0]==cards[2]:
          return cards[0]+7
        else: 
          return cards[-1]+7
    if is_bomb(cards):
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
    possible_choices=[]
    all_possible_dic = get_legal_choices(cards)
    
    for card_type in all_possible_dic.keys():
        for cards_out in all_possible_dic[card_type]:
            # make 2 copies
            # card = deepcopy of cards
            
            card = copy.deepcopy(cards)
            print("before",card)
            print("before",cards)
            for one_card in cards_out:
               card.remove(one_card)
            print("after",card)
            print("after",cards)
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
                    if  possible_choice.total_times>7: return []
            if card !=[]: 
                possible_choices=possible_choices+get_value(card,choices_list)
    return  possible_choices

def get_tvTuple_from_list(possible_choices_list):
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
        def wang_zha():
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
            return False

        # the avialable types of your cards_out
        available_types = [i for i in range(10)]

        # if passive, the only available type is the last person
        if (self.name!=gamestate.last_turn):
            if  wang_zha():                        return None
            def passive_type():
                if dan_pai() :                     return 1
                if two() :                         return 2
                if three() :                       return 3
                if dan_lian() is not None:         return 4
                if er_lian() is not None:          return 5
                if san_lian() is not None:         return 6
                if is_sandaiyi(self.other_cards):  return 7
                if is_sandaier(self.other_cards):  return 8
                if bomb():                         return 9
                return None
            available_types = passive_type()

        # traverse all actions and compute the remaining value
        tv_pairs = []          # (action, remain_min_times, remain_max_value)
        for i in available_types:
            # i: index
            if len(self.possible_choice[i])!=0:
                for action in self.possible_choice[i]:
                    # the remaining
                    rem_cards = copy.deepcopy(self.cards)
                    rem_cards.remove(action)
                   
                    min_times, max_value = get_tvTuple_from_list(get_value(rem_cards, []))
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
                return atv[0]


