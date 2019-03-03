import requests
from bs4 import BeautifulSoup

class NBAGameScraper:

    def __init__(self):
        self.NBADictionary = {
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

    def scrapeGames(self, m, d, y):
        requestURL = 'https://www.basketball-reference.com/boxscores/?month='
        requestURL += str(m) + '&day=' + str(d) + '&year=' + str(y)
        page = requests.get(requestURL)
        pageContent = BeautifulSoup(page.content, 'html.parser')
        return pageContent.find_all(class_='teams')

    def createMatchList(self, games):
        matchList = []
        for game in games:
            gameText = game.getText()
            teams = self.getTeams(gameText)
        matchList.append(teams)
        return matchList

    def getTeams(self, gameText):
        replacements = {'\n':' ', 'LA Clippers':'LAClippers', 'LA Lakers':'LALakers',
            'Golden State':'GoldenState', 'New Orleans':'NewOrleans', 'New York':'NewYork',
            'Oklahoma City':'OklahomaCity', 'San Antonio':'SanAntonio'}
        for replacementKey in replacements:
            gameText = gameText.replace(replacementKey, replacements[replacementKey])
        gameText = gameText.split()
        homeTeam = self.NBADictionary[gameText[0]]
        awayTeam = self.NBADictionary[gameText[3]]
        return homeTeam + awayTeam

    def makeURL(self, date, teams):
        pattern = 'https://www.nba.com/games/[date]/[teams]#/video'
        output = pattern.replace('[date]', date).replace('[teams]', teams)
        return output
