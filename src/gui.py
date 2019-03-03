from tkinter import *
from webscraper import NBAGameScraper
import re
from ttkcalendar import Calendar

class GameID:
    def __init__(self, game, month, day, year):
        self.month = month
        self.day = day
        self.year = year
        month = str(month)
        while len(month) < 2:
            month = '0'+month
        day = str(day)
        while len(day) < 2:
            day = '0'+day
        year = str(year)
        self.date = year + month + day
        self.team1 = self.processTeamName(game[0])
        self.team2 = self.processTeamName(game[3])
        self.team1Score = game[1]
        self.team2Score = game[4]

        self.gameString = month + '/' + day + '/' + year + ' | '
        self.gameString += self.team1 + ' (' + self.team1Score + ') vs ' + self.team2 + ' (' + self.team2Score + ')'
       
        self.url = None

    def processTeamName(self, teamname):
        return re.sub(r'\B([A-Z])', r' \1', teamname)

    def setURL(self, teams):
        pattern = 'https://www.nba.com/games/[date]/[teams]#/video'
        output = pattern.replace('[date]', self.date).replace('[teams]', teams)
        self.url = output


class NBAVideoApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidgets()

        self.webscraper = NBAGameScraper()
    
    def createWidgets(self):
        self.windowLabel = Label(self, text='NBA Highlight Reel', font=('Helvetica', 30))
        self.windowLabel.pack(side='top')

        self.datePicker = Calendar(self)
        self.datePicker.pack(side='top')

        self.detailedGameList = []
        self.gameScrollbar = Scrollbar(self)
        self.gameScrollbar.pack(side='right', fill=constants.Y)
        self.gameList = Listbox(self, height=20, width=60, selectmode=constants.MULTIPLE,
                            justify=constants.LEFT, yscrollcommand=self.gameScrollbar.set)
        self.gameList.pack(side='top')

        self.scrapeButton = Button(self, text="Grab Games", command=self.populateGameList)
        self.scrapeButton.pack(side='top')

        self.stitchButton = Button(self, text="Create Video", command=self.printGameList)
        self.stitchButton.pack(side='top')

    def insertGame(self, game, month, day, year):
        gameObj = GameID(game, month, day, year)
        gameObj.setURL(self.webscraper.getTeams(game))
        self.detailedGameList.insert(0, gameObj)
        self.gameList.insert(0, gameObj.gameString)

    def populateGameList(self):
        datetime = self.datePicker.selection
        dsl = str(datetime).split('-')
        year = int(dsl[0])
        month = int(dsl[1])
        dsl = dsl[2].split()
        day = int(dsl[0])
        games = self.webscraper.scrapeGames(month, day, year)
        for game in games:
            self.insertGame(game, month, day, year)

    def printGameList(self):
        values = [self.detailedGameList[idx] for idx in self.gameList.curselection()]
        for value in values:
            print(value.url)
        

if __name__ == '__main__':
    root = Tk()
    root.title('NBA Highlight Reel')
    root.geometry('800x800')

    app = NBAVideoApp(master=root)
    app.mainloop()