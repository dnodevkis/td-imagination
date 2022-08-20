import pygame
import spritesheet
import os

class Enemies:
   
    def __init__(self, matrix, e_type):

        # basic
        self.matrix = matrix
        self.tile = 32
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.rect = self.image.get_rect(center=(len(self.matrix[0]) * self.tile // 20, len(self.matrix) * self.tile // 2))
        #print('len matrix[0]', self.matrix[0])
       
        # movement
        self.pos = self.rect.center
        self.speed = 3
        self.direction = pygame.math.Vector2(0, 0)

        # path
        self.path = []
        self.collision_rects = []
        self.e_type = e_type
        # self.empty_path = empty_path

    def empty_path(self):
        self.path = []

    def get_coord(self):
        col = self.rect.centerx // self.tile
        row = self.rect.centery // self.tile
        return (col, row)

    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = point[0] * self.tile
                y = point[1] * self.tile
                rect = pygame.Rect((x - 2, y - 2), (8, 8))
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
                else:
                    self.empty_path()

    def update(self):
        self.pos += self.direction * self.speed
        self.check_collisions()
        self.rect.center = self.pos

    def get_animation(self, e_type, e_action, a_direction, frame):
        self.e_type = e_type
        self.e_action = e_action
        self.a_direction = a_direction
        self.frame = frame
        self.sprite_sheet_image = pygame.image.load(os.path.join("enemies/" + e_type + "/" + e_type + '-' + e_action + '-' + a_direction + ".png")).convert_alpha()
        
        
        #self.sprite_sheet_image = pygame.image.load(os.path.join("enemies/skeleton/skeleton-walk-right.png")).convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.animation_list = []
        self.animation_steps = 6
        black     = (  0,   0,   0)   # черный  
        for frame in range (self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(frame, self.tile, self.tile, 1, black))
        return self.animation_list

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, __o: object) -> bool:
        return self is __o

