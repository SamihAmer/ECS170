from copy import deepcopy
import random
import time
import pygame
import math
import sys

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
		return deepcopy(env)

	def play(self, env, move):  #this is the "MINIMAX" function in the video, where we adjust our moves to actually do something (max_depth)
		self.Minimax(deepcopy(env), move, 5)

	def eval(self, env):   #this function is our evaluation function that we call in MIN and MAX 
		# if win return 1000
		# if lose return -1000
		# if tie return 0
		# return eval function if game is not done
		our_seq = [0,0,0]
		our_count = 0

		opp_seq = [0,0,0]
		opp_count = 0


		# rows
		for i in range(len(env.board)):
			for j in range(len(env.board[i])):
				if env.board[i][j] == 1: # change 1 as us, and 2 as opponent
					our_count += 1
					if opp_count != 0:
						opp_seq[opp_count - 1] += 1
					opp_count = 0
				elif env.board[i][j] == 2:
					opp_count += 1
					if our_count != 0:
						our_seq[our_count - 1] += 1
					our_count = 0
				else:
					print(our_count, opp_count)
					if our_count == 0 and opp_count == 0:
						continue
					elif our_count == 0 and opp_count != 0:
						opp_seq[opp_count - 1] += 1
						opp_count = 0
					elif our_count != 0 and opp_count == 0:
						our_seq[our_count - 1] += 1
						our_count = 0
		# columns
		

	def Minimax(self, env, move, max_depth):
		possible = env.topPosition >= 0 # possible is an array of seven True
		max_v = -math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.opponent.position) # move should be integer
			v = self.MIN(child, max_depth - 1, self.opponent.position)
			if v > max_v:
				max_v = v 
				move[:] = [move]
		return move

		
	def MAX(self, env, depth, player): #env is the board 

		if env.gameOver(env.history[0][-1], player) or depth == 0: # prev_move is integer of column of the last move
			return self.eval(env.board)

		possible = env.topPosition >= 0
		max_v = -math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.position) #simulatemove adding whoever turn it is to environment 
			max_v = max(max_v, self.MIN(child, depth - 1, self.opponent.position))
			print(max_v)
		return max_v

	
	def MIN(self, env, depth, player):
		
		if env.gameOver(env.history[0][-1], player) or depth == 0:
			return self.eval(env.board)

		possible = env.topPosition >= 0
		min_v = math.inf

		for move_index, p in enumerate(possible):
			if not p:
				continue
			child = self.simulateMove(deepcopy(env), move_index, self.opponent.position)
			min_v = min(min_v, self.MAX(child, depth - 1, self.position))
		print(min_v)
		return min_v 

	


class alphaBetaAI(connect4Player):

	def play(self, env, move):
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




