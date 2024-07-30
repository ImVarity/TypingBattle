import pygame
pygame.init()

MISCLICK_SFX = pygame.mixer.Sound("click.mp3")
CORRECT_CLICK_SFX = pygame.mixer.Sound("click2.mp3")

class Player():
    def __init__(self, x, y, color, text):
        self.x = x
        self.y = y
        self.winner = False
        self.focusColor = color
        self.passiveColor = (255, 255, 255)
        self.catchColor = self.passiveColor
        self.shootColor = self.focusColor
        self.healthBarColor = color
        self.shoot = True
        self.catch = False
        self.velocity = 1
        self.words = text
        self.currentWord = self.words[0]
        self.wordCount = len(self.words)
        self.outcome = []
        self.income = []
        self.incomingWord = ""
        self.delpointer = 0
        self.originalHealth = self.getOriginalWordCount() * 6 // 4
        self.health = self.getOriginalHealth()
        self.combo = 1
        self.isLast = False
        self.counter = 0
        self.deleted = None
        self.clearedOutcome = False


    """
    Draws the current word that the user is typing
    """
    def drawWords(self, window, font, loc):

        current = font.render(self.currentWord, False, self.shootColor)
        window.blit(current, (loc[0], loc[1]))

    """
    Draws the next word that the user is typing to below their health bar
    """
    def drawNextWord(self, window, font, next):
        if len(self.words) > 1:
            middle = font.render(self.words[1], False, self.shootColor)
            window.blit(middle, (next[0], next[1]))


    """
    Draws a health bar given a window and loc
    """
    def drawHealthBar(self, window, loc):
        pygame.draw.rect(window, self.healthBarColor, (loc[0], loc[1], (self.health / self.originalHealth) * 150, 30))


    """
    Draws the words that are incoming
    """
    def drawIncome(self, window, font):
        for i in range(self.delpointer, len(self.income)):
            if i == self.delpointer: # Draws the first word so you can see the letters disappear when typing
                text = font.render(self.incomingWord, False, self.catchColor)
                window.blit(text, (450, self.x + self.income[i][2]))
                self.income[i][2] += self.velocity
                continue
            text = font.render(self.income[i][0], False, self.catchColor)
            window.blit(text, (450, self.x + self.income[i][2]))
            self.income[i][2] += self.velocity

    
    """
    Draws the words that are being shot
    """
    def drawOutcome(self, window, font, pointer):
        for i in range(pointer, len(self.outcome)):
            text = font.render(self.outcome[i][0], False, self.shootColor)
            window.blit(text, (self.x, self.y - self.outcome[i][2]))
            self.outcome[i][2] += self.velocity

    

    def setWords(self, text):
        self.words = text
        self.wordCount = len(self.words)
        self.originalHealth = self.getOriginalWordCount() * 6 // 4
        
    """
    Takes in the outcome of other opponent and takes it as income
    """
    def addIncome(self, outcome):
        try:
            if self.isLast:
                if self.counter < 3:
                    self.counter += 1
                    return
                self.counter = 0
                self.isLast = False
                return
            if len(outcome) > len(self.income):
                last_outcome = outcome[-1]  # Get the last element of the outcome list
                inside = False
                for sub_list in self.income:
                    if last_outcome == sub_list:  # Check if the last outcome sublist is equal to a sublist in self.income
                        inside = True
                if not inside:
                    self.income.append(last_outcome)
                    self.setIncomingWord()
            if len(outcome) < len(self.income):
                self.income.pop(-1)
        except:
            pass

    """
    If the incoming word is empty this method fills it if there are incoming words
    Usually only happens in the beginning
    """
    def setIncomingWord(self):
        if self.incoming() and self.incomingWord == "":
            self.incomingWord = self.income[self.delpointer][0]
    
    
    """
    Removes the word that is being shot from the word bank and adds it to outcome
    """
    def dequeue(self):
        self.outcome.append([self.words[0], self.x, 0, len(self.words[0])])
        self.words.pop(0)
        try:
            self.currentWord = self.words[0]
        except:
            pass

    """
    Moves current word to next word after typing it
    """
    def finishedWord(self):
        if len(self.income) == 1:
            self.isLast = True
        self.popper()
        self.setIncomingWord()


    """
    Saves the word that is to be deleted to a variable and pops it from its list
    """
    def popper(self):
        self.deleted = self.income[0]
        self.income.pop(0)

    
    """
    Handles the incoming words that pass the point of deletion
    Moves the deletion pointer accordingly
    """
    def watchIncoming(self, combo):
        if self.isLast:
            if self.counter < 5:
                self.counter += 1
                return
            self.counter = 0
            self.isLast = False
        for i in range(len(self.income)- 1, -1, -1):
            if self.income[i][2] > 550:
                if i == 0:
                    self.isLast = True
                self.health -= self.income[i][3] * combo
                print(self.income[i][3])
                self.popper()
                try: # Fixed a glitch where the incoming word is different from outcoming
                    if self.income[self.delpointer] is not None:
                        self.incomingWord = self.income[self.delpointer][0]
                except:
                    self.incomingWord = ""





    """
    Checks the health of the player to see if they won
    """
    def checkHealth(self, oppHealth):
        if oppHealth <= 0:
            self.winner = True

    """
    Sets the player as the winner and sends that to the Network
    """
    def win(self, n):
        if self.winner == True:
            n.send("winner")

    """
    Checks if the player typed all the words to see if they won
    """
    def checkWordCount(self):
        if self.getChangingWordCount() <= 0:
            self.winner = True

    """
    Deletes the words that have already passed the point of deletion
    """
    def safeDeleteOutcome(self):
        self.outcome.pop(0)

    
    """
    Changes the focus color to whether the user is "shooting" words or "catching" words
    """
    def focus(self):
        if self.shoot:
            self.shootColor = self.focusColor
            self.catchColor = self.passiveColor
        
        if self.catch:
            self.catchColor = self.focusColor
            self.shootColor = self.passiveColor


    
    """
    Returns true if the pointer is smaller than the length of the income list
    """
    def incoming(self):
        return len(self.income) > 0
    
    """
    Subtracts damage given from the players health
    """
    def takeDamage(self, damage):
        self.health -= damage



    """
    Get functions
    """
    def getDeleted(self):
        return self.deleted

    def getWinner(self):
        return self.winner

    def getPointer(self):
        return self.delpointer

    def getOutcome(self):
        return self.outcome
    
    def getIncome(self):
        return self.words
    
    def getOriginalHealth(self):
        return self.originalHealth

    def getChangingWordCount(self):
        return len(self.words)

    def getOriginalWordCount(self):
        return self.wordCount

    def getCombo(self):
        return self.combo

    def getHealth(self):
        return self.health

    def getColor(self):
        return self.healthBarColor

    """
    Handles the typing of each character from the user
    """
    def typing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                key_mappings = {
                    97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g',
                    104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n',
                    111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u',
                    118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z', pygame.K_RETURN: 'enter',
                    pygame.K_SPACE: 'space'
                }

                if event.key in key_mappings:
                    letter = key_mappings[event.key]
                    if letter == 'enter':
                        self.shoot = not self.shoot
                        self.catch = not self.catch
                        CORRECT_CLICK_SFX.play() # Sound when pressing enter
                    elif self.currentWord[0] == letter and self.shoot:
                        self.currentWord = self.currentWord[1:]
                        self.combo += .01
                        self.combo = round(self.combo, 2)
                        CORRECT_CLICK_SFX.play() # Sound when shooting
                    elif self.incoming() and self.incomingWord[0] == letter and self.catch:
                        self.incomingWord = self.incomingWord[1:]
                        self.combo += .01
                        self.combo = round(self.combo, 2)
                        CORRECT_CLICK_SFX.play() # Sound when catching
                    else:
                        self.combo = 1
                        MISCLICK_SFX.play() # Sound when making a mistake
                    self.focus() # Changes the colors after checking if user pressed enter
                    

                if len(self.currentWord) < 1: 
                    self.dequeue()
                if self.incoming() and len(self.incomingWord) < 1:
                    self.finishedWord()