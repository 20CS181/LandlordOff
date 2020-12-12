# import random as R 
  
# def reduce(L, w):
#     for x in w:
#         L.pop(L.index(x))
#     return L
 
# L = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
# H = ['\u2660', '\u2663', '\u2665', '\u2666']
 
# P = ['X','x']
# for x in H:
#     for y in L:
#         s = x + y
#         P.append(s)
 
# R.shuffle(P)
 
# i = 0
# L2 = []
# while i < 2:
#     if len(P) > 17:
#         w = R.sample(P, 17) 
#         L2.append(w)
#         P = reduce(P, w)
#         print(w)
#         input()
#     else:
#         break
# print(P)

import random as R

 
L = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
L1 = ['X', 'x']
 
L1.extend(map(lambda x: x+"\u2660", L))
L1.extend(map(lambda x: x+"\u2663", L))
L1.extend(map(lambda x: x+"\u2665", L))
L1.extend(map(lambda x: x+"\u2666", L))
 
R.shuffle(L1)
print(L1[0:17])
input()
print(L1[17:34])
input()
print(L1[34:51])
input()
print(L1[51:])
# import random as R

 
# L = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
# H = ['\u2660', '\u2663', '\u2665', '\u2666']
# w1 = []
# w2 = []
# w3 = []
 
# P = ['X','x']
# for x in H:
#     for y in L:
#         s = x + y
#         P.append(s)
 
# R.shuffle(P)
 
# i = 1
# while i <= 17:
#     w1.append(P.pop())
#     w2.append(P.pop())
#     w3.append(P.pop())
#     i += 1
 
# print(w1)
# input()
# print(w2)
# input()
# print(w3)
# input()
# print(P)
