import sys
import requests
from bs4 import BeautifulSoup
NBA_dict = {
"Atlanta": "ATL",
"Brooklyn": "BKN",
"Boston": "BOS",
"Charlotte": "CHA",
"Chicago": "CHI",
"Cleveland": "CLE", 
"Dallas": "DAL",
"Denver": "DEN",
"Detroit": "DET",
"GoldenState": "GSW",
"Houston": "HOU",
"Indiana": "IND",
"LAClippers": "LAC",
"LALakers": "LAL",
"Memphis": "MEM",
"Miami": "MIA",
"Milwaukee": "MIL",
"Minnesota": "MIN",
"NewOrleans": "NOP",
"NewYork": "NYK",
"OklahomaCity": "OKC",
"Orlando": "ORL",
"Philadelphia": "PHI",
"Pheonix": "PHX",
"Portland": "POR",
"Sacramento": "SAC",
"SanAntonio": "SAS",
"Toronto": "TOR",
"Utah": "UTA",
"Washington": "WAS"
}

def get_games(m, d, y): #format mmddyyyy, no 0s on mmdd
	page = requests.get("https://www.basketball-reference.com/boxscores/?month="\
	+ str(m) +"&day="+ str(d) +"&year="+ str(y))
	cont = BeautifulSoup(page.content, 'html.parser')
	games = cont.find_all(class_="teams")
	n = 0 
	urls = ""
	pattern = "https://www.nba.com/games/[date]/[teams]#/video"
	month = str(m)
	while len(month) < 2:
		month = "0"+month
	day = str(d)
	while len(day) < 2:
		day = "0"+day
	year = str(y)
	date = year + month + day
	for i in games:
		text = games[n].getText()
		teams = games_iter(text)
		url = pattern.replace("[date]", date)
		url = url.replace("[teams]", teams)
		urls += url + "\n"
		n += 1
	print (urls)

def games_iter(txt):
	text = txt.replace("\n", " ")
	text = text.replace("LA Clippers", "LAClippers")
	text = text.replace("LA Lakers", "LALakers")
	text = text.replace("Golden State", "GoldenState")
	text = text.replace("New Orleans", "NewOrleans")
	text = text.replace("New York", "NewYork")
	text = text.replace("Oklahoma City", "OklahomaCity")
	text = text.replace("San Antonio", "SanAntonio")
	text = text.split()
	#print (text)
	h = NBA_dict[text[0]]
	a = NBA_dict[text[3]]
	return (h+a)

get_games(2, 28, 2019)