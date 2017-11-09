import pygame
import time
from agent import agent
from snake import snake
from pygame.locals import *
from sys import exit


class Simulator:
    def __init__(self):
        self.intro = "press SPACE to change to ai mode"
        self.is_agent = False
        self.red = (255,0,0)
        self.blue = (0, 0, 255)
        self.green = (0,255,0)
        self.white = (255,255,255)
        self.pink = (255, 0, 255)
    def update_word(self):
        if self.is_agent:
            self.intro = "press SPACE to change back"
        else:
            self.intro = "press SPACE to change to ai mode"
        self.surface = self.my_font.render(self.intro, True, self.blue, self.pink)

    def simulate(self):
        a = agent()
        s = snake()
        offset = 50
        pygame.init()
        screen = pygame.display.set_mode((400,450))





        snake_color = self.green
        pygame.display.set_caption("snake.ai")
        self.my_font = pygame.font.SysFont("arial", 24)
        self.surface = self.my_font.render(self.intro, True, self.blue, self.pink)
        
        running = True
        screen.fill(self.white)
        pygame.draw.rect(screen, self.green, [0, 200, 40, 40], 3) 
        x = 0.
        direction = "right"
        while running:
            time.sleep(0.5)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.is_agent = not self.is_agent
                        self.update_word()
                    if event.key == K_LEFT:
                        direction = "left"
                    elif event.key == K_RIGHT:
                        direction = "right"
                    elif event.key == K_UP:
                        direction = "down"
                    elif event.key == K_DOWN:
                        direction = "up"
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            if not self.is_agent:
                snake_color = self.green
                ans = s.run(direction)
            else:
                snake_color = self.blue
                state = a.build_state()
                a.create_Q(state)                 # Create 'state' in Q-table
                direction = a.choose_action(state)
                ans = a.s.run(direction)
            if ans == False:
                s.reset()
                direction = "right"
                continue
            screen.fill(self.white)
            for item in ans[0]:
                pygame.draw.rect(screen, snake_color, [item[0] * 40,item[1] * 40 + offset, 40, 40], 0)
            food = s.get_food()
            pygame.draw.rect(screen, self.red, [food[0] * 40, food[1] * 40 + offset, 40, 40], 0)
            screen.blit(self.surface,(0,0))
            pygame.display.update()


simulator = Simulator()
simulator.simulate()