from collections import Counter

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

    
def get_legal_choices(cards):
        possible_choice={}
        mycards=cards
        for i in range(6):
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
        for i in self.mycards.keys():
                   if self.mycards[i]>3:
                       possible_choice[9].append(i)
        return possible_choice
class AI_agent(agent):
    def take_action(self,gamestate):
        self.other_cards=gamestate.cur_cards
        self.flag=gamestate.user_states
        self.mycards=self.cards
        self.possible_choice=get_legal_choices(self.mycards)
    def get_action(self):
        def wang_zha():
            if 'x' in self.other_cards and 'X' in self.other_cards: return None
            
        def dan_pai():
            if len(self.other_cards)==1:
                choices=self.possible_choice[1] 
                if choices==[]:return None
                
                pai_to_number[choices]
                pai_to_number[self.other_cards]
                choices.sort()
                for i in range(len(choices)):
                    if choices[i] > self.other_cards[0] :
                        number_to_pai(choices)
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
                    
                    pai_to_number[choices]
                    pai_to_number[self.other_cards]
                    choices.sort()
                    for i in range(len(choices)):
                        if choices[i] > self.other_cards[0] :
                            number_to_pai(choices)
                            act=[choices[i],choices[i]]
                            #delete
                            for j in range(2) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                            return act
                    return None
        
        def three():
            if len(self.other_cards)==3:
                if self.other_cards[0]==self.other_cards[1] and self.other_cards[0]==self.other_cards[2]:
                    choices=self.possible_choice[3]
                    if choices==[]:return None
                    
                    pai_to_number[choices]
                    pai_to_number[self.other_cards]
                    choices.sort()
                    for i in range(len(choices)):
                        if choices[i] > self.other_cards[0] :
                            number_to_pai(choices)
                            act=[choices[i],choices[i],choices[i]]
                            for j in range(3) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                            return act
                    return None
                
        # 3,4,5,...
        def dan_lian():
            pai_to_number[self.other_cards]
            self.other_cards.sort()
            if all([self.other_cards[i]+1 == self.other_cards[i+1] for i in range(len(self.other_cards)-1)]) :
                choices=self.possible_choice[4]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==len(self.other_cards) and len(choices)>2 :
                        pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >self.other_cards[0] :
                            act=choices[i]
                            number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                            
                            return act
                return None

        #33,44,55,...
        def er_lian():
            pai_to_number[self.other_cards]
            self.other_cards.sort()
            length_other=len(self.other_cards)
            #每个值频率为2
            dict = {}
            for key in self.other_cards:
                dict[key] = dict.get(key, 0) + 1
            a=[]
            a=dict.values()
            for i in range(len(a)):
                if a[i]!=2 :
                    return None

            #去重，再排序
            sorted(set(self.other_cards), key = self.other_cards.index)
            if all([self.other_cards[i]+1 == self.other_cards[i+1] for i in range(len(self.other_cards)-1)]) :
                choices=self.possible_choice[5]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==length_other and len(choices)>4 :
                        pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >self.other_cards[0] :
                            act=choices[i]
                            number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)
                                    
                            return act
                return None

        #333,444,555,...
        def san_lian():
            pai_to_number[self.other_cards]
            self.other_cards.sort()
            length_other=len(self.other_cards)
            #每个值频率为3
            dict = {}
            for key in self.other_cards:
                dict[key] = dict.get(key, 0) + 1
            a=[]
            a=dict.values()
            for i in range(len(a)):
                if a[i]!=3 :
                    return None

            #去重，再排序
            sorted(set(self.other_cards), key = self.other_cards.index)
            if all([self.other_cards[i]+1 == self.other_cards[i+1] for i in range(len(self.other_cards)-1)]) :
                choices=self.possible_choice[6]
                if choices==[]:return None

                for i in range(len(choices)):
                    if len(choices) ==length_other and len(choices)>3 :
                        pai_to_number(choices[i])
                        choices[i].sort()
                        if choices[i][0] >self.other_cards[0] :
                            act=choices[i]
                            number_to_pai(act)
                            
                            #delete
                            for j in range(len(act)) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            
                            return act
                return None
            
        def three_plus_one():
            if len(self.other_cards)==4:
                pai_to_number[self.other_cards]
                #出现频率最高的一个数的频率为3
                if  Counter(self.other_cards).most_common(1)[0][1]==3 :
                    choices=self.possible_choice[7]
                    if choices==[]:return None

                    for i in range(len(choices)):
                        pai_to_number(choices[i])
                        three=Counter(choices[i]).most_common(1)[0][0]
                        if three > Counter(self.other_cards).most_common(1)[0][0] :
                            number_to_pai(choices[i])
                            act=choices[i]
                            #delete
                            for j in range(4) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            return act
                    return None
                
        def three_plus_two():
            if len(self.other_cards)==5:
                pai_to_number[self.other_cards]
                #出现频率最高的一个数的频率为3，次高为2
                max_f=Counter(self.other_cards).most_common(1)[0][1]
                most_number==Counter(self.other_cards).most_common(1)[0][0]
                while most_number in self.other_cards:
                    self.other_cards.remove(most_number)
                min_f=Counter(self.other_cards).most_common(1)[0][1]
                if  max_f==3 and min_f==2 :
                    choices=self.possible_choice[8]
                    if choices==[]:return None

                    for i in range(len(choices)):
                        pai_to_number(choices[i])
                        three=Counter(choices[i]).most_common(1)[0][0]
                        if three > most_number :
                            number_to_pai(choices[i])
                            act=choices[i]
                            #delete
                            for j in range(5) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            return act
                    return None

        def bomb():
            if len(self.other_cards)==4:
                if all(item ==self.other_cards[0] for item in self.other_cards):
                    choices=self.possible_choice[9]
                    if choices==[]:return None
                    
                    pai_to_number[choices]
                    pai_to_number[self.other_cards]
                    choices.sort()
                    for i in range(len(choices)):
                        if choices[i] > self.other_cards[0] :
                            number_to_pai(choices)
                            act=[choices[i],choices[i],choices[i],choices[i]]
                            #delete
                            for j in range(4) :
                                self.mycard.remove(act[j])
                            self.possible_choice=get_legal_choices(self.mycards)   
                            return act
                    return None
          

        # we can freely decide to output which cards.
        if flag:
            dan_pai()
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
            
            
        
