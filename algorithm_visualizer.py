#!/usr/bin/python3
from turtle import width
import pygame
import random
import math
pygame.init()


class DrawInformation:
    """ Window Draw Information """
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 112, 255, 136
    RED = 255, 159, 159
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (148, 159, 255),
        (92, 108, 247),
        (52, 63, 166)
    ]


    FONT = pygame.font.SysFont('Arial', 20)
    LARGE_FONT = pygame.font.SysFont('Arial', 40)
    # Padding to the left and right
    SIDE_PAD = 100
    # Padding to the top
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        """ initiates """
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        """ sets the list draw info"""
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # How the width of each block will be calculated
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        # How the max height of all blocks will be calculated
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        # Drawing point start
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    """ draws the background and text"""
    # Access the window defined in __init__
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2 , 5))

    # A surface
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    # Blit a surface to another screen. auto adjust to the center
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2 , 50))

    sorting = draw_info.FONT.render(f"I - Insertion Sort | B - Bubble Sort | Speed - Up or Down", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2 , 75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    """ draws the blocks """
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        # Re-draws the background on the coordinates above
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        # Starting position + index * width of the blocks
        x = draw_info.start_x + i * draw_info.block_width

        # height of the screen - (value of the item - minimum value (0)) *
        # height of the blocks
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]
        # Draws rectangles on every loop
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    """ generates the starting list """
    lst = []

    # Sets a random list
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                # Pauses the execution of the function where it was left and
                # starts again from that place next time is called
                # If I don't yield the function will have whole control
                # of whats happening and I wont be able to stop it
                yield True

    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and  lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 100
    min_val = 0
    max_val = 150
    speed = 150

    lst = generate_starting_list(n, min_val, max_val)
    # draw_info is an instance of a DrawInformation class
    draw_info = DrawInformation(1200, 900, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(speed)

        if sorting:
            # if this doesn't work it means the generator is done
            try:
                next(sorting_algorithm_generator)
            # we switch sorting to false cause it is done
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # Checks for specific events to happen
        for event in pygame.event.get():
            # When we break the main while loop the program will quit
            # This events happens when clicking the red X
            if event.type == pygame.QUIT:
                run = False

            # This event happens when pressing a key
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst =  generate_starting_list(n, min_val, max_val)
                # We need to store it on draw_info object for it to be updated
                # by draw()
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_UP:
                speed += 50
            elif event.key == pygame.K_DOWN:
                speed -= 50
                if speed < 0:
                    speed = 1


    pygame.quit()

if __name__ == "__main__":
    main()