import sys, os, random, math
from constants import *
from pygame.locals import *
from Base import Base
from BaseFire import BaseFire
from Spider import Spider
from SpiderBomb import SpiderBomb
from utils.Collision import collision

class Level:

	Score=0
	AI_SPIDER_WEIGHT=0
	AI_BOMB_WEIGHT=0

	# lives: For display
	# totalSpiders: Total number of Spiders appearing 
	# gravity: affects all Fire
	# waitSpiderAppear: 1 in x chance of appearing 
	# waitSpiderBomb: 1 in x chance of firing 
	# reloadTime Cycles between firing cycle
	# godMode Base cannot be destroyed
	# autoPlay demo mode

	def __init__(self, screen, backdrop, lives, totalSpiders, gravity, waitSpiderAppear, waitSpiderBomb, maxSpiderBomb, reloadTime, godMode, autoPlay):
		self.screen=screen
		self.backdrop=backdrop
		self.lives=lives
		self.totalSpiders=totalSpiders
		self.gravity=gravity
		self.waitSpiderAppear=waitSpiderAppear
		self.waitSpiderBomb=waitSpiderBomb
		self.maxSpiderBomb=maxSpiderBomb
		self.reloadTime=reloadTime
		self.godMode=godMode
		self.autoPlay=autoPlay
		Level.AI_SPIDER_WEIGHT=random.randint(-2, 10) # 5
		Level.AI_BOMB_WEIGHT=random.randint(-2, 10) # 8
		
	# Identify the Vertical 'slot' for this X value
	def whatSlot(self, xVal):
		result=0
		for i in range(AP_VERT_RES-1,-1,-1):
			if xVal>AP_SLOT_WIDTH*i:
				result=i
				break
		return result
		
	def start(self):
		levelFont = pygame.font.SysFont("", 40)
		scoreFont = pygame.font.SysFont("", 24)
			
		self.clock = pygame.time.Clock()
		self.screen.blit(levelFont.render("Get ready...", 1, (255,0,0)), (230, 200))
		pygame.display.flip()
		
		initX=(WINDOW_WIDTH/2)-(Spider.FRAME_WIDTH/2)
		initY=WINDOW_HEIGHT-(Spider.FRAME_HEIGHT)
		basexPrev=baseX=initX
		baseyPrev=baseY=initY
		base=Base(self.screen, baseX, baseY, self.reloadTime)
		baseHit=False
		baseHitWait=0
				
		spiders=[]
		for x in range(self.totalSpiders):	# Seed all Spiders (descend speed depends on gravity)
			spiders.append(Spider(self.screen, random.randint(0, WINDOW_WIDTH - Spider.FRAME_WIDTH), -Spider.FRAME_HEIGHT, random.randint(1,int(self.gravity*20))*.2))

		baseFire=[]
		for x in range(BASE_FIRE_COUNT):	# Seed all base fire 
			baseFire.append(BaseFire(self.screen, self.gravity))	# left cannon
			baseFire.append(BaseFire(self.screen, self.gravity))	# right cannon
			
		spiderBomb=[]
		for x in range(self.maxSpiderBomb):	# Seed all base fire 
			spiderBomb.append(SpiderBomb(self.screen, self.gravity))
			
		running=True
		mouseDown=False
		
		ignoreMouse=False
		
		# AutoPlay Vertical Resolution (no of vertical slots). Odd number
		aX=baseX
		aY=baseY
		aXV=4	# Horizontal movement
		aYV=4	# Vertical movement
		autoplayDangerRectCol=(0,0,0)
		targetSlot=(AP_VERT_RES-1)/2	# Start mis-point
		minY=0
		
		self.clock.tick(0.5)	# Show level for 2 secs
		while running:

			# Start a Spider down its web
			if random.randint(0, self.waitSpiderAppear)==0:
				for sx in spiders:
					if sx.isInit():
						sx.startDescending()
						break;
				
			if (random.randint(0, self.waitSpiderBomb)==0 and not baseHit):
				# A Spider is going to fire
				spiderToFire=None
				for sx in spiders:
					if sx.readyToFire():
						if spiderToFire:
							if sx.getLastFired() > spiderToFire.getLastFired():
								spiderToFire=sx
						else:
							spiderToFire=sx
				if spiderToFire is not None:
					for sbx in spiderBomb:
						if sbx.readyToFire():
							spiderToFire.fire()
							sbx.fire(spiderToFire.launchFireX(), spiderToFire.launchFireY(), spiderToFire.getId())
							break;
				
			# Collision detection (Spider's own fire cannot hit itself and base can only be hit by its own fire downwards)
			for bfx in baseFire:
				if bfx.isFiring():
					for sx in spiders:
						hitScore=sx.checkIfHit(bfx.getWarheadX(), bfx.getWarheadY(), BaseFire.WARHEAD_WIDTH, BaseFire.WARHEAD_HEIGHT)
						if hitScore>0:
							Level.Score+=hitScore;
							bfx.destroy()
					if not self.godMode and bfx.isFiringDown() and base.checkIfHit(bfx.getWarheadX(), bfx.getWarheadY(), BaseFire.WARHEAD_WIDTH, BaseFire.WARHEAD_HEIGHT):
						self.lives-=1
						bfx.destroy()
						baseHit=True
					for sbx in spiderBomb:
						if sbx.isFiring() and collision(bfx.getWarheadX(), bfx.getWarheadY(), BaseFire.WARHEAD_WIDTH, BaseFire.WARHEAD_HEIGHT, sbx.getWarheadX()-2, sbx.getWarheadY()-5, SpiderBomb.WARHEAD_WIDTH+4, SpiderBomb.WARHEAD_HEIGHT+10):
							bfx.destroy()
							sbx.destroy()
			for sbx in spiderBomb:
				if sbx.isFiring():
					for sx in spiders:
						if sx.isFlying() and sx.getId()!=sbx.getSpiderId() and sx.checkIfHit(sbx.getWarheadX(), sbx.getWarheadY(), SpiderBomb.WARHEAD_WIDTH, SpiderBomb.WARHEAD_HEIGHT)>0:
							sbx.destroy()
					if not self.godMode and base.checkIfHit(sbx.getWarheadX(), sbx.getWarheadY(), SpiderBomb.WARHEAD_WIDTH, SpiderBomb.WARHEAD_HEIGHT):
						self.lives-=1
						sbx.destroy()
						baseHit=True
			for sx in spiders:
				if not self.godMode and not sx.isDead() and sx.checkIfHit(baseX+Base.HIT_BOUNDARY, baseY+Base.HIT_BOUNDARY, Base.FRAME_WIDTH-(Base.HIT_BOUNDARY*2), Base.FRAME_HEIGHT-(Base.HIT_BOUNDARY*2))>0 and base.hitAllowed():
					self.lives-=1
					baseHit=True

			'''
			####################
			#  AUTOPLAY START  #
			####################
			'''
			
			if not self.autoPlay=="No":
			
				# 1: Move Base, and set lateral movement indicators
				# =================================================
				moveHoriz=None
				moveVert=None
				if (baseX-aX)>aXV:
					baseX-=aXV
					moveHoriz="L"
				elif (aX-baseX)>aXV:
					baseX+=aXV
					moveHoriz="R"
				if (baseY-aY)>aYV:
					baseY-=aYV
					moveVert="U"
				elif (aY-baseY)>aYV:
					baseY+=aYV
					moveVert="D"

				# 2: Build 'spiderSlots" array containing Spiders in that slot
				# ============================================================
				spiderSlots=[0]*AP_VERT_RES	#Array to hold count of Spiders in slots
				for sx in spiders:
					if sx.isVisible():
						spX=sx.getMidX()
						if sx.getY()<baseY-Base.FRAME_HEIGHT:	# Spider higher than Base - potential target
							# Locate the vertical slot
							spiderSlots[self.whatSlot(spX)]+=1	# +1 if active Spider in that section
					
					
				# 3: Build 'dangerSlots' array evaluating relative level of danger in each slot
				# =============================================================================
				dangerSlots=[0]*AP_VERT_RES	# Most dangerous vertical slots
				
				# Base Fire is heading down and near Base
				for bfx in baseFire:
					if bfx.isFiringDown() and bfx.getY()>0 and baseY>bfx.getWarheadY():
						# Locate the vertical slot
						i=self.whatSlot(bfx.getWarheadX())
						dangerWeight = int(bfx.getY())*int(math.ceil(bfx.getDownwardsVelocity()))
						dangerSlots[i]+=dangerWeight
						if bfx.getSidewaysMovement()=="R":
							if i<(AP_VERT_RES-1):
								dangerSlots[i+1]+=dangerWeight
								if i<(AP_VERT_RES-2):
									dangerSlots[i+2]+=dangerWeight/2
						elif bfx.getSidewaysMovement()=="L":
							if i>0:
								dangerSlots[i-1]+=dangerWeight
								if i>1:
									dangerSlots[i-2]+=dangerWeight/2
						#print "1: "+str(int(bfx.getY()))+" * "+str(int(math.ceil(bfx.getDownwardsVelocity())))
				
				# where Spider is near or below Base
				for sx in spiders:
					if sx.isVisible() and sx.getY()+Spider.FRAME_HEIGHT > baseY-Base.FRAME_HEIGHT:
						# Locate the vertical slot
						i=self.whatSlot(sx.getMidX())
						dangerSlots[i]+=int(sx.getY())*Level.AI_SPIDER_WEIGHT
						if sx.isFlying():
							if sx.isMovingLeft() and i>=0:	# Slot to the left
								dangerSlots[i-1]+=int(sx.getY())*Level.AI_SPIDER_WEIGHT
							if sx.isMovingRight() and i<=AP_VERT_RES-2:	# Slot to the right
								dangerSlots[i+1]+=int(sx.getY())*Level.AI_SPIDER_WEIGHT
						#print "2: "+str(int(sx.getY()))+" * 5"

				# Spider Bomb, the nearer the more dangerous
				bombSlots=[0]*AP_VERT_RES	#Array to hold count of Bombs in slots				
				for sbx in spiderBomb:
					if sbx.isFiring() and sbx.getY()>0: # and baseY>sbx.getWarheadY():
						# Locate the vertical slot
						i=self.whatSlot(sbx.getWarheadX())
						dangerSlots[i]+=(WINDOW_HEIGHT-(abs(sbx.getY()-baseY)))*Level.AI_BOMB_WEIGHT
						bombSlots[i]+=1	# +1 if active Bomb in that section
						#print "3: "+str(sbx.getY())+" * "+str(sbx.getDownwardsVelocity()*2)
								
				
				# 4: Determine 'baseSlot' (0 to AP_VERT_RES-1)
				# ============================================
				basX=base.getCentreX()
				baseSlot=self.whatSlot(basX)
				

				# 5: Should Base choose safer neighbouring slot ('targetSlot')?
				# =============================================================
				tmpTargetSlot=None	# Init as unselected	(will only reset 'targetSlot' if actually used)
				slotL=baseSlot-1
				if slotL<0:
					slotL=baseSlot
				slotR=baseSlot+1
				if slotR>AP_VERT_RES-1:
					slotR=baseSlot
				safestSlot=min(dangerSlots[slotL], dangerSlots[baseSlot], dangerSlots[slotR])
				if not safestSlot==dangerSlots[baseSlot]:	# Are we in safest of surroundings? 
					if safestSlot==dangerSlots[slotL]:
						tmpTargetSlot=slotL
					elif safestSlot==dangerSlots[slotR]:
						tmpTargetSlot=slotR
					#print("[{}] L{}={}:B{}={}:R{}={}").format(tmpTargetSlot,slotL,dangerSlots[slotL],baseSlot,dangerSlots[baseSlot],slotR,dangerSlots[slotR])
			
				# 6: If not found a safer slot then keep moving until target position reached and choose new one
				# ===========================================================================
				elif abs(baseX-aX)<=aXV and abs(baseY-aY)<=aYV:	# Reached previous auto-target location
					maxSpiderSlot=0
					totalSpiders=0
					for i in range(0, AP_VERT_RES):
						totalSpiders+=spiderSlots[i]
						if spiderSlots[i]>maxSpiderSlot:
							maxSpiderSlot=spiderSlots[i]
							tmpTargetSlot=i
							
					# Identify overall vertical slot with highest no of targets to move to
					#if tmpTargetSlot is not None:
						#print("Highest tmpTargetSlot {} scores {}").format(tmpTargetSlot,maxSpiderSlot)

				# 7: If we have a new 'targetSlot' then use that to create target position
				# ========================================================================
				if tmpTargetSlot is not None:
					targetSlot=tmpTargetSlot
					aX=(AP_SLOT_WIDTH*targetSlot)+random.randint(0,AP_SLOT_WIDTH)-(Base.FRAME_WIDTH/2)
					if aX<Base.MIN_X:
						aX=0
					elif aX>Base.MAX_X:
						aX=Base.MAX_X
						
					# Go no higher than anything in any of that or the surrounding vertical slots
					lowestSpiderSlots=[0]*AP_VERT_RES	# Lowest
					for sx in spiders:
						if sx.isVisible():
							spX=sx.getMidX()
							if sx.getY()<baseY-Base.FRAME_HEIGHT:	# Spider higher than Base - hone in
								# Locate the vertical slot
								i=self.whatSlot(spX)
								if sx.getY()>lowestSpiderSlots[i]:	# Keep track of lowest Spider in that slot
									lowestSpiderSlots[i]=sx.getY()				
					lowestY=0;
					if targetSlot==0:
						lowestY=max(lowestSpiderSlots[0], lowestSpiderSlots[1])
					elif targetSlot==AP_VERT_RES-1:
						lowestY=max(lowestSpiderSlots[AP_VERT_RES-2], lowestSpiderSlots[AP_VERT_RES-1])
					else:
						lowestY=max(lowestSpiderSlots[targetSlot-1], lowestSpiderSlots[targetSlot], lowestSpiderSlots[targetSlot+1])
					minY=min(max(Base.MIN_Y, int(lowestY)+(Spider.FRAME_HEIGHT*2)), Base.MAX_Y)
					aY=random.randint(minY, Base.MAX_Y)
					
				# 8: Auto fire (if spider or bomb above or ahead of movement)
				# ===========================================================
				if not moveVert=="D" and random.randint(0,self.reloadTime)==0:
					targetsNearby=spiderSlots[baseSlot]+bombSlots[baseSlot]
					if moveHoriz=="R":
						if baseSlot<AP_VERT_RES-1:
							targetsNearby+=(spiderSlots[baseSlot+1]+bombSlots[baseSlot+1])
						else:
							targetsNearby+=(spiderSlots[AP_VERT_RES-1]+bombSlots[AP_VERT_RES-1])
					elif moveHoriz=="L":
						if baseSlot>0:
							targetsNearby+=(spiderSlots[baseSlot-1]+bombSlots[baseSlot-1])
						else:
							targetsNearby+=(spiderSlots[0]+bombSlots[0])
					if targetsNearby>0:
						base.fire()

				# 9: ESC exit
				# ===========
				pygame.event.get()	# Necessary!
				keys=pygame.key.get_pressed()
				if keys[K_ESCAPE]:
					self.lives=-1
					running=False
					
				'''
				##################
				#  AUTOPLAY END  #
				##################
				'''
			else:
				if TARGET=="PI":
					pygame.event.get()	# Necessary!
					keys = pygame.key.get_pressed()
					if not baseHit:
						if keys[K_UP] and baseY>Base.MIN_Y:
							baseY-=4
						if keys[K_DOWN] and baseY<Base.MAX_Y:
							baseY+=4
						if keys[K_LEFT] and baseX>Base.MIN_X:
							baseX-=4
						if keys[K_RIGHT] and baseX<Base.MAX_X:
							baseX+=4
						if keys[K_z]:
							base.fire()
					if keys[K_ESCAPE]:
						self.lives=-1
						running=False			

				elif TARGET=="PC":
					if ignoreMouse:
						ignoreMouse=False	# Kludge avoid 1st reading!
					else:
						newX,newY=pygame.mouse.get_pos()
					for event in pygame.event.get():
						if event.type==pygame.QUIT:
							running=False
						elif event.type==KEYDOWN:
							if event.key==K_ESCAPE:
								self.lives=-1
								running=False
						elif event.type==MOUSEBUTTONDOWN:
							mouseDown=True
						elif event.type==MOUSEBUTTONUP:
							mouseDown=False

					stickMouse = False
					if not baseHit:
						if newX > Base.MAX_X:
							baseX = Base.MAX_X
							stickMouse = True
						else:
							baseX = newX
						if newY < Base.MIN_Y:
							baseY = Base.MIN_Y
							stickMouse = True
						elif newY > Base.MAX_Y:
							baseY = Base.MAX_Y
							stickMouse = True
						else:
							baseY = newY

						if mouseDown:
							base.fire()
					if stickMouse:	# Keep mouse to fixed areas
						pygame.mouse.set_pos(baseX, baseY)
					
			# End control
			
			if base.readyToFireLeft():
				for bfx1 in baseFire:
					if bfx1.readyToFire():
						bfx1.fire(baseX-2, baseY, (baseX-basexPrev)*0.5, baseyPrev-baseY)
						break;
			if base.readyToFireRight():
				for bfx2 in baseFire:
					if bfx2.readyToFire():
						bfx2.fire(baseX+Base.FRAME_WIDTH-7, baseY, baseX-basexPrev, baseyPrev-baseY)
						break;
			
			# Drawing code #
			self.screen.fill((0,0,0))	# Clear before writing new stuff
			self.screen.blit(pygame.transform.scale(self.backdrop, (WINDOW_WIDTH,WINDOW_HEIGHT)),(0,0))
			
			# Draw Autoplay processes for Visual mode
			if self.autoPlay=="Visual":
			
				# Yellow-highlight target slot
				pygame.draw.line(self.screen, (150,150,0), (AP_SLOT_WIDTH*targetSlot, WINDOW_HEIGHT-6), (AP_SLOT_WIDTH*(targetSlot+1), WINDOW_HEIGHT-6), 4)
				#self.screen.blit(scoreFont.render(str(targetSlot), 0, (150,150,150)), (AP_SLOT_WIDTH*targetSlot+30, WINDOW_HEIGHT-20))
				
				# Cyan-line Spiders in slots
				targetsLengthFactor=totalSpiders
				if targetsLengthFactor>0:
					targetsLengthFactor=100/float(targetsLengthFactor)
				for i in range(0, AP_VERT_RES):
					midX=AP_SLOT_WIDTH*i+(AP_SLOT_WIDTH/2)
					if spiderSlots[i]>0:
						pygame.draw.line(self.screen, (150,0,150), (midX, WINDOW_HEIGHT-(spiderSlots[i]*targetsLengthFactor)), (midX, WINDOW_HEIGHT-8), 4)
					
				# Red-frame danger slots
				redFactor=max(dangerSlots)
				if redFactor>0:
					redFactor=254/float(redFactor)
				for i in range(0,AP_VERT_RES):
					red=dangerSlots[i]*redFactor
					if red>20:
						autoplayDangerRectCol=(red,0,0)
						pygame.draw.rect(self.screen, autoplayDangerRectCol,((AP_SLOT_WIDTH*i)+1,1,AP_SLOT_WIDTH-2,baseY-2), 1)
			
			spidersAlive=0
			for sx in spiders:
				sx.draw()
				if not sx.isDead():
					spidersAlive+=1
				
			for sbx in spiderBomb:
				sbx.draw();
				
			activeBf=0
			for bfx in baseFire:
				if bfx.draw():
					activeBf+=1
				
			# Score, Ship and Spider count
			self.screen.blit(scoreFont.render("{0:3d} : {1:04d}".format(self.lives, Level.Score), 0, (250,40,0)), (0, WINDOW_HEIGHT-20))
			self.screen.blit(scoreFont.render("{0:3d}".format(spidersAlive), 0, (250,40,0)), (WINDOW_WIDTH-30, WINDOW_HEIGHT-20))

			# Must come last
			base.draw(baseX, baseY)
			basexPrev = baseX
			baseyPrev = baseY
			
			# After Base hit allow any live Fire to complete, and then wait another 2 second
			if baseHitWait>0:
				baseHitWait-=1
				if baseHitWait==0:
					baseHit=False
					if (spidersAlive>0):
						basexPrev=baseX=newX=initX
						baseyPrev=baseY=newY=initY
						base.reStart(baseX, baseY)
					if TARGET=="PC":
						pygame.mouse.set_pos(baseX, baseY)
						ignoreMouse=True	# kludge avoid glitch
			elif baseHit:
				anyLiveFire=False
				for bfx in baseFire:
					if bfx.isFiring():
						anyLiveFire=True
						break;
				if not anyLiveFire:
					for sbx in spiderBomb:
						if sbx.isFiring():
							anyLiveFire=True
							break;
				if not anyLiveFire:
					if baseHitWait==0:
						baseHitWait=FPS*1.5	#Start final wait

			# self.clock.tick(FPS)
			pygame.display.update()	# Finally, redraw screen
			
			# Check whether all Spiders dead
			if self.lives==0 and not baseHit:
				running=False
			elif spidersAlive==0:
				if baseHitWait==0:
					baseHitWait=FPS*1.5
				elif baseHitWait==1 and activeBf==0:
					running=False
				
		self.screen.fill((0,0,0))	# Clear before writing new stuff
		return self.lives


