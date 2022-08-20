import sys
import time
import pygame
import os
from enemies import Enemies
from towers import Towers
from matrix import Matrixgrid
from pathmaker2 import Pathmaker


def get_l_click_pos():
    x, y = pygame.mouse.get_pos()
    grid_x, grid_y = x // tile_size, y // tile_size
    click = pygame.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def get_r_click_pos():
    x, y = pygame.mouse.get_pos()
    grid_x, grid_y = x // tile_size, y // tile_size
    click = pygame.mouse.get_pressed()
    return (grid_x, grid_y) if click[2] else False


def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    grid_x, grid_y = x // tile_size, y // tile_size
    return (grid_x, grid_y)

# Определяем цвета
aqua      = (  0, 255, 255)   # морская волна
black     = (  0,   0,   0)   # черный      
blue      = (  0,   0, 255)   # синий       
fuchsia   = (255,   0, 255)   # фуксия      
gray      = (128, 128, 128)   # серый       
green     = (  0, 128,   0)   # зеленый     
lime      = (  0, 255,   0)   # цвет лайма  
maroon    = (128,   0,   0)   # темно-бордовый
navy_blue = (  0,   0, 128)   # темно-синий 
olive     = (128, 128,   0)   # оливковый   
purple    = (128,   0, 128)   # фиолетовый  
red       = (255,   0,   0)   # красный     
silver    = (192, 192, 192)   # серебряный  
teal      = (  0, 128, 128)   # зелено-голубой
white     = (255, 255, 255)   # белый       
yellow    = (255, 255,   0)   # желтый  

# waves are in form
# frequency of enemies
# (skeletons, red_skeletons)
waves = [
    [0,5,0],
    [1,2,0],
    [4,1,3],
    [3,1,2],
]
enemy_types = ['skeleton','golem','green_skeleton']
wave = 0
e_type = 'green_skeleton'
e_action = 'walk'
a_direction = 'right'    
frame = 0


def get_rect(x, y):
    return x * tile_size + 1, y * tile_size + 1, tile_size - 2, tile_size - 2

field_width = 40
field_height = 23
tile_size = 32
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((field_width * tile_size, field_height * tile_size))

# Загрузка изображений
bg_surf = pygame.image.load('background'+str(field_width)+'x'+str(field_height)+'x'+str(tile_size)+'.png').convert()
stone = pygame.image.load(os.path.join('towers/stone.png')).convert()
selection = pygame.image.load(os.path.join('icons/selection.png')).convert_alpha()
heart = pygame.image.load(os.path.join('icons/heart.png')).convert_alpha()
coin = pygame.image.load(os.path.join('icons/coin.png')).convert_alpha()
tower = pygame.image.load(os.path.join('towers/tower.png')).convert_alpha()


lives = 4
coins = 420

# Создание рамки под курсором
selection_frame = (0, 0)
# Создание массива башен
stones_list = []
# Создание матрицы для поля
matrix = Matrixgrid(field_width, field_height)
# Создание сетки для поля
wave_path_obj = Pathmaker(matrix.matrix)
# Создание маршрута от старта до финиша
wave_path_obj.create_path()
# Сохранение маршрута от старта до финиша в переменную
wave_path = wave_path_obj.path
# Создание пустого массива точек и добавление туда координат из path
points = []
for point in wave_path:
    x = (point[0] * tile_size) + tile_size / 2
    y = (point[1] * tile_size) + tile_size / 2
    points.append((x, y))

# wave generation attributes
wave_started = False
wave_spawn = False
wave_enemies = set()
towers_list = set()
wave_start_time = 0
enemy_shown = 0
wave_started_delete_list = []

# Game state and menu settings
build_stage = True
game_paused = False
game_started = True
wave_stage = False
t_frame = 0


# Starting maze drawer for 40x23 field
if field_width == 40 and field_height == 23:
    for x in range(5, 33, 27):
        for y in range(11):
            matrix.matrix[y][x] = 0
            stones_list.append((x,y))
        for y in range(12,23,1):
            matrix.matrix[y][x] = 0
            stones_list.append((x,y))


# print(a.grid.nodes)


