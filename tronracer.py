from cmu_graphics import *
import math
import PIL
import random

class Car:
    def __init__(self, x, y, name, color):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.l = 20
        self.w = 7
        self.speed = 0
        self.dx = 0
        self.dy = 0
        self.angle = 90
        self.laps = 0
        self.lives = 3
        self.checkpoint = False

    def lap(self, app):
        if 400 <= self.x <= app.trackWidth and 400 - self.l < self.y <= 400 + self.l:
            self.checkpoint = True
        if 67 <= self.x <= 134 and 400 - self.l < self.y <= 400 + self.l and self.checkpoint == True:
            self.laps += 1
            self.checkpoint = False

    def attack(self, other):
        left0 = self.x
        right0 = left0 + self.w
        top0 = self.y
        bottom0 = top0 + self.l
        left1 = other.x
        right1 = left1 + other.w
        top1 = other.y
        bottom1 = top1 + other.l
        if (right0 >= left1-10 and right1 >= left0-10 and bottom0 >= top1-10 and bottom1 >= top0-10):
            other.lives -= 1
            other.speed *= -1

def makeTrack(app):
    #all PIL documentation came from https://pillow.readthedocs.io/en/stable/reference/Image.html
    toptobottom = PIL.Image.open('graytoptobottom.png')
    lefttoright = PIL.Image.open('graylefttoright.png')
    bottomtoleft = PIL.Image.open('graybottomtoleft.png')
    bottomtoright = PIL.Image.open('graybottomtoright.png')
    lefttotop = PIL.Image.open('graylefttotop.png')
    righttotop = PIL.Image.open('grayrighttotop.png')
    blank = PIL.Image.open('grayblank.png')
    app.toptobottom = toptobottom.resize((200, 200))
    app.lefttoright = lefttoright.resize((200, 200))
    app.bottomtoleft = bottomtoleft.resize((200, 200))
    app.bottomtoright = bottomtoright.resize((200, 200))
    app.lefttotop = lefttotop.resize((200, 200))
    app.righttotop = righttotop.resize((200, 200))
    app.blank = blank.resize((200, 200))
    app.tiles = [app.toptobottom, app.lefttoright, app.bottomtoleft, app.bottomtoright, app.lefttotop, app.righttotop]
    app.scrambledtiles = scrambleTiles(app.tiles)
    app.trackWidth = 1600
    app.trackHeight = 1000
    app.newImage = PIL.Image.new('RGB', (app.trackWidth, app.trackHeight), (31, 31, 31))
    app.newImage.paste(app.toptobottom, (0, 400))
    app.track = makeTrackHelper(app, app.newImage, app.trackWidth, app.trackHeight, app.scrambledtiles, [])

def makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot = (0, 200), direction = 'up'):
    if 0 <= lastspot[0] < width-200 and 0 <= lastspot[1] < height-200:
        if lastspot == (0, 400) and len(placedtiles) >= 20 and (placedtiles[-1] == app.toptobottom or placedtiles[-1] == app.righttotop):
            return track
        else:
            if (track.getpixel((lastspot[0]+100, lastspot[1]+10)) == (31, 31, 31) and
                track.getpixel((lastspot[0]+190, lastspot[1]+100)) == (31, 31, 31) and
                track.getpixel((lastspot[0]+100, lastspot[1]+190)) == (31, 31, 31) and
                track.getpixel((lastspot[0]+10, lastspot[1]+100)) == (31, 31, 31)):
                for tile in tiles:
                    if direction == 'up' and lastspot[1] >= 0 and (tile == app.toptobottom or tile == app.bottomtoleft or tile == app.bottomtoright):
                        if tile == app.toptobottom:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            y -= 200
                            lastspot = (x, y)
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            y += 200
                            lastspot = (x, y)
                            track.paste(app.blank, lastspot)
                        elif tile == app.bottomtoleft:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            x -= 200
                            lastspot = (x, y)
                            direction = 'left'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            x += 200
                            lastspot = (x, y)
                            direction = 'up'
                            track.paste(app.blank, lastspot)
                        elif tile == app.bottomtoright:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            x += 200
                            lastspot = (x, y)
                            direction = 'right'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            x -= 200
                            lastspot = (x, y)
                            direction = 'up'
                            track.paste(app.blank, lastspot)
                    elif direction == 'left' and lastspot[0] >= 0 and (tile == app.lefttoright or tile == app.righttotop or tile == app.bottomtoright):
                        if tile == app.lefttoright:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            x -= 200
                            lastspot = (x, y)
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            x += 200
                            lastspot = (x, y)
                            track.paste(app.blank, lastspot)
                        elif tile == app.righttotop:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            y -= 200
                            lastspot = (x, y)
                            direction = 'up'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            y += 200
                            lastspot = (x, y)
                            direction = 'left'
                            track.paste(app.blank, lastspot)
                        elif tile == app.bottomtoright:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            y += 200
                            lastspot = (x, y)
                            direction = 'down'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            y -= 200
                            lastspot = (x, y)
                            direction = 'left'
                            track.paste(app.blank, lastspot)
                    elif direction == 'right' and lastspot[0] < width-200 and (tile == app.lefttoright or tile == app.lefttotop or tile == app.bottomtoleft):
                        if tile == app.lefttoright:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            x += 200
                            lastspot = (x, y)
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            x -= 200
                            lastspot = (x, y)
                            track.paste(app.blank, lastspot)
                        elif tile == app.lefttotop:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            y -= 200
                            lastspot = (x, y)
                            direction = 'up'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            y += 200
                            lastspot = (x, y)
                            direction = 'right'
                            track.paste(app.blank, lastspot)
                        elif tile == app.bottomtoleft:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            y += 200
                            lastspot = (x, y)
                            direction = 'down'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            y -= 200
                            lastspot = (x, y)
                            direction = 'right'
                            track.paste(app.blank, lastspot)
                    elif direction == 'down' and lastspot[1] < height-200 and (tile == app.toptobottom or tile == app.lefttotop or tile == app.righttotop):
                        if tile == app.toptobottom:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            y += 200
                            lastspot = (x, y)
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            y -= 200
                            lastspot = (x, y)
                            track.paste(app.blank, lastspot)
                        elif tile == app.lefttotop:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            x -= 200
                            lastspot = (x, y)
                            direction = 'left'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            x += 200
                            lastspot = (x, y)
                            direction = 'down'
                            track.paste(app.blank, lastspot)
                        elif tile == app.righttotop:
                            track.paste(tile, lastspot)
                            x, y = lastspot
                            x += 200
                            lastspot = (x, y)
                            direction = 'right'
                            placedtiles.append(tile)
                            solution = makeTrackHelper(app, track, width, height, tiles, placedtiles, lastspot, direction)
                            if solution != None:
                                return solution
                            placedtiles.pop()
                            x -= 200
                            lastspot = (x, y)
                            direction = 'down'
                            track.paste(app.blank, lastspot)
                return None
            return None
    return None

def scrambleTiles(tiles):
    result = []
    options = [0, 1, 2, 3, 4, 5]
    while len(result) < len(tiles):
        n = random.choice(options)
        result.append(tiles[n])
        options.remove(n)
    return result

def newGame(app):
    app.countdown = 90
    app.timer = 0
    app.play = False
    app.explain = False
    app.race = False
    makeTrack(app)
    app.background = 'black'
    app.stepsPerSecond = 30
    app.Tron = Car(105, 410, 'Tron', rgb(104, 224, 248))
    app.scrollX = -(app.width/2 - app.Tron.x)
    app.scrollY = -(app.height/2 - app.Tron.y)
    app.Clu = Car(85, 410, 'Clu', 'orange')
    app.cars = [app.Tron, app.Clu]
    app.powerups = []
    app.shields = []
    app.winner = None
    app.x = 0
    app.y = 0

def onAppStart(app):
    newGame(app)
    x = random.randint(0, 1400)
    y = random.randint(0, 800)
    if app.track.getpixel((x, y)) == (0, 0, 0) and (x,y) not in app.powerups:
        app.shields.append((x,y))

