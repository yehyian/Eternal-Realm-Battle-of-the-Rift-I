import pygame
from sprite import *
from config import *
from pygame.locals import *
import sys
import tkinter as tk
import time  

class battle:

    def __init__(self, game, rival, progress):
        pygame.init()
        self.game_status = 'prebattle'

        self.game = game
        self.level = 30

        self.rival = rival
        self.progress = progress
        
        if progress == 'first_battle':
            self.player_pokemon = Pokemon(self.game, '節勳', self.level, 175, 70, 70, 6, 40, 30, ['上鉤拳', '橫砍', '蓄力突刺', '旋風斬'], [10, 20, 30, 40], "pygame/rpg_game/img/single.png")
            self.rival_pokemon = Pokemon(self.game, '魏柏諭', self.level, 25, 150, 100, 5, 34, 40, ['黏液束縛', '蠕動突進', '怒吼', '野蠻衝撞'], [62, 33, 57, 52], "pygame/rpg_game/img/webber.png")
        if progress == 'battle_with_coach':
            self.player_pokemon = Pokemon(self.game, '節勳', self.level, 175, 70, 200, 6, 40, 30, ['上鉤拳', '橫砍', '蓄力突刺', '旋風斬'], [40, 30, 50, 60], "pygame/rpg_game/img/single.png")
            self.rival_pokemon = Pokemon(self.game, '教練', self.level, 25, 150, 100, 5, 34, 40, ['狂暴連擊', '野蠻摔投', '裂地轟擊', '碎顱重拳'], [67, 36, 87, 72], "pygame/rpg_game/img/instructor.png")

        self.rival_pokemon.level = int(self.rival_pokemon.level * .75)

        self.player_pokemon.hp_x = 275
        self.player_pokemon.hp_y = 250
        self.rival_pokemon.hp_x = 800
        self.rival_pokemon.hp_y = 50

        self.font = pygame.font.Font('NotoSansCJK.ttc', 20)

    def main(self):
        #game loop
        while self.game_status != 'quit':
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_status = 'quit'

                #detect mouse click
                if event.type == MOUSEBUTTONDOWN:
                    
                    mouse_click = event.pos

                    if self.game_status == 'player turn':
                        
                        time.sleep(.5)
                        # check if fight button was clicked
                        if fight_button.collidepoint(mouse_click):
                            self.game_status = 'player move'
                            
                        # check if potion button was clicked
                        if potion_button.collidepoint(mouse_click):
                            
                            # force to attack if there are no more potions
                            if self.player_pokemon.num_potions == 0:
                                display_message(self.game, '沒藥了!!')
                                time.sleep(2)
                                self.game_status = 'player move'
                            else:
                                self.player_pokemon.use_potion()
                                display_message(self.game, f'{self.player_pokemon.name} 用了一瓶藥')
                                time.sleep(2)
                                self.game_status = 'rival turn'

                    elif self.game_status == 'player move':

                        #check which move button was clicked
                        for i in range(len(move_buttons)):
                            button = move_buttons[i]

                            if button.collidepoint(mouse_click):
                                move = self.player_pokemon.moves[i]
                                power = self.player_pokemon.power[i]
                                self.player_pokemon.perform_attack(self.rival_pokemon, move, power)

                                #check if the rival's pokemon fainted
                                if self.rival_pokemon.current_hp == 0:
                                    self.game_status = 'fainted'
                                else:
                                    self.game_status = 'rival turn'
            
            if self.game_status == 'prebattle':

                g.screen.fill(white)
                pygame.display.update()

                self.player_pokemon.set_moves()
                self.rival_pokemon.set_moves()

                self.player_pokemon.x = 0
                self.player_pokemon.y = 150
                self.rival_pokemon.x = 1000
                self.rival_pokemon.y = 0

                self.player_pokemon.size = 300
                self.rival_pokemon.size = 300
                self.player_pokemon.set_sprite('back_default')
                self.rival_pokemon.set_sprite('front_default')

                self.game_status = 'start battle'

            #start battle animation
            if self.game_status == 'start battle':

                alpha = 0
                while alpha < 255:
                    g.screen.fill(white)
                    self.rival_pokemon.draw(alpha)
                    display_message(self.game, f'敵方派出 {self.rival_pokemon.name}!')
                    alpha += .4

                    pygame.display.update()
                
                time.sleep(1)

                alpha = 0
                while alpha < 255:
                    g.screen.fill(white)
                    self.rival_pokemon.draw()
                    self.player_pokemon.draw(alpha)
                    display_message(self.game, f'去吧 {self.player_pokemon.name}!')
                    alpha += .4

                    pygame.display.update()
                
                self.player_pokemon.draw_hp()
                self.rival_pokemon.draw_hp()

                #determine who goes first
                if self.rival_pokemon.speed > self.player_pokemon.speed:
                    self.game_status = 'rival turn'
                else:
                    self.game_status = 'player turn'

                pygame.display.update()

                time.sleep(1)

            if self.game_status == 'player turn':

                g.screen.fill(white)
                self.player_pokemon.draw()
                self.rival_pokemon.draw()
                self.player_pokemon.draw_hp()
                self.rival_pokemon.draw_hp()

                #create the fight and potion buttons
                fight_button = create_button(self.game, 240, 100, 710, 440, 830, 487, '戰鬥')
                potion_button = create_button(self.game, 240, 100, 950, 440, 1070, 487, f'吃藥({self.player_pokemon.num_potions})')

                pygame.draw.rect(g.screen, black, (710, 440, 480, 100), 3)

                pygame.display.update()
            
            if self.game_status == 'player move':
                
                g.screen.fill(white)
                self.player_pokemon.draw()
                self.rival_pokemon.draw()
                self.player_pokemon.draw_hp()
                self.rival_pokemon.draw_hp()
                
                move_buttons = []
                for i in range(len(self.player_pokemon.moves)):
                    move = self.player_pokemon.moves[i]
                    button_width = 240
                    button_height = 70
                    left = 710 + i % 2 * button_width
                    top = 400 + i // 2 * button_height
                    text_center_x = left + 120
                    text_center_y = top + 35
                    button = create_button(self.game, button_width, button_height, left, top, text_center_x, text_center_y, move)
                    move_buttons.append(button)
                    
                # draw the black border
                pygame.draw.rect(self.game.screen, black, (710, 400, 480, 140), 3)
                
                pygame.display.update()

            if self.game_status == 'rival turn':

                g.screen.fill(white)
                self.player_pokemon.draw()
                self.rival_pokemon.draw()
                self.player_pokemon.draw_hp()
                self.rival_pokemon.draw_hp()

                display_message(self.game, '')
                time.sleep(2)

                #select a random move
                move = random.choice(self.rival_pokemon.moves)
                power = random.choice(self.rival_pokemon.power)
                self.rival_pokemon.perform_attack(self.player_pokemon, move, power)

                #check if the player's pokemon fainted
                if self.player_pokemon.current_hp == 0:
                    self.game_status = 'fainted'
                else:
                    self.game_status = 'player turn'
                
                pygame.display.update()

            #one of the pokemons fainted
            if self.game_status == 'fainted':

                alpha = 255
                while alpha > 0:

                    self.game.screen.fill(white)
                    self.player_pokemon.draw_hp()
                    self.rival_pokemon.draw_hp()

                    if self.rival_pokemon.current_hp == 0:
                        self.player_pokemon.draw()
                        self.rival_pokemon.draw(alpha)
                        display_message(self.game, f'{self.rival_pokemon.name} 死了!')
                    else:
                        self.player_pokemon.draw(alpha)
                        self.rival_pokemon.draw()
                        display_message(self.game, f'{self.player_pokemon.name} 死了!')

                    alpha -= .4

                    pygame.display.update()

                self.game_status = 'gameover'
            
            if self.game_status == 'gameover':
                self.game.player.is_battling = False
                if self.rival_pokemon.current_hp == 0:
                    display_message(self.game, '你贏了')
                    self.rival.is_alive = False
                    self.game.player.battle_status = 'win'
                    
                else:
                    display_message(self.game, '為柏諭好菜')
                    self.game.player.battle_status = 'lose'
                    

                pygame.display.update()

                time.sleep(1)
                
                self.game_status = 'quit'
                print('end')

            print(self.game_status)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("永恆之境：裂縫之戰I")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('NotoSansCJK.ttc', 32)
        self.running = True

        self.character_spritesheet = Spritesheet("pygame/rpg_game/img/character.png")
        self.terrain_spritesheet = Spritesheet("pygame/rpg_game/img/terrain.png")
        self.enemy_spritesheet = Spritesheet("pygame/rpg_game/img/enemy.png")
        self.attack_spritesheet = Spritesheet("pygame/rpg_game/img/attack.png")
        self.intro_background = pygame.image.load("pygame/rpg_game/img/start.png")
        self.game_over_background = pygame.image.load("pygame/rpg_game/img/lose.png")
        self.end_background = pygame.image.load("pygame/rpg_game/img/continue.png")

        self.progress = 'start'
        self.phase = 0  
        self.walk_count = 0
        self.killed_enemies = 0
        
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column != ' ':
                    Ground(self, j, i)
                '''if column == ' ':
                    Webber(self, j, i)'''
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i, [])
                if column == 'W':
                    Webber(self, j, i)
                if column == 'H':
                    House(self, j, i)
                if column == 'T':
                    Tree(self, j, i)
                if column == 'b':
                    Bush(self, j, i)
                if column == 'V':
                    Wall(self, j, i, "pygame/rpg_game/img/village_wall.png")
                if column == 'A':
                    Wall(self, j, i, "pygame/rpg_game/img/adventure_wall.png")
                if column == '-':
                    Wall(self, j, i, "pygame/rpg_game/img/fence_front.png")
                if column == '|':
                    Wall(self, j, i, "pygame/rpg_game/img/fence_side.png")
                #road
                if column == 'u':
                    Road(self, j, i, 'U')
                if column == 'd':
                    Road(self, j, i, 'D')
                if column == 'l':
                    Road(self, j, i, 'L')
                if column == 'r':
                    Road(self, j, i, 'R')
                if column == '(':
                    Road(self, j, i, 'tl')
                if column == ')':
                    Road(self, j, i, 'tr')
                if column == '[':
                    Road(self, j, i, 'bl')
                if column == ']':
                    Road(self, j, i, 'br')
                if column == 'm':
                    Road(self, j, i, 'M')

                if column == 'R':
                    River(self, j, i)
                if column == 'G':
                    self.goblin1 = Goblin(self, j, i, [])
                if column == 'p':
                    self.plain_dog = NPC(self, j, i, [], "pygame/rpg_game/img/plain_dog.png", 5)
                if column == 'g':
                    self.guardian = NPC(self, j, i, [], "pygame/rpg_game/img/guardian.png", 5)
                if column == 'I':
                    self.instructor = NPC(self, j, i, ['A:可以跟你打聽一下情報嗎',
                                                      '冒險家:.....',
                                                      '(一通講解之後)',
                                                      'A:原來是這樣啊，情況比我預想的更可怕呢，怎麼辦呢',
                                                      ], "pygame/rpg_game/img/instructor.png", 2)
                if column == 'K':
                    self.katheryne = NPC(self, j, i, [], "pygame/rpg_game/img/katheryne.png", 5)
                if column == 't':
                    print(j, i)
        self.A = NPC(self, 56, 10, ['(撥開草叢後)', 
                                    '節勳:阿阿阿阿阿',
                                    'A:阿阿阿阿阿',
                                    'A:喔，是你喔',
                                    '節勳:欸，阿妳怎麼也在這樹林',
                                    '節勳:這節是國文欸，我要記你曠課',
                                    'A:?',
                                    'A:隨便你，反正我不差這一次',
                                    'A:阿我們現在要怎麼辦',
                                    '節勳:你怎麼會問我啊',
                                    'A:喔，我的鍋',
                                    'A:那就先試著找點水吧',
                                    'A:我有看很多貝爺',
                                    '節勳:我也知道我們可以吃老鼠',
                                    'A:信我一把',
                                    '節勳:那就走吧',
                                    'A:不要',
                                    '節勳:???',
                                    'A:跟著這條路走會看到一個山洞',
                                    'A:去裡面找我'
                                    ], "pygame/rpg_game/img/A.png", 0)
        self.A = NPC(self, 183, 32, [], "pygame/rpg_game/img/A.png", 1)
        self.A = NPC(self, 61, 83, ['A:去找冒險者問問吧'], "pygame/rpg_game/img/A.png", 1)
        self.A = NPC(self, 111, 83, [], "pygame/rpg_game/img/A.png", 3)
        
        self.treasrue = NPC(self, 381, 45, ['這個寶箱有人開過了'], "pygame/rpg_game/img/treasure.png", 1)
        self.airwall_triggerbox()
       
    def airwall_triggerbox(self):
         #trigger box
        for i in range(1, 15):
            self.see_shadow_trigger_box = Trigger_box(self, 37, i, 'shadow', 0)

        for i in range(32, 40):
            self.into_cave_trigger_box = Trigger_box(self, 55, i, 'into_cave', 0)
        for i in range(52, 68):
            self.into_cave_trigger_box = Trigger_box(self, i, 42, 'into_cave', 0)
        for i in range(51, 67):
            self.into_cave_trigger_box = Trigger_box(self, i, 32, 'into_cave', 0)

        self.in_cave_trigger_box = Trigger_box(self, 136, 32, 'in_cave', 0)

        for i in range(27, 40):
            self.see_goblin_cave_trigger_box = Trigger_box(self, 179, i, 'notice_plain_dog', 0)

        self.out_cave_trigger_box = Trigger_box(self, 69, 36, 'out_cave', 1)
        self.out_cave_trigger_box = Trigger_box(self, 69, 37, 'out_cave', 1)

        for i in range(75, 86):
            self.get_in_village = Trigger_box(self, 40, i, 'outside_village', 1)
        
        for i in range(75, 86):
            self.get_in_village = Trigger_box(self, 50, i, 'get_in_village', 1)

        for i in range(79, 84):
            self.meet_instructor_trigger_box = Trigger_box(self, 58, i, 'meet_instructor', 1)
        
        for i in range(80, 83):
            self.talk_to_katheryne_trigger_box = Trigger_box(self, 109, i, 'talk_to_katheryne', 1)
        
        for i in range(175, 184):
            self.talk_to_katheryne_trigger_box = Trigger_box(self, i, 75, 'arrive_training_ground', 1)

        for i in range(80, 83):
            self.meet_katheryne_again_trigger_box = Trigger_box(self, 114, i, 'meet_katheryne_again', 2)

        for i in range(27, 40):
            self.see_goblin_cave_trigger_box = Trigger_box(self, 140, i, 'back_to_cave', 2)

        self.generate_goblin_trigger_box = Trigger_box(self, 121, 32, 'generate_goblin', 2)

        self.nothing_trigger_box = Trigger_box(self ,309, 24, 'nothing_happen1', 1)
        self.nothing_trigger_box = Trigger_box(self ,440, 24, 'nothing_happen2', 1)
        self.nothing_trigger_box = Trigger_box(self ,336, 54, 'nothing_happen3', 1)
        self.nothing_trigger_box = Trigger_box(self ,335, 34, 'nothing_happen4', 1)
        self.nothing_trigger_box = Trigger_box(self ,381, 45, 'nothing_happen5', 1)

        #air wall
        self.airwall = Air_wall(self, 13, 57, 1)
        self.airwall = Air_wall(self, 14, 57, 1)

        for i in range(1, 15):
            self.airwall = Air_wall(self, 137, i, 2)
        
        for i in range(52, 57):
            self.airwall = Air_wall(self, 108, i, 2)

        for i in range(59, 66):
            self.airwall = Air_wall(self, 116, i, 2)

        self.airwall = Air_wall(self, 116, 68, 2)
        self.airwall = Air_wall(self, 116, 69, 2)

        self.airwall = Air_wall(self, 116, 93, 2)
        self.airwall = Air_wall(self, 116, 94, 2)

        for i in range(96, 99):
            self.airwall = Air_wall(self, 116, i, 2)

    def new(self):
        # a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npc = pygame.sprite.LayeredUpdates()
        self.trigger_boxes = pygame.sprite.LayeredUpdates()
        self.tree = pygame.sprite.LayeredUpdates()
        self.goblin = pygame.sprite.LayeredUpdates()
        self.goblin_king = pygame.sprite.LayeredUpdates()
        self.createTilemap()

        self.target = Goblin(self, -100, -100, [])

    def events(self):
        #game loop events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.player.is_talking:
                        self.player.next_line()
                        
                    for n in self.npc:
                        if n.is_talking:
                            #print('start draw')
                            n.next_line()
                            #print('draw fin')

                if event.key == pygame.K_LSHIFT:
                    if self.player.is_running:
                        #print('walking')
                        self.player.speed = 3
                        self.player.is_running = False

                    else:
                        #print('running')
                        self.player.speed = 8
                        self.player.is_running = True

                if event.key == pygame.K_SPACE:

                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y - TILESIZE)
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y - TILESIZE)

                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y - 2 * TILESIZE)
                        Attack(self, self.player.rect.x, self.player.rect.y - 2 * TILESIZE)
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y - 2 * TILESIZE)

                    if self.player.facing == 'down': 
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y + TILESIZE)
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y + TILESIZE)

                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y + 2 * TILESIZE)
                        Attack(self, self.player.rect.x, self.player.rect.y + 2 * TILESIZE)
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y + 2 * TILESIZE)

                    if self.player.facing == 'left': 
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y + TILESIZE)
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y - TILESIZE)

                        Attack(self, self.player.rect.x - 2 * TILESIZE, self.player.rect.y + TILESIZE)
                        Attack(self, self.player.rect.x - 2 * TILESIZE, self.player.rect.y)
                        Attack(self, self.player.rect.x - 2 * TILESIZE, self.player.rect.y - TILESIZE)

                    if self.player.facing == 'right': 
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y + TILESIZE)
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y - TILESIZE)

                        Attack(self, self.player.rect.x + 2 * TILESIZE, self.player.rect.y + TILESIZE)
                        Attack(self, self.player.rect.x + 2 * TILESIZE, self.player.rect.y)
                        Attack(self, self.player.rect.x + 2 * TILESIZE, self.player.rect.y - TILESIZE)

    def update(self):
        #game loop updates
        self.all_sprites.update()
        '''Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y - TILESIZE)
        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y + TILESIZE)
        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y + TILESIZE)
        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y - TILESIZE)'''

    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        for n in self.npc:
            if n.is_talking and n.talk_count == 0:
                n.draw_talk_box()

        if self.player.is_talking:
            self.player.draw_talk_box()

        if self.progress == 'shadow' and self.player.is_talking == False:
            self.screen.fill(BLACK)

        if self.progress == 'choose_the_way':
            self.stay_button = create_button(self, 240, 100, 710, 440, 830, 487, '留下來種田')
            self.leave_button = create_button(self, 240, 100, 950, 440, 1070, 487, '踏上冒險之路')

        if self.progress == 'katheryne_walking':
            self.walk_count += 1
            if self.walk_count < 100:
                self.katheryne.rect.y -= 2
            else:
                self.walk_count = 0
                self.progress = 'meet_coach'

        if self.progress == 'coach_walking':
            if self.coach.rect.x > 640:
                self.coach.rect.x -= 4
            else:
                self.walk_count = 0
                self.progress = 'talk_to_coach'

        if self.progress == 'katheryne_walk_back':
            self.walk_count += 1
            if self.walk_count < 100:
                self.katheryne.rect.y += 2
            else:
                self.walk_count = 0
                self.progress = 'talk_to_katheryne_and_coach'

        if self.progress == 'choose_accept_or_not' and self.player.is_talking == False:
            self.accept_button = create_button(self, 360, 100, 470, 440, 650, 487, '接受這艱難的任務')
            self.reject_button = create_button(self, 360, 100, 830, 440, 1010, 487, '使勁往門的方向逃跑')
        
        if self.progress == 'the_next_day' and self.player.is_talking == False:
            self.screen.fill(BLACK)

        if self.progress == 'coach_and_A_walking':
            self.walk_count += 1
            if self.walk_count < 260:
                self.final_A.rect.x += 5
                self.final_coach.rect.x += 5
            else:
                self.walk_count = 0
                self.progress = 'meet_goblin_king'
        
        if self.progress == 'goblin_king_move':
            self.walk_count += 1
            if self.walk_count < 4:
                self.gking1.rect.x -= 16
                self.gking2.rect.x -= 16
                self.gking3.rect.x -= 16
                self.gking4.rect.x -= 16
                self.gking5.rect.x -= 16
                self.gking6.rect.x -= 16
                self.gking7.rect.x -= 16
                self.gking8.rect.x -= 16
                self.gking9.rect.x -= 16
                self.walk_count += 1
            else:
                self.walk_count = 0
                self.progress = 'instructor_attack'

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if self.player.battle_count == 0:
                if self.player.is_battling:

                    if self.progress == 'first_battle':
                        self.target = NPC(self, -100, -100, [], 'pygame/rpg_game/img/goblin.png', 5)
                    
                    if self.progress == 'battle_with_coach':
                        self.target = NPC(self, -100, -100, [], 'pygame/rpg_game/img/instructor.png', 5)

                    self.player.battle_count = 1
                    b = battle(g, self.target, self.progress)
                    self.progress = 'battling'
                    b.main()
                    self.player.is_battling = 0
                    self.player.battle_count = 0
                    self.target.kill()
                        
            if self.progress == 'start':
                self.player.dialogues = ['節勳:Ashiba，這甚麼鬼地方                                                                (按e繼續對話)', 
                                        '節勳:難道這就是輕小說中所謂穿越的劇情嗎?',
                                        '節勳:算了啦，至少這裡沒有數學課',
                                        '節勳:先跟著這條路走吧'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'shadow' and self.player.is_talking == False:

                time.sleep(.3)
                self.player.dialogues = ['(看到黑影閃過)', 
                                        '節勳:(發出了驚訝的讚嘆聲)',
                                        '節勳:幹那三小啦',
                                        '(去前面的草叢看看吧)'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'

            if self.progress == 'into_cave':

                self.player.dialogues = ['節勳:這裡有一個山洞欸，或許我們可以在這裡紮營過夜',
                                        '(進入山洞)'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'in_cave':

                self.player.dialogues = ['(角落好像有黑影在竄動)',
                                        '土撥鼠聖女:節勳救救我........'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'notice_plain_dog':

                self.player.dialogues = ['節勳:!!',
                                        '(一絲不掛的聖女正在被一大群柯布林做著不可告人的事情)',
                                        '(柯布林得意的叫聲)',
                                        '節勳:騙人的吧',
                                        'A:一起上吧',
                                        '(進入了戰鬥)'
                                        ]
                self.player.is_talking = True
                self.progress = 'first_battle'

            if self.progress == 'first_battle' and self.player.is_talking == False:
                self.player.is_battling = True

            if self.progress == 'battling' and b.progress == 'first_battle':
                if self.player.battle_status == 'lose':
                    self.progress = 'first_battle_lose'
                    self.player.battle_status = 'none'

                if self.player.battle_status == 'win':
                    self.progress = 'first_battle_win'
                    self.player.battle_status = 'none'
            
            #if self.progress == 'first_battle_win':

            if self.progress == 'first_battle_lose':

                self.player.dialogues = ['節勳:可惡！我們太弱了，才會讓土撥鼠眼睜睜被它們帶走',
                                        'A:看來這個山洞是魔物的聚集地，感覺不能在這裡過夜了，我們另找地方吧',
                                        'A:這個世界的南方有一座村莊',
                                        'A:我們在那邊會合吧',
                                        '(先離開洞穴吧)'
                                        ]
                self.player.is_talking = True
                self.phase = 1
                self.progress = 'none'

            if self.progress == 'out_cave':

                self.player.dialogues = ['(先跟著下面那條路走吧)',
                                        '(村莊應該就在這條路的盡頭)'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'

            if self.progress == 'outside_village':

                self.player.dialogues = ['（看見了遠處的村莊）',
                                         '節勳:原來這個世界也有人類居住地啊！進去看看吧'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'

            if self.progress == 'get_in_village':

                self.player.dialogues = ['節勳:（這個村莊怎麼跟我想不太一樣，到處都死氣沈沈的）',
                                        '守衛：站住，何許人也！',
                                        '節勳:我們是穿越而…嗚嗚嗚',
                                        '(現在還是不要透漏我們的身分比較好)',
                                        '(好吧)',
                                        '節勳:我們來自東方，只是個平平無奇的冒險家而已',
                                        '守衛：原來是這樣，那你們為甚麼要來這個村莊呢',
                                        '節勳:我受到了哥布林的攻擊，想在這個村莊過夜',
                                        '守衛：嘖，哥布林潮也蔓延到這裡來了嗎，好吧，你們跟我來',
                                        'A:看來今天是可以在這裡過夜了'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'meet_instructor':

                self.player.dialogues = ['（遇到了一個冒險家）',
                                        '(A也在那邊)',
                                        '(去問問冒險家吧)'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.instructor.talk_count == 0:
                if self.instructor.is_talked:
                    self.progress = 'choose_the_way'
                    self.instructor.talk_count += 1
                         
            if self.progress == 'choose_the_way':
                
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        mouse_click = event.pos

                        if self.stay_button.collidepoint(mouse_click):
                            self.progress = 'stay'

                        if self.leave_button.collidepoint(mouse_click):
                            self.progress = 'leave'

            if self.progress == 'stay':
                self.player.dialogues = ['冒險者：好吧',
                                         'A：太失望了'
                                        ]
                self.player.is_talking = True
                self.progress = 'the_end'

            if self.progress == 'leave':

                self.player.dialogues = ['A:好吧，既然你這樣選擇了，我也會盡力幫助你的',
                                        'A:那我們先去他剛剛說的冒險者協會看看吧'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'talk_to_katheryne':
                self.player.dialogues = ['（抵達冒險者協會）',
                                        '凱瑟琳：您好，我是凱瑟琳，有什麼可以幫你的嗎',
                                        '節勳:嗚哇，怎麼每一個冒險家協會都有凱瑟琳',
                                        'A:?',
                                        '凱瑟琳：?',
                                        '節勳:沒事',
                                        '凱瑟琳：如果需要幫助的話，需要註冊成為冒險者才行喔',
                                        '節勳:好吧，那我們就註冊吧',
                                        '（填寫表格）',
                                        '節勳：我去 魔法劍士這職位聽起來好炫砲',
                                        '節勳：決定了 我要成為魔法劍士 剩下的資料就亂填吧',
                                        'A:那我要當魔法使 在你身後亂轟一堆魔法',
                                        '節勳：？',
                                        'A:?',
                                        '凱瑟琳：那我現在就依表格上的資料替各位申請身分 請在此稍等'
                                        ]
                self.player.is_talking = True
                self.progress = 'katheryne_go_away'

            if self.progress == 'katheryne_go_away' and self.player.is_talking == False:

                self.player.dialogues = ['節勳：現在這樣直接去救土撥鼠也是毫無勝算 ',
                                        '節勳：我們還是先在這裡訓練一下吧 還可以順便打工賺錢',
                                        'A:我沒意見'
                                        ]
                self.player.is_talking = True
                self.progress = 'katheryne_walking'
            
            if self.progress == 'meet_coach' and self.player.is_talking == False:
                self.coach = NPC(self, 39, 8, [], "pygame/rpg_game/img/instructor.png", 3)
                self.progress = 'coach_walking'

            if self.progress == 'talk_to_coach':

                self.player.dialogues = ['教官：有人說到訓練！？ 沒問題 我可以負責鍛鍊你們兩個弱雞',
                                        '節勳：呃啊 謝謝？',
                                        'A:（小聲說）不是 這老兄看起來就不是什麼善茬 確定要相信他嗎',
                                        '節勳：沒事啦 反正通常肌肉大的人都沒什麼腦袋',
                                        '節勳：他應該是單純想幫我們而已吧'
                                        ]
                self.player.is_talking = True
                self.progress = 'katheryne_move'

            if self.progress == 'katheryne_move' and self.player.is_talking == False:
                self.progress = 'katheryne_walk_back'

            if self.progress == 'talk_to_katheryne_and_coach':

                self.player.dialogues = ['凱瑟琳：哎呀 看來兩位已經和我們分部的教官認識了',
                                        '凱瑟琳：你們有任何戰鬥上的問題都可以請教他哦 還有 別死了 加油',
                                        '節勳：聽起來不太妙',
                                        '教官：那麼現在就給你們第一個訓練',
                                        '教官：去討伐WEBBER吧',
                                        '節勳：啊？',
                                        'A:啊？',
                                        '節勳：我們就此因為打不贏哥布林才會想要訓練一下',
                                        '教官：沒想到現在的新晉冒險家都這麼菜 但不需要害怕',
                                        '教官：我會在旁邊協助你們的',
                                        'A:完了 但感覺拒絕他會發生更可怕的事'
                                        ]
                self.player.is_talking = True
                self.progress = 'choose_accept_or_not'

            if self.progress == 'choose_accept_or_not' and self.player.is_talking == False:
                
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        mouse_click = event.pos

                        if self.accept_button.collidepoint(mouse_click):
                            self.progress = 'accept'

                        if self.reject_button.collidepoint(mouse_click):
                            self.progress = 'reject'
            
            if self.progress == 'accept':

                self.player.dialogues = ['教官：很好',
                                        '教官：雖然沒有實力',
                                        '教官：但你們的決心我確實看見了',
                                        '教官：我會幫助你們成長的',
                                        '教官：村莊東邊有一個訓練場',
                                        '教官：我在那邊等你'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'

            if self.progress == 'arrive_training_ground':
                self.player.dialogues = ['教官：這邊有15隻WEBBER',
                                        '教官：把他們處理掉',
                                        '教官：證明你的實力',
                                        '節勳：只好硬上了',
                                        '(按空白鍵攻擊WEBBER)'
                                        ]
                self.player.is_talking = True
                self.progress = 'dealing_with_webber'

            if self.progress == 'dealing_with_webber':
                if self.killed_enemies >= 15:
                    self.progress = 'train_finished'
                    self.phase = 2
                    self.killed_enemies = 0

            if self.progress == 'train_finished':
                self.player.dialogues = ['A:呼 儘管已經對峙過了 但真的要把他們掛了還是很可怕',
                                        '節勳：真的 但我們又離目標進了一步',
                                        '教官：看來你們完成訓練了',
                                        '教官：先回協會休息一下吧'
                                        ]
                self.player.is_talking = True
                self.progress = 'none'

            if self.progress == 'meet_katheryne_again':
                self.player.dialogues = ['凱瑟琳：你們還活著呀 能撐過那教官訓練的新人沒幾個',
                                        '你們就先好好休息吧 還有...',
                                        '教官：Yo 辛苦啦',
                                        'A：啊啊啊別再來啦',
                                        '教官：別怕 我這次是來告訴你們好消息的',
                                        '教官：聽說你們在打聽有關土撥鼠的事情',
                                        '教官：有線報指出他現在就被囚禁在哥布林巢穴中',
                                        '節勳：真的嗎 知道位置就代表我們可以去救他了A',
                                        'A:嗯 但依我們現在的實力想要闖入哥布林的大本營還是有點難度',
                                        '教官：哼哼 不用擔心 這次我會跟你們一起戰鬥的',
                                        '節勳：那就這樣決定了 明天一早就出發前往哥布林巢穴拯救土撥鼠'
                                        ]
                self.player.is_talking = True
                self.progress = 'the_next_day'

            if self.progress == 'the_next_day' and self.player.is_talking == False:
                time.sleep(2)
                self.progress = 'tomorrow_morning'
            
            if self.progress == 'tomorrow_morning':
                self.player.dialogues = ['（隔天',
                                        '教官：人都到了嗎 那就廢話少說',
                                        '教官：去把哥布林們滅了吧  巢穴就在北方 走吧',
                                        'A：回去我們第一次遇到哥布林的地方吧'
                                        ]
                self.player.is_talking = True
                self.phase = 3
                self.progress = 'none'

            if self.progress == 'generate_goblin':
                for i in range(41, 77):
                    for j in range(2, 17):
                        self.gb = Goblin(self, i, j, [])
                self.final_A = NPC(self, 39, 11, [], "pygame/rpg_game/img/A.png", 3)
                self.final_coach = NPC(self, 40, 10, [], "pygame/rpg_game/img/instructor.png", 3)
                self.gking1 = NPC(self, 83, 9, [], "pygame/rpg_game/img/king_1.png", 3)
                self.gking2 = NPC(self, 84, 9, [], "pygame/rpg_game/img/king_2.png", 3)
                self.gking3 = NPC(self, 85, 9, [], "pygame/rpg_game/img/king_3.png", 3)
                self.gking4 = NPC(self, 83, 10, [], "pygame/rpg_game/img/king_4.png", 3)
                self.gking5 = NPC(self, 84, 10, [], "pygame/rpg_game/img/king_5.png", 3)
                self.gking6 = NPC(self, 85, 10, [], "pygame/rpg_game/img/king_6.png", 3)
                self.gking7 = NPC(self, 83, 11, [], "pygame/rpg_game/img/king_7.png", 3)
                self.gking8 = NPC(self, 84, 11, [], "pygame/rpg_game/img/king_8.png", 3)
                self.gking9 = NPC(self, 85, 11, [], "pygame/rpg_game/img/king_9.png", 3)
                self.progress = 'none'

            if self.progress == 'back_to_cave':
                self.player.dialogues = ['（抵達巢穴',
                                        '哥布林：嗚嗄',
                                        'A:一堆哥布林擠在一起有點太噁',
                                        '教官：看我的'
                                        ]
                self.player.is_talking = True
                self.progress = 'coach_create_road'
            
            if self.progress == 'coach_create_road' and self.player.is_talking == False:
                self.progress = 'kill_goblin'
                for gob in self.goblin:
                    if gob.be_killed:
                        gob.kill()
                
            if self.progress == 'kill_goblin':
                self.player.dialogues = ['教官：快點 走這裡']
                self.player.is_talking = True
                self.progress = 'coach_and_A_move'
            
            if self.progress == 'coach_and_A_move' and self.player.is_talking == False:
                self.progress = 'coach_and_A_walking'

            if self.progress == 'meet_goblin_king':
                self.player.dialogues = ['哥布林王：咯咯咕咕！咕嚕咕嚕！嘿嘿嘿！',
                                        '哥布林：嗚嗄',
                                        '節勳：聽不懂他在說什麼 反正打他就對了',
                                        '（你打了哥布林王',
                                        '哥布林王：嗚嗚嗚啊啊',
                                        '教官：糟糕 看這架勢 他要狂暴了！ 你們兩個 到我身後',
                                        'A:救命 我的腳被它們抓住了',
                                        '教官：不好',
                                        '哥布林王：嗚嗄嗄'
                                        ]
                self.player.is_talking = True
                self.progress = 'goblin_king_attack'
            
            if self.progress == 'goblin_king_attack' and self.player.is_talking == False:
                self.progress = 'goblin_king_move'

            if self.progress == 'instructor_attack':
                self.player.dialogues = ['（哥布林王dash 到旁邊開大',
                                         '教官：呃阿'
                                        ]
                self.player.is_talking = True
                self.progress = 'goblin_king_died'
            
            if self.progress == 'goblin_king_died' and self.player.is_talking == False:
                self.gking1.kill()
                self.gking2.kill()
                self.gking3.kill()
                self.gking4.kill()
                self.gking5.kill()
                self.gking6.kill()
                self.gking7.kill()
                self.gking8.kill()
                self.gking9.kill()
                self.progress = 'instructor_last_talk'
            
            if self.progress == 'instructor_last_talk':
                self.player.dialogues = ['（教官一拳轟掉哥布林王',
                                         '(哥布林王自爆傷到了教官',
                                         '教官：咳咳 你們兩個…沒事吧'
                                        ]
                self.player.is_talking = True
                self.progress = 'instructor_died'

            if self.progress == 'instructor_died' and self.player.is_talking == False:
                self.final_coach.kill()
                self.progress = 'sad'

            if self.progress == 'sad':
                self.player.dialogues = ['節勳、A： 教官！',
                                         'A:他幫我抵擋了最致命的攻擊 卻沒能為自己擋下…',
                                         '節勳：噢 雖然我們才剛認識不久但他確實是個好人 帶他回協會吧',
                                         '土撥鼠：救我呀！',
                                         '節勳:對了 土撥鼠！',
                                         'A:這樣就結束了 一條命換一條命..',
                                         '節勳：…',
                                         '土撥鼠：… 我餓了 有吃的嗎',
                                         'A:靠 現在別講話',
                                         '節勳：走吧'
                                        ]
                self.player.is_talking = True
                self.progress = 'the_end'

            if self.progress == 'reject':

                self.player.dialogues = ['教官：在我面前想要逃跑？ 沒門']
                self.player.is_talking = True
                self.progress = 'battle_with_coach'
            
            if self.progress == 'battle_with_coach' and self.player.is_talking == False:
                self.player.is_battling = True

            if self.progress == 'battling' and b.progress == 'battle_with_coach':
                if self.player.battle_status == 'lose':
                    self.progress = 'battle_coach_lose'
                    self.player.battle_status = 'none'

                if self.player.battle_status == 'win':
                    self.progress = 'battle_coach_win'
                    self.player.battle_status = 'none'
            
            if self.progress == 'battle_coach_win':
                self.player.dialogues = ['(教練被你打死了)',
                                         '(冒險家協會替除了你的冒險家資格)',
                                         '(這個世界逐漸被哥布林佔領)',
                                         '(你沒能成功拯救土撥鼠)'
                                         ]
                self.player.is_talking = True
                self.progress = 'the_end'

            if self.progress == 'battle_coach_lose':
                self.player.dialogues = ['你死了']
                self.player.is_talking = True
                self.progress = 'you_lose'

            if self.progress == 'the_end' and self.player.is_talking == False:
                self.playing = False

            if self.progress == 'you_lose' and self.player.is_talking == False:
                self.playing = False

            if self.progress == 'nothing_happen1':
                self.player.dialogues = ['(這裡什麼都沒有)']
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'nothing_happen2':
                self.player.dialogues = ['(真的)']
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'nothing_happen3':
                self.player.dialogues = ['(都不相信我)']
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'nothing_happen4':
                self.player.dialogues = ['(前面真的什麼都沒有)']
                self.player.is_talking = True
                self.progress = 'none'
            
            if self.progress == 'nothing_happen5':
                self.player.dialogues = ['(活該)']
                self.player.is_talking = True
                self.progress = 'none'
                    
    def game_over(self):
        text = self.font.render('菜', True, WHITE)
        text_rect = text.get_rect(center = ((WIN_WIDTH/2), (WIN_HEIGHT/2) - 50))
        
        restart_button = Button((WIN_WIDTH/2) - 50, (WIN_HEIGHT/2), 100, 50, WHITE, BLACK, '重新', 30)
        exit_button = Button((WIN_WIDTH/2) - 50, (WIN_HEIGHT/2) + 70, 100, 50, WHITE, BLACK, '離開', 30)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.running = False
        
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.__init__()
                self.new()
                self.main()
            
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(self.game_over_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('永恆之境：裂縫之戰I', True, WHITE)
        title_rect = title.get_rect(x = (WIN_WIDTH/2) - 155, y = (WIN_HEIGHT/2) - 70)

        play_button = Button((WIN_WIDTH/2) - 60, (WIN_HEIGHT/2), 100, 50, WHITE, BLACK, '開始', 30)
        exit_button = Button((WIN_WIDTH/2) - 60, (WIN_HEIGHT/2) + 70, 100, 50, WHITE, BLACK, '離開', 30)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                sys.exit()

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def the_end(self):
        intro = True

        title = self.font.render('TO BE CONTINUE', True, BLACK)
        title_rect = title.get_rect(center = ((WIN_WIDTH/2) - 10, (WIN_HEIGHT/2) - 70))

        exit_button = Button((WIN_WIDTH/2) - 60, (WIN_HEIGHT/2), 100, 50, WHITE, BLACK, '離開', 30)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                sys.exit()

            self.screen.blit(self.end_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
   
g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    if g.progress == 'the_end':
        g.the_end()
    else:
        g.game_over()

pygame.quit()
sys.exit()
