import pygame, random, math, time

class mdp:
	def __init__(self):
		
		self.ball_x = 0.5 * 500
		self.ball_y = 0.5*500
		self.velocity_x = 0.03*500
		self.velocity_y = 0.01*500
		self.paddle_h = 0.2*500
		self.paddle_y = 0.5*500 - self.paddle_h/2
		self.action = [-0.04*500, 0, 0.04*500]
	def update(self, action):
		
		# update paddle position
		self.paddle_y += self.action[action]
		
		self.paddle_y = max(0, min(1*500 - self.paddle_h, self.paddle_y))
		# update ball position
		self.ball_x += self.velocity_x
		self.ball_y += self.velocity_y
		
		# top wall
		if self.ball_y < 0: 
			self.ball_y = -self.ball_y
			self.velocity_y = -self.velocity_y
		# bottom wall
		if self.ball_y > 1*500:
			self.ball_y = 2*500 - self.ball_y
			self.velocity_y = -self.velocity_y
		
		# left wall
		if self.ball_x < 0:
			self.ball_x = -self.ball_x
			self.velocity_x = -self.velocity_x
		
		# nothing happens
		if self.ball_x < 1*500: 
			return 0
					
		# miss paddle -> ggwp
		if self.ball_x > 1*500 and (self.ball_y < self.paddle_y or self.ball_y > self.paddle_y + 0.2*500): return -1
		
		# hit paddle -> nice
		else:
			self.ball_x = 2 * 1*500 - self.ball_x
			orig_velocity_x = self.velocity_x
			self.velocity_x = -self.velocity_x + random.uniform(-0.015*500, 0.015*500)
			self.velocity_y = -self.velocity_y + random.uniform(-0.03*500, 0.03*500)
			while abs(self.velocity_x) <= 0.03*500: 
				self.velocity_x = -orig_velocity_x + random.uniform(-0.015*500, 0.015*500)
			return 1
	
	def state_converter(self):
		# treat entire board as 12x12
		# each row or col has 12 states that are 0-1(11) and >1
		
		ballx_state = int(math.floor(self.ball_x/500 * 12))
		bally_state = int(math.floor(self.ball_y/500 * 12))
		
		# velocity_x state(positive or negative direction)
		if self.velocity_x > 0: velocityx_state = 1
		else: velocityx_state = -1
		
		# velocity_y state(positive or negative direction)
		if abs(self.velocity_y) < 0.015*500: velocityy_state = 0
		elif self.velocity_y > 0: velocityy_state = 1
		else: velocityy_state = -1
		
		# paddle_y state
		if self.paddle_y == 1*500 - 0.2*500: paddley_state = 11
		else: paddley_state = math.floor(12 * self.paddle_y/(1*500 - 0.2*500))	
		
		return (ballx_state, bally_state, velocityx_state, velocityy_state, paddley_state)



class pong:
	def __init__(self, train_times, alpha, gamma, epsilon):
		self.train_times = train_times
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon	
		self.action = [-0.04*500, 0, 0.04*500]
		self.policy = {}
		self.mdp = mdp()
		self.training()
	


	def get_actions(self, state):
		if state not in self.policy: self.policy[state] = [0, 0, 0]
		return self.policy[state]

	def set(self, action, state, value):
		self.policy[state][action] = value
		
		
	def exploration(self, state):
		# epsilon greedy approach
		actions = self.get_actions(state)
		
		if random.random() < self.epsilon:
			random_action = random.randint(0, 2)
			return actions[random_action], random_action
		else:
			return max(actions), actions.index(max(actions))

	def play_game(self):
		bounce = 0

		while True:
			# Get current state and an action
			state = self.mdp.state_converter()

			value, action = self.exploration(state)


			reward = self.mdp.update(action)

			# Gather information about the new state
			new_state = self.mdp.state_converter()
			future_value, _ = self.exploration(new_state)

			# Estimate new value
			new_value = value + self.alpha * (reward + self.gamma * future_value - value)

			self.set(action, state, new_value)

			# Missed
			if reward == -1:
			    return bounce

			bounce += reward

	def training(self):

		print ('Training ', self.train_times)

		for x in range(1, self.train_times + 1):
			self.play_game()
			self.mdp = mdp()

		print ("finish training, now testing 10K games")
		
		performance = 0.0
		for x in range(10000):
			performance += self.play_game() / 10000.0
			self.mdp = mdp()

		print ('Average rebouce over 10K games: ', performance)
		return self.policy


