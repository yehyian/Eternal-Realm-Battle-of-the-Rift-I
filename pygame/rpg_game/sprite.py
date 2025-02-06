import pygame
#from main import *
from config import *
from pygame.locals import *
import time
import math
import random
import sys

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dialogue):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        #image_to_load = pygame.image.load("pygame/rpg_game/img/single.png")
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.set_colorkey(BLACK)
        #self.image.blit(image_to_load, (0,0))

        self.dialogues = dialogue
        self.current_line = 0
        self.is_running = False
        self.speed = 3

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.battle_count = 0
        self.is_battling = False
        self.is_alive = True
        self.is_talking = False
        self.battle_status = 'none'

        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemies()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if self.is_talking == False:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += self.speed
                self.x_change -= self.speed
                self.facing = 'left'
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= self.speed
                self.x_change += self.speed
                self.facing = 'right'
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += self.speed
                self.y_change -= self.speed
                self.facing = 'up'
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= self.speed
                self.y_change += self.speed
                self.facing = 'down'

    def collide_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.speed
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= self.speed

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.speed
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= self.speed
    
    def animate(self):
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1 
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1 
        
        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1 
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1 

    def talk(self):
        if self.current_line < len(self.dialogues):
            return self.dialogues[self.current_line]
        return ""
    
    def next_line(self):
        '''print('n')
        print('is_talking = ', self.is_talking)
        print('current line = ',self.current_line)'''
        if self.is_talking:
            if self.current_line < len(self.dialogues) - 1:
                self.current_line += 1
            else:
                self.is_talking = False
                self.current_line = 0
            #print('nextline')
        
    def draw_talk_box(self):
        if self.is_talking:
            # Draw a gray rectangle for the talk box
            
            box_rect = pygame.Rect(50, WIN_HEIGHT - 150, WIN_WIDTH - 100, 100)
            pygame.draw.rect(self.game.screen, GRAY, box_rect)
            pygame.draw.rect(self.game.screen, BLACK, box_rect, 3)
            

            # Get the current dialogue text
            #print(self.talk())
            dialogue_text = self.talk()

            # Render the text and blit it to the screen
            self.text = self.game.font.render(dialogue_text, True, BLACK)
            self.text_rect = self.text.get_rect(midleft = (box_rect.x + 20, box_rect.y + 50))
            #dsvhdkcjsikhduvhsdhuhuhsduhishusdchushusdcuhjksdhujksfdchujksedfguefsogulvewdwguevdewgfhueflh print(self.text, self.text_rect)
            self.game.screen.blit(self.text, self.text_rect)  

