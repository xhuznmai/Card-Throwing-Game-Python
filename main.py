import pygame, sys, time, random
from pygame import mixer
#------------------------Import------------------------------------------------------------------------------------------------#



last_enemy_time = pygame.time.get_ticks()
last_hand_time = pygame.time.get_ticks()
enemy_creation_delay = 2000
hand_animation_delay = 150
shot_delay = 1000
score = 0
health = 5
score_increment = 10
card_created = False
transColor = pygame.Color(255, 255, 255)
music_enabled = True
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.last_shot_time = 0
        #self.image = pygame.Surface((100, 86))
        self.image = pygame.image.load("img/hand.png")
        self.image.set_colorkey(transColor)
        #self.image.fill(("white"))
        self.rect = self.image.get_rect(center = (screen_width/2, screen_height-160))
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
    def create_card(self):
        current_time = pygame.time.get_ticks()  # Get the current time

        if current_time - self.last_shot_time >= shot_delay:
            self.last_shot_time = current_time  # Update the last shot time
            card_created = True
            return Attack_Card(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        else:
            card_created = False
            return None

class Attack_Card(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("img/attack_card_1.png",)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    def update(self):
        self.rect.y -= 10

        if self.rect.y >= screen_height + 200:
            self.kill()
    def card_physics(self):
        pass

class Defense_Card(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("img/defense_card_1.png",)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    def card_physics(self):
        pass

class Health_Card(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__()
            self.image = pygame.image.load("img/defense_card_1.png",)
            self.rect = self.image.get_rect(center = (pos_x, pos_y))
        def update(self):
            self.rect.y += 1
        def card_physics(self):
            pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("img/cthulhu_eye_closed.png")
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
    def update(self):
        self.rect.y += 1

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

                # Toggle music state
                if self.image == music_img:
                    global music_enabled
                    music_enabled = not music_enabled
                    if music_enabled:
                        background_music_channel.unpause()
                    else:
                        background_music_channel.pause()

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

def display_lose_message():
    font = pygame.font.Font(None, 36)
    text = font.render("You lose", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width//2, screen_height//2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def display_win_message():
    win_message_font = pygame.font.Font(None, 36)
    text = font.render("You win", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width//2, screen_height//2))
    screen.blit(text, text_rect)
    pygame.display.flip()
#Basics
pygame.init()
run = True
game_state = "menu"
clock = pygame.time.Clock()
screen_width, screen_height = 600, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Card Battle")


#Background Image
background_image = pygame.image.load("img/background2.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

#Sound file load
mixer.init()
background_music = mixer.Sound("sound/background.mp3")
throw_sound = mixer.Sound("sound/whoosh.mp3")
hit_sound = mixer.Sound("sound/hit_sound.mp3")
background_music_channel = mixer.Channel(0)
throw_sound_channel = mixer.Channel(1)
hit_sound_channel = mixer.Channel(2)

#Play background music
background_music_channel.set_volume(0.5)
background_music_channel.play(background_music)

#Game Object
hand = Player()
hand_group = pygame.sprite.Group()
hand_group.add(hand)

attack_card_group = pygame.sprite.Group()
defense_card_group = pygame.sprite.Group()
health_card_group = pygame.sprite.Group()

defense_card_created = False
defense_card_incremented = False

enemy_group = pygame.sprite.Group()
game_over = False
game_paused = False

#button image load
play_img = pygame.image.load("img/play_button.png").convert_alpha()
option_img = pygame.image.load("img/option_button.png").convert_alpha()
quit_img = pygame.image.load("img/quit_button.png").convert_alpha()
option_menu_img = pygame.image.load("img/option_background.jpg")
back_button_img = pygame.image.load("img/back_button.png")
main_menu_img = pygame.image.load("img/background.png")
resume_img = pygame.image.load("img/resume_button.png")
music_img = pygame.image.load("img/music_on.png")

#Game Loop
while run and not game_over:
    if game_state == "menu":
        pygame.mouse.set_visible(True)
        screen.fill("purple")
        screen.blit(main_menu_img, (0, 0))
        # creat button instances
        play_button = Button(screen_width / 2 - play_img.get_width() / 2, 125, play_img, 1)
        option_button = Button(screen_width / 2 - option_img.get_width() / 2, 125 + play_img.get_height(), option_img,
                               1)
        quit_button = Button(screen_width / 2 - quit_img.get_width() / 2,
                             125 + play_img.get_height() + option_img.get_height(), quit_img, 1)
        play_button.draw(screen)
        option_button.draw(screen)
        quit_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if play_button.draw(screen):
            game_state = "game"
            pygame.display.set_caption("Game")
        pygame.display.update()
        if option_button.draw(screen):
            pygame.display.set_caption("Option")
            game_state = "option"
        if quit_button.draw(screen):
            pygame.quit()
            sys.exit()
    if game_state == "option":
        screen.fill("purple")
        screen.blit(option_menu_img, (0, 0))
        back_button = Button(screen_width / 2 - back_button_img.get_width() / 2, 125, back_button_img, 1)
        music_button = Button(screen_width / 2 - music_img.get_width() / 2, 125 + music_img.get_height(), music_img,1)
        music_button.draw(screen)
        if music_enabled:
            screen.blit(music_img, (screen_width / 2 - music_img.get_width() / 2, 125 + music_img.get_height()))
        else:
            # Display a different image for the button when music is off
            music_off_img = pygame.image.load("img/music_off.png")
            screen.blit(music_img, (screen_width / 2 - music_img.get_width() / 2, 125 + music_img.get_height()))
        if back_button.draw(screen):
            game_state = "menu"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    if game_state == "resume_option":
        screen.fill("purple")
        screen.blit(option_menu_img, (0, 0))
        back_button = Button(screen_width / 2 - back_button_img.get_width() / 2, 125, back_button_img, 1)
        music_button = Button(screen_width / 2 - music_img.get_width() / 2, 125 + music_img.get_height(),
                              music_img, 1)
        music_button.draw(screen)
        if back_button.draw(screen):
            game_state = "pause"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    if game_state == "pause":
        pygame.mouse.set_visible(True)
        pygame.display.set_caption("Pause")
        screen.fill("purple")
        screen.blit(main_menu_img, (0, 0))
        # creat button instances
        resume_button = Button(screen_width / 2 - resume_img.get_width() / 2, 125, resume_img, 1)
        option_button = Button(screen_width / 2 - option_img.get_width() / 2, 125 + resume_img.get_height(), option_img,
                               1)
        quit_button = Button(screen_width / 2 - quit_img.get_width() / 2,
                             125 + play_img.get_height() + option_img.get_height(), quit_img, 1)
        resume_button.draw(screen)
        option_button.draw(screen)
        quit_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if resume_button.draw(screen):
            game_state = "game"
            pygame.display.set_caption("Game")
        pygame.display.update()
        if option_button.draw(screen):
            pygame.display.set_caption("Option")
            game_state = "resume_option"
        if quit_button.draw(screen):
            pygame.quit()
            sys.exit()
    if game_state == "game":
        pygame.mouse.set_visible(False)
        defense_card_1 = Defense_Card(screen_width - 100, screen_height - 100)
        defense_card_group.add(defense_card_1)
        defense_card_created = True
        font = pygame.font.Font(None, 36)
        hand_current_time = pygame.time.get_ticks()
        if hand_current_time - last_hand_time >= hand_animation_delay:
            hand.image = pygame.image.load("img/hand.png")
            hand.image.set_colorkey(transColor)
            last_hand_time = hand_current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_card = hand.create_card()
                    if new_card is not None:
                        attack_card_group.add(new_card)
                        throw_sound_channel.play(throw_sound)
                        hand.image = pygame.image.load("img/hand2.png")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Pause")
                    game_state = "pause"
        boss_warning_1 = font.render(f'Boss Stage 1', True, (255, 255, 255))
        current_time = pygame.time.get_ticks()  # Get the current time
        enemy_created = True
        # Create an enemy only if enough time has passed since the last enemy creation
        if current_time - last_enemy_time >= enemy_creation_delay and enemy_created:
            enemy = Enemy(random.randint(0 + 100 , screen_width - 100), 0)  # Adjust the initial position of the enemy
            enemy_group.add(enemy)
            last_enemy_time = current_time  # Update the last enemy creation time
        if current_time - last_enemy_time >= enemy_creation_delay and enemy_created:
            health = Health_Card(random.randint(0 + 100 , screen_width - 100), 0)
            health_card_group.add(health)
            last_enemy_time = current_time  # Update the last enemy creation time
        for enemy in enemy_group:
            enemy.update()
            #Losing game
            if enemy.rect.y >= screen_height:
                enemy.kill()
                enemy_created = False
                health = health - 1
                hit_sound_channel.play(hit_sound)
                if health == 0:
                    display_lose_message()
                    print("Player lose, game losing in 5 seconds")
                    time.sleep(5)
                    game_over = True
            #Winning game
            if score == 300:
                enemy.kill()
                enemy_created = False
                display_win_message()
                print("Player win, game losing in 5 seconds")
                time.sleep(5)
                game_over = True
            if pygame.sprite.groupcollide(attack_card_group, enemy_group, True, True):
                score += score_increment
            if score >= 50:
                enemy.image = pygame.image.load("img/cthulhu.png")
                enemy.rect.y += 5.5
                shot_delay = 500
                enemy_creation_delay = 1000
            if score >= 100:
                enemy.rect.y += 6
                shot_delay = 300
                enemy_creation_delay = 500
            #Boss_stage_1
            if score >= 200:
                enemy.rect.y -= 4
                enemy.image = pygame.image.load("img/cthulhu_boss_stage_1.png")
                enemy_creation_delay = 1000
        #Drawing
        screen.fill(("purple"))
        screen.blit(background_image, (0, 0))
        attack_card_group.draw(screen)
        defense_card_group.draw(screen)
        hand_group.draw(screen)
        hand_group.update()
        defense_card_group.update()
        if defense_card_created and not defense_card_incremented:
            health += 3
            defense_card_incremented = True
        if defense_card_created:
            defense_text = font.render(f'(Defense: +3)', True, (255, 255, 255))
            defense_card_1.kill()
        attack_card_group.update()
        enemy_group.update()
        health_card_group.update()
        enemy_group.draw(screen)
        health_text = font.render(f'Health: {health}', True, (255, 255, 255))
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        if score >= 200:
            screen.blit(boss_warning_1, (screen_width/4 + 35, 10))
        screen.blit(health_text, (10, 40))
        screen.blit(score_text, (10, 10))
        screen.blit(defense_text, (10, 70))
        pygame.display.flip()
        clock.tick(60)
