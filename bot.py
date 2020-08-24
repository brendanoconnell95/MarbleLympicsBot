#new python script
import praw
from pathlib import Path
import collections
import datetime

now = datetime.datetime.now()

action_list = ["bet", "info", "lines"]
comment_list = []

teams = open("team_list.txt").read().splitlines()

lf = "ledger_"+now.strftime("%m-%d-%Y")+".txt"
ledger = open(lf, "a")

oif = "open_interest_"+now.strftime("%m-%d-%Y")+".txt"
open_interest_file = open(oif, "w")

oi_dict = {}
odds_dict = {}

#populate open interest dict and odds dict
for team in teams: 
	oi_dict[team] = 0
	odds_dict[team] = len(teams) * 100



reddit = praw.Reddit(client_id='d_c9EE4gWxXEOQ', client_secret='IQPZR4_IEW17GP2xGDOFWpjDFO0', username='MarbleLympicsBot', password='Thisis2gay!', user_agent='bot by u/soccer3222')

subreddit = reddit.subreddit('soccer3222')

keyphrase = '!marblebot'

def cacheComment(id): 
	#only cache unique comments
	if id not in comment_list: 
		comment_list.append(id)
	
		file = open("cache.txt", "a")
		file.write(id)
		file.write('\n')
		file.close()

def loadCache():
	if Path('cache.txt').exists():
		commented = open('cache.txt').read().splitlines() 
		global comment_list 
		comment_list = commented
		#print ("comment list", comment_list)
		
def isAction(comment):
	action = comment.body.split(' ')[1]
	print("action: ", action)
	if action in action_list:
		return True
	else:
		return False

def getLines(): 
	#read the odds dict and return lines
	lines = ""
	for team in odds_dict: 
		lines += (team+" +"+str(odds_dict[team])+"\n\n")
	return lines
	
def properBet(bet):
	parts = comment.body.split(' ')
	#print("parts:", parts)
	if len(parts) != 4:
		print("wrong number of arguments for betting!")
		return False
	elif parts[2] not in teams:
		print("not a valid team to bet on. (check your spelling)")
		return False
	elif parts[3][0:].isdigit():
		print("Bet amount is valid")
		return True
	else: 
		print("Bet amount is bad")
		return False
	
def adjustLines(oi_dict): 
	#parameter for max change in moneyline
	max_change = 30
	
	total_open_interest = 0
	for k in oi_dict: 
		 total_open_interest += oi_dict[k]
	
	#calculate new ML odds by adding/subtracting no more than 30
	for team in teams:
		#the team is more than an even split chance of winning
		if oi_dict[team]/total_open_interest > 1/len(teams):
			#odds should go down as a result
			odds_dict[team] = round(odds_dict[team]-max_change*oi_dict[team]/total_open_interest)
		else:
			#odds should go up to reflect team's proportion of open interest
			odds_dict[team] = round(odds_dict[team]+max_change*oi_dict[team]/total_open_interest)
	
	#print to see algorithm at work
	#print(odds_dict, "\n")
	
#another method that could be used to adjust lines is to scale each bet's impact on the line on a logarithm so that big bets have proportionally more impact on the lines than a linear extension of a small bet. This "values" the "smart" money/pro bettors' opinions more	


def doAction(comment): 
	act = comment.body.split(' ')[1] 
	if act == "info":
		response = "This is a bot that tracks bets on the MarbleLympics. Possible commands are INFO, LINES to see upcoming events and their lines, and BET [team] [amount] to place a wager. I'm still in alpha so please be kind. Message u/soccer3222 with comments or concerns."
	if act == "lines":
		lines = getLines()
		response = "Lines for the upcoming events are:\n\n"
		for line in lines: 
			response += (str(line))
	if act == "bet":
		if not properBet(comment):
			response = "This bet was not structured correctly. Proper syntax is BET [team] [amount]."
		else: 
			#Record bet in ledger and open interest files, and adjust lines
			author = comment.author.name
			team = comment.body.split(' ')[2]
			amount = comment.body.split(' ')[3]
			print("username: ", author)
			print("Writing to ledger: " + team + " " + amount + " " + author + "\n")
			ledger.write(team + " " + amount + " " + author + "\n")

			oi_dict[team] += int(amount)
			adjustLines(oi_dict)
			
			#clear the contents of the file before each write
			open_interest_file.seek(0)
			open_interest_file.truncate()
			
			#write to the file
			for team in teams: 
				open_interest_file.write(team+" "+str(oi_dict[team])+"\n")
				
			response = "Your bet of: " + amount + " on " + team + " has been placed. Good luck!"			
	return response	

loadCache()

for comment in subreddit.stream.comments():
	if keyphrase in comment.body: 
		#try: 
			if comment.id not in comment_list:
				print("comment id,", comment.id, "judged unique")
				if isAction(comment): 
					#do the action
					reply = doAction(comment)
					comment.reply(reply)
					print('posted action:', comment.body.split(' ')[1] )
				else: 
					reply = "This is not a valid action"
					comment.reply(reply)
					print('posted no action')
				cacheComment(comment.id)
			#else: 
				#print("Already replied to comment", comment.id)
		#except: 
		#	print("An error occured.")
			
			
			
			
			
			