from PIL import Image, ImageDraw
import math
while True:
    try:
        fileName = input('What is the name of the picture verbatim? Include file type at end (I.E picture.png)\n>> ')
        im = Image.open(fileName)
        break
    except:
        print("What? Try again...")

im=im.convert('RGB')
im=im.rotate(180)
im=im.transpose(Image.FLIP_LEFT_RIGHT)
draw = ImageDraw.Draw(im)
pixdata = im.load()
x,y=im.size
autoFill=0

while True:
    try:
        size = input("what map type? Dual, Tiny, Small, Standard, Large, or Huge?\n>> ")
        if size.lower()=='dual':
            gx,gy=44,26
            im = im.resize((round(y*(44/26)),y))
            break
        elif size.lower()=='tiny':
            gx, gy = 60,38
            im = im.resize((round(y * (60/38)), y))
            break
        elif size.lower()=='small':
            gx, gy = 74,46
            im = im.resize((round(y * (74/46)), y))
            break
        elif size.lower()=='standard':
            gx, gy = 84,54
            im = im.resize((round(y * (84/54)), y))
            break
        elif size.lower()=='large':
            gx, gy = 96, 60
            im = im.resize((round(y * (96/60)), y))
            break
        elif size.lower()=='huge':
            gx, gy = 106,66
            im = im.resize((round(y * (106/66)), y))
            break
        else:
            print("Unkown Choice, Try Again...\n>> ")
    except:
        print("Unkown Choice, Try Again...\n>> ")
while True:
    choice = input("AutoFill Tiles?\nNo: 1\nNormal AutoFill: 2\nMore-Averaged-Coloring AutoFill: 3:\n>> ")
    try:
        if choice=='1':
            autoFill=1
            break
        elif choice=='2':
            autoFill=2
            break
        elif choice=='3':
            autoFill=3
            break
        else:
            print("Unkown Choice, Try Again...\n>> ")
    except:
        print("Unkown Choice, Try Again...\n>> ")

draw = ImageDraw.Draw(im)
pixdata = im.load()
x,y=im.size
totalHexagons=gx*gy
if gy%2==1:
    stretchy=((math.ceil(gy/2))+math.floor(gy/2)/2)/gy
else:
    stretchy=((gy/2)+(gy/4)+.27)/gy
horizontalheight=(x/(gx+.5))
verticleheight=(y/(gy*stretchy))
sideLength=(verticleheight/2)
verticleOffset=(verticleheight-sideLength)/2
rowCount=0
for hexagon in range(totalHexagons):
    if hexagon%gx==0:
        horizontalShift=0
        verticleShift=rowCount*(verticleOffset+sideLength)
        rowCount+=1
        if rowCount%2==0:
            horizontalShift=horizontalheight/2
        lasttop = (0 - (horizontalheight / 2)+horizontalShift, verticleShift)
        lasttopright = (0+horizontalShift, verticleShift+verticleOffset)
        lasttopleft = (0 - horizontalheight+horizontalShift, verticleShift+verticleOffset)
        lastbotleft = (0 - horizontalheight+horizontalShift, verticleShift+(verticleheight - verticleOffset))
        lastbotright = (0+horizontalShift, verticleShift+(verticleheight - verticleOffset))
        lastbottom = (0 - (horizontalheight / 2)+horizontalShift, verticleShift+verticleheight)

    top=((lasttop[0]+horizontalheight),(lasttop[1]))
    topright=((lasttopright[0]+horizontalheight),(lasttopright[1]))
    topleft=((lasttopleft[0]+horizontalheight),(lasttopleft[1]))
    botleft=((lastbotleft[0]+horizontalheight),(lastbotleft[1]))
    botright=((lastbotright[0]+horizontalheight),(lastbotright[1]))
    bottom=((lastbottom[0]+horizontalheight),(lastbottom[1]))
    middle=((lasttop[0]+horizontalheight),(lasttop[1]+(verticleheight/2)))

    if autoFill==2 or autoFill==3:
        if autoFill==2:
         colorChosen = pixdata[middle[0],middle[1]]
        if autoFill==3:
            colorChosen = [0,0,0]
            for color in range(3):
                for xrange in range(math.floor(horizontalheight / 2)):
                    colorChosen[color] += pixdata[middle[0] + xrange, middle[1]][color]
                for xrange in range(1, math.floor(horizontalheight / 2)):
                    colorChosen[color] += pixdata[middle[0] - xrange, middle[1]][color]
                colorChosen[color] = round(colorChosen[color] / (2 * math.floor(horizontalheight / 2)))
            a, b, c = colorChosen[0], colorChosen[1], colorChosen[2]
            colorChosen = (a, b, c)
        draw.polygon(
            [top[0], top[1], topleft[0], topleft[1], botleft[0], botleft[1], bottom[0], bottom[1], botright[0], botright[1],topright[0],topright[1]],fill=colorChosen,outline='black')
    else:
        draw.polygon(
            [top[0], top[1], topleft[0], topleft[1], botleft[0], botleft[1], bottom[0], bottom[1], botright[0],
             botright[1], topright[0], topright[1]], fill=None, outline='black')

    if hexagon<gx:
        draw.polygon(
            [top[0], top[1], topright[0], topright[1], top[0]+horizontalheight,top[1]], fill='black', outline='black')
    if hexagon > gx*(gy-1):
        draw.polygon(
            [bottom[0],bottom[1],botleft[0],botleft[1],bottom[0]-horizontalheight,bottom[1]],
            fill='black', outline='black')
    if hexagon%gx==0and rowCount%2==1:
        draw.polygon(
            [bottom[0], bottom[1], botleft[0], botleft[1],botleft[0],botleft[1]+verticleheight, bottom[0], bottom[1]+sideLength,],
            fill='black', outline='black')
    if hexagon%gx==gx-1and rowCount%2==0:
        draw.polygon(
            [bottom[0], bottom[1], botright[0], botright[1], botright[0], botright[1] + verticleheight, bottom[0],
             bottom[1] + sideLength ],
            fill='black', outline='black')
    if hexagon%gx==gx-1and rowCount==1:
        draw.polygon(
            [x,0,topright[0], topright[1], botright[0], botright[1],  x,verticleheight],
            fill='black', outline='black')
    lasttop = (top[0],top[1])
    lasttopright = (topright[0],topright[1])
    lasttopleft = topleft[0],topleft[1]
    lastbotleft = botleft[0],botleft[1]
    lastbotright = botright[0],botright[1]
    lastbottom = bottom[0],bottom[1]
im=im.rotate(180)
im=im.transpose(Image.FLIP_LEFT_RIGHT)
im.save(size.lower()+'_'+fileName)
print('file saved as '+size.lower()+'_'+fileName)
im.show()