def redrawAll(app):
    if app.play == False and app.explain == False:
        drawLabel('TRON', app.width/2, app.height/2-120, size = 180, fill = 'black', border = rgb(104, 224, 248), borderWidth = 7)
        drawLabel('RACER', app.width/2, app.height/2, size = 180, fill = 'black', border = rgb(104, 224, 248), borderWidth = 7)
        drawRect(app.width/2 - 70, app.height/2 + 120, 140, 70, border = rgb(104, 224, 248))
        drawLabel('PLAY', app.width/2, app.height/2 + 155, fill = rgb(104, 224, 248), size = 40)
        drawRect(app.width/2 - 70, app.height/2 + 210, 140, 70, border = rgb(104, 224, 248))
        drawLabel('RULES', app.width/2, app.height/2 + 245, fill = rgb(104, 224, 248), size = 40)
    elif app.explain == True:
        drawLabel('Welcome to Tron Racer', app.width/2, 100, size = 30, fill = rgb(104, 224, 248))
        drawLabel('Use left, right, and up to move Tron (the blue car)', app.width/2, 180, size = 20, fill = rgb(104, 224, 248))
        drawLabel("If Tron glows red you're in danger", app.width/2, 210, size = 20, fill = rgb(104, 224, 248))
        drawLabel("If you get too close to Clu (the orange car) you will get hit", app.width/2, 240, size = 20, fill = rgb(104, 224, 248))
        drawLabel("Survive all 3 rounds and beat Clu", app.width/2, 270, size = 20, fill = rgb(104, 224, 248))
        drawLabel("Good luck", app.width/2, 300, size = 20, fill = rgb(104, 224, 248))
        drawRect(app.width/2 - 70, app.height/2 + 120, 140, 70, border = rgb(104, 224, 248))
        drawLabel('PLAY', app.width/2, app.height/2 + 155, fill = rgb(104, 224, 248), size = 40)
    elif app.play == True:
        if app.winner == None:
            drawImage(CMUImage(app.track), 0-app.scrollX, 0-app.scrollY, border = 'black')
            drawLine(67-app.scrollX, 400-app.scrollY, 134-app.scrollX, 400-app.scrollY, fill = 'white', lineWidth = 5, dashes = True)
            drawRect(app.Clu.x-app.scrollX, app.Clu.y-app.scrollY, app.Clu.l, app.Clu.w, fill = app.Clu.color, rotateAngle = -app.Clu.angle, align = 'center')
            left0 = app.Tron.x
            right0 = left0 + app.Tron.w
            top0 = app.Tron.y
            bottom0 = top0 + app.Tron.l
            left1 = app.Clu.x
            right1 = left1 + app.Clu.w
            top1 = app.Clu.y
            bottom1 = top1 + app.Clu.l
            if (right0 >= left1-15 and right1 >= left0-15 and bottom0 >= top1-15 and bottom1 >= top0-15):
                outline = 'red'
            else:
                outline = None
            drawRect(app.Tron.x-app.scrollX, app.Tron.y-app.scrollY, app.Tron.l, app.Tron.w, fill = app.Tron.color, border = outline, rotateAngle = -app.Tron.angle, align = 'center')
            drawLabel(f'Laps: {app.Tron.laps}', 100, 50, fill = rgb(104, 224, 248), size = 30)
            drawLabel(f'{pythonRound(app.timer, 2)} s', app.width/2, 50, fill = 'white', size = 30)
            if app.countdown > 0:
                if 60 < app.countdown <= 90:
                    num = 3
                elif 30 < app.countdown <= 60:
                    num = 2
                else:
                    num = 1
                drawLabel(num, app.width/2, app.height/2, size = 40, fill = 'red', bold = True)
            if -30 < app.countdown <= 0:
                drawLabel('GO', app.width/2, app.height/2, size = 60, fill = 'green', bold = True)
            for i in range(1, 4):
                if i <= app.Tron.lives:
                    drawPolygon(app.width-(50*i), 50, app.width-((50*i)+10), 40, app.width-((50*i)+20), 50, app.width-((50*i)+30), 40, app.width-((50*i)+40), 50, app.width-((50*i)+20), 70, fill = app.Tron.color)
                else:
                    drawPolygon(app.width-(50*i), 50, app.width-((50*i)+10), 40, app.width-((50*i)+20), 50, app.width-((50*i)+30), 40, app.width-((50*i)+40), 50, app.width-((50*i)+20), 70, fill = None, border = app.Tron.color)
        else:
            if app.winner == 'Tron':
                drawLabel(f'{pythonRound(app.timer)} s', app.width/2, app.height/2 - 100, size = 80, fill = rgb(104, 224, 248))
                drawLabel('TRON WINS', app.width/2, app.height/2, size = 100, fill = rgb(104, 224, 248))
                color = rgb(104, 224, 248)
            else:
                drawLabel(f'{pythonRound(app.timer)} s', app.width/2, app.height/2 - 100, size = 80, fill = 'orange')
                drawLabel('CLU WINS', app.width/2, app.height/2, size = 100, fill = 'orange')
                color = 'orange'
            drawRect(app.width/2 - 135, app.height/2 + 80, 270, 70, border = color)
            drawLabel('RACE AGAIN', app.width/2, app.height/2 + 115, fill = color, size = 40)

