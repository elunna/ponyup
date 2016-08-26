Python Card and Poker FrameWork
===============

Author: Erik Lunna
Date Started: 01-01-2016


The Todo List
-----------------
todo: Test the profitability of 5 card-draw hands WITH the draw.
todo: Create hand groups for holdem
todo: Go through codebase and Implement more pythonic idioms.
todo: Check if the Joker exists. Is there a function to make it fill in a hand?
pycards TODO
Refactor auto discard
Implement repr for all objects
evaluator:
Fix the draw evaluator
evaluate discards: looks at all discard combos and rates them against random hands.
find best draw
best joker substitute – What card would the joker best represent?
misc:
Deal with deck depletion in 5card draw.
cardlist: add count rank
cardlist: best suited+connect run?
dealer tips/rake
Add more complexity to the Player Strategies
Handhistory log
5 card draw variant with Joker
Randomize CPU player sessions, entering/leaving games.
Random flipping of dealt cards (1/500)
Random showing of folds (1/1000?)
Rabbit cam?
Rebuys
Add some common structures to the blinds
Add straddle blind
Add kill game feature
Betting structures: NL, Limit, Spread, Pot limit, Ante only

deck:
    dealing from empty deck raises exception
    separate Deck subclasses?
    isEmpty, contains, __add__, __sub__.
    pinochle deck
    Blackjack decks, subclass, takes an integer shoe

v Menu options:
View Help
Change view
View odds
Auto sort cards
View pot
View Status
Toggle sound
View handhistory
Set speed

Basic GUI
Title menu
splash screen
Show a deck
Display cards
Animate dealing

Unit test EVERYTHING
blinds.py
card.py
casino.py
combos.py
deck.py
draw5.py
draws_eval.py
hand.py
hand
names
player
pokerhands
rnd
sim_pokerhands
strategy
stud5
table
tools
war
Doc comments
Try nose on something (Deck? Hand?)




# How to pick the best card for the joker to represent
pick_joker(cards):
	# Should cards have the joker in it?
	
	# If the Joker is in the pile of cards, remove it for analysis.
	if Joker in cards:	
		remove the joker
	# Generally, we will only be using the joker with 4 cards...
	# But longterm, it would be good to make this more flexible.

	
	# Create a new deck
	d = deck.Deck()

	bestvalue = 0
	bestcard = None

	for c in d.cards:
		
		testhand = hand.Hand(cards)
		testhand.add(c)
		if testhand.value > bestvalue:
			bestvalue = testhand.value
			bestcard = c
	return bestcard


Find the best draw in a group of cards(1-7)?
	It will ideally be a MAX of 4 and min of 3. You need 3 for a backdoor draw.
	I suppose having 2 high/connected suited cards could be counted as well. Way-backdoor draw.

def find_best_draw(cards):



# Testing the getupcards method
import game, blinds, draw5
b = blinds.limit["50/100"]
g = draw5.Draw5Game("DRAW5", b, hero="LUNNA")
r = game.Round(g)
r.deal_cards(1, faceup=True)
r.deal_cards(1)
print(r.tbl)


Cards:
Make a deck in a list and tuple.
Try a named list?
Make a dictionary that does blackjack values and one for straight values
Make a desk from a list comp
Make all different types of decks: shoe size, pinochile, just faces, just numbers, 1 wild, 2 wilds.

Try making all 2/3/4/5 card combos with a list comp or tuples.

Make hand groups:
	Skylansky
	kill phil shoving and calling ranges.
	nash ranges
	
Poker hand evaluator

Simulate all the table games canterbury and mystic have.

Simplest card game is WAR. That's a good way to test cards out and create players with score keeping.
War is also recursive and requires 2 jokers.


Make a poker shoving quiz. should be pretty easy.



The structure of the poker games:

Tournaments(blinds go up/no rebuys)

Sessions(blinds are statis/rebuys allowed)
	Can create a new Cash session of Poker deciding:
		Table size
		Stakes
		Game type
		betting type(limit/nl)
	
	The Session tracks:
		how many rounds have passed
		how much time has passed?
		the table
		the blind structure
		* potentially, handhistories
		* Weird situations with the blinds(player leaves on sb/bb etc)
		
		play method: manages the structure of the select game using tools in the Round
		
A "Round" is a single hand of the session:
	* Safety check that players don't have lingering cards.
	* Posts antes and/or blinds
	* Deals out the appropriate cards
	* It manages the betting
	* It calculates the winners
	* It awards the winner(s) their respective portions of the pot.
	
		ie: 
		
Make bad players like pretty hands 
Add post flop betting 
Make a few different player types 
Add random player types to setup table 
Adjust raise vs reraise and call vs cold call
Strong draw 8+ outs
Mid draw 4+ outs 
Weak,  2 or backdoor

When I finish the full betting for five card draw,  might be good to start on five card stud to exercise the api. Then 7 stud. Also we can use Antes there.  But this will get me to separate the betting and individual game elements out. 5stud also has 4 betting rounds. 5stud is much like holdem. So we can use a similar taking system

The art of the deal

Other standard poker room features;  sitting out, auto pay blinds,  sit out next blind

Hands history. 
Maybe make the display a little less verbose? The history is basically a log , should be pretty easy just to record the essentials

Also,  missed blinds due to busted players are handled differently in cash vs tournament

Text color display for suits?



######################################################################
The Done List
-----------------
DONE: Holdem: suitedness, connectnes, and paired-ness testing
DONE: Use a cleaner algorithm for scoring hands
DONE: Port to git and Clean-up the rough draft of the entire project
done: Create value system for evaluating poker hands
done: Create the War card game that recursively deals with War scenarios.
done: Create a poker table class.
done: An entertaining unique username library for creating table of players.
DONE: 5 card simulations to calculate the winning percent of each unique hand
DONE: Enhance 5-card draw with some AI characters
DONE: Simple 5-card draw game with working discard.



