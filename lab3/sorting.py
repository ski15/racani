import pygame 
import random

pygame.init()

WINDOW_SIZE = 750
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

RECT_WIDTH = 20
clock = pygame.time.Clock()
FPS = 10

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (140, 0, 120)
GREY = (170, 170, 170)
LIGHT_BLUE = (64, 224, 208)

class Rectangle:
    def __init__(self, color, x, height):
        self.color = color
        self.x = x
        self.width = RECT_WIDTH
        self.height = height

    def select(self):
        self.color = BLUE

    def unselect(self):
        self.color = PURPLE

    def set_smallest(self):
        self.color = LIGHT_BLUE

    def set_sorted(self):
        self.color = GREEN

def create_rectangles():
    num_rectangles = WINDOW_SIZE // RECT_WIDTH - 5
    rectangles = []
    heights = []

    for i in range(5, num_rectangles):
        height = random.randint(20, 500)
        while height in heights:
            height = random.randint(20, 500)

        heights.append(height)

        rect = Rectangle(PURPLE, i * RECT_WIDTH, height)
        rectangles.append(rect)

    return rectangles

def center_rectangles(rectangles):
    for i, rect in enumerate(rectangles):
        rect.x = (i + 5) * RECT_WIDTH

def draw_rects(rectangles):
    WINDOW.fill((240,240,255))

    for rect in rectangles:
        pygame.draw.rect(WINDOW, rect.color, (rect.x, WINDOW_SIZE - rect.height, rect.width, rect.height))
        pygame.draw.line(WINDOW, BLACK, (rect.x, WINDOW_SIZE), (rect.x, WINDOW_SIZE - rect.height))
        pygame.draw.line(WINDOW, BLACK, (rect.x + rect.width, WINDOW_SIZE), (rect.x + rect.width, WINDOW_SIZE - rect.height))
        pygame.draw.line(WINDOW, BLACK, (rect.x, WINDOW_SIZE - rect.height), (rect.x + rect.width, WINDOW_SIZE - rect.height))

def selection_sort(rectangles):
    num_rectangles = len(rectangles)

    for i in range(num_rectangles):
        min_index = i
        rectangles[i].set_smallest()

        for j in range(i + 1, num_rectangles):
            rectangles[j].select()
            draw_rects(rectangles)

            if rectangles[j].height < rectangles[min_index].height:
                rectangles[min_index].unselect()
                min_index = j
                
            rectangles[min_index].set_smallest()
            draw_rects(rectangles)
            rectangles[j].unselect()
            yield
            
        rectangles[i].x, rectangles[min_index].x = rectangles[min_index].x, rectangles[i].x
        rectangles[i], rectangles[min_index] = rectangles[min_index], rectangles[i]
        rectangles[min_index].unselect()
        rectangles[i].set_sorted()
        draw_rects(rectangles)

    center_rectangles(rectangles)
    draw_rects(rectangles)

def bubble_sort(rectangles):
    num_rectangles = len(rectangles)
    for i in range(num_rectangles):
        for j in range(num_rectangles - i - 1):
            rectangles[j].select()
            rectangles[j + 1].select()
            draw_rects(rectangles)

            if rectangles[j].height > rectangles[j + 1].height:
                rectangles[j].x, rectangles[j + 1].x = rectangles[j + 1].x, rectangles[j].x
                rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
                draw_rects(rectangles)

            yield
            rectangles[j].unselect()
            rectangles[j + 1].unselect()

        rectangles[num_rectangles - i - 1].set_sorted()

    # Center the rectangles after sorting
    center_rectangles(rectangles)
    draw_rects(rectangles)

def insertion_sort(rectangles):
    for i in range(1, len(rectangles)):
        
        key_rect = rectangles[i]
        # pygame.time.delay(50)
        key_rect.color = LIGHT_BLUE 
        # pygame.time.delay(50)       
        j = i - 1

        while j >= 0 and key_rect.height < rectangles[j].height:
            rectangles[j].unselect()
            
            pygame.time.delay(50)
            
            rectangles[j + 1] = rectangles[j]
            rectangles[j + 1].x = rectangles[j].x + RECT_WIDTH
            
            draw_rects(rectangles)
            yield
            j -= 1

        rectangles[j + 1] = key_rect
        rectangles[j + 1].x = (j + 1) * RECT_WIDTH

        key_rect.color = LIGHT_BLUE
        draw_rects(rectangles)
        
        pygame.time.delay(10)

    for rect in rectangles:
        rect.set_sorted()
        
    center_rectangles(rectangles)
    draw_rects(rectangles)


def display_text(txt, y, size):
    FONT = pygame.font.SysFont('Futura', size)
    text = FONT.render(txt, True, BLACK)
    text_rect = text.get_rect(center=(WINDOW_SIZE / 2, y))
    WINDOW.blit(text, text_rect)

def main():
    rectangles = create_rectangles()
    draw_rects(rectangles)
    sorting_generator = None
    algorithm = ""

    run = True
    sorting = False
    while run:
        clock.tick(FPS)

        if sorting and sorting_generator:
            try:
                next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            draw_rects(rectangles)

        display_text(f'Current Algorithm: {algorithm}', 20, 30)
        display_text('S: selection sort', 40,25)
        display_text('B: bubble sort', 60,25)
        display_text('I: insertion sort', 80,25)
        display_text('Space: start', 100,25)
        display_text('ESC: exit', 120,25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sorting = not sorting
                    if sorting and not sorting_generator:
                        if algorithm == "Selection sort":
                            sorting_generator = selection_sort(rectangles)
                        elif algorithm == "Bubble sort":
                            sorting_generator = bubble_sort(rectangles)
                        elif algorithm == "Insertion sort":
                            sorting_generator = insertion_sort(rectangles)
                        
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_s:
                    algorithm = "Selection sort"
                    sorting_generator = None
                    rectangles = create_rectangles()
                if event.key == pygame.K_b:
                    algorithm = "Bubble sort"
                    sorting_generator = None
                    rectangles = create_rectangles()
                if event.key == pygame.K_i:
                    algorithm = "Insertion sort"
                    sorting_generator = None
                    rectangles = create_rectangles()

        pygame.display.update()
    pygame.quit()

main()