def enemyMove(app, enemy):
    if canMove(app, enemy):
        dangle = 30
        turndist = 30
        dxlt = (math.cos(math.radians(enemy.angle+dangle)))*(turndist)
        dylt = (math.sin(math.radians(enemy.angle+dangle)))*(turndist)
        dxrt = (math.cos(math.radians(enemy.angle-dangle)))*(turndist)
        dyrt = (math.sin(math.radians(enemy.angle-dangle)))*(turndist)
        cos = (math.cos(math.radians(enemy.angle)))
        sin = (math.sin(math.radians(enemy.angle)))
        newdx = cos*enemy.speed
        newdy = sin*enemy.speed
        newx = enemy.x + newdx
        newy = enemy.y - newdy
        if (app.track.getpixel((newx + dxlt, newy - dylt)) != (31, 31, 31) and
            app.track.getpixel((newx + dxrt, newy - dyrt)) != (31, 31, 31)):
            if enemy.speed < 10:
                enemy.speed += 1
        elif (app.track.getpixel((newx + dxlt, newy - dylt)) != (31, 31, 31) and
            app.track.getpixel((newx + dxrt, newy - dyrt)) == (31, 31, 31)):
            enemy.angle += 10
        elif (app.track.getpixel((newx + dxlt, newy - dylt)) == (31, 31, 31) and
            app.track.getpixel((newx + dxrt, newy - dyrt)) != (31, 31, 31)):
            enemy.angle -= 10
        enemy.dx = newdx
        enemy.dy = newdy
        enemy.x = newx
        enemy.y = newy
    else:
        enemy.x = enemy.x
        enemy.y = enemy.y
        enemy.speed -= enemy.speed*0.1
        enemy.angle = enemy.angle

def playerMove(app, player):
    if canMove(app, player):
        cos = (math.cos(math.radians(player.angle)))
        sin = (math.sin(math.radians(player.angle)))
        player.dx = cos*player.speed
        player.dy = sin*player.speed
        player.x += player.dx
        player.y -= player.dy
    else:
        player.x = player.x
        player.y = player.y
        player.speed -= player.speed*0.1

def onStep(app):
    if app.play == True:
        app.countdown -= 1
        if app.countdown <= 0:
            app.race = True
        if app.race == True:
            if app.winner == None:
                app.timer += 1/30
            app.scrollX += app.Tron.dx
            app.scrollY -= app.Tron.dy
            enemyMove(app, app.Clu)
            playerMove(app, app.Tron)
            app.Clu.attack(app.Tron)
            for car in app.cars:
                if onTrack(app, car):
                    if car.speed > 0:
                        #friction equation from https://byjus.com/physics/frictional-force/
                        friction = 0.5*20
                        car.speed -= friction/20
                        if car.speed < 0:
                            car.speed == 0
                else:
                    if car.speed > 0:
                        friction = 0.8*20
                        car.speed -= friction/20
                        if car.speed < 0:
                            car.speed == 0
                car.lap(app)
                if car.laps == 3 and app.winner == None:
                    app.winner = car.name
                if car.lives == 0:
                    if car.name == 'Tron':
                        app.winner = 'Clu'
                    else:
                        app.winner = 'Tron'


