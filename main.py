import pygame, sys, random
pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
pygame.init()
WIDTH = 432
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
#Tạo hàm cho game
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+432, 650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-700))
    return  bottom_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 650:
        hit_sound.play()
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return  new_bird,new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(score),True,(255,255,255))
        score_rect = score_surface.get_rect(center= (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {score} ', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {high_score} ', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)
def check_pass(pipes,pipes_passed):
    global score
    for pipe in pipes:
        if pipe not in pipes_passed:
            if pipe.right < bird_rect.left:
                pipes_passed.append(pipe)
                score+=5
                score_sound.play()
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
FPS = 120
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)
#Các biến của game
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
pipe_passed_list = []
#Tạo Background
bg = pygame.image.load('img/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#Tạo sàn
floor = pygame.image.load('img/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#Tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('img/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('img/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('img/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('img/yellowbird-midflap.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,HEIGHT/2))
#Tạo timer cho chim
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)
#Tạo ống
pipe_surface = pygame.image.load('img/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [300,400,500]
#Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,800)
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('img/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (WIDTH/2,HEIGHT/2))
#Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
#Vòng lặp của game
while True:
    for event  in pygame.event.get():
        if event.type ==  pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active == True:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center =  (100,384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird,bird_rect = bird_animation();
    screen.blit(bg,(0,0))
    if game_active:
        #Chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        #Ống
        draw_pipe(pipe_list)
        pipe_list = move_pipe(pipe_list)
        check_pass(pipe_list,pipe_passed_list)
        score_display('main game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    #Sàn
    floor_x_pos -=1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(FPS)