class AI_Paddle(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.xpos = 500
		self.actions = [-0.04*500, 0, 0.04*500]
		self.image =  pygame.Surface((10, 100))
		self.rect = self.image.get_rect()
		self.rect.topright = (self.xpos, 200)
		self.image.fill(pygame.Color("white"))
		self.train = pong(100000, 0.4, 0.95, 0.04)
		self.policy = self.train.policy
	
	def get_state(self, ball_x, ball_y, velocity_x, velocity_y, paddle_y):
		# treat entire board as 12x12
		# each row or col has 12 states that are 0-1(11) and >1
		
		ballx_state = math.floor(ball_x/500 * 12)
		bally_state = math.floor(ball_y/500 * 12)
		
		# velocity_x state(positive or negative direction)
		if velocity_x > 0: velocityx_state = 1
		else: velocityx_state = -1
		
		# velocity_y state(positive or negative direction)
		if abs(velocity_y) < 0.015*500: velocityy_state = 0
		elif velocity_y > 0: velocityy_state = 1
		else: velocityy_state = -1
		
		# paddle_y state
		if paddle_y == 1*500 - 0.2*500: paddley_state = 11
		else: paddley_state = math.floor(12 * paddle_y/(1*500 - 0.2*500))	
		
		return (ballx_state, bally_state, velocityx_state, velocityy_state, paddley_state)	
	
	def get_actions(self, state):
		if state not in self.policy: self.policy[state] = [0, 0, 0]
		#print (self.policy[state])
		for i in range(0, len(self.policy[state])):
			if self.policy[state][i] == max(self.policy[state]): return i
		
	def update(self):
		global ball
		state_input = [ball.rect.right, ball.rect.top, ball.velocity_x, ball.velocity_y, self.rect.top]
		state = self.get_state(state_input[0], state_input[1], state_input[2], state_input[3], state_input[4])
		selected = self.get_actions(state)
		self.rect.centery = self.rect.centery + self.actions[selected]
		if self.rect.top <= 0: self.rect.top = 0
		if self.rect.bottom >= 500: self.rect.bottom = 500

class Ball(pygame.sprite.Sprite):
	def __init__(self, paddle):
		pygame.sprite.Sprite.__init__(self)

		self.velocity_x = 0.03 * 500
		self.velocity_y = 0.01 * 500
		self.paddle = paddle
		self.image = pygame.Surface((10,10))
		self.rect = self.image.get_rect(center = (250, 250))
		self.image.fill(pygame.Color("red"))
		
	def update(self):
		
		if self.rect.bottom >= 500: 
			self.rect.bottom = 2*500 - self.rect.bottom
			self.velocity_y = -self.velocity_y
			
		if self.rect.top <= 0:
			self.rect.top = -self.rect.top
			self.velocity_y = -self.velocity_y
			
		if self.rect.left <= 0:
			self.rect.left = -self.rect.left
			self.velocity_x = -self.velocity_x
			
		print (self.rect.right, self.rect.centery, self.paddle.rect.top, self.paddle.rect.bottom)	
			
		if self.rect.right >= 500 and self.rect.centery > self.paddle.rect.top and self.rect.centery < self.paddle.rect.bottom:			
			orig_velocity_x = self.velocity_x
			self.velocity_x = -self.velocity_x + random.uniform(-0.015*500, 0.015*500)
			self.velocity_y = -self.velocity_y + random.uniform(-0.03*500, 0.03*500)
			while abs(self.velocity_x) <= 0.03*500: 
				self.velocity_x = -orig_velocity_x + random.uniform(-0.015*500, 0.015*500)
			
			self.rect.right = 2*500 - self.rect.right				

		elif self.rect.right >= 500:
			print ("gg")
			start_game()	

			#return 1
		self.rect.move_ip(self.velocity_x, self.velocity_y)


def start_game():
	global ball, sprites
	ball = Ball(computer)
	sprites = pygame.sprite.RenderPlain((computer, ball))
  



pygame.init()
# game setup
computer = AI_Paddle()
ball = Ball(computer)

sprites = pygame.sprite.RenderPlain((computer, ball))

# screen size
screen = pygame.display.set_mode((500,500))

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(pygame.Color("black"))

screen.blit(background, (0,0))
pygame.display.flip()
pygame.display.set_caption("part2.1: test trained AI")

clock = pygame.time.Clock()
running = True

# game loop
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: running = False

	clock.tick(50)
	pygame.event.pump()
	sprites.update()
	screen.blit(background,(0,0))
	sprites.draw(screen)
	pygame.display.flip()
	
	
pygame.quit()	