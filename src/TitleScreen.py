import os, json
from constants import *
from pygame.locals import *

class TitleScreen:

	settingsFile=os.getcwd()+os.sep+"MutantSpyders"+os.sep+"data"+os.sep+"settings.json"
	
	def __init__(self, screen):
		self.screen=screen
		
		self.livesArr=[1,3,5,10]
		self.initLives=1
		
		self.totalSpidersArr=[0,1,2,3,5,10,20,30,50,75,100]
		self.initTotalSpiders=6
		
		self.gravityArr=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.5, 1.8, 2]
		self.initGravity=1
		
		self.waitSpiderAppearArr=[0, 10, 15, 20, 30, 40, 60, 90, 120]
		self.initWaitSpiderAppear=5
		
		self.waitSpiderFireArr=[0, 10, 15, 20, 30, 40, 60, 90, 120]
		self.initWaitSpiderFire=6
		
		self.maxSpiderFireArr=[0, 10, 20, 30]
		self.initMaxSpiderFire=1
		
		self.reloadTimeArr=[0, 5, 10, 15, 20, 30, 60, 120, 9999]
		self.initReloadTime=3
		
		self.godModeArr=[False, True]
		self.initGodMode=0
		
		self.autoPlayArr=["No", "Yes", "Visual"]
		self.initAutoPlay=0
		
		self.keyPress=0
		self.textFont = pygame.font.SysFont("", 30)		
		
	#Draw the title page and allow user to set variables
	def draw(self):
		quit=False
		self.screen.fill((0,0,0))
		
		titleFont = pygame.font.SysFont("", 40, True, False)	# Bold, Italic
		titleFont.set_underline(True)
		smallTextFont = pygame.font.SysFont("", 25, False, True)

		self.screen.blit(titleFont.render("Mutant Spyders", 1, (255,100,100)), (190, 10))
		self.screen.blit(self.textFont.render("Author: Trevor Lawford (2017)", 1, (220,220,20)), (160, 50))
		self.screen.blit(smallTextFont.render("(A Python/Pygame port of my 1999 C++/DirectX5 game)", 1, (100,100,200)), (80, 80))
		self.screen.blit(smallTextFont.render("Set game variables using Joystick,", 1, (100,200,100)), (90, 140))
		self.screen.blit(smallTextFont.render("and then press Fire to start or Escape to exit", 1, (100,200,100)), (150, 160))
		pygame.display.update()
		
		finished=False
		activeVar1=1
		activeVar2=0
		while not finished:
			self.setSetting("lives", self.setVariable("Lives", 200, (activeVar2==1), self.livesArr, self.getLivesIx(), self.initLives))
			self.setSetting("totalSpiders", self.setVariable("Total Spiders", 230, (activeVar2==2), self.totalSpidersArr, self.getTotalSpidersIx(), self.initTotalSpiders))
			self.setSetting("gravity", self.setVariable("Gravity (speed)", 260, (activeVar2==3), self.gravityArr, self.getGravityIx(), self.initGravity))
			self.setSetting("waitSpiderAppear", self.setVariable("Wait for Spider to appear", 290, (activeVar2==4), self.waitSpiderAppearArr, self.getWaitSpiderAppearIx(), self.initWaitSpiderAppear))
			self.setSetting("waitSpiderFire", self.setVariable("Wait for Spider to fire", 320, (activeVar2==5), self.waitSpiderFireArr, self.getWaitSpiderFireIx(), self.initWaitSpiderFire))
			self.setSetting("maxSpiderFire", self.setVariable("Max Spider fire", 350, (activeVar2==6), self.maxSpiderFireArr, self.getMaxSpiderFireIx(), self.initMaxSpiderFire))
			self.setSetting("reloadTime", self.setVariable("Base reload time", 380, (activeVar2==7), self.reloadTimeArr, self.getReloadTimeIx(), self.initReloadTime))
			self.setSetting("godMode", self.setVariable("'God' mode", 410, (activeVar2==8), self.godModeArr, self.getGodModeIx(), self.initGodMode))
			self.setSetting("autoPlay", self.setVariable("Auto-play (demo)", 440, (activeVar2==9), self.autoPlayArr, self.getAutoPlayIx(), self.initAutoPlay))
			if activeVar2==0:
				activeVar2=activeVar1
				continue
				
			if self.keyPress.type==KEYDOWN:
				if self.keyPress.key==K_z:
					finished=True
				elif self.keyPress.key==K_ESCAPE:
					finished=True
					quit=True
				elif self.keyPress.key==K_UP and activeVar1>1:
					activeVar1-=1
					activeVar2=0
				elif self.keyPress.key==K_DOWN and activeVar1<9	:
					activeVar1+=1
					activeVar2=0
		self.screen.fill((0,0,0))
		pygame.display.update()
		return quit
		
	def setVariable(self, name, y, edit, values, ix, initX):
		if edit:
			color1=(100,255,255)
		else:
			color1=(80,120,120)
		self.screen.blit(self.textFont.render(name, 1, color1), (150, y))
		varLoop=True
		while varLoop:
			pygame.draw.rect(self.screen, (0,0,0), (420,y,60,20), 0)
			if edit:
				if ix==initX:
					color2=(40,255,40)
				else:
					color2=(100,255,255)
			else:
				if ix==initX:
					color2=(40,150,40)
				else:
					color2=(80,120,120)
			self.screen.blit(self.textFont.render("{}".format(values[ix]), 1, color2), (420, y))
			pygame.display.update()
			if not edit:
				break
			self.keyPress=pygame.event.wait()
			if self.keyPress.type==KEYDOWN:
				if self.keyPress.key==K_UP or self.keyPress.key==K_DOWN or self.keyPress.key==K_z or self.keyPress.key==K_ESCAPE:
					varLoop=False
				elif self.keyPress.key==K_LEFT and ix>0:
					ix-=1
				elif self.keyPress.key==K_RIGHT and ix<(len(values)-1):
					ix+=1
		return ix
		
	def getSetting(self, item):
		with open(TitleScreen.settingsFile) as settingsFileR:
			settings = json.load(settingsFileR)
			settingsFileR.close()
			if item in settings:
				return settings[item]
			else:
				return None

	def setSetting(self, item, value):
		with open(TitleScreen.settingsFile) as settingsFileR:
			settings = json.load(settingsFileR)
			settingsFileR.close()
			if not item in settings or not settings[item]==value:
				settings[item]=value
				with open(TitleScreen.settingsFile, "w") as settingsFileW:
					json.dump(settings, settingsFileW)
					settingsFileW.close()
		
	# Getters for all stored settings
	def getLivesIx(self):
		index = self.getSetting("lives")
		if index is None:
			index = self.initLives;
		return index
	def getLives(self):
		return self.livesArr[self.getLivesIx()]

	def getTotalSpidersIx(self):
		index = self.getSetting("totalSpiders")
		if index is None:
			index = self.initTotalSpiders;
		return index
	def getTotalSpiders(self):
		return self.totalSpidersArr[self.getTotalSpidersIx()]

	def getGravityIx(self):
		index = self.getSetting("gravity")
		if index is None:
			index = self.initGravity;
		return index
	def getGravity(self):
		return self.gravityArr[self.getGravityIx()]

	def getWaitSpiderAppearIx(self):
		index = self.getSetting("waitSpiderAppear")
		if index is None:
			index = self.initWaitSpiderAppear
		return index
	def getWaitSpiderAppear(self):
		return self.waitSpiderAppearArr[self.getWaitSpiderAppearIx()]

	def getWaitSpiderFireIx(self):
		index = self.getSetting("waitSpiderFire")
		if index is None:
			index = self.initWaitSpiderFire
		return index
	def getWaitSpiderFire(self):
		return self.waitSpiderFireArr[self.getWaitSpiderFireIx()]

	def getMaxSpiderFireIx(self):
		index = self.getSetting("maxSpiderFire")
		if index is None:
			index = self.initMaxSpiderFire
		return index
	def getMaxSpiderFire(self):
		return self.maxSpiderFireArr[self.getMaxSpiderFireIx()]

	def getReloadTimeIx(self):
		index = self.getSetting("reloadTime")
		if index is None:
			index = self.initReloadTime
		return index
	def getReloadTime(self):
		return self.reloadTimeArr[self.getReloadTimeIx()]

	def getGodModeIx(self):
		index = self.getSetting("godMode")
		if index is None:
			index = self.initGodMode
		return index
	def getGodMode(self):
		return self.godModeArr[self.getGodModeIx()]

	def getAutoPlayIx(self):
		index = self.getSetting("autoPlay")
		if index is None:
			index = self.initAutoPlay
		return index
	def getAutoPlay(self):
		return self.autoPlayArr[self.getAutoPlayIx()]
