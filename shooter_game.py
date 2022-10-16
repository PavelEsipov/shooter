from pygame import *
from random import randint
from time import sleep
win_wid=700
win_hei=500
window=display.set_mode((win_wid,win_hei))
display.set_caption("SHOOTER")
clock=time.Clock()
FPS=60
back=image.load('galaxy.jpg')
back=transform.scale(back,(win_wid,win_hei))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
killed=0
passed=0
class GameSprite(sprite.Sprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__()
		self.width=width
		self.height=height
		self.image=image.load(img)
		self.image=transform.scale(self.image,(self.width,self.height))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.speed=speed
	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))

class Hero(GameSprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__(width, height, img, x, y, speed)
	def update(self):
		keys=key.get_pressed()
		if keys[K_a] and self.rect.x>0:
			self.rect.x-=self.speed
		elif keys[K_d] and self.rect.x+self.width<win_wid:
	  		self.rect.x+=self.speed
	def fire(self):
		bullet=Bullet(20, 20, "bullet.png", self.rect.x+self.width/2, self.rect.y, 10)
		bullets.add(bullet)
	

class UFO(GameSprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__(width, height, img, x, y, speed)
	def update(self):
		global passed
		self.rect.y+=self.speed
		if self.rect.y>win_hei:
			self.rect.y=0
			self.rect.x=randint(0, win_wid-self.width)
			window.blit(text_passed,(10,40))
			passed+=1
			
class Bullet(GameSprite):
	def __init__(self, width, height, img, x, y, speed):
		super().__init__(width, height, img, x, y, speed)
	def update(self):
		self.rect.y-=self.speed
		if self.rect.y<0:
			self.kill()

n=24
font.init()
font24=font.SysFont('Arial',24)
font40=font.SysFont('Arial',40)	
text_win = font40.render('ВЫИГРАЛ',True,(0,255,0))
text_lose = font40.render('ПРОИГРАЛ',True,(255,0,0))
	
rocket=Hero(width=50, height=50, img="rocket.png", x=325, y=450, speed=3)
ufos=sprite.Group()
ast=sprite.Group()
for i in range(3):
	ufo = UFO(width=50, height=50, img="ufo.png", x=randint(0, win_wid-50), y=0, speed=1)
	ufos.add(ufo)
	astr = UFO(width=50, height=50, img="asteroid.png", x=randint(0, win_wid-50), y=0, speed=1)
	ast.add(astr)
bullets=sprite.Group()
FPS=150
while 1:
	window.blit(back,(0,0))
	rocket.reset()
	rocket.update()
	ufos.draw(window)
	ufos.update()
	ast.draw(window)
	ast.update()
	bullets.draw(window)
	bullets.update()
	text_killed = font24.render("Убито:"+str(killed),True,(255,255,255))
	text_passed = font24.render("Пропущенно:"+str(passed),True,(255,255,255))
	window.blit(text_killed,(10,10))
	window.blit(text_passed,(10,40))
	display.update()
	hits = sprite.groupcollide(ufos, bullets, True, True)
	hits2 = sprite.groupcollide(ast, bullets, True, True)
	for hit in hits:
		killed+=1
		ufo = UFO(width=50, height=50, img="ufo.png", x=randint(0, win_wid-50), y=0, speed=1)
		ufos.add(ufo)
		window.blit(text_killed,(10,10))
	for hit in hits2:
		killed+=1
		astr= UFO(width=50, height=50, img="asteroid.png", x=randint(0, win_wid-50), y=0, speed=1)
		ast.add(astr)
		window.blit(text_killed,(10,10))
	if sprite.spritecollide(rocket, ufos, True) or passed>=3:
		window.blit(text_lose,(270,210))
		display.update()
		sleep(3)	
		quit()
	if sprite.spritecollide(rocket, ast, True):
		window.blit(text_lose,(270,210))
		display.update()
		sleep(3)	
		quit()
	if killed==50:
		window.blit(text_win,(270,210))
		display.update()
		sleep(3)	
		quit()
	for i in event.get():
		if i.type==QUIT:
			quit()
		if i.type==KEYDOWN:
			if i.key==K_SPACE:
				rocket.fire()
			if i.key==K_r:
				killed=0
				passed=0
				rocket.rect.x=325
				rocket.rect.y=450
				bullets.empty()
				ufos.empty()
				ast.empty()
				for i in range(3):
					ufo = UFO(width=50, height=50, img="ufo.png", x=randint(0, win_wid-50), y=0, speed=1)
					ufos.add(ufo)
					astr = UFO(width=50, height=50, img="asteroid.png", x=randint(0, win_wid-50), y=0, speed=1)
					ast.add(astr)
				sleep(1)
				game='in_process'
				
	clock.tick(FPS)




