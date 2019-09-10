# Sidescroller Pygame
import pygame
import random
import math
 
# Global constants
 
# Colors
BLUE = (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
 
class Player(pygame.sprite.Sprite):
    frame=0
    frames = []
 
    # -- Methods
    def __init__(self):
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.frame = 0
        for i in range(5):
            self.frames.append(pygame.image.load("mario"+str(i+1)+".png"))
        self.image = self.frames[0]
        
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
		
		#Animation
        if self.change_x != 0:
            self.frame+=.25
            self.image = self.frames[math.floor(self.frame)%5]
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit // Collision fixing
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite. //Collision fixing
                self.rect.left = block.rect.right
 
        # Move up/down through jumping or falling
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                if block.type == 1:
                    block.CreateCoin(self.level)
 
            # Stop the vertical movement when you hit the ground
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # Check if on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
 
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        self.change_x = -6
 
    def go_right(self):
        self.change_x = 6
 
    def stop(self):
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    """ Used instead of bricks """
    type = 0
	
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.image.load("brick.png")
 
        self.rect = self.image.get_rect()
			
 
 
class Level():
 
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
 
    def draw(self, screen):
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def scroll(self, shift_x):
        """ Scrolling function """
 
        # Keep track of the scroll amount
        self.world_shift += shift_x
 
        # Scroll bricks and coin blocks
        for platform in self.platform_list:
            platform.rect.x += shift_x
 

 
 
# Create bricks and coin bricks for the level
class Map(Level):
 
    def __init__(self, player):
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with x,y,w,h, type of brick
        level = [[70, 70, 500, 500, 0],
                 [140, 70, 800, 400, 0],
                 [70, 70, 1000, 500, 0],
                 [140, 70, 1120, 280, 0],
                 [20, 20, 1000, 200, 1],
				 [20, 20, 500, 300, 1]
				 ]
 
        # Go through the array above and add bricks 0 or coin bricks 1
        for platform in level:
            if platform[4] == 0:
                block = Platform(platform[0], platform[1])
                block.rect.x = platform[2]
                block.rect.y = platform[3]
                block.player = self.player
                self.platform_list.add(block)
            else:
                block = CB(platform[0],platform[1])
                block.rect.x = platform[2]
                block.rect.y = platform[3]
                block.player = self.player
                self.platform_list.add(block)

class CB(pygame.sprite.Sprite):
    type = 1
    coinList = []
    def __init__(self, width, height):
        """ Constructor for the coinblock """
        super().__init__()
        self.image = pygame.image.load("CB1.png")
        self.rect = self.image.get_rect()
        self.coinNum=5
	
    def CreateCoin(self,level):
        if self.coinNum > 0:
            self.coinNum-=1
            tempCoin = Coin()
            tempCoin.rect.y=self.rect.y-32
            tempCoin.rect.x=self.rect.x
            self.coinList.append(tempCoin)
            level.platform_list.add(tempCoin)
            if self.coinNum == 0:
                self.image = pygame.image.load("CB2.png")
	
class Coin(pygame.sprite.Sprite):
    """ Constructor for coin """
    type = 2
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.change_y = -3
		
    def update(self):
        self.rect.y+=self.change_y
        self.change_y+=.25
        if self.change_y >= 3:
            self.rect.x = 0
            self.rect.y = 0
            self.image = pygame.image.load("empty.png")
 
def main():
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Side-scrolling Platformer")
 
    # Create the Mario
    player = Player()
 
    # Create the level
    level_list = []
    level_list.append(Map(player))
 
    # Set the only level i made
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
 
    # Loop until closed.
    done = False
 
    # slow the screen update because python is slow
    clock = pygame.time.Clock()
 
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the mario
        active_sprite_list.update()
 
        # Player goes too far right, kick back left
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.scroll(-diff)
 
        # Player goes too far left, kick back right
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.scroll(diff)
 
 
        # Draw
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
 
        # Limit the frames because python is slow as a turtle
        clock.tick(60)
 
        # update screen with drawn objects
        pygame.display.flip()
 
    # Work in IDLE
    pygame.quit()
 
if __name__ == "__main__":
    main()