# Тут сурфейсмейкер должен получить path для отрисовки


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



        if build_stage:            
            # Condition becomes true when keyboard is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('Spacebar pressed!')
                    #wave_started = not wave_started
                    wave_spawn = not wave_spawn
                    build_stage = False
                    wave_stage = True
                    print('Wave_started:', wave_started, 'Wave_spawn:', wave_spawn, 'Wave size:', waves[wave])
                    if wave_started == False and wave_spawn == False:
                        try:
                            wave += 1
                            print('Wave increased!')
                            print('Wave:', wave, 'Skeletons:', waves[0][wave], 'Red_skeletons:', waves[1][wave])
                        except:  
                            print('Exception in spacebar wave generating, wave = 0!') 
                            wave = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                # add wall
                add_obstacle = get_l_click_pos()
                if add_obstacle:
                    #Проверяем что место не занято
                    
                    tower: Towers
                    towers_list.add(Towers(add_obstacle[0], add_obstacle[1], 'arrow', t_frame))
                    matrix.add_obstacle(add_obstacle[1], add_obstacle[0])
                    wave_path_obj = Pathmaker(matrix.matrix)
                    wave_path_obj.create_path()
                    wave_path = wave_path_obj.path
                    points = []
                    for point in wave_path:
                        x = (point[0] * tile_size) + tile_size / 2
                        y = (point[1] * tile_size) + tile_size / 2 
                        points.append((x, y))

                # remove wall
                remove_obstacle = get_r_click_pos()
                if remove_obstacle:
                    for tower in towers_list.copy():
                        tower: Towers
                        if tower.grid_x == remove_obstacle[0] and tower.grid_y == remove_obstacle[1]:
                            towers_list.discard(tower)
                            matrix.remove_obstacle(remove_obstacle[1], remove_obstacle[0])
                            wave_path_obj = Pathmaker(matrix.matrix)
                            wave_path_obj.create_path()
                            wave_path = wave_path_obj.path
                            points = []
                            for point in wave_path:
                                x = (point[0] * tile_size) + tile_size / 2
                                y = (point[1] * tile_size) + tile_size / 2 
                                points.append((x, y))

    # генерируем новых врагов
    if wave_stage:
            if wave_spawn:
                if waves[wave] == [0,0,0]:
                    print('Wave spawn ended')
                    wave_spawn = False
                else:
                    #Проходим для каждого типа из списка
                    for enemy_type in range(len(enemy_types)):        
                        # Для количества указанного в волне
                        for enemy_type_count in range(waves[wave][enemy_type]):
                            # Создаем столько монстров сколько указано в волне                           
                            if (time.time() - wave_start_time) > 1:
                                print('Wave:', wave, 'Enemy_type:', enemy_types[enemy_type], 'Left to spawn:', waves[wave][enemy_type])
                                wave_start_time = time.time()
                                fresh_enemy = Enemies(matrix.matrix, enemy_types[enemy_type])
                                waves[wave][enemy_type] += -1
                                wave_enemies.add(fresh_enemy)
                                fresh_enemy.set_path(wave_path_obj.path)


          
    if wave_enemies == set() and wave_stage == True:
        wave_stage = False
        build_stage = True
        print('Wave ended')
        try:
            wave += 1
            print('Wave increased! Next wave:', wave, 'skeletons:', waves[wave][0], 'red_skeletons:', waves[wave][1], 'green_skeletons:', waves[wave][2])      
        except: 
            print('Automatic wave spawn problem!') 
            wave = 0
        tower: Towers
        enemy: Enemies

    # draw background
    screen.blit(bg_surf, (0, 0))

    # draw walls
    for i in range(len(stones_list)):
        screen.blit(stone, (stones_list[i][0] * tile_size, stones_list[i][1] * tile_size))

    # draw towers

    for tower in towers_list.copy():
        tower: Towers
        # рисуем врагов
        t_frame = t_frame + 1
        t_action = 'idle'
        t_type = 'archer'
        t_direction = 'left' 
        tower_animation = tower.get_animation(t_type, t_action, t_direction, t_frame)
        #print(enemy_animation)
        if t_frame >= len(tower_animation):
            t_frame = 0
        screen.blit(
            tower_animation[t_frame],
            (tower.grid_x * tile_size, tower.grid_y * tile_size)
        )

    # draw wave_path
    try:
        pygame.draw.lines(screen, '#4a4a4a', False, points, 5)

    except:        
        font = pygame.font.Font(None, 25)
        text = font.render("Вы заблокировали проход! Удалите одну или несколько башен",True,red)
        screen.blit(text, [field_width * tile_size // 4 ,50])

# Обработка врагов на экране
    for enemy in wave_enemies.copy():
        enemy: Enemies
        #print(enemy.direction)
        if enemy.direction[0] > 0:
            a_direction = 'right'
        if enemy.direction[0] < 0:
            a_direction = 'left'
        # удаляем тех кто дошел до конца
        if enemy.direction == [0, 0]:
            wave_enemies.discard(enemy)
            lives -= 1
        # рисуем врагов
        frame += 1
        enemy_animation = enemy.get_animation(enemy.e_type, e_action, a_direction, frame)
        #print(enemy_animation)
        if frame >= len(enemy_animation):
            frame = 0
        screen.blit(
            enemy_animation[frame],
            enemy.pos,
        )
        enemy.update()

    #Inform messages      
    if wave_spawn:
        font = pygame.font.Font(None, field_width*2)
        text = font.render("Wave "+str(wave)+" started!",True,yellow)
        screen.blit(text, [field_width // 3 * tile_size, 50])
        
    if wave_stage:
        font = pygame.font.Font(None, field_width)
        text = font.render("Wave stage!",True,red)
        screen.blit(text, [field_width // 2 * tile_size,10])

    if build_stage: 
        font = pygame.font.Font(None, field_width)
        text = font.render("Build stage!",True,black)
        screen.blit(text, [field_width // 2 * tile_size,10])

    if lives <= 0: 
        font = pygame.font.Font(None, field_width*4)
        game_over_text = font.render("GAME OVER!",True,black)
        screen.blit(game_over_text, [field_width // 2 * tile_size -380,field_height // 2 * tile_size - 100])

    # draw selection under mouse
    new_selection = get_mouse_pos()
    if new_selection:
        if matrix.matrix[new_selection[1]][new_selection[0]] == 1:
            screen.blit(selection, (new_selection[0] * tile_size, new_selection[1] * tile_size))
    
    #draw lives and coins
         
    font = pygame.font.Font(None, 30)
    lives_count_text = font.render(str(lives),True,black)
    screen.blit(lives_count_text, [field_width * tile_size - 60,17])
    screen.blit(heart, [field_width * tile_size - 35 ,10])
    coins_count_text = font.render(str(coins),True,black)
    screen.blit(coins_count_text, [field_width * tile_size - 130,17])
    screen.blit(coin, [field_width * tile_size - 95 ,10])
   
    pygame.display.update()
    clock.tick(60)


