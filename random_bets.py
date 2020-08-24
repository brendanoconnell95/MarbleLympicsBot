#script to generate random bets on the 16 teams in the MarbleLympics
import random
from random import randint
from pathlib import Path
import collections

if Path('ledger.txt').exists():
	print("deleting old ledger file")
	Path("ledger.txt").unlink()
	
if Path('open_interest.txt').exists():
	print("deleting old open interest file")
	Path("open_interest.txt").unlink()

teams = open("team_list.txt").read().splitlines()
ledger = open("ledger.txt", "a")
open_interest_file = open("open_interest.txt", "a")

oi_dict = {}
odds_dict = {}

for team in teams: 
	oi_dict[team] = 0
	odds_dict[team] = len(teams) * 100

open_interest = collections.OrderedDict(sorted(oi_dict.items()))


#the plan is to calculate odds based on total money bet on a team compared to all 
#money bet. Need to use a modifier to stop the early bets from drastically swinging
#the lines

#working on this pots method, it is striking that the formula is focused on balancing
#the odds based on not who will win, but on what price each team is attractive at

def adjustLines(open_interest): 
	#parameter for max change in moneyline
	max_change = 30
	
	total_open_interest = 0
	for k in open_interest: 
		 total_open_interest += open_interest[k]
	
	#calculate new ML odds by adding/subtracting no more than 30
	for team in teams: 
		if open_interest[team]/total_open_interest > 1/len(teams):
			odds_dict[team] = round(odds_dict[team]-max_change*open_interest[team]/total_open_interest)
		else:
			odds_dict[team] = round(odds_dict[team]+max_change*open_interest[team]/total_open_interest)
	
	#print to see algorithm at work
	#print(odds_dict, "\n")
	
#another method that could be used to adjust lines is to scale each bet's impact on the line on a logarithm so that big bets have proportionally more impact on the lines than a linear extension of a small bet. This "values" the "smart" money/pro bettors' opinions more	


	
for x in range(0,100): 
	#produce wager amount
	wager = randint(1,30)
	#choose team
	team = random.choice(teams)
	#print("team:", team)
	#print("wager:", wager)
	
	#write the wager to the list of ALL wagers AKA the ledger. 
	#will need to add a name as well but I didn't wanna make up a bunch of them
	ledger.write(team + ": " + str(wager)+ "\n")
	
	#add the wager the pot of all the money bet on each team. Will use this to adjust lines
	open_interest[team]+=wager
	adjustLines(open_interest)

print(odds_dict)


#write the open interest to a file after all wagers have been considered
for key, val in open_interest.items(): 
	open_interest_file.write(key + ": " + str(val) + "\n")
	
#print(open_interest)

