import os, json, random
from pygame.locals import *
from constants import *
from Level import Level

class HiScoreTable:

	hiScoreFile=os.getcwd()+os.sep+"MutantSpyders"+os.sep+"data"+os.sep+"HiScores.json"
	letters=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"," ","!","-"]

	def __init__(self, screen):
		self.screen=screen
		self.keyPress=None
		
	# Allow user to enter Initials for HiScore
	# Write scores somewhere!
	def draw(self, lives, isAutoplay):		
		self.screen.fill((0,0,0))
		self.textFont = pygame.font.SysFont("", 35)
		self.selectFont = pygame.font.SysFont("", 50)

		titleFont = pygame.font.SysFont("", 40, True, False)	# Bold
		titleFont.set_underline(True)
		italicTextFont = pygame.font.SysFont("", 30, False, True)	# Italic
		
		print "Sw="+str(Level.AI_SPIDER_WEIGHT)+",Bw="+str(Level.AI_BOMB_WEIGHT)+"="+str(Level.Score)

		if Level.Score>0 and self.isNewHiScore(lives, Level.Score):
		
			if isAutoplay:
				self.insert(lives, " * ", Level.Score);
			else:
				self.screen.blit(titleFont.render("You've got a new HIGH SCORE!!", 1, (255,50,255)), (100, 100))
				self.screen.blit(italicTextFont.render("Use the Joystick to enter your initials", 1, (40,255,40)), (120, 200))
				self.screen.blit(italicTextFont.render("and press Fire to continue.", 1, (40,255,40)), (180, 220))
				
				letter1=0
				letter2=0
				letter3=0
				pygame.display.update()

				userFinished=False
				activeVar1=1
				activeVar2=0
				while not userFinished:
					letter1 = self.selectIntial(1, (activeVar2==1), letter1)
					letter2 = self.selectIntial(2, (activeVar2==2), letter2)
					letter3 = self.selectIntial(3, (activeVar2==3), letter3)
					if activeVar2==0:
						activeVar2=activeVar1
						continue

					if self.keyPress==K_z:
						self.insert(lives, HiScoreTable.letters[letter1]+HiScoreTable.letters[letter2]+HiScoreTable.letters[letter3], Level.Score);
						userFinished=True
					elif self.keyPress==K_LEFT and activeVar1>1:
						activeVar1-=1
						activeVar2=0
					elif self.keyPress==K_RIGHT and activeVar1<3:
						activeVar1+=1
						activeVar2=0
				self.screen.fill((0,0,0))
				pygame.display.update()			

		liveStr = str(lives)
		if lives==1:
			liveStr = liveStr+" life"
		else:
			liveStr = liveStr+" lives"
		self.screen.blit(titleFont.render("Hi-Scores with "+liveStr, 1, (100,250,100)), (160, 40))
		y=90;
		with open(HiScoreTable.hiScoreFile) as hiscoreDatafileR:
			data = json.load(hiscoreDatafileR)
			pos=1
			for sc in data["L"+str(lives)]:
				self.screen.blit(self.textFont.render(sc["initials"]+":", 1, (255-(pos*18),255-(pos*22),255)), (220, y))
				self.screen.blit(self.textFont.render("{0:04d}".format(sc["score"]), 1, (255-(pos*18),255-(pos*22),255)), (310	, y))
				y+=30;
				pos+=1
			hiscoreDatafileR.close()
		self.screen.blit(italicTextFont.render("Press Fire to start again, or Escape to exit.", 1, (255,40,40)), (200, 440))
		pygame.display.update()
		
		restartGame=True
		if isAutoplay:
			finished=True
			pygame.time.wait(3000)
		else:
			finished=False
		while not finished:
			keyPress=pygame.event.wait()
			if keyPress.type==KEYDOWN:
				if keyPress.key==K_z:
					finished=True
				if keyPress.key==K_ESCAPE:
					finished=True
					restartGame=False
		self.screen.fill((0,0,0))
		pygame.display.update()						
		return restartGame
		# END =================================

	def isNewHiScore(self, lives, newValue):
		scoreSet="L"+str(lives)
		with open(HiScoreTable.hiScoreFile) as hiscoreDatafileR:
			data = json.load(hiscoreDatafileR)
			hiscoreDatafileR.close()
			if len(data[scoreSet])<10:
				return True
			else:
				return data[scoreSet][9]["score"]<newValue
		return False
		
	def selectIntial(self, charNo, edit, letterX):
		if edit:
			color=(255,60,60)
		else:
			color=(120,30,30)
		
		varLoop=True
		clock = pygame.time.Clock()
		while varLoop:
			pygame.draw.rect(self.screen, (0,0,0), (188+(charNo*50),250,34,40), 0)
			self.screen.blit(self.selectFont.render(HiScoreTable.letters[letterX], 1, color), (190+(charNo*50), 250))
			pygame.display.update()
			if not edit:
				break
				
			pygame.event.get()	# Necessary!
			keys = pygame.key.get_pressed()	

			if keys[K_UP]:
				self.keyPress=K_UP
			elif keys[K_DOWN]:
				self.keyPress=K_DOWN
			elif keys[K_LEFT]:
				self.keyPress=K_LEFT
			elif keys[K_RIGHT]:
				self.keyPress=K_RIGHT
			elif keys[K_z]:
				self.keyPress=K_z
			else:
				self.keyPress=None

			if self.keyPress==K_LEFT or self.keyPress==K_RIGHT or self.keyPress==K_z:
				varLoop=False
			elif self.keyPress==K_UP:
				if letterX>0:
					letterX-=1
				else:
					letterX=len(HiScoreTable.letters)-1
			elif self.keyPress==K_DOWN:
				if letterX<(len(HiScoreTable.letters)-1):
					letterX+=1
				else:
					letterX=0
			clock.tick(8)
		return letterX


	def insert(self, lives, newName, newValue):
		scoreSet="L"+str(lives)
		with open(HiScoreTable.hiScoreFile) as hiscoreDatafileR:
			data = json.load(hiscoreDatafileR)
			hiscoreDatafileR.close()
			newData = {
				"initials":newName,
				"score":newValue
			}
			ix=0
			inserted=False
			for sc in data[scoreSet]:
				if newData["score"]>sc["score"]:
					data[scoreSet].insert(ix, newData)
					inserted=True
					break;
				ix+=1
			if not inserted:
				data[scoreSet].append(newData)
			del data[scoreSet][10:]
			with open(HiScoreTable.hiScoreFile, "w") as hiscoreDatafileW:
				json.dump(data, hiscoreDatafileW)
			hiscoreDatafileW.close()
