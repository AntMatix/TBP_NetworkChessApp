import pygame
import time

from data.classes.Board import Board
from server import refreshSrvBoard, open_cs2


from ZODB import DB
import transaction
from ZEO.ClientStorage import ClientStorage
from persistent.list import PersistentList





pygame.init()

screen = pygame.display.set_mode((800,800))

def refreshBoard(c):
	return refreshSrvBoard(c)

def setDisplayTitle(txt):
	pygame.display.set_caption(txt)

# Define connection to the server
c = open_cs2('localhost', 2709)
root = c.root()
board = refreshBoard(c)

white = (0,0,0)
black = (255,255,255)

def draw(display):
	display.fill(white)
	board.draw(display)
	pygame.display.update()


if __name__ == '__main__':
	running = True
	
	while running:
		if (board.turn == 'white'):
			setDisplayTitle("Your turn. Move white piece.")
			try:
				transaction.begin()
				mx, my = pygame.mouse.get_pos()
				for event in pygame.event.get():
					# Quit the game if the user presses the close button
					if event.type == pygame.QUIT:
						running = False
					elif event.type == pygame.MOUSEBUTTONDOWN: 
						# If the mouse is clicked
						if event.button == 1:
							board.handle_click(mx, my)
				if board.is_in_checkmate('black'): # If black is in checkmate
					setDisplayTitle("White wins")
					time.sleep(2.5)
					print('White wins!')
					running = False
				elif board.is_in_checkmate('white'): # If white is in checkmate
					setDisplayTitle("Black wins")
					time.sleep(2.5)
					print('Black wins!')
					running = False
				# Draw the board
				draw(screen)

				root['board'] = board
				transaction.commit()
			except:
				pass
		else:
			draw(screen)
			setDisplayTitle("Not your turn. Waiting for other player to make move.")
			#print(f"White waiting for turn. Current turn: {board.turn}")
			for event in pygame.event.get():
					# Quit the game if the user presses the close button
					if event.type == pygame.QUIT:
						running = False
			board = refreshBoard(c)
			
