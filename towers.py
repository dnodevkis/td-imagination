import pygame
import spritesheet
import os

class Towers:
   
    def __init__(self, grid_x, grid_y, t_type, t_frame):

        self.frame = t_frame
        self.t_type = t_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.attack_speed = 2
        self.attack_damage = 1
        self.attack_range = 3
        self.projectile_type = 'arrow'
        self.image = pygame.image.load('tower.png').convert_alpha()

    def set_action(self, t_action, t_direction):
        
        self.t_action = t_action
        self.t_direction = t_direction
        

    def get_animation(self, t_type, t_action, t_direction, t_frame):
        self.t_type = t_type
        self.t_action = t_action
        self.t_direction = t_direction
        self.frame = t_frame
        self.sprite_sheet_image = pygame.image.load(os.path.join("towers/" + t_type + "-tower/" + t_action + '/' + t_type + "-tower-" + t_action + ".png")).convert_alpha()
        
        #self.sprite_sheet_image = pygame.image.load(os.path.join("enemies/skeleton/skeleton-walk-right.png")).convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animation_list = []
        self.animation_steps = 6
        self.tile = 32
        black     = (  0,   0,   0)   # черный  
        for frame in range (self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(frame, self.tile, self.tile, 1, black))
        return self.animation_list
    
    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, __o: object) -> bool:
        return self is __o

