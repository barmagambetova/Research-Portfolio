from random import randint
import math
from cmu_graphics import *
from cmu_graphics.shape_logic import loadImageFromStringReference

#creating a class for character attributes and parametres
class Coin(object):
    image = loadImageFromStringReference("coins.png")  #load coin image

    def __init__(self, x, y):
        self.w, self.h = getImageSize(Coin.image)
        self.x = x
        self.y = y
        self.direction = 1
        self.counter = 0

    def update(self):
        self.y += self.direction
        self.counter += 1
        if abs(self.counter) > 20:
            self.direction *= -1
            self.counter *= -1

    def inFrame(self, app, dx, dy):           #creating method to ensure that coins do not collide with the blocks          

        x1 = self.x + dx
        y1 = self.y + dy


        for (bx, by, bw, bh) in app.level1.blocks:
            if (bx < x1 < bx + bw) and (by < y1):
                return False
            
        for b in app.level1.floatingBlocks:
            fx = b.x
            fy = b.y
            fw = b.width
            fh = b.height
            if (fx < x1 < fx + fw) and (fy < y1 < fy + fh + self.h):
                return False

        return True

    def draw(self, app):
        drawImage(Coin.image, self.x - app.scrollX, self.y - self.h // 2, align="center")

    def collidesWithPlayer(self, app):
        w, h = getImageSize(Player.jumping_image)
        d = distance(self.x, self.y, app.p.x, app.p.y)
        a = ((self.w//2) ** 2 + (self.h//2) ** 2) ** 0.5 + ((w//2) ** 2 + (h//2) ** 2) ** 0.5
        if d < a:
            return True
        else:
            return False
    
class FloatingBlock(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = 1
        self.counter = 0

    def update(self):
        self.y += self.direction
        self.counter += 1
        if abs(self.counter) > 20:
            self.direction *= -1
            self.counter *= -1

    def draw(self, app):
        drawRect(self.x - app.scrollX, self.y, self.width, self.height, fill="brown")

    def get_boundaries(self):
        return (self.x, self.x + self.width)
    

class Projectile(object):
    def __init__(self, x, y, direction, block_boundaries):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 30
        self.block_boundaries = block_boundaries

    def move(self):
        self.x += self.speed * self.direction
        if self.x < self.block_boundaries[0] or self.x > self.block_boundaries[1]:
            return False  #out of bounds
        return True

    def draw(self, app):
        drawCircle(self.x - app.scrollX, self.y, 5, fill="red")

    def collidesWithPlayer(self, app):
        w, h = getImageSize(Player.standing_image)
        d = distance(self.x, self.y, app.p.x, app.p.y)
        a = 5 + ((w//2) ** 2 + (h//2) ** 2) ** 0.5
        if d < a:
            return True
        else:
            return False
    
class ShootingEnemy(object):
    def __init__(self, x, y, block_boundaries):
        self.x = x
        self.y = y
        self.block_boundaries = block_boundaries
        self.projectiles = []

    def draw(self, app):
        drawRect(self.x - app.scrollX, self.y, 50, 30, fill="green")

    def shoot(self):
        self.projectiles.append(Projectile(self.x, self.y + 15, -1, self.block_boundaries))

    def move_projectiles(self):
        updated_projectiles = []
        for projectile in self.projectiles:
            if projectile.move():
                updated_projectiles.append(projectile)
        self.projectiles = updated_projectiles

    def draw_projectiles(self, app):
        for projectile in self.projectiles:
            projectile.draw(app)
    
class Player(object): 

    standing_image = loadImageFromStringReference("Ground.png")
    standing_left_image = loadImageFromStringReference("Ground Left.png")
    running_images = [loadImageFromStringReference("Run1.png"),
                      loadImageFromStringReference("Run2.png"),
                      loadImageFromStringReference("Run4.png"),
                      loadImageFromStringReference("Run5.png")]
    running_left_images = [loadImageFromStringReference("Run1L.png"),
                      loadImageFromStringReference("Run2L.png"),
                      loadImageFromStringReference("Run4L.png"),
                      loadImageFromStringReference("Run5L.png")]
    jumping_image = loadImageFromStringReference("Jump.png")
    jumping_left_image = loadImageFromStringReference("Jump Left.png")
    falling_image = loadImageFromStringReference("Fall.png")
    falling_left_image = loadImageFromStringReference("Fall Left.png")
    hit_image = [loadImageFromStringReference("Hit 1.png"),
                loadImageFromStringReference("Hit 2.png"),
                loadImageFromStringReference("Hit 3.png"),
                loadImageFromStringReference("Hit 4.png")]
    

    def __init__(self, x, y):
        self.w, self.h = getImageSize(Player.standing_image)  
        self.invulnerable = False   #invulnerability state
        self.invulnerableTime = 0   #invulnerability timer
        self.x = x                  #setting x coordinate
        self.y = y                  #setting y coordinate
        self.cell = 50              #size of the square
        self.left = False           #will use it later to change the image based on which direction player goes
        self.right = False
        self.isDead = False         #checking status of the player
        self.dy = 0                 #for jumping
        self.ddy = 1
        self.onGround = False       #checking if player is on the ground
        self.points = 0

        self.curr_image = self.standing_image
        self.curImg = 0                                                     #tracking current image
        self.blips = 0
        self.state = "standing"
        self.count = 0
        self.release = "right"

    def makeInvulnerable(self, duration):
        self.invulnerable = True
        self.invulnerableTime = duration


    #drawing the player
    def draw(self, app):
        drawImage(self.curr_image, self.x - app.scrollX, self.y, align = "center")
        

    def update_image(self):
        if self.state == "hit":
            self.curr_image = self.hit_image[self.curImg]
        elif self.state == "standing":
            self.curr_image = self.standing_image
        elif self.state == "standing left":
            self.curr_image = self.standing_left_image
        elif self.state == "running":
            self.curr_image = self.running_images[self.curImg]
        elif self.state == "running left":
            self.curr_image = self.running_left_images[self.curImg]
        elif self.state == "jumping":
            self.curr_image = self.jumping_image
        elif self.state == "jumping left":
            self.curr_image = self.jumping_left_image
        elif self.state == "falling":
            self.curr_image = self.falling_image
        elif self.state == "falling left":
            self.curr_image = self.falling_left_image

    #jumping
    def onStep(self, app):
        self.blips += 1                                                 #changing the image every {stepspersec ^ 10}
        if self.blips % 5 == 0:        
            self.curImg = (self.curImg + 1) % 4

        if self.state == "hit":
            self.count +=1
            if self.count == 3*30:
                self.count = 0
             
        self.y += self.dy
        self.dy += self.ddy

        if self.invulnerable:  #decrease the invulnerability timer
            self.invulnerableTime -= 1
            if self.invulnerableTime <= 0:
                self.invulnerable = False

        if not self.isDead:                     #checking if player is alive
            self.onGround = False               #checking if player is on the ground

            for (bx, by, bw, bh) in app.level1.blocks:

                #check if player stand on this particular block, checking the xy coordinates
                if (bx <= self.x<= bx + bw) and by <= self.y + self.h//2 <= by + self.dy:
                    self.dy = 0                         #setting v to 0
                    self.y = by - self.h//2             #setting y coordinate so that it stand on this block
                    self.onGround = True                #changing status to onground
                    break

            for b in app.level1.floatingBlocks:
                fx = b.x
                fy = b.y
                fw = b.width
                fh = b.height
                if (fx <= self.x <= fx + fw) and (fy <= self.y +self.h//2 <= fy + self.dy):
                    self.dy = 0                         #setting v to 0
                    self.y = fy - self.h//2             #setting y coordinate so that it stand on this block
                    self.onGround = True                #changing status to onground
                    break

            if self.count != 0:
                self.state = "hit"
            elif self.dy > 0:
                if self.release =="right":
                    self.state = "falling"
                else:
                    self.state = "falling left"
            elif self.dy < 0:
                if self.release =="right":
                    self.state = "jumping"
                else:
                    self.state = "jumping left"
            elif self.right:
                self.state = "running"
            elif self.left:
                self.state = "running left"
            else:
                if self.release =="right":
                    self.state = "standing"
                else:
                    self.state = "standing left"

        self.update_image()


    def kill(self):                 #changing the status of the player
        self.isDead = True
        

    #if the movement is possible return true
    def inFrame(self, app, dx, dy):           #creating method to ensure that player does not collide with the blocks          

        x1 = self.x + dx
        y1 = self.y + dy


        for (bx, by, bw, bh) in app.level1.blocks:
            if (bx < x1 < bx + bw) and (by < y1):
                
                return False
            
        for b in app.level1.floatingBlocks:
            fx = b.x
            fy = b.y
            fw = b.width
            fh = b.height
            if (fx < x1 < fx + fw) and (fy < y1 < fy + fh):
                return False

        return True

    def findClosestEnemy(self, app):
        closest_distance = float('inf')
        closest_enemy = None

        for enemy in app.enemies:
            d = distance(self.x, self.y, enemy.x, enemy.y)
            if d < closest_distance:
                closest_distance = d
                closest_enemy = enemy
        app.closestEnemy = closest_enemy
        app.closestDist = closest_distance

class Background(object):

    Life = loadImageFromStringReference("PowerDown.png")

    def __init__(self):
        self.blocks = []            #list of tuples (x, y, width, height) of the block
        self.visitedColumns = set() #keeping track of the generated columns
        self.cell_size = 160        #size of the block
        self.max_rows = 3           #max N of the blocks in a column
        self.predefined_sizes = [   #predefined width/height of the blocks
            (160, 50),
            (160, 100),
            (160, 150)
        ]

        self.powerUps = []
        self.coins = []
        self.powerDown = []
        
        self.floatingBlocks = []
        self.shootingEnemies = []
        self.rightFloatingBlock = -self.cell_size
        self.leftFloatingBlock = +self.cell_size

    def highest_block_y(self, x):                     #method to ensure that player stands on the highest part of the block
        hy = 600

        for (bx, by, bw, bh) in self.blocks:
            if bx < x < bx + bw and by < hy:                     #checking x coordinate of player and block
                hy = by                                 #changing y coord to y coord of the block
        return hy                      #returning y value
        
    def generate_column(self, col, app, PowerUp, Coin):

        #randomly choosing a predefined block size
        width, height = self.predefined_sizes[randint(0, len(self.predefined_sizes) - 1)]

        x = col * self.cell_size    #setting x coordinate
        y = 600 - height            #setting y coordinate
        self.y = y

        self.blocks.append((x, y, width, height))       #adding blocks to the list
        self.visitedColumns.add(col)                    #adding generated columns

        if len(self.visitedColumns) % 5 == 0:  #creating them every 800 pixels

            x_powerup = randint(app.scrollX, app.scrollX + app.width)
            y_curr = self.highest_block_y(x_powerup)
            y_powerup = randint(y_curr - 170, y_curr - 165)                    #generate random height above the block
            powerups = PowerUp(x_powerup, y_powerup)
            if powerups.inFrame(app, 20, 0) or powerups.inFrame(app, -20, 0):
                self.powerUps.append(powerups)

        if randint(0, 1):

            x_coin = randint(x, x + width - 20)
            y_coin = randint(250, y - 50)
            coins = Coin(x_coin, y_coin)
            if coins.inFrame(app, 0, 20) or coins.inFrame(app, 0, -20):
                self.coins.append(coins)


        if randint(0, 1) and (x > self.rightFloatingBlock + app.width//2 or x < self.leftFloatingBlock - app.width//2):
            x_float = randint(x, x + width - 20)
            y_curr = self.highest_block_y(x)
            y_float = randint(y_curr - 280, y_curr - 200)
            floating_block = FloatingBlock(x_float, y_float, 180, 30)
            self.floatingBlocks.append(floating_block)
            if x > self.rightFloatingBlock + app.width:
                self.rightFloatingBlock = x_float
            else:
                self.leftFloatingBlock = x_float
            n = randint(0, 2)
            if n == 1:
                block_boundaries = floating_block.get_boundaries()
                self.shootingEnemies.append(ShootingEnemy(x_float + 100, y_float - 30, block_boundaries))
                if randint(0, 1):
                    x_power2 = x_float + 110
                    y_power2 = y_float - 60
                    powerdowns = PowerDown(x_power2, y_power2)
                    self.powerDown.append(powerdowns)

    
    def update_blocks(self, app):
        left_col = (app.scrollX // self.cell_size) - 1                  #N of the most left column
        right_col = (app.scrollX + app.width) // self.cell_size + 1     #N of the most right column

        for col in range(left_col, right_col + 1):                      #looping over all the columns on the screen
            if col not in self.visitedColumns:                          #checking if the columns was not generated
                self.generate_column(col, app, PowerUp, Coin)                               #adding to the set of generated columns

    def draw(self, app):
        self.update_blocks(app)                                              #generating all the needed blocks

        for (x, y, width, height) in self.blocks:                            #looping over the list with blocks
            if x - app.scrollX + width > 0 and x - app.scrollX < app.width:  #checking if the blocks are on the screen
                drawRect(x - app.scrollX, y, width, height, fill="brown")    #drawing blocks on the screen
                drawRect(x - app.scrollX, y, width, 20, fill="green")    #drawing blocks on the screen

        for powerUp in self.powerUps:
            powerUp.draw(app)

        for p in self.powerDown:
            p.draw(app)

        for coin in self.coins:
            coin.draw(app)

        for floatingBlock in self.floatingBlocks:
            floatingBlock.draw(app)

        for shootingEnemy in self.shootingEnemies:
            shootingEnemy.draw(app)
            shootingEnemy.draw_projectiles(app)

class Enemy(object):

    images = [loadImageFromStringReference("enemy1.png"),          #loading images for the enemy character
              loadImageFromStringReference("enemy2.png")]

    def __init__(self, x, y):
        self.w, self.h = getImageSize(Enemy.images[0])                      #finding width and height based on the size of the image
        self.x = x + self.w//2                                                          #setting x coordinate
        self.y = y - self.h//2                                           #setting y coordinate, accounting for the height
        self.dy = 0                                                         #velocity for falling
        self.ddy = 1                                                        #aceleration for falling
        self.dx = 3                                                        #constanly going left
        self.curImg = 0                                                     #tracking current image
        self.blips = 0                                                      #tracking switch of the image
        self.isDead = False   
        self.onGround = False 

    def draw(self, app):
        drawImage(Enemy.images[self.curImg], self.x - app.scrollX, self.y, align="center")      #drawing enemy, add highest y

    def onStep(self, app):
        self.blips += 1                                                 #changing the image every {stepspersec ^ 10}
        if self.blips % 15 == 0:                                    
            self.curImg = (self.curImg + 1) % 2


        self.x -= self.dx                                               #going left
        self.y += self.dy                                               #for falling
        self.dy += self.ddy

        if not self.isDead:
            for (bx, by, bw, bh) in app.level1.blocks:
                if (bx <= self.x - self.w//2 <= bx + bw or bx <= self.x + self.w//2 <= bx + bw) and by <= self.y + self.h//2 <= by + self.dy:
                    self.dy = 0
                    self.y = by - self.h//2
                    self.onGround = True
                    break


        #checking for collisions with blocks to change direction
        if not self.isDead:
            for (bx, by, bw, bh) in app.level1.blocks:
                if bx <= self.x <= bx + bw and (self.y + self.h//2 > by or self.y + self.h//2 < by):
                    self.dx = -self.dx
                    self.x -= self.dx
                    break
                

    def collidesWithPlayer(self, other):
        if self.isDead:                                         #not checking if the enemy is dead
            return False
        
        w, h = getImageSize(Player.standing_image)

        d = distance(self.x, self.y, other.x, other.y)        #finding distance between enemy and player, not working right now???
        a = ((self.w//2) ** 2 + (self.h//2) ** 2) ** 0.5 + ((w//2) ** 2 + (h//2) ** 2) ** 0.5

        if d < a:                           #if distance is less than 50 than we collide with hero
            return True
        else:
            return False

    def angleToPlayer(self, other):                         #finding angle between player and enemy
        return angleTo(self.x, self.y, other.x, other.y)

    def kill(self, app):             
        self.isDead = True                  #changing the status, stopping movements
        self.dx = 0

class PowerUp(object):
    image = loadImageFromStringReference("PowerUp1.png")  #load power-up image
    time = 5

    def __init__(self, x, y):
        self.w, self.h = getImageSize(PowerUp.image)
        self.x = x
        self.y = y
        self.direction = 1
        self.counter = 0

    def update(self):
        self.x += self.direction
        self.counter += 3
        if abs(self.counter) > 50:
            self.direction *= -1
            self.counter *= -1

    def inFrame(self, app, dx, dy):           #creating method to ensure that coins do not collide with the blocks          

        x1 = self.x + dx
        y1 = self.y + dy


        for (bx, by, bw, bh) in app.level1.blocks:
            if (bx < x1 < bx + bw) and (by < y1):
                return False
            
        for b in app.level1.floatingBlocks:
            fx = b.x
            fy = b.y
            fw = b.width
            fh = b.height
            if (fx < x1 < fx + fw) and (fy < y1 < fy + fh):
                return False

        return True
    
    
    def draw(self, app):
        drawImage(PowerUp.image, self.x - app.scrollX, self.y, align="center")

    def collidesWithPlayer(self, app):
        w, h = getImageSize(Player.jumping_image)
        d = distance(self.x, self.y, app.p.x, app.p.y)
        a = ((self.w//2) ** 2 + (self.h//2) ** 2) ** 0.5 + ((w//2) ** 2 + (h//2) ** 2) ** 0.5
        if d < a:
            return True
        else:
            return False
    
class PowerDown(object):
    image = loadImageFromStringReference("PowerDown.png")

    def __init__(self, x, y):
        self.w, self.h = getImageSize(PowerDown.image)
        self.x = x
        self.y = y
    
    
    def draw(self, app):
        drawImage(PowerDown.image, self.x - app.scrollX, self.y)

    def collidesWithPlayer(self, app):
        w, h = getImageSize(Player.jumping_image)
        d = distance(self.x, self.y, app.p.x, app.p.y)
        a = ((self.w//2) ** 2 + (self.h//2) ** 2) ** 0.5 + ((w//2) ** 2 + (h//2) ** 2) ** 0.5
        if d < a:
            return True
        else:
            return False

class Lives(object):
    redheart = loadImageFromStringReference("redheart2.png")

    greyheart = loadImageFromStringReference("greyheart2.png")
    
    def __init__(self, app, initial_lives=3):
        self.lives1 = initial_lives
        self.heart_margin = 10
        self.app = app

    def draw(self):
        for i in range(3):
            if i < self.lives1:
                drawImage(Lives.redheart, i * 50, 10)
            else:
                drawImage(Lives.greyheart, i * 50, 10)

    def lose_life(self):
        self.lives1 -= 1
        if self.lives1 <= 0:
            self.app.gameState = 'gameOver'
    
    def add_life(self):
        if self.lives1 <= 2:
            self.lives1 += 1

def onAppStart(app):
    app.closestEnemy = None
    app.closestDist = 0
    app.gameState = 'mainPage'              #setting game status to the main page
    app.bgcolor = rgb(137, 207, 240)        #adding color to the background when game starts
    app.cell = 160                                               #setting size of the cell/block
    app.scrollX = 0                                             #setting scrolling coord
    app.groundLevel = app.height - app.height / 10              
    app.groundWidth = app.width                                 
    app.sky = loadImageFromStringReference('IMG_4010.JPG')
    app.lives = Lives(app)

    app.time1 = 0
    app.time = 0
    app.speed = 1
    app.powerUp_status = "nonactive"
    
def reset(app):
    app.gameState = 'game'
    app.blips = 0                                               #adding blips for image change

    app.level1 = Background()                                   #creating background
    app.level1.update_blocks(app)                               #creating background

    app.wp, app.hp = getImageSize(Player.standing_image)
    xp = 400
    yp = app.level1.highest_block_y(xp) - app.hp//2 #getting highest block for player start
    app.p = Player(xp, yp)                                 #creating player

    app.w, app.h = getImageSize(Enemy.images[0])


    app.enemies = [Enemy(600, app.level1.highest_block_y(600 + app.w//2) ),
                   Enemy(900, app.level1.highest_block_y(900 + app.w//2) ),
                   Enemy(200, app.level1.highest_block_y(200 + app.w// 2) )]
    
    app.cell = 160                                               #setting size of the cell/block
    app.scrollX = 0                                             #setting scrolling coord
    app.groundLevel = app.height - app.height / 10              #need to change it, since now ground level changes
    app.groundWidth = app.width                                 #need to change it, since no actual ground width because of scrolling
    app.sky = loadImageFromStringReference('IMG_4010.JPG')
    app.lives = Lives(app)

    app.time1 = 0
    app.time = 0
    app.speed = 1
    app.powerUp_status = "nonactive"
    app.ptime = PowerUp.time
    app.pcolor = "yellow"
    
def restart(app):
    reset(app)
    app.gameState = 'game'

def onKeyPress(app, key):

    if app.gameState == 'mainPage':
        if key == 'enter':
            app.gameState = 'game'
            reset(app)

    if app.gameState == 'game':
        if key in 'Rr':
            reset(app)

    if app.gameState == 'gameOver':
        if key == 'enter':
            reset(app)
            app.gameState = 'game'

def onKeyHold(app, keys):

    if app.gameState == 'game':

        if "right" in keys and app.p.inFrame(app, 10 * app.speed, 0):

            if app.p.x - app.scrollX > 600:
                app.scrollX += 10 * app.speed
            app.p.x += 10 * app.speed                       #app.dx
            app.p.right = True
            app.p.left = False

        elif "left" in keys and app.p.inFrame(app, -10 * app.speed, 0):

            if app.p.x - app.scrollX < 200:
                app.scrollX -= 10 * app.speed
            app.p.x -= 10 * app.speed
            app.p.right = False
            app.p.left = True

        if "up" in keys and app.p.onGround:
            app.p.dy = -20

def onKeyRelease(app, key):
    if key == 'left':
        app.p.left = False
        app.p.release = "left"
    if key == 'right':
        app.p.right = False
        app.p.release = "right"

def onStep(app):
    app.time1 += 1

    if app.powerUp_status == "active":
        if app.time1 % 30 == 0:
            app.ptime -= 1
        if app.ptime <= 3:
            app.pcolor = "red"
        app.time -= 10

    if app.gameState == 'game':
        app.p.onStep(app)

        for coin in app.level1.coins:
            coin.update()
            if coin.collidesWithPlayer(app):
                app.p.points += 1
                app.level1.coins.remove(coin)

        for enemy in app.level1.shootingEnemies:
            enemy.move_projectiles()

            for projectile in enemy.projectiles:
                if projectile.collidesWithPlayer(app):
                    if not app.p.invulnerable:
                        app.lives.lose_life()
                        app.p.state = "hit"
                        app.p.makeInvulnerable(3 * 30)
                    if app.lives.lives1 <= 0:
                        app.gameState = 'gameOver'
                        app.p.kill()
                    enemy.projectiles.remove(projectile)

        if app.time1 % 10 == 0:  #adjusting the shooting frequency as needed
            for enemy in app.level1.shootingEnemies:
                enemy.shoot()

        app.p.findClosestEnemy(app)  #updating closest enemy tracking

        #generating new enemy if distance is >= 600
        if app.closestDist >= 700:
            if app.closestEnemy:
                if app.p.right:
                    new_enemy_x = app.p.x + 301  #placing new enemy to the right
                else:
                    new_enemy_x = app.p.x - 301  #placing new enemy to the left
                
                new_enemy_y = app.level1.highest_block_y(new_enemy_x + app.w//2) - app.h // 2
                app.enemies.append(Enemy(new_enemy_x, new_enemy_y))
                app.closestDist = app.p.findClosestEnemy(app)  #reseting closest distance to avoid continuous enemy generation
        for e in app.enemies:
            e.onStep(app)

        for powerUp in app.level1.powerUps:
            powerUp.update()
            if powerUp.collidesWithPlayer(app):
                app.time = 1500
                app.ptime = PowerUp.time
                app.pcolor = "yellow"
                app.powerUp_status = "active"
                app.level1.powerUps.remove(powerUp)

        for p in app.level1.powerDown:
            if p.collidesWithPlayer(app):
                app.lives.add_life()
                app.level1.powerDown.remove(p)
        
        if app.time > 0:
            app.speed = 2
        else:
            app.powerUp_status = "nonactive"
            app.speed = 1
            app.time = 0
            app.ptime = 5


    if app.gameState == 'game':
        for e in app.enemies:
            e.onStep(app)

            if e.collidesWithPlayer(app.p) and not app.p.invulnerable:
                a = e.angleToPlayer(app.p)
                app.p.makeInvulnerable(3 * 30)
                if a > 315 or a < 45:
                    e.kill(app)
                    app.p.points += 10
                    app.enemies.remove(e)
                else:
                    app.lives.lose_life()
                    app.p.state = "hit"
                    if app.lives.lives1 <= 0:
                        app.gameState = 'gameOver'
                        app.p.kill()

def redrawAll(app):

    if app.gameState == 'mainPage':
        drawImage(app.sky, 0, 0)
        drawRect(100, 30, app.width - 200, app.height - 60, fill='white', opacity=80)
        drawRect(150, app.height // 2 - 100, 500, 100, fill='white', border="lightBlue", borderWidth= 8, opacity=90)
        drawLabel('Python Jump Quest', app.width // 2, app.height // 2 - 50, size=50, fill='black', font="helvetica", bold=True)
        drawLabel('Press Enter to Start', app.width // 2, app.height // 2 + 50, size=30, fill='black')

    if app.gameState == 'game':
        drawImage(app.sky, 0, 0)
        app.level1.draw(app)
        app.p.draw(app)
        app.lives.draw()
        for e in app.enemies:
            e.draw(app)
        drawLabel(f'Points: {app.p.points}', 700, 20, size=20, fill='yellow', font="helvetica", bold = True)
        if app.powerUp_status == "active":
            drawLabel(f'Power Up: 00:0{app.ptime}', 370, 20, size=20, fill=app.pcolor, font="helvetica", bold = True)

    if app.gameState == 'gameOver':
        drawRect(0, 0, app.width, app.height, fill="lightBlue")
        drawLabel('Game Over', app.width // 2, app.height // 2 - 50, size=50, fill='red', font="helvetica", bold = True)
        drawLabel('Press Enter to Restart', app.width // 2, app.height // 2 + 50, size=30, fill='white')


def main():
    runApp(800, 600)

main()