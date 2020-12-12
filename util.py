import random as R

# cards of three players
w1 = []
w2 = []
w3 = []

""" press 3 enter and 
output: cards of three players, with 3 cards for landlord
"""
def deliver():
	L = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
	P = ['X','x']
	H = ['\u2660', '\u2663', '\u2665', '\u2666']

	for x in H:
		for y in L:
			s = x + y
			P.append(s)
 
	R.shuffle(P)
 
	i = 1
	while i <= 17:
		w1.append(P.pop())
		w2.append(P.pop())
		w3.append(P.pop())
		i += 1


def print_cards():
	legal_id = [0, 1, 2]
	id = input("enter your player id(in 0, 1, 2): ")
	assert (id not in legal_id), "invalid player id"
	if id == 0:
		print(w1)
	if id == 1:
		print(w2)
	if id == 2:
		print(w3)

