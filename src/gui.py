from tkinter import *
from webscraper import NBAGameScraper
import re
from ttkcalendar import Calendar
import os
import time
import random
from multiprocessing import Process

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

        self.detailedGameList = []
    
    def createWidgets(self):
        # Title Frame
        self.titleFrame = Frame(self)
        self.titleFrame.pack(side='top')
        self.windowLabel = Label(self.titleFrame, text='NBA HACKLIGHTS 19', font=('Helvetica', 30))
        self.windowLabel.pack(side='top', pady=50)

        # Game Scraper Frame
        self.gameScraperFrame = Frame(self)
        self.gameScraperFrame.pack(side='top')
        self.gameScrollbar = Scrollbar(self.gameScraperFrame)
        self.gameScrollbar.pack(side='right', fill=constants.Y)
        self.gameList = Listbox(self.gameScraperFrame, height=20, width=60, selectmode=constants.MULTIPLE,
                            justify=constants.LEFT, yscrollcommand=self.gameScrollbar.set, font=('Helvetica', 14))
        self.gameList.pack(side='right')

        # Option Frame
        self.optionFrame = Frame(self.gameScraperFrame)
        self.optionFrame.pack(side='left', padx=20)

        self.datePicker = Calendar(self.optionFrame)
        self.datePicker.pack(side='top', pady=20, fill=constants.BOTH)

        # Button Frame
        self.buttonFrame = Frame(self.optionFrame)
        self.buttonFrame.pack(side='top')

        self.scrapeButton = Button(self.buttonFrame, text="Grab Games", command=self.populateGameList)
        self.scrapeButton.pack(side='left', ipady=20, ipadx=30)

        self.stitchButton = Button(self.buttonFrame, text="Create Video", command=self.stitchVideo)
        self.stitchButton.pack(side='right', ipady=20, ipadx=30)

        # Working Frame
        self.workingFrame = Frame(self.optionFrame)
        self.workingFrame.pack(side='top')

        self.workingString = StringVar()
        self.workingString.set('')
        self.workingLabel = Label(self.workingFrame, textvariable=self.workingString, font=('Helvetica', 12))
        self.workingLabel.pack(side='top', pady=7)

        # Output Frame
        self.outputFrame = Frame(self)
        self.outputFrame.pack(side='top')

        self.outputLabel = Label(self.outputFrame, text='OUTPUT DIRECTORY', font=('Helvetica', 15))
        self.outputLabel.pack(side='top', pady=20)

        self.outputScrollbar = Scrollbar(self.outputFrame)
        self.outputScrollbar.pack(side='right', fill=constants.Y)
        self.outputList = Listbox(self.outputFrame, height=10, width=40, justify=constants.LEFT, yscrollcommand=self.outputScrollbar.set, font=('Helvetica', 14),
                                    selectmode=constants.SINGLE)
        self.outputList.pack(side='right')

        self.playVideoButton = Button(self.outputFrame, text='Play Highlight', command=self.playVideo)
        self.playVideoButton.pack(side='right', ipady=40, padx=5)

        self.refreshButton = Button(self.outputFrame, text='Refresh', command=self.updateOutput)
        self.refreshButton.pack(side='left', ipady=40, padx=5)

        self.updateOutput()

    def playVideoProcess(self):
        filename = self.outputList.get(constants.ACTIVE)
        os.system('vlc ' + './../highlights/' + filename)

    def playVideo(self):
        p = Process(target=self.playVideoProcess)
        p.start()

    def updateOutput(self):
        self.outputList.delete(0, 'end')
        for outputFile in os.listdir('./../highlights'):
            self.outputList.insert(0, outputFile)

    def updateWorkingString(self):
        print(os.getpid())
        self.after(5000, self.updateWorkingString)

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

    def stitchVideoProcess(self):
        urlFile = open('./../backend/urls.txt', 'w')
        values = [self.detailedGameList[idx] for idx in self.gameList.curselection()]
        for value in values:
            urlFile.write(value.url + '\n')
        urlFile.close()

        urlFile = open('./../backend/urls.txt', 'r')
        os.chdir('./../')
        i = 1
        for line in urlFile:
            line = line.replace('\n', '')
            name = 'output'
            name += str(i)
            i += 1
            cmd = 'python3 ./backend/addressresolution.py ' + line + ' ' + name
            print(cmd)
            os.system(cmd)

        urlFile.close()

    def stitchVideo(self):
        p = Process(target=self.stitchVideoProcess)
        p.start()

        

if __name__ == '__main__':
    root = Tk()
    root.title('NBA Highlight Reel')
    root.geometry('1000x900')

    app = NBAVideoApp(master=root)
    app.mainloop()