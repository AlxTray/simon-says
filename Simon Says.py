from tkinter import *
import random
import pickle

class SimonSays(Tk):
    def __init__(self, userName):
        super().__init__()

        # Default configuration for main window
        self.title("Simon Says")
        self.geometry("500x500")

        # Generates canvas on top of the main window
        # Will store all further objects
        self.simonCanvas = Canvas(self, bg="black", highlightthickness=0)
        self.simonCanvas.pack(fill="both", expand=True)

        #Attributes needed for the game
        self.round = 1 #Starting round; this will also be used to get the length of the pattern by adding 2
        self.loopCheck = -1
        self.afterID = None
        self.pauseCheck = True
        self.userName = userName
        self.highScoreDictionary = {}
        self.highScore = "N/A"
        self.patternArray = []
        self.coloursArray = ["Red", "Blue", "Green", "Yellow"]
        self.comparativeColourArray = {"Red":"#7d0000", "Green":"#005500", "Yellow":"#dba800", "Blue":"#000055"}

        self.centralCircle = self.simonCanvas.create_oval("100 100 400 400", fill="#999999", outline="#dddddd", width=2)
        # Generates ovals and text for the displaay of user high-score and round indicator
        self.simonCanvas.create_oval("-100 400 125 600", fill="#999999", outline="#dddddd", width=2)
        self.simonCanvas.create_oval("375 400 600 600", fill="#999999", outline="#dddddd", width=2)
        self.simonCanvas.create_text("50 450", text = "High-score", font="Roboto 10 underline bold")
        self.highScoreText = self.simonCanvas.create_text("50 475", text = self.highScore, font="Roboto 13 bold")
        self.simonCanvas.create_text("450 450", text = "Round", font="Roboto 10 underline bold")
        self.roundText = self.simonCanvas.create_text("450 475", text = self.round, font="Roboto 13 bold")
        self.informationText = self.simonCanvas.create_text("250 250", font="Roboto 15 bold", text="Watch...", fill="#444444")

        # Generates the 4 coloured circles within the canvas
        self.redCircle = self.simonCanvas.create_oval("200 75 300 175", fill="black", outline="red", width=4, tags="Red")
        self.greenCircle = self.simonCanvas.create_oval("75 200 175 300", fill="black", outline="green", width=4, tags="Green")
        self.yellowCircle = self.simonCanvas.create_oval("200 325 300 425", fill="black", outline="yellow", width=4, tags="Yellow")
        self.blueCircle = self.simonCanvas.create_oval("325 200 425 300", fill="black", outline="blue", width=4, tags="Blue")

        self.retrieveHighScore()
        self.generatePattern()

    def generatePattern(self, restarted=False):
        """Generates a random array of X number of colours"""
        
        # Only comes here if the game has been restarted after losing
        if restarted:
            self.round = 1
            self.simonCanvas.itemconfig(self.roundText, text=self.round)
            self.simonCanvas.unbind("<Return>")
            self.simonCanvas.itemconfig(self.informationText, text="Watch...", font="Roboto 15 bold", width=150, justify="center")

        self.patternArray = []
        self.loopCheck = -1
        self.pauseCheck = True
        # Repeats for an amount that is 2 plus the current round
        # If the user was on round 3; 5 colours would be generated
        for _ in range(self.round + 2):
            self.patternArray.append(random.choice(self.coloursArray))

        print(self.patternArray)
        self.showPattern()

    def showPattern(self):
        """Shows the generated pattern using the circles"""

        if self.pauseCheck:
            self.loopCheck += 1
        # Starts checking user input once the pattern has completed
        if self.loopCheck == (self.round + 2):
            self.simonCanvas.after_cancel(self.afterID)
            self.afterID = None
            self.checkUserInput()
            return

        item = self.patternArray[self.loopCheck]
        # Fills the current circle with its inner colour
        if self.pauseCheck:
            self.simonCanvas.itemconfig(item, fill=self.comparativeColourArray[item])
        else:
            self.simonCanvas.itemconfig(item, fill="Black")
        self.pauseCheck = not self.pauseCheck

        # Recurses after a second
        self.afterID = self.simonCanvas.after(1000, self.showPattern)

    def checkInputAgainstSequence(self, input):
        """Checks which key the user pressed against the current item in the sequence"""

        # Removes the front element from the list if it matches input
        if self.patternArray[0] == input:
            self.patternArray.pop(0)
            self.selectionCorrect()
        else:
            self.selectionWrong()

    def selectionCorrect(self):
        """If a selection is correct then input will be reset here until the pattern is done"""

        # Goes here if the entirety of the pattern has been repeated back correctly
        if self.patternArray == []:
            # Flashes the central circle green and tells the user that that input was correct
            self.simonCanvas.itemconfig(self.informationText, text="Correct!")
            self.simonCanvas.itemconfig(self.centralCircle, fill="#00AA00")
            self.simonCanvas.update_idletasks()
            self.simonCanvas.after(500)
            self.simonCanvas.itemconfig(self.centralCircle, fill="#999999")
            self.simonCanvas.update_idletasks()
            self.simonCanvas.after(1500)
            self.simonCanvas.itemconfig(self.informationText, text="Watch...")

            self.round += 1
            self.simonCanvas.itemconfig(self.roundText, text=self.round)
            self.generatePattern()
        # Goes here if an input was correct but hasnt finished the entire pattern yet
        else:
            self.checkUserInput()

    def selectionWrong(self):
        """If any selection is wrong it will come here and restart the game"""

        self.patternArray = []
        # Flashes the central circle red and tells the user that that input was incorrect
        self.simonCanvas.itemconfig(self.informationText, text="Incorrect.")
        self.simonCanvas.itemconfig(self.centralCircle, fill="#AA0000")
        self.simonCanvas.update_idletasks()
        self.simonCanvas.after(500)
        self.simonCanvas.itemconfig(self.centralCircle, fill="#999999")
        self.simonCanvas.update_idletasks()
        self.simonCanvas.after(1500)
        # Allows the user to restart from round 1 if they press return
        self.simonCanvas.itemconfig(self.informationText, text="Press Enter to Restart.", font="Roboto 13 bold", width=150, justify="center")
        self.saveHighScore()
        self.retrieveHighScore()
        self.simonCanvas.bind("<Return>", lambda re: self.generatePattern(True))


    def keyPress(self, input):
        """Completes an action depending which key was pressed"""

        # Stops the users input so hey can only press the key once
        self.simonCanvas.unbind("<Left>")
        self.simonCanvas.unbind("<Right>")
        self.simonCanvas.unbind("<Down>")
        self.simonCanvas.unbind("<Up>")
        self.checkInputAgainstSequence(input)

    def checkUserInput(self):
        """Checks which arrow key the user presses"""

        self.simonCanvas.itemconfig(self.informationText, text="Repeat!")

        self.simonCanvas.bind("<Left>", lambda key: self.keyPress("Green"))
        self.simonCanvas.bind("<Right>", lambda key: self.keyPress("Blue"))
        self.simonCanvas.bind("<Down>", lambda key: self.keyPress("Yellow"))
        self.simonCanvas.bind("<Up>", lambda key: self.keyPress("Red"))
        # Sets focus to the Simon Says window so keyboard prsses are recorded to this window
        self.simonCanvas.focus_set()

    def saveHighScore(self):
        """Updates the highScore dictionary and pickles it to a .dat file"""
        
        # Only saves the high-score if it greater than one already saved
        if self.highScore == "N/A" or self.highScore < self.round:
            self.highScoreDictionary.update({self.userName: self.round})
            with open("highscore.dat", "wb") as highScoreFile:
                pickle.dump(self.highScoreDictionary, highScoreFile)
                highScoreFile.close()

    def retrieveHighScore(self):
        """Unpickles the high-score disctionary so a high-score can be retrieved"""

        # Retreives the dictionary from the .dat file
        with open("highscore.dat", "rb") as highScoreFile:
            self.highScoreDictionary = pickle.load(highScoreFile)
            highScoreFile.close()
        
        # Makes sure that it only sets the high-score if one can be found
        try:
            self.highScore = self.highScoreDictionary[self.userName]
        except KeyError:
            print("No high-score found for this username.")
        finally:
            self.simonCanvas.itemconfig(self.highScoreText, text=self.highScore)


if __name__ == "__main__":
    userName = input("Please enter a user-name (This will be used to save/retrieve high-scores)")
    print("Information: when repeating back a pattern, use the arrow keys on your keyboard.")
    simonSays = SimonSays(userName)
    simonSays.mainloop()