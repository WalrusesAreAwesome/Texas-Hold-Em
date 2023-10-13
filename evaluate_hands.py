# Times the evaluation of hands
import math
import random
import time

# bevore: 23.2 mcs

class Card:
	def __init__(self, suit, rank):
		self.suit = suit # string
		self.rank = rank # int

def make_hand():
	hand = []
	for i in range(5):
		ID = deck.pop(math.floor( random.random()*len(deck) ))
		hand.append( Card(math.floor(ID/13), ID%13) )
	return hand

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
	
	if uniqueRanks == 5:
		return "High Card"
	
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


timesGotten = {
	"Royal Flush": 0,
	"Straight Flush": 0,
	"Four of a Kind": 0,
	"Full House": 0,
	"Flush": 0,
	"Straight": 0,
	"3 of a Kind": 0,
	"Two Pair": 0,
	"Pair": 0,
	"High Card": 0
}
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

trials = 25989600

start = time.time()
for t in range(trials):
	deck = []
	for i in range(52):
		#deck.append( Card(math.floor(i/13), i%13) )
		deck.append(i)
	hand = make_hand()
	trick = evaluate_hand(hand)
	timesGotten[trick] += 1
	
	if t % 500000 == 1:
		print(f"{t} / {trials}")
		endP = time.time()
		secPerEval = (endP-start)/t
		print(f"Average time to evaluate: {round(secPerEval * 1000000, 2)}μs")
		print(f"Average speed: {round(60/secPerEval)} evals / min")
end = time.time()

for trick, times in timesGotten.items():
	print(f"{trick} - {times}")

secPerEval = (end-start)/trials
print(f"Average time to evaluate: {round(secPerEval * 1000000, 2)}μs")
print(f"Average speed: {round(60/secPerEval)} evals / min")
