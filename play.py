from util import *
from game import *


name = input("enter your name:")
# list = input("player %s: \nplease enter your card choices in ONE LINE:"%(name))
# input()
# print("list:", list)
# print("list:", list.split())
# print("is empty:", list.split())
# print("list:", newlist) 
print("delivering")
deliver()
player = HumanAgent(name, w1, True)

while not player.isWinner():
    print("your cards:", player.cards)
    player.takeAction(None)
print("finish!")
