import sys, os
from constants import *
from utils.SpriteSheet import SpriteStripAnim

class SpiderBomb:

	FRAME_WIDTH = 16
	FRAME_HEIGHT = 16
	WARHEAD_WIDTH = 2
	WARHEAD_HEIGHT = 2
	FIRE_FRAMES = 4
	
	def __init__(self, screen, gravity):
		self.screen=screen
		self.gravity=gravity
		self.status=0; # 0=ready, 1=firing
		self.fireSpriteStrip = SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"spider_fire.png", (0, 0, SpiderBomb.FRAME_WIDTH, SpiderBomb.FRAME_HEIGHT), SpiderBomb.FIRE_FRAMES, -1, True, 1)	# Change every 1 cycle
		self.spiderFireSound = pygame.mixer.Sound(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"sounds"+os.sep+"spider_fire.ogg")
	
	def getWarheadX(self):
		return self.x+(SpiderBomb.FRAME_WIDTH/2)-(SpiderBomb.WARHEAD_WIDTH/2)
		
	def getWarheadY(self):
		return self.y+(SpiderBomb.FRAME_HEIGHT-SpiderBomb.WARHEAD_HEIGHT)
		
	def getY(self):
		return self.y
		
	def getSpiderId(self):
		return self.spiderId
		
	def readyToFire(self):
		return self.status==0
		
	def isFiring(self):
		return self.status==1

	def getDownwardsVelocity(self):
		return self.my
	
		
	def destroy(self):
		self.status = 0
	
	# x/y-initial pos,
	def fire(self, x, y, spiderId):
		self.x = x
		self.y = y
		self.spiderId = spiderId	# Can't kill itself
		self.my=0
		self.status=1
		self.spiderFireSound.play()

	def draw(self):		
		if self.status==1:
			self.my+=(self.gravity*.2)
			self.y+=self.my
			self.screen.blit(self.fireSpriteStrip.next(), (self.x, self.y))
			if (self.y>WINDOW_HEIGHT):
				self.status=0
