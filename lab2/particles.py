import pygame
from random import randint, choice

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

class Particle(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, pos, color, direction: pygame.math.Vector2, speed):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed/2
        self.alpha = randint(100,255)
        self.fade_speed = randint(50,200)
        self.age = 0
        
        self.create_surf()
        
    def create_surf(self):
        self.image = pygame.Surface((4,4)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface=self.image, color=self.color, center=(2,2), radius=2)
        self.rect = self.image.get_rect(center=self.pos)
        
    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        
    def fade(self, dt):
        self.alpha -= self.fade_speed*dt*0.5
        self.image.set_alpha(self.alpha)
           
    def change_color(self, dt):
        if (dt*1000)%2==0:
            self.color = choice(("red", "green", "blue"))
            # self.color = (randint(0,255), randint(0,255), randint(0,255))
    def change_age(self,dt):
        self.age+=dt
    
    def check_age(self):
        if self.age>=10: 
            self.kill()
            
    def check_alpha(self):
        if self.alpha<=0:
            self.kill()
    
    def check_collision(self, object: list, dt):
        
        next_pos = self.pos + self.direction*self.speed*dt
        particle_line = (self.pos, next_pos)
        sides = []
        for i in range(len(object)):
            start = pygame.math.Vector2(object[i])
            end = pygame.math.Vector2(object[(i+1)%len(object)])
            
            polygon_edge = (start, end)
            
            if self.lines_intersect(particle_line, polygon_edge):
                edge_vector = end-start
                normal = pygame.math.Vector2(-edge_vector.y, edge_vector.x).normalize()
                self.direction = self.direction.reflect(normal)
                break
    
    def lines_intersect(self, line1, line2):
        x1,y1 = line1
        x2,y2 = line2
        
        r = y1 - x1
        s = y2 - x2
        denominator = r.cross(s)
        
        if denominator == 0:
            return False
        
        t = (x2-x1).cross(s)/denominator
        u = (x2-x1).cross(r)/denominator
        
        return 0<=t<=1 and 0<=u<=1
        
        
    
    def update(self, dt, polygon):
        self.move(dt)
        self.fade(dt)
        self.change_age(dt)
        self.change_color(dt)
        self.check_alpha()
        self.check_age()
        self.check_collision(polygon, dt)