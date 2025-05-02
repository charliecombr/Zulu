import pygame
import random
import sys
from config import *
from entities import Obstacle

def generate_obstacles(obstacles, elapsed_time, last_obstacle_time, obstacle_frequency):

    current_time = pygame.time.get_ticks()
    time_since_last = current_time - last_obstacle_time
    
    adjusted_frequency = max(500, obstacle_frequency - (elapsed_time // 10000) * 100)
    
    if time_since_last > adjusted_frequency:
        lane = random.randint(0, 2)
        obstacles.append(Obstacle(lane))
        return current_time, adjusted_frequency
    
    return last_obstacle_time, adjusted_frequency