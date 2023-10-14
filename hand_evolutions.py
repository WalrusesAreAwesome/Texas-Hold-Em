# Calculates how often one hand will evolve into others over the course of a game of Texas Hold Em, by playing millions of games.
# Notes: This counts hands by "use." I.e. your trick must use your cards
import math
import random
import time

class Card:
	def __init__(self, suit, rank, inHand):
		self.suit = suit # string
		self.rank = rank # int
		self.inHand = inHand # boolean


def draw_card(inHand):
	ID = deck.pop(math.floor( random.random()*len(deck) ))
	card = Card(math.floor(ID/13), ID%13, inHand)
	return card


"""
Trick - Need to check hole

RF - no
SF - no
4K - yes
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
	
	# Check for a very common trick BEFORE hard evaluation
	if uniqueRanks == 4:
		return "Pair"
	
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
		if not(hand[i].suit == hand[4].suit):
			flush = False
			break
	
	# If both, check if Royal. Otherwise, Straight Flush
	if straight and flush:
		if (sortedRanks[0] == 0) and (sortedRanks[1] == 9):
			return "Royal Flush"
		else:
			return "Straight Flush"
	
	if flush:
		return "Flush"
	if straight:
		return "Straight"
	
	# This is just smart. Just marvel at this
	if uniqueRanks == 2:
		if (sortedRanks[1] == sortedRanks[3]):
			return "Four of a Kind"
		else:
			return "Full House"
	
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


def load(fName):
	evoTable = [[], [], []]
	f = open(fName, "r")
	evoTxt = f.read()
	f.close()
	evo = evoTxt.split("\n\n")
	evo.pop(-1)
	for i in range(len(evo)):
		evo[i] = evo[i].split("\n")
		for j in range(len(evo[i])):
			evo[i][j] = evo[i][j].split(" ")
			evo[i][j].pop(-1)
			for k in range(len(evo[i][j])):
				evo[i][j][k] = int(evo[i][j][k])
	return evo


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

#    ENDING
#  
# S
# T
# A
# R
# T
# 

evolutions = load("evolutions.txt")
print(evolutions)
"""
tenZeroes = [0,0,0,0,0,0,0,0,0,0]
evolutions = [[tenZeroes.copy()]]
for i in range(2):
	evolutions.append([])
	for j in range(10):
		evolutions[i+1].append(tenZeroes.copy())
"""
# Currently: 64.5μs per game, or 930k / min
trials = 9000000
start = time.time()
for t in range(trials):
	# Init
	history = [0]
	deck = []
	hand = []
	river = []
	# Create deck
	for i in range(52):
		deck.append(i)
	# Give the hand 2, give the River 3
	for i in range(2):
		hand.append(draw_card(True))
	for i in range(3):
		river.append(draw_card(False))
		
	# Round 1
	toCheck = [hand + river]
	best = 10
	for h in toCheck:
		trick = evaluate_hand(h)
		best = min(best, trickRank[trick])
	history.append(best)
	# Round 2
	river.append(draw_card(False))
	toCheck = []
	for i in range(6):
		allCards = hand + river
		allCards.pop(i)
		toCheck.append(allCards)
	best = 10
	for h in toCheck:
		trick = evaluate_hand(h)
		best = min(best, trickRank[trick])
	history.append(best)
	# Round 3
	river.append(draw_card(False))
	toCheck = []
	for i in range(5):
		riverAdd = river.copy()
		riverAdd.pop(i)
		for j in range(i+2):
			allCards = hand + riverAdd
			allCards.pop(j)
			toCheck.append(allCards)
	best = 10
	for h in toCheck:
		trick = evaluate_hand(h)
		best = min(best, trickRank[trick])
	history.append(best)
	
	# Update evolutions
	for i in range(3):
		evolutions[i][history[i]][history[i+1]] += 1
	
	if t % 100000 == 1:
		print(f"{t} / {trials}")
		endP = time.time()
		secPerEval = (endP-start)/t
		print(f"Average time to evaluate: {round(secPerEval * 1000000, 2)}μs")
		print(f"Average speed: {round(60/secPerEval)} evals / min")

end = time.time()
secPerEval = (end-start)/trials
print(f"Average time to evaluate: {round(secPerEval * 1000000, 3)}μs")
print(f"Average speed: {round(60/secPerEval)} evals / min")

save(evolutions)


