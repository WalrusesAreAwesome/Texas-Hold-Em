# Calculates how often one hand will evolve into others over the course of a game of Texas Hold Em, by playing millions of games.
# Notes: This counts hands by "use." I.e. your trick must use your cards
import math
import random


class Card:
	def __init__(self, suit, rank, inHand):
		self.suit = suit # string
		self.rank = rank # int
		self.inHand = inHand # boolean


def draw_card(inHand):
	card = deck.pop( math.floor(random.random()*len(deck)) )
	if inHand:
		card.inHand = True
	return card


"""
Trick - Need to check hole

RF - no
SF - no
4K - no
FH - no
St - no
Fl - no
3K - yes
2P - yes
Pr - yes
HK - yes

"""

def evaluate_hand(hand):
	# Declare
	straight = False
	flush = True # Filtered out later
	sortedRanks = []
	
	# Init those missed
	for card in hand:
		sortedRanks.append(card.rank)
	sortedRanks.sort()
	uniqueRanks = len(set(sortedRanks))
	
	# Check if straight
	if uniqueRanks == 5:
		jumps = 0
		for i in range(4):
			difference = sortedRanks[i+1] - sortedRanks[i]
			if difference != 1:
				jumps += 1
		# problem: Aces can be 0 OR 13: not both
		if (jumps == 0) or (jumps == 1 and sortedRanks[0] == 0 and sortedRanks[1] == 9):
			straight = True
	
	# Check if flush
	for i in range(4):
		if not(hand[i].suit is hand[4].suit):
			flush = False
			break
	
	# If both, check if Royal. Otherwise, Straight Flush
	if straight and flush:
		if (sortedRanks[0] == 0) and (sortedRanks[1] == 9):
			return "Royal Flush"
		else:
			return "Straight Flush"
	
	# This is just smart. Just marvel at this
	if uniqueRanks == 2:
		if (sortedRanks[1] == sortedRanks[3]):
			return "Four of a Kind"
		else:
			return "Full House"
	
	if flush:
		return "Flush"
	if straight:
		return "Straight"
	
	# Also smart, takes into account the "3 unique ranks" trick
	if uniqueRanks == 3:
		if sortedRanks[0] == sortedRanks[1]:
			if sortedRanks[1] == sortedRanks[2]:
				return "3 of a Kind"
			else:
				return "Two Pair"
		else:
			if sortedRanks[2] == sortedRanks[3]:
				return "3 of a Kind"
			else:
				return "Two Pair"
	
	if uniqueRanks == 4:
		return "Pair"
	
	return "High Card"


def save(evolutions):
	evoStr = ""
	
	for r in evolutions:
		for startTrick in r:
			for endTrick in startTrick:
				evoStr += str(endTrick) + " "
			evoStr += "\n"
		evoStr += "\n"
	
	f = open("evolutions.txt", "w")
	f.write(evoStr)
	f.close()


trickRank = {
	"Royal Flush": 0,
	"Straight Flush": 1,
	"Four of a Kind": 2,
	"Full House": 3,
	"Flush": 4,
	"Straight": 5,
	"3 of a Kind": 6,
	"Two Pair": 7,
	"Pair": 8,
	"High Card": 9
}
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

#    ENDING
#  
# S
# T
# A
# R
# T
# 

tenZeroes = [0,0,0,0,0,0,0,0,0,0]
evolutions = [[tenZeroes]]
for i in range(2):
	evolutions.append([])
	for j in range(10):
		evolutions[i+1].append(tenZeroes)

trials = 10000

for t in range(trials):
	# Init
	deck = []
	for i in range(52):
		deck.append( Card(suits[math.floor(i/13)], i%13, False) )
	hand = []
	river = []
	# Give the hand 2, give the River 3
	for i in range(2):
		hand.append(draw_card(True))
	for i in range(3):
		river.append(draw_card(False))
	toCheck = [hand + river]
	best = 0
	for h in toCheck:
		trick = evaluate_hand(h)
		best = max(best, trickRank[trick])
	
	if t % 100000 == 0:
		print(f"{t} / {trials}")

save(evolutions)


