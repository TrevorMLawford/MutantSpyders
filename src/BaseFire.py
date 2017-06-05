import sys, os
from constants import *
from utils.SpriteSheet import SpriteStripAnim

class BaseFire:

	FRAME_WIDTH=8
	FRAME_HEIGHT=16
	WARHEAD_WIDTH=2
	WARHEAD_HEIGHT=2
	FIRE_FRAMES=8
	MOMENTUM=[7,10,12,14,15.5,17,18.3,19.5,20.5,22, 23,24,25,26,26.5,27.5,28,29,30,31]	# Momentum for Gravity .1->2step .1
	
	def __init__(self, screen, gravity):
		self.screen=screen
		self.gravity=gravity
		self.momentum=BaseFire.MOMENTUM[int(gravity*10)-1]
		self.status=0; # 0=ready, 1=firing
		self.upSpriteStrip = SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"base_fire.png", (0, 0, BaseFire.FRAME_WIDTH, BaseFire.FRAME_HEIGHT), BaseFire.FIRE_FRAMES, -1, True, 1)	# Change every 1 cycle
		self.downSpriteStrip = SpriteStripAnim(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"base_fire.png", (0, BaseFire.FRAME_HEIGHT, BaseFire.FRAME_WIDTH, BaseFire.FRAME_HEIGHT), BaseFire.FIRE_FRAMES, -1, True, 1)	# Change every 1 cycle
		
	def getWarheadX(self):
		return self.x+(BaseFire.FRAME_WIDTH/2)-(BaseFire.WARHEAD_WIDTH/2)
		
	def getWarheadY(self):
		if self.moveUp:
			return self.y
		else:
			return self.y+(BaseFire.FRAME_HEIGHT-BaseFire.WARHEAD_HEIGHT)
		
	def getY(self):
		return self.y

	def getSidewaysMovement(self):
		if self.mx>0:
			return "R"
		elif self.mx<0:
			return "L"
		else:
			return None
		
	def readyToFire(self):
		return self.status==0
		
	def isFiring(self):
		return self.status==1
		
	def isFiringDown(self):
		return self.status==1 and not self.moveUp
		
	def destroy(self):
		self.status=0
		
	def getDownwardsVelocity(self):
		return -self.yv
	
	# x/y-initial pos, mx,my-initial extra momentum
	def fire(self, x, y, mx, my):
		self.x=x
		self.y=y
		self.mx=mx
		self.my=my
		self.status=1;
		self.moveUp=True
		self.yv=self.momentum; # Vertical speed for initial momentum of Base Ship Fire(y=y-this)
		# Counteract sideways on first draw		
		self.x-=self.mx;
		self.y+=self.my;

	
	def draw(self):		
		if self.status==1:
			self.x+=self.mx;			
			self.y-=(self.my+self.yv);			
			self.yv-=self.gravity;	# Gravity affects vertical velocity
			if self.yv<0:
				self.moveUp=False
			if self.moveUp:
				self.screen.blit(self.upSpriteStrip.next(), (self.x, self.y))
			else:
				self.screen.blit(self.downSpriteStrip.next(), (self.x, self.y))
			if self.y>(WINDOW_HEIGHT - BaseFire.FRAME_HEIGHT):
				self.status=0
				return False
			#pygame.draw.rect(self.screen, (0,255,0), (self.getWarheadX(), self.getWarheadY(), BaseFire.WARHEAD_WIDTH, BaseFire.WARHEAD_HEIGHT), 1);
			return True
		else:
			return False
