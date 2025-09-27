import pygame, sys, random, gif_pygame
import button

MIN_VER = (3, 7)

if sys.version_info[:2] < MIN_VER:
    sys.exit(
        "This game requires Python {}.{}.".format(*MIN_VER)
    )

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Game")

block = pygame.image.load('sprites/brick1.png').convert_alpha()
block = pygame.transform.scale(block, (block.get_width() * 2.5, block.get_height() * 2.5))

menu = gif_pygame.load('sprites/menu.gif')

font = pygame.font.Font('font.ttf')

city = pygame.image.load('sprites/1.png').convert_alpha()
img2 = pygame.image.load('sprites/2.png').convert_alpha()
img3 = pygame.image.load('sprites/3.png').convert_alpha()
img4 = pygame.image.load('sprites/4.png').convert_alpha()
img5 = pygame.image.load('sprites/5.png').convert_alpha()
img6 = pygame.image.load('sprites/6.png').convert_alpha()
img_list = [img2, img3, img4, img5, img6]

sound1 = pygame.mixer.Sound('sounds/crashing_sound.wav')

bit_1 = pygame.mixer.Sound('sounds/1_bit.wav')
bit_2 = pygame.mixer.Sound('sounds/2_bit.wav')
start = pygame.mixer.Sound('sounds/start.wav')
start.set_volume(1.5)
end = pygame.mixer.Sound('sounds/end.wav')


class Button:
    def __init__(self, image, pos):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            return True




def main_menu():

    pygame.mixer.music.load('sounds/menu_song.wav')
    pygame.mixer.music.play(-1)

    sound_quit = True
    sound_play = True

    while True:

        play_img = pygame.image.load('sprites/play_1.png').convert_alpha()
        play_img = pygame.transform.scale(play_img, (300,150))
        quit_img = pygame.image.load('sprites/quit_1.png').convert_alpha()
        quit_img = pygame.transform.scale(quit_img, (300, 150))

        play2_img = pygame.image.load('sprites/play_2.png').convert_alpha()
        play2_img = pygame.transform.scale(play2_img, (300,150))
        quit2_img = pygame.image.load('sprites/quit_2.png').convert_alpha()
        quit2_img = pygame.transform.scale(quit2_img, (300, 150))


        
        menu.render(screen, (0, 0))

        mouse = pygame.mouse.get_pos()

        play_b = Button(image = play_img, pos = (550, 250))
        quit_b = Button(image = quit_img, pos = (550, 500))

        if mouse[0] in range(play_b.rect.left, play_b.rect.right) and mouse[1] in range (play_b.rect.top, play_b.rect.bottom):
            play_b.image = play2_img
            if sound_play == True:
                bit_1.play()
                sound_play = False
        else:
            play_b.image = play_img
            sound_play = True

        if mouse[0] in range(quit_b.rect.left, quit_b.rect.right) and mouse[1] in range (quit_b.rect.top, quit_b.rect.bottom):
            quit_b.image = quit2_img
            if sound_quit == True:
                bit_1.play()
                sound_quit = False
        else:
            quit_b.image = quit_img
            sound_quit = True

        for button in [play_b, quit_b]:
            button.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_b.check_for_input(mouse):
                    start.play()
                    play()
                    
                if quit_b.check_for_input(mouse):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        


