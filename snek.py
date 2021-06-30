from graphics import*
import winsound
from random import randint

#global initializers
def initAll():
	global borderX,borderY,arr,size,sprite,winX,winY,win,border,borderUpperLeftCorner,borderLowerRightCorner,status,foodArray,initSnekLen,snekLen,hitItself, running

	borderX=110
	borderY=110
	arr=[]
	size=20
	sprite=Rectangle(Point(110,110),Point(110+size,110+size))
	winX=700
	winY=700
	win=GraphWin("Snek",winX,winY)
	border = Rectangle(Point(borderX,borderY),Point(winX-borderX,winY-borderY))
	borderUpperLeftCorner=border.getP1()
	borderLowerRightCorner=border.getP2()
	status=False
	foodArray=[]
	initSnekLen=0
	snekLen=0
	hitItself=False
	running =True


def checkLen():
	global arr
	if len(arr)>snekLen:
		firstObj=arr.pop(0)
		firstObj.undraw()

def moveSegment(xJump,yJump):

	copyObj=sprite.clone()
	copyObj.draw(win)
	arr.append(copyObj)
	sprite.move(xJump,yJump)
	checkLen()

def showStatus(text,num):
	global nameShow
	a=text +" " + str(num)
	nameShow=Text(Point(winX-200,30),a)
	nameShow.draw(win)

def makeGameSound(soundType):
	foldername="c:\\jojo\\sounds\\"
	filename = foldername + soundType + ".wav"
	#todo check if file exists
	winsound.PlaySound(filename, winsound.SND_FILENAME +winsound.SND_ASYNC )

def WallHit():
	global status, gameOverText
	nameShow.undraw()
	showStatus("OH NO! You killed Snek! Score: ",snekLen-initSnekLen)
	sprite.setFill("red")
	#makeGameSound("BEEP_FM")
	status=True
	#gameOverText=Text(Point(250,80),"GAME OVER CLICK ANYWHERE TO ESCAPE")
	#gameOverText.draw(win)

def WallNotHit():
	nameShow.undraw()
	showStatus("Score: ",snekLen-initSnekLen)
	sprite.setFill("blue")
	status=False

def checkWallHit():
	global spriteUpperLeftCorner, spriteLowerRightCorner
	spriteUpperLeftCorner=sprite.getP1()
	spriteLowerRightCorner=sprite.getP2()

	if spriteUpperLeftCorner.x < borderUpperLeftCorner.x:
		WallHit()

	elif spriteLowerRightCorner.x > borderLowerRightCorner.x:
		WallHit()

	elif spriteUpperLeftCorner.y < borderUpperLeftCorner.y:
		WallHit()

	elif spriteLowerRightCorner.y > borderLowerRightCorner.y:
		WallHit()

	else:
		WallNotHit()

def foodGenerate():
	global food,foodX,foodY
	for i in range(1):
		foodX=randint(borderX+10,winX-borderX-10)
		foodY=randint(borderY+10,winY-borderY-10)
		foodX=round(foodX,-1)
		foodY=round(foodY,-1)
		#print("foodX=",foodX," foodY=",foodY) debug code

		if foodX%20!=0:
			foodX=foodX+10

		if foodY%20!=0:
			foodY=foodY+10

		#print("foodXaftR=",foodX," foodYaftR=",foodY) debug code

		food=Circle(Point(foodX,foodY), (size/2))
		food.setFill("yellow")
		foodArray.append(food)
		food.draw(win)

def getSpriteCenter(object):
	return object.getCenter()

def getDistance(x1,y1,x2,y2):
	global distance
	distance = (((x2-x1)**2) + ((y2-y1)**2))**(0.5)
	return distance

def checkIfFoodEaten():
	global distanceBetweenSpriteAndFood, spriteCenter, snekLen
	spriteCenter=getSpriteCenter(sprite)
	distanceBetweenSpriteAndFood=getDistance(spriteCenter.x,spriteCenter.y,foodX,foodY)

	#print(distanceBetweenSpriteAndFood) debug code
	if distanceBetweenSpriteAndFood<20:
		snekLen=snekLen+1
		#print("YOU ATE!, Snek Lenght is",snekLen-initSnekLen) #debug code 
		food.undraw()
		#makeGameSound("ARRP")
		foodGenerate()

def didSnakeCollideWithItself():
	global hitItself
	for i in range(0,len(arr)-1):
		if arr[-1].getP1().x == arr[i].getP1().x and arr[-1].getP1().y == arr[i].getP1().y and arr[-1].getP2().x==arr[i].getP2().x and arr[-1].getP2().y==arr[i].getP2().y:
			WallHit()


def afterGameOverOrPauseText(givenText):
	global gText
	gText=Text(Point(250,80), givenText)
	gText.draw(win)


def snekFunction(alignment):
	global size, status, hitItself, running, lastKnownText	

	if alignment=="Left":
		jX=-size
		jY=0
	
	if alignment=="Right":
		jX=size
		jY=0  
	
	if alignment=="Up":
		jX=0
		jY=-size
	
	if alignment=="Down":
		jX=0
		jY=size	

	lastKnownText=alignment
	moveSegment(jX,jY)
	checkIfFoodEaten()
	checkWallHit()
	didSnakeCollideWithItself()
	if status==True or hitItself==True:
		running = False


#======================================================================================================

def main():
	#afterGameOver() debug code
	global lastKnownText, running, score
	#makeGameSound("OOMPH")
	border.draw(win)
	foodGenerate()
	showStatus("Score: ",snekLen-initSnekLen)
	sprite.draw(win)
	sprite.setFill("blue")

	k=""
	while running:
		#getSpriteCord(sprite)
		time.sleep(.09)
		#makeGameSound("KLICK")
		tk=	win.checkKey()
		if(tk != ""):
			k=tk

		if k=="Left":
			snekFunction(k)

		elif k=="Right":
			snekFunction(k)

		elif k=="Up":
			snekFunction(k)

		elif k=="Down":
			snekFunction(k)

		elif k=="space":
			afterGameOverOrPauseText("PRESS ANY KEY TO RESUME")
			win.getKey()
			gText.undraw()
			k=lastKnownText

		elif k=="Escape":
			break


initAll()
main()
location = 'C://jojo//python//play//snekData.txt'
mode = 'r'
f=open(location, mode)#creating a filestream
hs = int(f.read()) #high score

if( (snekLen-initSnekLen) > hs):
	mode = 'w'
	f=open(location, mode)#creating a filestream
	f.write(str(snekLen-initSnekLen))
	status = 'New High Score! : ' + str(snekLen-initSnekLen)
	afterGameOverOrPauseText(status)
	time.sleep(2)
	gText.undraw()
	afterGameOverOrPauseText("Click anywhere on the screen to exit")
	win.getMouse()
else:
	afterGameOverOrPauseText("Click anywhere on the screen to exit")
	win.getMouse()

#gText.undraw()


