import sys, os
from constants import *
from utils.SpriteSheet import SpriteStripAnim
from utils.Collision import collision

class Base:

	FRAME_WIDTH=32
	FRAME_HEIGHT=32
	HIT_BOUNDARY=2
	FIRE_FRAMES=5
	HIT_FRAMES=6
	HIT_DURATION=30
	
	MIN_X=0
	MAX_X=WINDOW_WIDTH-32 #-Base.FRAME_WIDTH
	MIN_Y=250
	MAX_Y=WINDOW_HEIGHT-32 #-Base.FRAME_HEIGHT

	def __init__(self, screen, x, y, reloadTime):
		self.screen=screen
		self.x=x
		self.y=y
		self.reloadTime=reloadTime

		self.status=0;	# 0=std, 1=firing, 2=hit, 3=no draw after Hit
		stdSpriteStrip=SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"base_ship.png", (0, 0, Base.FRAME_WIDTH, Base.FRAME_HEIGHT), (Base.FIRE_FRAMES+1), -1, False, 1)
		self.frame1=stdSpriteStrip.next()
		self.frames = [
			stdSpriteStrip.next(),
			stdSpriteStrip.next(),
			stdSpriteStrip.next(),
			stdSpriteStrip.next(),
			stdSpriteStrip.next(),
		]
		self.fireFrameCycle=0
		self.fireFrameNo=0
		self.hitSpriteStrip=SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"base_ship.png", (0, Base.FRAME_HEIGHT, Base.FRAME_WIDTH, Base.FRAME_HEIGHT), (Base.HIT_FRAMES), -1, True, 1)
		self.baseHitSound = pygame.mixer.Sound(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"sounds"+os.sep+"base_hit.ogg")
		self.baseFireSound = pygame.mixer.Sound(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"sounds"+os.sep+"base_fire.ogg")
		self.hitDurationCount=0
		self.reloadTimer=self.reloadTime
		
	def getCentreX(self):
		return self.x+(Base.FRAME_WIDTH/2)
		
	def draw(self, newX, newY):
		if self.status<2:
			self.x=newX
			self.y=newY
		if self.status==0:
			self.frame = self.frame1
		elif self.status==1:
			self.fireFrameNo+=1
			if self.fireFrameNo==Base.FIRE_FRAMES: # Reached end of firing cycle
				self.status=0
				self.fireFrameNo=0
			else:
				self.frame = self.frames[self.fireFrameNo]
		elif self.status==2:
			self.frame = self.hitSpriteStrip.next()
			self.hitDurationCount+=1
			if self.hitDurationCount>Base.HIT_DURATION:
				self.hitDurationCount=0
				self.status=3	# No draw for a while
		elif self.status==3:
			return
		self.screen.blit(self.frame, (self.x, self.y))
		
		if self.reloadTimer<self.reloadTime:
			self.reloadTimer+=1			
		
	# After all BaseFire finished when base hit
	def reStart(self, x, y):
		self.x=x
		self.y=y
		self.status=0
		
	def fire(self):
		if self.status==0 and self.reloadTimer==self.reloadTime:
			self.reloadTimer=0
			self.status=1
			self.frame = self.frames[0]
			self.baseFireSound.play()
			
	def readyToFireLeft(self):
		return self.status==1 and self.fireFrameNo==1
	
	def readyToFireRight(self):
		return self.fireFrameNo==3
		
		# x/y top-left w/h=dimensions
	def checkIfHit(self, x, y, w, h):
		if self.status<2 and collision(x, y, w, h, self.x+Base.HIT_BOUNDARY, self.y+Base.HIT_BOUNDARY, Base.FRAME_WIDTH-(Base.HIT_BOUNDARY*2), Base.FRAME_HEIGHT-(Base.HIT_BOUNDARY*2)):
			self.status=2
			self.reloadTimer=0
			self.fireFrameNo=0
			self.baseHitSound.play()
			return True
		else:
			return False
			
	def hitAllowed(self):
		if self.status<2:
			self.status=2
			self.baseHitSound.play()
			return True
		else:
			return False
		
