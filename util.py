"""
utils for Agents
"""
import time, os, traceback, sys, inspect
from collections import Counter

""" for `get_legal_choices` """
transf=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','A', '2', 'x','X']

def pai_to_number(pai):
    number=[]
    for i in pai:
        number.append(transf.index(i))
    return number
def number_to_pai(number):
    pai=[]
    for i in number:
        pai.append(transf[i])
    return pai
def tranf_from_list_to_dic(card_list): 
    d={}
    for i in transf:
        d[i]=card_list.count(i)
    return d
def tranf_from_dic_to_list(card_dic):
    l=[]
    for i in card_dic.keys():
        for _ in range(card_dic[i]):
           l.append(i)
    return l

def get_legal_choices(cards):
        """ 
        return a dictionary: {
            0:[wang_zha]
            1:[single cards]
            2:[two same]
            3:[three same]
            4:[dan_lian]
            5:[er_lian]
            6:[san_lian]
            7:[3+1]
            8:[3+2]
            9:[bomb]
        } 
        """
        possible_choice={}
       
        mycards= tranf_from_list_to_dic(cards)
        for i in range(10):
            possible_choice[i]=[]
        # maintain possible_choices
        # wang_zha
            #nothing need to be done

        # danpai
        for i in mycards.keys():
                   if mycards[i]>0:
                       possible_choice[1].append(i)
        # two same
        for i in mycards.keys():
                   if mycards[i]>1:
                       possible_choice[2].append(i)
        # three same
        for i in mycards.keys():
                   if mycards[i]>2:
                       possible_choice[3].append(i)

        # dan_lian
        count=0
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for j in t:
            if mycards[j]>0:
                count=count+1
                if count >=5:
                    for i in range(count-4):
                       possible_choice[4].append(t[(t.index(j)-count+1+i):(t.index(j)+1)])
            else:  count=0               
        # er_lian
        count=0
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for j in t:
            if mycards[j]>1:
                count=count+1
                if count >=3:
                    for i in range(count-2):
                       tep=t[(t.index(j)-count+1+i):(t.index(j)+1)]
                       possible_choice[5].append(tep+tep)
            else:  count=0
        # san_lian
        count=0
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for j in t:
            if mycards[j]>2:
                count=count+1
                if count >=2:
                    for i in range(count-1):
                       tep=t[(t.index(j)-count+1+i):(t.index(j)+1)]
                       possible_choice[6].append(tep+tep+tep)
            else:  count=0
        # three_plus_one
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','A', '2']
        for j in t:
            if mycards[j]>2:
                for i in mycards.keys():
                    if i != j and mycards[i]>0:
                        possible_choice[7].append([j, j, j, i])
        # three_plus_two
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','A', '2']
        for j in t:
            if mycards[j]>2:
                for i in mycards.keys():
                    if i != j and mycards[i]>1:
                        possible_choice[8].append([j, j, j, i, i])
        # bomb
        for i in mycards.keys():
                   if mycards[i]>3:
                       possible_choice[9].append(i)
        return possible_choice

""" for judge the card types """
def is_wangzha(cards):
    flag=False
    if len(cards)==2:
        if 'x' in cards and 'X' in cards:
            flag=True
    return flag
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
    #print(cards)
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
    dic = {}
    for key in cards:
        dic[key] = dic.get(key, 0) + 1

    for i in dic.values():
        if i!=3 :
            return flag
   
    flag=True
    return flag
def is_liandui(cards):
    flag=False
    cards=pai_to_number(cards)
    cards.sort()
    length=len(cards)
    #每个值频率为2
    if length <6 : return flag
    dic = {}
    for key in cards:
        dic[key] = cards.count(key)
    for i in dic.values():
        if i!=2 :
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


""" find list of all cards for certain card type """
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
    
######################## helper function ##############################

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)
