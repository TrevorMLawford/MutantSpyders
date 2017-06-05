"""
 Mutant Spyders
 
 Pythin port of C++ PC-based 'Mutant Xpiders' (1999)
 Trevor Lawford (Jan 2017)
  
"""

import sys, os
from src.constants import *
from pygame.locals import *
from src.TitleScreen import TitleScreen
from src.HiScoreTable import HiScoreTable
from src.Level import Level

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.display.set_caption("Mutant Spyders v0.1")
pygame.mouse.set_visible(False)
SCREEN=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))	# origin top/left
BACKDROP=pygame.image.load(os.getcwd()+os.sep+"MutantSpyders"+os.sep+"images"+os.sep+"backdrop.png")
titleScreen=TitleScreen(SCREEN)

continueGame=True	# From HiScore table
exitFromTitle=False			# From TitleScreen
restartGame=False
while continueGame:
	Level.Score=0
	if not restartGame:
		exitFromTitle=titleScreen.draw()
	if not exitFromTitle:
		livesLeft=titleScreen.getLives()
		while livesLeft>0:
			levelToPlay = Level(SCREEN, BACKDROP, livesLeft,
				titleScreen.getTotalSpiders(),
				titleScreen.getGravity(),
				titleScreen.getWaitSpiderAppear(),
				titleScreen.getWaitSpiderFire(),
				titleScreen.getMaxSpiderFire(),
				titleScreen.getReloadTime(),
				titleScreen.getGodMode(),
				titleScreen.getAutoPlay())
			livesLeft=(levelToPlay.start())
		if livesLeft==0 and not titleScreen.getGodMode():
			hiScoreTable=HiScoreTable(SCREEN)
			restartGame=hiScoreTable.draw(titleScreen.getLives(), (not titleScreen.getAutoPlay()=="No"))
		elif livesLeft<0:
			restartGame=False
	else:
		continueGame=False

pygame.quit()
sys.exit()