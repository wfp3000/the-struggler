
# Imports
import pygame
import random
import json



# Window settings
GRID_SIZE = 64
WIDTH = 25 * GRID_SIZE
HEIGHT = 14 * GRID_SIZE
TITLE = "The Struggler"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_ = (61, 61, 61)
WHITE = (255, 255, 255)

# staegs

START = 0
PLAYING = 1
LOSE = 2

LEVEL_COMPLETE = 3
WIN = 4

# Load fonts
font_xs = pygame.font.Font(None, 14)
font_xl = pygame.font.Font(None, 96)

font_lg = pygame.font.Font(None, 64)

font_md = pygame.font.Font(None, 32)
font_sm = pygame.font.Font(None, 24)



# Load images
hero_idle_imgs_rt = [pygame.image.load('assets/images/characters/Idle_right.png').convert_alpha()]
hero_idle_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_idle_imgs_rt]

hero_crouch_imgs_rt = [pygame.image.load('assets/images/characters/crouch.png').convert_alpha()]
hero_crouch_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_crouch_imgs_rt]


hero_walk_imgs_rt = [pygame.image.load('assets/images/characters/walk1.png').convert_alpha(),
                     pygame.image.load('assets/images/characters/walk2.png').convert_alpha(),
                     pygame.image.load('assets/images/characters/walk3.png').convert_alpha(),
                     pygame.image.load('assets/images/characters/walk4.png').convert_alpha(),
                     pygame.image.load('assets/images/characters/walk5.png').convert_alpha()]
hero_walk_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_walk_imgs_rt]

hero_jump_imgs_rt = [pygame.image.load('assets/images/characters/jump.png').convert_alpha()]
hero_jump_imgs_lt = [pygame.transform.flip(img, True, False) for img in hero_jump_imgs_rt]




grass_dirt_img = pygame.image.load('assets/images/tiles/Dead_Ground.png').convert_alpha()
platform2_img = pygame.image.load('assets/images/tiles/Cobble_Ceiling.png').convert_alpha()
platform_img = pygame.image.load('assets/images/tiles/Cobble_Wall.png').convert_alpha()
sit_img = pygame.image.load('assets/images/tiles/skeleton_sit.png').convert_alpha()
egg_img = pygame.image.load('assets/images/items/egg.png').convert_alpha()
steak_img = pygame.image.load('assets/images/items/health.png').convert_alpha()
heart_img = pygame.image.load('assets/images/items/heart.png').convert_alpha()




enemy_imgs_rt = [pygame.image.load('assets/images/characters/badguy.png').convert_alpha(),
                 pygame.image.load('assets/images/characters/badguy2.png').convert_alpha(),
                 pygame.image.load('assets/images/characters/badguy3.png').convert_alpha()]
              
enemy_imgs_lt = [pygame.transform.flip(img, True, False) for img in enemy_imgs_rt]




              
slug_imgs_rt = [pygame.image.load('assets/images/characters/prey_slug1.png').convert_alpha(),
                pygame.image.load('assets/images/characters/prey_slug2.png').convert_alpha(),
                pygame.image.load('assets/images/characters/prey_slug3.png').convert_alpha()]

slug_imgs_lt = [pygame.transform.flip(img, True, False) for img in slug_imgs_rt]


bonfire_img = pygame.image.load('assets/images/tiles/Bonfire.png').convert_alpha()




# Load sounds
jump_snd = pygame.mixer.Sound('assets/sounds/jump.wav')
egg_snd = pygame.mixer.Sound('assets/sounds/pickup_egg.wav')
level_up_snd = pygame.mixer.Sound('assets/sounds/next_level.wav')
hurt_snd = pygame.mixer.Sound('assets/sounds/hurt.wav')
game_win_snd = pygame.mixer.Sound('assets/sounds/game_win.wav')
game_over_snd = pygame.mixer.Sound('assets/sounds/game_over.wav')
eat_snd = pygame.mixer.Sound('assets/sounds/eat.wav')

#music
music = 'assets/music/music.wav'