def play():
    pygame.mixer.music.load('sounds/game_song.wav')
    pygame.mixer.music.play(-1)
    
    clock = pygame.time.Clock()
    running = True

    block = pygame.image.load('sprites/brick1.png').convert_alpha()
    block = pygame.transform.scale(block, (block.get_width() * 2, block.get_height() * 2))

    fade_surface = pygame.Surface((screen.get_size()), pygame.SRCALPHA)
    fade_color = (0, 0, 0)
    fade_surface.fill(fade_color)
    alpha = 0
    fade_speed = 5
    fading_out = False
    

    x = 0
    y = 500
    speed = 5
    moving = True
    blocks = []
    count = 0

    screen_shake = 0
    shake_offset = [0, 0]

    delta_time = 0.1
    camera_y = 0
    background_queue = [city] + [random.choice(img_list) for _ in range(10)]
    img_index = 0
    
    wall1 = pygame.Rect(770, 50, 30, 800)
    
    game_over = False

    end_sound = False

    space_text = True

    while running:
        screen.fill((0, 0, 0))

        camera_y += 12.5 * delta_time
        bg_height = city.get_height()

        for i in range(-1, 6):
            image = background_queue[(img_index + i) % len(background_queue)]
            screen.blit(image, (0 + shake_offset[0], i * bg_height + (camera_y % bg_height) + shake_offset[1]))

        if camera_y % bg_height == 0:
            background_queue.pop(0)
            img_index += 1
            if img_index >= len(background_queue) - 5:
                background_queue.append(random.choice(img_list))

        volume = 0

        for i in range(10):
            pygame.mixer.music.set_volume(volume)
            volume += 0.2 * delta_time

        
        if moving:
            x += speed


        for bx, by, b_img in blocks:
            screen.blit(b_img, (bx + shake_offset[0], by + camera_y + shake_offset[1]))
        screen.blit(block, (x + shake_offset[0], y + camera_y + shake_offset[1]))

        hitbox = pygame.Rect(x, y, block.get_width(), block.get_height())


        if hitbox.colliderect(wall1):
            fading_out = True


        
        if fading_out:
            alpha += fade_speed
            pygame.mixer.music.stop()
            if alpha >= 255:
                alpha = 255
            game_over = True
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            text = font.render("Press\n\nQ to restart\n\nor\n\nESC to leave", True, (255, 255, 255))
            text = pygame.transform.scale(text, (text.get_width() * 2, text.get_height() * 2))
            screen.blit(text, (50, 200))

        if game_over and end_sound == False:
            end.play()
            end_sound = True
            moving = False

        font_count = font
        text = font_count.render(str(count), True, (255, 255, 255))
        text = pygame.transform.scale(text, (50, 70))
        screen.blit(text, (330, 20))

        font_space = font
        text_space = font_space.render('Press\nSpace', True, (0, 0, 0))
        text_space = pygame.transform.scale(text_space, (200, 100))
        if space_text:
            screen.blit(text_space, (5, 200))

        pygame.display.flip()
        clock.tick(30)

        if screen_shake > 0:
            screen_shake -= 1
        
        if screen_shake:
            shake_offset[0]  = random.randint(-4, 4)
        
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and game_over:
                    block = pygame.image.load('sprites/brick1.png').convert_alpha()
                    block = pygame.transform.scale(block, (block.get_width() * 2, block.get_height() * 2))
                    x = 0
                    y = 500
                    speed = 5
                    moving = True
                    blocks = []
                    game_over = False
                    camera_y = 0
                    count = 0
                    img_index = 0
                    alpha = 0
                    fading_out = False
                    background_queue = [city] + [random.choice(img_list) for _ in range(10)]
                    end_sound = False
                    space_text = True
                    volume = 0
                    pygame.mixer.music.play(-1)
                if event.key == pygame.K_ESCAPE and game_over:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE and not game_over:
                    space_text = False
                    screen_shake = 10
                    moving = False
                    sound1.play()
                    bit_2.play()
                    if blocks:
                        last_x, last_y, last_img = blocks[-1]
                        last_rect = pygame.Rect(last_x, last_y - block.get_height(), last_img.get_width(), last_img.get_height())
                        hitbox = pygame.Rect(x, y, block.get_width(), block.get_height())

                        overlap = hitbox.clip(last_rect)
                        if overlap.width == 0:
                            fading_out = True
                            
                            continue
                        new_block = block.subsurface(
                            (overlap.x - hitbox.x, overlap.y - hitbox.y, overlap.width, overlap.height)).copy()
                        
                        new = overlap.x, overlap.y, new_block
                        
                        blocks.append((new))
                        x = 0
                        y = overlap.y - new_block.get_height()
                        block = new_block.copy()

                    else:
                        new_b = x, y, block.copy()
                        blocks.append(new_b)
                        x = 0
                        y -= block.get_height()
                    
                    moving = True
                    count += 1
main_menu()

pygame.quit()
sys.exit()



