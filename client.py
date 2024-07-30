import pygame
import sys
from player import Player
from network import Network
from game import excerpts
import random

pygame.init()
width = 600
height = 600
userLoc = [50, 550]
oppLoc = [450, 50]
userHealthBarLoc = [225, 340]
opponentHealthBarLoc = [225, 240]
nextWordLoc = [225, 380]
GREEN = (255, 127, 127)
RED = (118, 242, 104)
AQUA = (0, 175, 185)
LIGHTRED = (240, 113, 103)
SAIL = (254, 217, 183)
LIGHTYELLOW = (253, 252, 220)
window = pygame.display.set_mode((width, height))
minecraftFont = pygame.font.Font("Monocraft.ttf", 20)
lunchFont = pygame.font.Font("lunchds.ttf", 30)
font = minecraftFont
pygame.display.set_caption("Client")


def redrawWindow(window, user, opponent, n):
    window.fill(SAIL)


    # Health = font.render(str(user.getHealth()), False, (255, 255, 255))
    # window.blit(Health, (255, 30))

    WordCount = lunchFont.render(str(user.getChangingWordCount()), False, (255, 255, 255)) # Prints woudcount to middle of the screen
    Combo = lunchFont.render("x" + str(user.getCombo()), False, (255, 255, 255))
    window.blit(WordCount, (290, 280))
    window.blit(Combo, (280, 310))



    user.typing()
    user.addIncome(opponent.getOutcome())
    user.drawWords(window, font, userLoc)
    user.drawNextWord(window, font, nextWordLoc)
    opponent.drawWords(window, font, oppLoc)
    user.drawHealthBar(window, userHealthBarLoc)
    opponent.drawHealthBar(window, opponentHealthBarLoc)
    user.drawIncome(window, font)
    user.drawOutcome(window, font, opponent.getPointer())
    user.watchIncoming(opponent.getCombo())
    user.checkHealth(opponent.getHealth())
    user.checkWordCount() # Checks if you typed all words
    user.win(n) # Checks if theres a winner
    if opponent.getDeleted() is not None: # Checks if theres words to delete and deletes them
        try:
            if user.getOutcome()[0][0] == opponent.getDeleted()[0]:
                user.safeDeleteOutcome()
        except:
            pass



    
    pygame.display.update()



def waitingMenu():
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    waiting = "Waiting..."
    for i in range(len(waiting)):
        LoadingText = font.render(waiting[:i + 1], False, (255, 255, 255))
        window.blit(LoadingText, (250, 280))
        pygame.display.update()
        pygame.time.delay(200)


def endScreen(winner, n):
    
    window.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("pressed reset")
                n.send("reset")
        
    waiting = "WINNER" if winner else "LOSER"
    for i in range(len(waiting)):
        LoadingText = font.render(waiting[:i + 1], False, (255, 255, 255))
        window.blit(LoadingText, (250, 280))
        pygame.display.update()
        pygame.time.delay(200)


def sample():
    window.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    LoadingText = font.render("sample", False, (0, 0, 0))
    window.blit(LoadingText, (250, 280))
    pygame.display.update()
    pygame.time.delay(200)


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()
    p = n.getP()
    color = p.getColor()
    while run:
        clock.tick(60)        
        p2 = n.send(p)
        game = n.send("getGame")

        if not game.connected():
            waitingMenu()
        else:
            if game.reset:
                game = n.send("unreset")
                p = Player(50, 550, color, game.text)
                pygame.time.delay(1000)

            elif game.winner:
                endScreen(p.getWinner(), n)
            else:
                redrawWindow(window, p, p2, n)

main()