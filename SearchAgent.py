from collections import Counter
from AIagent import *
import random


class OneChoice:
    """
    One possible choice.
    a partition of a series of card types
    """
    def __init__(self):
        # 0~9:10 num_of_type
        self.num_of_wangzha=0
        self.num_of_danzhang=0
        self.num_of_duizi=0
        self.num_of_sanzhang=0
        self.num_of_shunzi=0    # dan_lian
        self.num_of_liandui=0   # er_lian
        self.num_of_feiji=0     # san_lian
        self.num_of_san_dai_yi=0# 3+1
        self.num_of_san_dai_er=0# 3+2
        self.num_of_bomb=0

        # 0~9: 10 list_of_type
        self.list_of_wangzha=[]
        self.list_of_danzhang=[]
        self.list_of_duizi=[]
        self.list_of_sanzhang=[]
        self.list_of_shunzi=[]
        self.list_of_liandui=[]
        self.list_of_feiji=[]
        self.list_of_3_plus_1=[]
        self.list_of_3_plus_2=[]
        self.list_of_bomb=[]

        # other attributes
        self.total_times_to_finish=0
        self.value=0

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

def chai_pai(mycards, possible_choice):
    """
    第一步，将手牌拆成不可带牌的套牌。即排除：三带一、三带二、四带两单、四带两对、飞机带单张、飞机带对子这6种牌型。
    第二步，对每一种拆法计算带牌后的套牌。将三张、飞机、炸弹与单张、对子进行组合，分析出包括带牌在内的所有套牌。
    拆牌逻辑的输入：手牌的一维数组
    拆牌逻辑的输出：套牌的二维数组，n种拆法（一维），每种拆法包括m个套牌（二维）
    """
    #FIRST STEP
    #danzhang      
    if len(possible_choice)==0 :
        danpai=OneChoice()
        danpai.num_of_danzhang+=1
        danpai.total_times_to_finish+=1
        danpai.list_of_danzhang.append(mycards[0])
        possible_choice.append(danpai)
    else :
        possible_choice[-1].num_of_danzhang+=1
        possible_choice[-1].total_times_to_finish+=1
        possible_choice[-1].list_of_danzhang.append(mycards[0])
    mycards.remove(mycards[0])
    if len(mycards)==0 :
        return
    else :
        return chai_pai(mycards, possible_choice)

    #duizi  
    if find_duizi(mycards) :
        i=find_duizi(mycards)
        if len(possible_choice)==0 :
            duizi=OneChoice()
            duizi.num_of_duizi+=1
            duizi.total_times_to_finish+=1
            duizi.list_of_duizi.append(i)
        else :
            possible_choice[-1].num_of_duizi+=1
            possible_choice[-1].total_times_to_finish+=1
            possible_choice[-1].list_of_duizi.append(i)
    mycards.remove(i)
    mycards.remove(i)
    if len(mycards)==0 :
        return
    else :
        return chai_pai(mycards, possible_choice)

    #sanzhang
    if find_sanzhang(mycards) :
        i=find_sanzhang(mycards)
        if len(possible_choice)==0 :
            sanzhang=OneChoice()
            sanzhang.num_of_sanzhang+=1
            sanzhang.total_times_to_finish+=1
            sanzhang.list_of_sanzhang.append(i)
        else :
            possible_choice[-1].num_of_sanzhang+=1
            possible_choice[-1].total_times_to_finish+=1
            possible_choice[-1].list_of_sanzhang.append(i)
    for j in range(3) :
        mycards.remove(i)
    if len(mycards)==0 :
        return
    else :
        return chai_pai(mycards, possible_choice)

    #shunzi                    1
    if len(find_shunzi(mycards)) !=0 :
        
        i=find_shunzi(mycards)
        if len(possible_choice)==0 :
            shunzi=OneChoice()
            shunzi.num_of_shunzi+=1
            shunzi.total_times_to_finish+=1
            shunzi.list_of_shunzi.append(i)
        else :
            possible_choice[-1].num_of_shunzi+=1
            possible_choice[-1].total_times_to_finish+=1
            possible_choice[-1].list_of_shunzi.append(i)
 
    mycards.remove(i)
    if len(mycards)==0 :
        return
    else :
        return chai_pai(mycards, possible_choice)

    #bomb
    if find_bomb(mycards) :
        i=find_bomb(mycards)
        if len(possible_choice)==0 :
            bomb=OneChoice()
            bomb.num_of_sanzhang+=1
            bomb.total_times_to_finish+=1
            bomb.list_of_bomb.append(i)
        else :
            possible_choice[-1].num_of_bomb+=1
            possible_choice[-1].total_times_to_finish+=1
            possible_choice[-1].list_of_bomb.append(i)
    for j in range(4) :
        mycards.remove(i)
    if len(mycards)==0 :
        return
    else :
        return chai_pai(mycards, possible_choice)

    #feiji
    if find_feiji(mycards) :
        ans=[]
        ans=find_feiji(mycards)
        if len(possible_choice)==0 :
            feiji=OneChoice()
            feiji.num_of_feiji+=1
            feiji.total_times_to_finish+=1
            feiji.list_of_feiji.append(ans)
        else :
            possible_choice[-1].num_of_feiji+=1
            possible_choice[-1].total_times_to_finish+=1
            possible_choice[-1].list_of_feiji.append(ans)
    for j in range(3) :
        mycards.remove(ans[0])
        mycards.remove(ans[-1])
    if len(mycards)==0 :
        return
    else :
        return chai_pai(mycards, possible_choice)
    #wangzha
    if find_wangzha(mycards) :
        if len(possible_choice)==0 :
            wangzha=OneChoice()
            wangzha.num_of_wangzha+=1
            wangzha.total_times_to_finish+=1
            wangzha.list_of_wangzha.append('x')
            wangzha.list_of_wangzha.append('X')
        else :
            possible_choice[-1].num_of_wangzha+=1
            possible_choice[-1].total_times_to_finish+=1
            possible_choice[-1].list_of_wangzha.append('x')
            possible_choice[-1].list_of_wangzha.append('X')
    mycards.remove('x')
    mycards.remove('X')
    if len(mycards)==0 :
        return
    else :
        return chai_pai(mycards, possible_choice)

    #liandui                           2
    if len(find_liandui(mycards)) !=0 :
        return False

