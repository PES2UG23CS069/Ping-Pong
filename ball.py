import pygame
import random
import math

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-3, 3])
        self.velocity_y = random.choice([-2, 2])
        self.MAX_SPEED = 7

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            pygame.mixer.Sound('sounds/wall_bounce.wav').play()  # wall bounce sound


    def check_collision(self, player, ai):
        current_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)

        if self.rect().colliderect(player.rect()):
            if current_speed < self.MAX_SPEED:
                self.velocity_x *= -1.1
            else:
                self.velocity_x *= -1
            self.x = player.x + player.width
            return True # CHANGED: Report that a collision happened

        if self.rect().colliderect(ai.rect()):
            if current_speed < self.MAX_SPEED:
                self.velocity_x *= -1.1
            else:
                self.velocity_x *= -1
            self.x = ai.x - self.width
            return True # CHANGED: Report that a collision happened
        
        return False # CHANGED: Report that no collision happened

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-2, 2])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)