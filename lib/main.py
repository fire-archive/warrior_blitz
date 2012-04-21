import pygame
import pygame.transform
import pygame.display
import pygame.draw
import pygame.time
import pygame.key

from math import *
import sys

from util import *
from data import *
from game import *
from menu import *

def init():
    pygame.init()
    sys.exitfunc = pygame.quit
    
    pygame.display.set_mode(WIN_SIZE,(pygame.HWSURFACE|pygame.DOUBLEBUF),0)
    pygame.display.set_caption('Warrior Blitz')
    

def run():
    running = True
    clock = pygame.time.Clock()
    
    world = None
    
    game_factory = GameFactory()
    
    world = game_factory.makeTestWorld()
    
    input_state = {
        'select':False,
        'command':False,
        'pause':False,
        
        'mouse pos':[0,0],
        
    }
    
    draw_surface = pygame.Surface(WIN_SIZE)
    
    def updateVideoSurface():
        pygame.display.get_surface().blit(draw_surface,(0,0))
        pygame.display.flip()
        
    
    while running:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                break
                
            elif event.type in (pygame.KEYDOWN,pygame.KEYUP):
                key_name = pygame.key.name(event.key)
                key_down = event.type == pygame.KEYDOWN
                
                if key_name == 'escape':
                    running = False
                    break
                    
                
            elif event.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP):
                
                # Whether the button was down
                button_down = event.type == pygame.MOUSEBUTTONDOWN
                
                if event.button == 1:
                    input_state['select'] = button_down
                    
                elif event.button == 1:
                    input_state['command'] = button_down
                    
                
            elif event.type == pygame.MOUSEMOTION:
                input_state['mouse pos'][0] = event.pos[0]
                input_state['mouse pos'][1] = event.pos[1]
                
            
        
        if not running:
            break
            
        
        dt_ms = clock.tick(FRAME_RATE)
        dt_sec = dt_ms / 1000.0
        
        if world:
            world.update(dt_sec,input_state)
            world.draw(draw_surface)
            
        
        updateVideoSurface()
        
    

def main():
    init()
    run()
    

if __name__.lower() == '__main__':
    main()
    
