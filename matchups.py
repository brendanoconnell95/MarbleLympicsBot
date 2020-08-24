#script to create random lines to test betting line adjustments

#CURRENTLY NOT USED


from pathlib import Path
from random import randint

teams = open("team_list.txt").read().splitlines()

lines = []

if Path('matchups.txt').exists():
	print("deleting old matchups file")
	Path("matchups.txt").unlink()
	
file = open("matchups.txt", "a")
	
for x in teams: 
	#for random odds
	#val = randint(0, 250)+100
	#for even odds with 16 teams
	val = 1500
	lines.append(val)
	file.write(x + " +" + str(val))
	file.write('\n')
	
