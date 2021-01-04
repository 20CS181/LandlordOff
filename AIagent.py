from collections import Counter
from HumanAgent import * 
import random

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
        for j in range(card_dic[i]):
           l.append(i)
    return l
        
    
def get_legal_choices(cards):

        possible_choice={}
       
        mycards= tranf_from_list_to_dic(cards)
        for i in range(10):
            possible_choice[i]=[]
        #maintain possible_choices
        #wang_zha
            #nothing needa to be done
            
        #danpai
        for i in mycards.keys():
                   if mycards[i]>0:
                       possible_choice[1].append(i)
        #two
        for i in mycards.keys():
                   if mycards[i]>1:
                       possible_choice[2].append(i)      
        #three
        for i in mycards.keys():
                   if mycards[i]>2:
                       possible_choice[3].append(i)                   
        #dan_lian
        count=0
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for j in t:
            if mycards[j]>0:
                count=count+1
                if count >=5:
                    for i in range(count-4):
                       possible_choice[4].append(t[(t.index(j)-count+1+i):(t.index(j)+1)])
            else:  count=0               
        #er_lian
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
        #san_lian
        count=0
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for j in t:
            if mycards[j]>1:
                count=count+1
                if count >=2:
                    for i in range(count-1):
                       tep=t[(t.index(j)-count+1+i):(t.index(j)+1)]
                       possible_choice[6].append(tep+tep+tep)
            else:  count=0                 
        #three_plus_one
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','A', '2']
        for j in t:
            if mycards[j]>2:
                for i in mycards.keys():
                    if i != j and mycards[i]>0:
                        possible_choice[7].append([j,j,j,i])
        #three_plus_two
        t=['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K','A', '2']
        for j in t:
            if mycards[j]>2:
                for i in mycards.keys():
                    if i != j and mycards[i]>1:
                        possible_choice[8].append([j,j,j,i,i])     
        #bomb
        for i in mycards.keys():
                   if mycards[i]>3:
                       possible_choice[9].append(i)
        return possible_choice
class AI_agent(Agent):
    def takeAction(self,gamestate):
        self.other_cards=gamestate.cards_out
         
        self.mycards=self.cards
        print("before_cards:",self.mycards)
        self.possible_choice=get_legal_choices(self.cards)
        self.cards_out=self.get_action(gamestate)
        self.cards=self.mycards
        print("try:",self.cards_out)
        print("after_cards:",self.mycards)
        if self.cards_out!=None:
            gamestate.cards_out=self.cards_out
            gamestate.last_turn=self.name
            print("this round player %s take out:"%(self.name),self.cards_out)
        return self.cards

    def get_action(self,gamestate):
        def wang_zha():
            if 'x' in self.other_cards and 'X' in self.other_cards: return None
            
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
                
        def three_plus_two():
            if len(self.other_cards)==5:
                other_cards=pai_to_number(self.other_cards)
                #出现频率最高的一个数的频率为3，次高为2
                max_f=Counter(other_cards).most_common(1)[0][1]
                most_number==Counter(other_cards).most_common(1)[0][0]
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
          

        # we can freely decide to output which cards.
        if gamestate.last_turn==self.name:
            #func=[dan_pai,two,three,three_plus_one,three_plus_two,dan_lian,er_lian,san_lian]
            #self.other_cards=[-1]
            #we_action=dan_pai()
            rand_num=random.randint(1,9)
            print(self.possible_choice)
            if self.possible_choice[rand_num] !=[]:
              we_action=self.possible_choice[rand_num][0]
            else:
              we_action=None
            while we_action is None : 
                rand_num=random.randint(1,9)
                if self.possible_choice[rand_num] !=[]:
                    we_action=self.possible_choice[rand_num][0]
                else:
                    we_action=None
            if rand_num==2:
                we_action=[we_action]+[we_action]
            if rand_num==3:
                we_action=[we_action]+[we_action]+[we_action]
            for i in range(len(we_action)):
                self.mycards.remove(we_action[i])
            return we_action
        else:
            we_action=wang_zha()
            if  we_action is not None: return we_action
            
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
            
        