def onTrack(app, car):
    dangle = 30
    dist = 15
    dxlt = (math.cos(math.radians(car.angle+dangle)))*(dist)
    dylt = (math.sin(math.radians(car.angle+dangle)))*(dist)
    dxrt = (math.cos(math.radians(car.angle-dangle)))*(dist)
    dyrt = (math.sin(math.radians(car.angle-dangle)))*(dist)
    dxlb = (math.cos(math.radians(car.angle+180-dangle)))*(dist)
    dylb = (math.sin(math.radians(car.angle+180-dangle)))*(dist)
    dxrb = (math.cos(math.radians(car.angle+180+dangle)))*(dist)
    dyrb = (math.sin(math.radians(car.angle+180+dangle)))*(dist)
    if (app.track.getpixel((car.x + dxlt, car.y - dylt)) != (31, 31, 31) and
        app.track.getpixel((car.x + dxrt, car.y - dyrt)) != (31, 31, 31) and
        app.track.getpixel((car.x + dxlb, car.y - dylb)) != (31, 31, 31) and
        app.track.getpixel((car.x + dxrb, car.y - dyrb)) != (31, 31, 31)):
        return True
    return False

def canMove(app, car):
    cos = (math.cos(math.radians(car.angle)))
    sin = (math.sin(math.radians(car.angle)))
    newdx = cos*car.speed
    newdy = sin*car.speed
    newx = car.x + newdx
    newy = car.y - newdy
    dangle = 30
    dist = 15
    dxlt = (math.cos(math.radians(car.angle+dangle)))*(dist)
    dylt = (math.sin(math.radians(car.angle+dangle)))*(dist)
    dxrt = (math.cos(math.radians(car.angle-dangle)))*(dist)
    dyrt = (math.sin(math.radians(car.angle-dangle)))*(dist)
    dxlb = (math.cos(math.radians(car.angle+180-dangle)))*(dist)
    dylb = (math.sin(math.radians(car.angle+180-dangle)))*(dist)
    dxrb = (math.cos(math.radians(car.angle+180+dangle)))*(dist)
    dyrb = (math.sin(math.radians(car.angle+180+dangle)))*(dist)
    if (0 <= newx + dxlt < 1600 and 0 <= newx + dxrt < 1600 and 0 <= newx + dxlb < 1600 and 0 <= newx + dxrb < 1600 and
        0 <= newy - dylt < 1000 and 0 <= newy - dyrt < 1000 and 0 <= newy - dylb < 1000 and 0 <= newy - dyrb < 1000):
        return True
    return False

def onKeyHold(app, keys):
    if 'up' in keys and canMove(app, app.Tron):
        app.Tron.slowDown = False
        if app.Tron.speed < 10:
            app.Tron.speed += 1
    if 'right' in keys:
        app.Tron.angle -= 5
        if app.Tron.angle < 0:
            app.Tron.angle = 360
    if 'left' in keys:
        app.Tron.angle += 5
        if app.Tron.angle > 360:
            app.Tron.angle = 0

def onMousePress(app, mouseX, mouseY):
    app.x = mouseX
    app.y = mouseY
    if app.width/2 - 70 <= mouseX <= app.width/2 + 70 and app.height/2 + 120 <= mouseY <= app.height/2 + 190:
        app.play = True
        app.explain = False
    elif app.width/2 - 70 <= mouseX <= app.width/2 + 70 and app.height/2 + 210 <= mouseY <= app.height/2 + 280:
        app.explain = True
    elif app.width/2 - 135 <= mouseX <= app.width/2 + 135 and app.height/2 + 80 <= mouseY <= app.height + 150 and app.play == True:
        newGame(app)


def main():
    runApp(width = 800, height = 600)

main()