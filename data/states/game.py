

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
        
        self.bg_color = (255,255,255)

        self.help_overlay = False
        self.card_bufferX = 100
        self.card_bufferY = 25
        
        button_config = {
            "hover_color"        : (100,255,100),
            "clicked_color"      : (255,255,255),
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (0,0,0),
            'font'               : tools.Font.load('impact.ttf', 24),
            'font_color'         : (0,0,0),
            'call_on_release'    : False
        }
        self.play_card_button = button.Button((25,50,175,50),(100,200,100), 
            None, text='Play Card', **button_config
        )
        
        self.bg_music_files = ['human1.wav','human2.wav','human3.wav','human4.wav','human5.wav','human6.wav',]
        self.bg_music = tools.Music(.3)
        
        self.hud_bg_orig = tools.Image.load('hud.png')
        self.hud_bg = pg.transform.scale(self.hud_bg_orig, (self.screen_rect.width, self.screen_rect.height))
        self.hud_bg_rect = self.hud_bg.get_rect(center=self.screen_rect.center)
    
    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == self.keybinding['back']:
                if not self.help_overlay:
                    self.button_sound.sound.play()
                    self.done = True
                    self.next = 'MENU'
                else:
                    self.help_overlay = not self.help_overlay
                
        elif event.type == self.bg_music.track_end:
            self.bg_music.track = (self.bg_music.track+1) % len(self.bg_music.tracks)
            pg.mixer.music.load(self.bg_music.tracks[self.bg_music.track]) 
            pg.mixer.music.play()
                    
    def update(self, now, keys):
        self.help_overlay_title, self.help_overlay_title_rect = self.make_text('test',
            (255,255,255), (self.screen_rect.centerx, 100), 60, fonttype='impact.ttf')
        
        #string = self.database[filename]['info']
        #my_font = tools.Font.load('impact.ttf', 20)
        #self.help_overlay_text_rect = pg.Rect((400, 200, 300, 300))
        #self.help_overlay_text = tools.render_textrect(string, my_font, self.help_overlay_text_rect, (216, 216, 216), (48, 48, 48, 255), 0)
        
    def render(self, screen):
        screen.fill((self.bg_color))
        screen.blit(self.hud_bg, self.hud_bg_rect)
        if self.help_overlay:
            screen.blit(self.overlay_bg,(0,0))
            screen.blit(self.help_overlay_title, self.help_overlay_title_rect)
            
    def cleanup(self):
        pg.mixer.music.stop()
        
    def entry(self):
        self.bg_music.load_files(self.bg_music_files)
        pg.mixer.music.play()
