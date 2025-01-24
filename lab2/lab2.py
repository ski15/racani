import pygame
from particles import Particle
from random import choice, uniform, randint
from math import sin, floor,pi

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

particle_group = pygame.sprite.Group()

collision_object_points = ((0,100),(200,100),(200,600),(0,600))

collision_object_points = ((450,200),(550,200),(550,600),(450,600))

def point_is_inside_polygon(point, polygon):
    x, y = point
    inside = False
    
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1)%len(polygon)]
        
        if (y1>y)!=(y2>y):
            intersect_x = x1 + (y-y1)*(x2-x1)/(y2-y1)
            if x < intersect_x:
                inside = not inside
                
    return inside

def main_loop():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = randint(100,2000)
                for i in range(n):
                    pos = pygame.mouse.get_pos()
                    if point_is_inside_polygon(point=pos, polygon=collision_object_points):
                        break
                    color = choice(("red", "green", "blue"))
                    direction = pygame.math.Vector2(uniform(-1,1), uniform(-1,1))
                    direction = direction.normalize()
                    speed = randint(50,500)
                    Particle(particle_group, pos, color, direction, speed)
        
        dt = clock.tick() / 1000
        
        
        
        display_surface.fill((3, 12, 33))
        particle_group.draw(display_surface)
        
        particle_group.update(dt,collision_object_points)
        pygame.draw.polygon(display_surface, color=(69, 125, 84), points=collision_object_points, )
        
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    main_loop()