#enemy
class Webber(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(10, 30)

        #self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        #self.image.set_colorkey(BLACK)

        image_to_load = pygame.image.load("pygame/rpg_game/img/webber.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        '''
        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]
        '''

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0
    
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        '''
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1 
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1 
        '''

        '''if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1 
        
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1'''
    
class House(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = HOUSE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        ground_type = random.randint(1, 2)
        if ground_type == 1:
            image_to_load = pygame.image.load("pygame/rpg_game/img/house_1.png")
        else:
            image_to_load = pygame.image.load("pygame/rpg_game/img/house_2.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.tree
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load("pygame/rpg_game/img/tree.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Flower(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.tree
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load("pygame/rpg_game/img/flower.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bush(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER + 1
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load("pygame/rpg_game/img/bush.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Road(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.direction = direction
        if self.direction == 'U':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_up.png")
        if self.direction == 'D':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_down.png")
        if self.direction == 'L':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_left.png")
        if self.direction == 'R':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_right.png")
        if self.direction == 'tr':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_right_top.png")
        if self.direction == 'tl':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_left_top.png")
        if self.direction == 'br':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_right_bottom.png")
        if self.direction == 'bl':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_left_bottom.png")
        if self.direction == 'M':
            image_to_load = pygame.image.load("pygame/rpg_game/img/village_road_middle.png")

        
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class River(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        image_to_load = pygame.image.load("pygame/rpg_game/img/river.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if (x > 103 and x < 206 and y > 24 and y < 43) or x > 307:
            self.image = self.game.terrain_spritesheet.get_sprite(992, 544, self.width, self.height)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        
        #image_to_load = pygame.image.load("pygame/rpg_game/img/single1.png")
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.set_colorkey(BLACK)
        #self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if (x > 103 and x < 206 and y > 24 and y < 43) or x > 307:
            ground_type = random.randint(1, 2)
            if ground_type == 1:
            #self.image = self.game.terrain_spritesheet.get_sprite(352, 160, self.width, self.height)
                image_to_load = pygame.image.load("pygame/rpg_game/img/cave_ground.png")
            else:
                image_to_load = pygame.image.load("pygame/rpg_game/img/cave_ground2.png")
            self.image = pygame.Surface([self.width, self.height])
            self.image.set_colorkey(BLACK)
            self.image.blit(image_to_load, (0,0))
            
        elif x > 106 and x < 127 and y > 69 and y < 93:
            self.image = self.game.terrain_spritesheet.get_sprite(416, 576, self.width, self.height)
        
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
            decorate = random.randint(1, 1000)
            if decorate < 2:
                Tree(self.game, x, y)
            if decorate >= 5 and decorate < 10:
                Flower(self.game, x, y)
            
        
        #image_to_load = pygame.image.load("pygame/rpg_game/img/single1.png")
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.set_colorkey(BLACK)
        #self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('NotoSansCJK.ttc', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center = (self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)
    
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(500, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()
        if self.game.player.is_battling:
            self.kill()
    
    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            if self.game.progress == 'dealing_with_webber':
                self.game.killed_enemies += 1
        hits = pygame.sprite.spritecollide(self, self.game.tree, True)
        hits = pygame.sprite.spritecollide(self, self.game.goblin, False)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.3
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.3
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.3
            if self.animation_loop >= 5:
                self.kill()
        
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.3
            if self.animation_loop >= 5:
                self.kill()

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dialogues, image, phase):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.npc
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load(image)
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.dialogues = dialogues
        self.current_line = 0
        self.is_talking = False
        self.is_talked = False
        self.talk_count = 0

        self.phase = phase

    def update(self):
        self.interact(self.game.player)
        if self.phase < self.game.phase:
            self.kill()
        #print(self.is_talking)
        '''if self.is_talking:
            self.draw_talk_box()'''
            #print('draw finished')

    def interact(self, player):
        if self.rect.colliderect(player.rect):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.is_talking = True
        else:
            self.is_talking = False
            self.current_line = 0

    def talk(self):
        if self.current_line < len(self.dialogues):
            return self.dialogues[self.current_line]
        return ""
    
    def next_line(self):
        '''print('n')
        print('is_talking = ', self.is_talking)
        print('current line = ',self.current_line)'''
        if self.is_talking:
            if self.current_line < len(self.dialogues) - 1:
                self.current_line += 1
            else:
                self.is_talked = True
                self.is_talking = False
            #print('nextline')
        
    def draw_talk_box(self):
        if self.is_talking:
            # Draw a gray rectangle for the talk box
            
            box_rect = pygame.Rect(50, WIN_HEIGHT - 150, WIN_WIDTH - 100, 100)
            pygame.draw.rect(self.game.screen, GRAY, box_rect)
            pygame.draw.rect(self.game.screen, BLACK, box_rect, 3)
            

            # Get the current dialogue text
            #print(self.talk())
            dialogue_text = self.talk()

            # Render the text and blit it to the screen
            self.text = self.game.font.render(dialogue_text, True, BLACK)
            self.text_rect = self.text.get_rect(midleft = (box_rect.x + 20, box_rect.y + 50))
            #dsvhdkcjsikhduvhsdhuhuhsduhishusdchushusdcuhjksdhujksfdchujksedfguefsogulvewdwguevdewgfhueflh print(self.text, self.text_rect)
            self.game.screen.blit(self.text, self.text_rect)

class Goblin(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dialogues):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.goblin, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load("pygame/rpg_game/img/goblin.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        if y >= 9 and y <= 12:
            self.be_killed = True
        else:
            self.be_killed = False

        self.dialogues = dialogues
        self.current_line = 0

        self.is_talking = False
        self.is_alive = True
    
    def update(self):
        if self.is_alive == False:
            self.kill()

    def talk(self):
        if self.current_line < len(self.dialogues):
            return self.dialogues[self.current_line]
        return ""
    
    def next_line(self):
        if self.is_talking:
            if self.current_line < len(self.dialogues) - 1:
                self.current_line += 1
            else:
                self.is_talking = False
            #print('nextline')
        
    def draw_talk_box(self):
        if self.is_talking:
            # Draw a gray rectangle for the talk box
            
            box_rect = pygame.Rect(50, WIN_HEIGHT - 150, WIN_WIDTH - 100, 100)
            pygame.draw.rect(self.game.screen, GRAY, box_rect)
            pygame.draw.rect(self.game.screen, BLACK, box_rect, 3)
            

            # Get the current dialogue text
            #print(self.talk())
            dialogue_text = self.talk()

            # Render the text and blit it to the screen
            self.text = self.game.font.render(dialogue_text, True, BLACK)
            self.text_rect = self.text.get_rect(midleft = (box_rect.x + 20, box_rect.y + 50))
            #dsvhdkcjsikhduvhsdhuhuhsduhishusdchushusdcuhjksdhujksfdchujksedfguefsogulvewdwguevdewgfhueflh print(self.text, self.text_rect)
            self.game.screen.blit(self.text, self.text_rect)

class Pokemon(pygame.sprite.Sprite):

    def __init__(self, game, name, level, x, y, max_hp, speed, attack, defense, moves, power, image_file):

        pygame.sprite.Sprite.__init__(self)

        #req = requests.get(f'{base_url}/pokemon/{name.lower()}')
        #self.json = req.json()

        #set pokemon's name and level
        self.name = name
        self.level = level

        self.game = game

        #set position
        self.x = x + 50
        self.y = y + 50

        #number of potions left
        self.num_potions = 3

        self.max_hp = max_hp
        self.current_hp = max_hp
        self.speed = speed
        self.attack = attack
        self.defense = defense

        self.moves = moves
        self.power = power

        self.image_file = image_file

        #set the sprite's width
        self.size = 10

        #set the sprite to the frong facing sprite
        self.set_sprite('front_default')

    def perform_attack(self, other, move, power):

        display_message(self.game, f'{self.name} 穡雿踹?? {move}')

        #pause for 2 seconds
        time.sleep(2)

        #calculate the damage
        damage = power

        #same type attack bonus (STAB)
        '''if move.type in self.types:
            damage *= 1.5'''

        #critical hit (6.25% chance)
        random_num = random.randint(1, 10000)
        if random_num <= 625:
            damage *= 1.5

        #round down the damage
        damage = math.floor(damage)

        other.take_damage(damage)

    def take_damage(self, damage):

        self.current_hp -= damage
        #hp should not go below 0
        if self.current_hp < 0:
            self.current_hp = 0
    
    def use_potion(self):

        #check if there are potions left
        if self.num_potions > 0:

            #add 30 hp (but don't go over the max hp)
            self.current_hp += 30
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp

            #decrease the number of the potions left
            self.num_potions -= 1

    def set_sprite(self, side):

        self.image = pygame.image.load(self.image_file)

        #scale the image
        scale = self.size / self.image.get_width()
        new_width = self.image.get_width() * scale / 3 * 2
        new_height = self.image.get_height() * scale / 3 * 2
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def set_moves(self):
        pass

    def draw(self, alpha = 255):
        
        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        self.game.screen.blit(sprite, (self.x, self.y))

    def draw_hp(self):

        #display the health bar
        bar_scale = 2
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(self.game.screen, red, bar)

        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(self.game.screen, green, bar)
        
        #display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.current_hp} / {self.max_hp}', True, black)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        self.game.screen.blit(text, text_rect)
    
    def get_rect(self):
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

class shadow(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load("pygame/rpg_game/img/shadow.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.move = True

    def update(self):
        if self.move:
            while self.rectl.y > 0:
                self.rect.y -= 20
            self.move = False
        
class Trigger_box(pygame.sprite.Sprite):
    def __init__(self, game, x, y, game_progress, game_phase):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.trigger_boxes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load("pygame/rpg_game/img/nothing.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.game_progress = game_progress
        self.phase = game_phase

    def update(self):
        if self.rect.colliderect(self.game.player.rect) and self.phase <= self.game.phase:
            self.game.progress = self.game_progress

            for box in self.game.trigger_boxes:
                if box.game_progress == self.game.progress:
                    box.kill()
            self.kill()

class Air_wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, game_phase):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load("pygame/rpg_game/img/nothing.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.phase = game_phase

    def update(self):
        if self.phase <= self.game.phase:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_to_load = pygame.image.load(image)
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(BLACK)
        self.image.blit(image_to_load, (0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

def display_message(game, message):

    g = game
    #draw a white box with black border
    pygame.draw.rect(g.screen, white, (10, 550, 1180, 140))
    pygame.draw.rect(g.screen, black, (10, 550, 1180, 140), 3)

    #display the message
    #font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = g.font.render(message, True, black)
    text_rect = text.get_rect()
    text_rect.x = 30
    text_rect.y = 610
    g.screen.blit(text, text_rect)

    pygame.display.update()

def create_button(game, width, height, left, top, text_cx, text_cy, label):

    g = game
    #position of the mouse cursor
    mouse_cursor = pygame.mouse.get_pos()

    button = Rect(left, top, width, height)

    #hightlight the button if mouse is pointing to it
    if button.collidepoint(mouse_cursor):
        pygame.draw.rect(g.screen, gold, button)
    else:
        pygame.draw.rect(g.screen, white, button)
    
    #add the label to the button
    #font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = g.font.render(f'{label}', True, black)
    text_rect = text.get_rect(center = (text_cx, text_cy))
    g.screen.blit(text, text_rect)

    return button
