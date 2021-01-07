"""
utils for Agents
"""
import time, os, traceback, sys, inspect


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


    
######################## helper function ##############################

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)
