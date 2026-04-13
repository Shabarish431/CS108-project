import pygame
import numpy as np
import matplotlib.pyplot as plt
import sys
import datetime



def main_menu():
    screen.fill('azure4')

pygame.init() #initializing the pygame
pygame.display.set_caption("Mini Gaming Hub")
screen=pygame.display.set_mode((600, 600)) #declaring the size of the screen
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    main_menu()
    pygame.display.update()
pygame.quit()