# lEVELS
levels = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json']
# Settings
gravity = 1.0
terminal_velocity =  127

# Game classes

class Entity(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2

        self.vx = 0
        self.vy = 0
        
        
    def apply_gravity(self):
        self.vy += gravity

        if self.vy > terminal_velocity:
            self.vy = terminal_velocity
        
        
class AnimatedEntity(Entity):
    def __init__(self, x, y, images):
         super().__init__(x,y, images[0])

         self.images = images
         self.image_index = 0
         self.ticks = 0
         self.animation_speed = 10

    def set_image_list(self):
        self.images = self.images

        
    def animate(self):
        self.set_image_list()
        self.ticks += 1

        if self.ticks % self.animation_speed == 0:
            self.image_index += 1

            if self.image_index >= len(self.images):
                self.image_index = 0
                
            self.image = self.images[self.image_index]
            
            
        








         
    
class Hero(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        
        

        self.speed = 5
        self.jump_power = 15
        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.jumping = False
        self.crouching = False
        

        self.hurt_timer = 0
        self.health = 3
        self.eggs = 0
        self.score = 0
        


    def move_to(self, x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE//2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE//2

    def crouch(self):
        self.crouching = True
    
    def move_right(self):
    	self.vx = self.speed
    	self.facing_right = True
    	
    def move_left(self):
    	self.vx = -self.speed
    	self.facing_right = False
    	

    def stop(self):
        self.vx = 0
    
    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        if len(hits) > 0:
            self.vy -= self.jump_power
            self.jumping = True
            jump_snd.play()

    

    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.rect.centerx < hit.rect.centerx:
                self.rect.right = hit.rect.left
            elif self.rect.centerx > hit.rect.centerx:
                self.rect.left = hit.rect.right

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
                self.jumping = False
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0


    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > world_width:
            self.rect.right = world_width

    def check_enemies(self):
            hits = pygame.sprite.spritecollide(self, enemies, False)

            for enemy in hits:
                if self.hurt_timer == 0 :
                    self.health -= 1
                    hurt_snd.play()
                    if self.health < 1:
                        self.health = 0
                    self.hurt_timer = 1.0 * FPS
                    print(self.health)
                    print("oof")#playsound

                    
                if self.rect.x < enemy.rect.x:
                    self.vx = -15
                    
                elif self.rect.x > enemy.rect.x:
                    self.vx = 15


                if self.rect.y < enemy.rect.y:
                    self.vy = -7
                    
                    
                elif self.rect.y > enemy.rect.y:
                    self.vy = 7
                    
                    
            if self.hurt_timer > 0:
                self.hurt_timer -= 1

                if self.hurt_timer < 0:
                    self.hurt_timer = 0
            
            
    def check_items (self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)
            
    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, goal)

    def set_image_list(self):
        if self.facing_right:
            if self.jumping:
                self.images = hero_jump_imgs_rt
            elif self.crouching:
                self.images = hero_crouch_imgs_rt
            elif self.vx == 0:
                self.images = hero_idle_imgs_rt
            else:
                self.images = hero_walk_imgs_rt
                
        else:
            if self.jumping:
                self.images = hero_jump_imgs_lt
            elif self.crouching:
                self.images = hero_crouch_imgs_lt
            elif self.vx == 0:
                self.images = hero_idle_imgs_lt
            else:
                self.images = hero_walk_imgs_lt


        left = self.rect.left
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom 
        
    def update(self):
        self.apply_gravity()
        
        self.check_world_edges()
        
        self.check_items()
        
        self.check_enemies()

        self.move_and_check_platforms()

        self.animate()
        
        

            
class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Bonfire(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.rect.y += 4
        

class Foreground(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.rect.bottom = y * GRID_SIZE + GRID_SIZE
        self.rect.right = x * GRID_SIZE + GRID_SIZE
    
        
class Enemy(AnimatedEntity):
    
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        
        self.speed = 2
        self.vx = -1 * self.speed
        self.vy = 0
        
    def reverse(self):
        self.vx *= -1

        
    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = hit.rect.right
                self.reverse()

        self.rect.y += self.vy

        hits = pygame.sprite.spritecollide(self, platforms, False)

        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom

            self.vy = 0

    def check_world_platforms(self):
    
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        must_reverse = True

        for platform in hits:
            if self.vx < 0 and platform.rect.left <= self.rect.left:
                must_reverse = False

            elif self.vx > 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

        if must_reverse:
            self.reverse()


        

        

    def check_world_edges(self):

        
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > world_width:
            self.rect.right = world_width
            self.reverse()

    

        
class Red_guy(Enemy) :
    def __init__(self, x, y, images):
        super().__init__(x, y, images)


    def set_image_list(self):
        if self.vx > 0:
            self.images = enemy_imgs_lt
        else:
            self.images = enemy_imgs_rt
            
        
        
    def update(self):
        self.check_world_edges()
        
        self.move_and_check_platforms()
        self.apply_gravity()
        self.animate()
        

class Slug(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        self.rect.bottom = y * GRID_SIZE + GRID_SIZE
        self.speed = 1
        
        self.vx = -1 * self.speed

    def set_image_list(self):
        if self.vx > 0:
            self.images = slug_imgs_lt
        else:
            self.images = slug_imgs_rt
        
    def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_world_platforms()
        self.apply_gravity()
        self.animate()


class Fallslug(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)
        self.rect.bottom = y * GRID_SIZE + GRID_SIZE
        self.speed = 1
        
        self.vx = -1 * self.speed
        
    def set_image_list(self):
        if self.vx > 0:
            self.images = slug_imgs_lt
        else:
            self.images = slug_imgs_rt

        
    def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        self.apply_gravity()
        self.animate()

        


        
    

    
class Egg(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

    def apply(self, character):
        character.eggs += 1
        character.score += 10
        print(character.eggs)
        egg_snd.play()

class Steak(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        

    def apply(self, character):
        character.health += 1
        character.score += 10
        
        eat_snd.play()


            

# Helper functoins
def show_hud():
    text = font_md.render(str(hero.score), True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, 16
    screen.blit(text, rect)


    screen.blit(egg_img, [WIDTH - 128, 16])
    text = font_md.render('x' + str(hero.eggs), True, WHITE)
    rect = text.get_rect()
    rect.topleft = WIDTH - 60, 20
    screen.blit(text, rect)


    for i in range(hero.health):
        x = i * 36 + 16
        y = 16
        screen.blit(heart_img, [x,y])



    
def show_start_screen():
    text = font_xl.render(TITLE, True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

    text = font_sm.render("Press any key to start", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect) 

def show_lose_screen():
    text = font_xl.render("GAME OVER", True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

    text = font_sm.render("Press R to restart", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

def show_win_screen():
    text = font_xl.render("You WON", True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)

    text = font_sm.render("Press R to restart", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2
    screen.blit(text, rect)
    
def show_level_complete_screen():
    text = font_xl.render("Level Complete", True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render("臭い", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect) 


#def show_grid():
#   for x in range(0,WIDTH, GRID_SIZE):
 #       pygame.draw.line(screen, WHITE, [x, 0], [x, HEIGHT], 1)
  #for y in range(0,HEIGHT, GRID_SIZE):
   #     pygame.draw.line(screen, WHITE, [0, y], [WIDTH, y], 1)
    #    
    #for x in range(0,WIDTH, GRID_SIZE):
     #   for y in range (0, HEIGHT, GRID_SIZE):
     #       point = '(' + str(x// GRID_SIZE) + "," + str(y // GRID_SIZE)

      #      text = font_xs.render(point, True, WHITE)
       #     screen.blit(text, [x + 4, y + 4])

       

def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, WHITE, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, WHITE, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, WHITE)
            screen.blit(text, [adj_x, adj_y])


# Setup
def start_game():
    global hero, stage, current_level
    
    hero = Hero(0, 0, hero_idle_imgs_rt)
    

    
    stage = START 
    current_level = 0


    
def start_level():
    global goal, stage, platforms, player, items, enemies, stage, foreground, block
    global gravity, terminal_velocity, world_width, world_height, all_sprites
    
    platforms = pygame.sprite.Group()
    items = pygame.sprite.Group()
    player = pygame.sprite.GroupSingle()
    foreground = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    goal = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()




    # load level file here
    with open(levels[current_level]) as f:
        data = json.load(f)


    world_width = data['width'] * GRID_SIZE
    world_height = data['height'] * GRID_SIZE
    
    

    
    hero.move_to(data['start'][0], data['start'][1])
    player.add(hero)

    goal.add(Bonfire(data['bonfire'][0], data['bonfire'][1], bonfire_img))



   
    
    for loc in data['block_locs']:
             platforms.add(Platform(loc[0], loc[1], grass_dirt_img))



    
    for loc in data['platform_locs']:
             platforms.add(Platform(loc[0], loc[1], platform_img))
    
    for loc in data['platform2_locs']:
             platforms.add(Platform(loc[0], loc[1], platform2_img))






    
    for loc in data['thing_locs']:
             foreground.add(Foreground(loc[0], loc[1], sit_img))
    
    for loc in data['egg_locs']:
             items.add(Egg(loc[0], loc[1], egg_img))

    for loc in data['steak_locs']:
             items.add(Steak(loc[0], loc[1], steak_img))





    
    for loc in data['Red_guy_locs']:
             enemies.add(Red_guy(loc[0], loc[1], enemy_imgs_rt) )

    for loc in data['Slug_locs']:
             enemies.add(Slug(loc[0], loc[1], slug_imgs_rt) )

    for loc in data['Fallslug_locs']:
             enemies.add(Fallslug(loc[0], loc[1], slug_imgs_rt) )

    


    
   
    
    # Physics settings
    gravity = data['gravity']
    terminal_velocity = data['terminal_velocity']

    all_sprites.add(player, platforms, items, enemies, goal)

    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    


# Game loop
grid_on = False
running = True

start_game()
start_level()

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                grid_on = not grid_on
            
            elif stage == START:
                stage = PLAYING

                
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    hero.jump()
            elif stage == LOSE or stage == WIN:
                if event.key == pygame.K_r:
                    start_game()

                    start_level()
                    
                    
                    

                 

           

    pressed = pygame.key.get_pressed()
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            hero.move_left()
        elif pressed[pygame.K_RIGHT]:
            hero.move_right()
        elif pressed[pygame.K_DOWN]:
            hero.crouch()
        else:
            hero.stop()
            hero.crouching = False

    
    # Game logic
    if stage == PLAYING:
        all_sprites.update()
        

        if hero.health ==  0:
            stage = LOSE

        elif hero.reached_goal():
            stage = LEVEL_COMPLETE
            countdown = 2 * FPS
            pygame.mixer.music.stop()
            level_up_snd.play()
            
    elif stage == LEVEL_COMPLETE:
        countdown -=1
        if countdown <= 0:
            current_level += 1
            if current_level < len(levels):
                start_level()
                stage = PLAYING
            else:
                stage = WIN
                game_win_snd.play()

    if hero.rect.centerx < WIDTH // 2:
        offset_x = 0
    elif hero.rect.centerx > world_width - WIDTH // 2:
        offset_x = world_width - WIDTH
    else:
        offset_x = hero.rect.centerx - WIDTH // 2  
    
    # Drawing code
    
    screen.fill(SKY_)
    
    
    

    for sprite in all_sprites:
        screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y])

    for sprite in foreground:
        screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y])
        #platforms.draw(screen)
    #goal.draw(screen)
    #player.draw(screen)
    #items.draw(screen)
    #enemies.draw(screen)
    #foreground.draw(screen)
        
    show_hud()


    
    if stage == START:
        show_start_screen()
    elif stage == LOSE:
        show_lose_screen()
        pygame.mixer.music.stop()
        game_over_snd.play()
    
    elif stage == LEVEL_COMPLETE:
        show_level_complete_screen()
    elif stage == WIN:
        show_win_screen()

    if grid_on:
        draw_grid(offset_x)

        
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