def choice_daipai(beidai,dpNum,one_possible_choice,possible_choice):
    """
    递归结束逻辑：所有可带牌套牌都已匹配到被带牌
    递归范围减少：每匹配好一组可带牌+被带牌，就其从待匹配可带牌套牌和待匹配被带牌的列表中删除，并生成匹配好的新套牌
    递归返回结果：在递归过程中记录，在递归结束时返回所有匹配好的新套牌。
    """
    for j in range(dpNum) :  #选j个套牌去带牌
        if j > beidai :
            return
        if dpNum==0 :
            return
        else :
            if one_possible_choice.num_of_danzhang !=0 :   #带1
                newone=OneChoice()
                if one_possible_choice.num_of_sanzhang !=0:  #3+1
                    newone.num_of_san_dai_yi+=1
                    newone.list_of_san_dai_yi.append([one_possible_choice.list_of_sanzhang[0],one_possible_choice.list_of_danzhang[0]])
                    one_possible_choice.num_of_danzhang-=1
                    one_possible_choice.list_of_danzhang.remove(0)
                    one_possible_choice.num_of_sanzhang-=1
                    one_possible_choice.list_of_sanzhang.remove(0)
                #if one_possible_choice.num_of_bomb !=0:    4+1？

                if one_possible_choice.num_of_feiji!=0:    # 3 555666 7
                    if one_possible_choice.num_of_danzhang>=2 :
                        newone.num_of_feiji_dai_yi+=1
                        newone.list_of_san_dai_yi.append([ one_possible_choice.list_of_feiji[0], one_possible_choice.list_of_danzhang[0:2] ])
                        one_possible_choice.num_of_danzhang-=2
                        one_possible_choice.list_of_danzhang=one_possible_choice.list_of_danzhang[2:]
                        one_possible_choice.num_of_feiji-=1
                        one_possible_choice.list_of_feiji.remove(0)
                newone.total_times_to_finish+=1
                possible_choice.append(newone)

            if one_possible_choice.num_of_duizi !=0 :   #带2
                newone=OneChoice()
                if one_possible_choice.num_of_sanzhang !=0:  #3+2
                    newone.num_of_san_dai_er+=1
                    newone.list_of_san_dai_er.append([one_possible_choice.list_of_sanzhang[0],one_possible_choice.list_of_duizi[0]])
                    one_possible_choice.num_of_duizi-=1
                    one_possible_choice.list_of_duizi.remove(0)
                    one_possible_choice.num_of_sanzhang-=1
                    one_possible_choice.list_of_sanzhang.remove(0)
                #if one_possible_choice.num_of_bomb !=0:    4+2？

                if one_possible_choice.num_of_feiji!=0:    # 33 555666 77
                    if one_possible_choice.num_of_duizi>=2 :
                        newone.num_of_feiji_dai_er+=1
                        newone.list_of_san_dai_er.append([ one_possible_choice.list_of_feiji[0], one_possible_choice.list_of_duizi[0:2] ])
                        one_possible_choice.num_of_duizi-=2
                        one_possible_choice.list_of_duizi=one_possible_choice.list_of_duizi[2:]
                        one_possible_choice.num_of_feiji-=1
                        one_possible_choice.list_of_feiji.remove(0)
                newone.total_times_to_finish+=1
                possible_choice.append(newone)
            
            dpNum-=1
            beidai-=1
            return choice_daipai(beidai,dpNum,one_possible_choice,possible_choice)

            
def chai_pai_second(possible_choice) :
    #SECOND STEP
    """
    1、查看拆牌结果中套牌是否包括：三张、炸弹和飞机，并且有可以被带的套牌：单张和对子。如果没有可带牌或被带牌直接返回。否则，进行下一步。
    2、计算可带牌套牌的数量为（dpNum），从1遍历到dpNum，求出每种可带牌数量下的所有带牌组合。
    """
    for i in range(len(possible_choice)) :
        beidai=possible_choice[i].num_of_danzhang+possible_choice[i].num_of_duizi
        dpNum=possible_choice[i].num_of_sanzhang+possible_choice[i].num_of_bomb+possible_choice[i].num_of_feiji
        if dpNum==0 or beidai==0 :
            return
        else:
            choice_daipai(beidai,dpNum,possible_choice[i],possible_choice)



def get_value(A_choice):
    return 0


class SearchAgent(AI_agent):
    def get_action(self, gamestate):
        """ judge the cards of others
        for active: random choose an available one
        for passive: try to follow the others under the rule
        if quit, return None.

        use `choices`: class `OneChoice`
        after kicking off the `cards_out`,
        we want the remaining as a `choice` with the largest value
        """
        def wang_zha():
            return ('x' in self.other_cards and 'X' in self.other_cards)

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
          
        # active carding: we can freely decide to output which cards.
        if gamestate.last_turn==self.name:
            # func=[dan_pai,two,three,three_plus_one,three_plus_two,dan_lian,er_lian,san_lian]
            # self.other_cards=[-1]
            # we_action=dan_pai()
            rand_num=random.randint(1,9)
            print("possible choices for %s: "%self.name, self.possible_choice)
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
            # passively carding
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

    def setChoiceFromCardsDic(self, dic_cards):
        choice=OneChoice()

