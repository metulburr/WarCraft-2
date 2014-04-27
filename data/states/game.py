

import pygame as pg
from .. import tools
from ..GUI import button
import os
import random

class Game(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.overlay_bg = pg.Surface((screen_rect.width, screen_rect.height))
        self.overlay_bg.fill(0)
        self.overlay_bg.set_alpha(200)
        self.overlay_card_position = (100,200)
        self.bg_color = (0,0,0)
        
        button_config = {
            "hover_color"        : (0,0,130),
            "clicked_color"      : (255,255,255),
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (205,195, 0),
            'font'               : tools.Font.load('warcraft.ttf', 18),
            'font_color'         : (255,255,255),
        }
        self.menu_button = button.Button((30,2,160,25),(0,0,100), 
            self.test, text='Menu', **button_config
        )
        
        self.bg_music_files = [
            'human1.wav','human2.wav','human3.wav',
            'human4.wav','human5.wav','human6.wav',
        ]
        self.bg_music = tools.Music(.3)
        
        self.hud_bg_orig = tools.Image.load('hud.png')
        self.hud_bg = pg.transform.scale(self.hud_bg_orig, (self.screen_rect.width, self.screen_rect.height))
        self.hud_bg_rect = self.hud_bg.get_rect(center=self.screen_rect.center)
        
        self.cursor = tools.Image.load('hand.png')
        
    def test(self):
        #method for temp callback
        self.button_click.sound.play()

    def render_cursor(self, screen):
        mouseX, mouseY = pg.mouse.get_pos()
        self.cursor_rect = self.cursor.get_rect(center=(mouseX+10, mouseY+13))
        screen.blit(self.cursor, self.cursor_rect)
        
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == self.keybinding['back']:
                self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'
                
        elif event.type == self.bg_music.track_end:
            self.bg_music.track = (self.bg_music.track+1) % len(self.bg_music.tracks)
            pg.mixer.music.load(self.bg_music.tracks[self.bg_music.track]) 
            pg.mixer.music.play()
        self.menu_button.check_event(event)
                    
    def update(self, now, keys):
        pass
        
    def render(self, screen):
        screen.fill((self.bg_color))
        screen.blit(self.hud_bg, self.hud_bg_rect)
        self.menu_button.render(screen)
        self.render_cursor(screen)
            
    def cleanup(self):
        pg.mouse.set_visible(True)
        pg.mixer.music.stop()
        
    def entry(self):
        pg.mouse.set_visible(False)
        self.bg_music.load_list(self.bg_music_files)
        pg.mixer.music.play()
