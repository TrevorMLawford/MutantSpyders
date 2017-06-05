import sys, os, random
from constants import *
from utils.SpriteSheet import SpriteStripAnim
from utils.Collision import collision

class Spider:

	ID=1
	FRAME_WIDTH=32
	FRAME_HEIGHT=32
	HIT_BOUNDARY=8
	DESCEND_FRAMES=4
	FLY_FRAMES=3
	HIT_FRAMES=7
	CYCLES_PER_FRAMES=4
	FIRE_RESET=FPS

	def __init__(self, screen, x, y, descendSpeed):
		self.screen=screen
		self.x=x
		self.y=y	# Will start at top, descend on line, then fly off
		self.id = Spider.ID
		Spider.ID+=1
		self.status=0	# 0=init, 1=descending, 2=flying, 3=hit, 4=dead
		self.firing=0
		self.moveX=0
		self.moveY=0
		self.descSpriteStrip=SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"spider.png", (0, 0, Spider.FRAME_WIDTH, Spider.FRAME_HEIGHT), Spider.DESCEND_FRAMES, -1, True, Spider.CYCLES_PER_FRAMES)
		self.flySpriteStrip=SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"spider.png", (0, Spider.FRAME_HEIGHT,Spider.FRAME_WIDTH, Spider.FRAME_HEIGHT), Spider.FLY_FRAMES, -1, True, Spider.CYCLES_PER_FRAMES)
		self.hitSpriteStrip=SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"spider.png", (0, (Spider.FRAME_HEIGHT*2),Spider.FRAME_WIDTH, Spider.FRAME_HEIGHT), Spider.HIT_FRAMES, -1, False, Spider.CYCLES_PER_FRAMES)
		self.spiderStartSound = pygame.mixer.Sound(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"sounds"+os.sep+"spider_start.ogg")
		self.spiderLaunchSound = pygame.mixer.Sound(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"sounds"+os.sep+"spider_launch.ogg")
		self.spiderHitSound = pygame.mixer.Sound(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"sounds"+os.sep+"spider_hit.ogg")
		self.flyFrameCount=0
		self.hitFrameCount=0
		self.descendSpeed=descendSpeed
		self.weblen=random.randint(50, 250)
		self.beforeFlight = random.randint(1*FPS, 5*FPS)
		self.flight=0
		self.lastFired=0
		
	def draw(self):	
		if self.status==1:	# Descending
			pygame.draw.line(self.screen, (0,255,0), (self.x+Spider.FRAME_WIDTH/2, 0), (self.x+Spider.FRAME_WIDTH/2, self.y+10), 1)
			self.screen.blit(self.descSpriteStrip.next(), (self.x, self.y))
			if self.y<self.weblen:
				self.y+=self.descendSpeed
			else:
				self.beforeFlight-=1	# not moving
				if self.beforeFlight==0:
					self.beforeFlight=1
					self.status=2	# release
					self.spiderLaunchSound.play()			
				
		elif self.status==2:	# Flying
			self.screen.blit(self.flySpriteStrip.next(), (self.x, self.y))
			if self.beforeFlight>0:
				self.beforeFlight-=1	# not moving
				if self.beforeFlight==0:	# Now ready to move
					# Keep spider in-frame
					outside=False
					if self.x<-Spider.FRAME_WIDTH:
						self.moveX = random.randint(2, 8)
					elif self.x<WINDOW_WIDTH/2-Spider.FRAME_WIDTH/2:						
						self.moveX = random.randint(-3, 6)
					elif self.x<WINDOW_WIDTH-Spider.FRAME_WIDTH:
						self.moveX = random.randint(-6, 3)
					else:
						self.moveX = random.randint(-8, -2)
	
					if self.y<-Spider.FRAME_HEIGHT:						
						self.moveY = random.randint(2, 7)
					elif self.y<WINDOW_HEIGHT/4-Spider.FRAME_HEIGHT/2:						
						self.moveY = random.randint(-3, 5)
					elif self.y<WINDOW_HEIGHT/2-Spider.FRAME_HEIGHT:
						self.moveY = random.randint(-5, 3)
					else:
						self.moveY = random.randint(-7, -2)
					self.flight = random.randint(FPS/4, FPS*2)					
			elif self.flight>0:
				self.flight-=1			# moving
				self.x += self.moveX
				self.y += self.moveY
				if self.x<-Spider.FRAME_WIDTH or self.x>WINDOW_WIDTH or self.y<-Spider.FRAME_HEIGHT or self.y>WINDOW_HEIGHT:					
					# Move outside screen area
					self.flight=0
					self.beforeFlight=1*FPS
			else:
				self.beforeFlight = random.randint(1*FPS, 3*FPS)
			self.lastFired+=1

		elif self.status==3:	# hit
			self.hitFrameCount+=1
			if self.hitFrameCount<=(Spider.HIT_FRAMES*Spider.CYCLES_PER_FRAMES):
				self.screen.blit(self.hitSpriteStrip.next(), (self.x, self.y))
			else:
				self.hitSpriteStrip.iter()
				self.status=4
				
		if self.firing>0:
			self.firing-=1
		# pygame.draw.rect(self.screen, (255,0,0), (self.x+Spider.HIT_BOUNDARY, self.y+Spider.HIT_BOUNDARY, Spider.FRAME_WIDTH-(Spider.HIT_BOUNDARY*2), Spider.FRAME_HEIGHT-(Spider.HIT_BOUNDARY*2)), 1);
	
	def getX(self):
		return self.x
	
	def getMidX(self):
		return self.x+(Spider.FRAME_WIDTH/2)
	
	def getY(self):
		return self.y
		
	def getMaxVelocity(self):
		return max(abs(self.moveX), abs(self.moveY))
		
	def isMovingLeft(self):
		return self.moveX>0
	
	def isMovingRight(self):
		return self.moveX<0
	
	# x/y top-left w/h=dimensions - Return points scored (1 for web, 5 for flying)
	def checkIfHit(self, x, y, w, h):
		result=0
		if self.status>0 and self.status<3 and collision(x, y, w, h, self.x+Spider.HIT_BOUNDARY, self.y+Spider.HIT_BOUNDARY, Spider.FRAME_WIDTH-(Spider.HIT_BOUNDARY*2), Spider.FRAME_HEIGHT-(Spider.HIT_BOUNDARY*2)):
			if self.status==1:
				result=1
			elif self.status==2:
				result=5
			self.status=3	# Hit animation
			self.hitFrameCount=0
			self.spiderHitSound.play()
			return result
		else:
			return result
			
	def isInit(self):
		return self.status==0
			
	def startDescending(self):
		self.status=1
		self.spiderStartSound.play()
			
	def readyToFire(self):
		return (self.status==2 and self.firing==0)
			
	def getLastFired(self):
		return self.lastFired
			
	def isFlying(self):
		return self.status==2 
		
	def isDead(self):
		return self.status==4 
		
	def isFiring(self):
		return self.firing>0
		
	def isVisible(self):
		return (self.status==1 or self.status==2) and self.x>0 and self.x<WINDOW_WIDTH-Spider.FRAME_WIDTH and self.y>0 and self.y<WINDOW_HEIGHT-Spider.FRAME_HEIGHT
			
	def fire(self):
		self.firing=Spider.FIRE_RESET
		self.lastFired=0
			
	def launchFireX(self):
		return self.x+8
			
	def launchFireY(self):
		return self.y+16
		
	def getId(self):
		return self.id;
