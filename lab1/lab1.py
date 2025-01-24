import pygame
import numpy as np
import random
import math

pygame.init()
window = pygame.display.set_mode((1000,750))
clock = pygame.time.Clock()

def cubic_spline(segment_points, t):
    #r0 početak, r1,r2 sredina, r3 kraj, t  0<=t<1 
    r0 = segment_points[0]
    r1 = segment_points[1]
    r2 = segment_points[2]
    r3 = segment_points[3]
    
    temp0 = -1*(t*t*t) + 3*(t*t) - 3*t + 1
    temp1 =  3*(t*t*t) - 6*(t*t) + 0*t + 4
    temp2 = -3*(t*t*t) + 3*(t*t) + 3*t + 1
    temp3 =  1*(t*t*t) + 0*(t*t) - 0*t + 0
    
    #x koordinata vektora p
    px = temp0*r0[0] + temp1*r1[0] + temp2*r2[0] + temp3*r3[0]
    #y koordinata vektora p
    py = temp0*r0[1] + temp1*r1[1] + temp2*r2[1] + temp3*r3[1]
    px = px/6
    py = py/6
    return (px, py)

def spline_derivative(segment_points, t):
    r0 = segment_points[0]
    r1 = segment_points[1]
    r2 = segment_points[2]
    r3 = segment_points[3]
    
    temp0 = -1 * (t*t) + 2*t - 1
    temp1 =  3 * (t*t) - 4*t + 0
    temp2 = -3 * (t*t) + 2*t + 1
    temp3 =  1 * (t*t) + 0*t + 0

    #x koordinata dp
    dpx = (temp0 * r0[0] + temp1 * r1[0] + temp2 * r2[0] + temp3 * r3[0])
    dpx = dpx/2
    #y koordinata dp
    dpy = (temp0 * r0[1] + temp1 * r1[1] + temp2 * r2[1] + temp3 * r3[1])
    dpy=dpy/2
    return (dpx, dpy)

def draw_triangle(window, position, angle, size=25):
    x, y = position

    points = []
    for i in range(3):
        theta = angle + (i*(2*math.pi/3))  #120
        points.append((x+size*math.cos(theta), y+size*math.sin(theta)))
        
    pygame.draw.polygon(window, (0, 255, 0), points)


def drawspline(points):
    #points: vektor r0...rn
    
    for i in range(0, len(points)-3):
        # color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        color = (255,255,255)
        segment_points = points[i:(i+4)]
        prev_point = cubic_spline(segment_points, 0)

        for t in range(0,101):
            t=t/100
            curr_point = cubic_spline(segment_points, t)
            pygame.draw.line(window, color, prev_point, curr_point, 2)
            prev_point = curr_point

    pygame.display.update()

points = []
f = open("tocke.txt")
for line in f:
    point_str = line.strip().split(",")
    point = (int(point_str[0]),int(point_str[1]))
    points.append(point)

t_triangle_pos = 0
t_step = 0.003

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    window.fill((0,0,0))
    drawspline(points)

    segment_index = int(t_triangle_pos) #na kojem segmentu je trokut
    local_t = t_triangle_pos - segment_index  #t na segmentu, 0<=t<1
    
    if segment_index + 3 < len(points):
        segment_points = points[segment_index:segment_index + 4]
        
        #trenutne koordinate trokuta
        triangle_position = cubic_spline(segment_points, local_t)
        
        #derivacija u trenutnom t
        tangent_vector = spline_derivative(segment_points, local_t)
        angle = math.atan2(tangent_vector[1], tangent_vector[0])
        # print(tangent_vector)
        # print(angle)
        
        draw_triangle(window, triangle_position, angle=angle)
        
        tangent_length = 0.3
        tangent_end = (triangle_position[0] + tangent_vector[0] * tangent_length,
                       triangle_position[1] + tangent_vector[1] * tangent_length)
        pygame.draw.line(window, (255, 0, 0), triangle_position, tangent_end, 2)
        
    t_triangle_pos += t_step
    if t_triangle_pos >= len(points) - 3:
        t_triangle_pos = 0
    
    pygame.display.flip()
    

pygame.quit()
exit()