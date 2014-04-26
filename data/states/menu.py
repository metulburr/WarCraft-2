

import pygame as pg
from .. import tools
from ..GUI import button
import random

class Menu(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.options = ['Play', 'Quit']
        self.next_list = ['GAME']
        self.pre_render_options()
        self.from_bottom = 200
        self.spacer = 75

        self.bg_orig = tools.Image.load('menu_bg.png')
        self.bg = pg.transform.scale(self.bg_orig, (self.screen_rect.width, self.screen_rect.height))
        self.bg_rect = self.bg.get_rect(center=self.screen_rect.center)
        self.cursor = tools.Image.load('mouse_pointer.png')
        #self.cursor_rect = self.cursor.get_rect(center=pg.mouse.get_pos())
        
        btn_config = {
            'font':tools.Font.load('impact.ttf', 25),
            'hover_color':(100,0,0),
            'font_color':(205,195,0),
            'hover_font_color':(255,255,255),
        }
        self.play_btn = button.Button((0,0,200,50), (100,0,0), None, text='Play', **btn_config)
        self.exit_btn = button.Button((100,100,200,50), (100,0,0), None, text='Quit', **btn_config)

    def render_cursor(self, screen):
        mouseX, mouseY = pg.mouse.get_pos()
        self.cursor_rect = self.cursor.get_rect(center=(mouseX+10, mouseY+13))
        screen.blit(self.cursor, self.cursor_rect)

    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)
                
            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        elif event.type == self.intro.track_end:
            self.intro.track = (self.intro.track+1) % len(self.intro.tracks)
            pg.mixer.music.load(self.intro.tracks[self.intro.track]) 

        self.mouse_menu_click(event)

    def update(self, now, keys):
        self.mouse_hover_sound()
        self.change_selected_option()

    def render(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.bg, self.bg_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (self.screen_rect.centerx, self.from_bottom+i*self.spacer)
            #self.red_bg_rect.center = opt[i].center
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                screen.blit(opt[0],opt[1])
        
        #self.play_btn.render(screen)
        #self.exit_btn.render(screen)
        self.render_cursor(screen)
        
    def cleanup(self):
        pg.mouse.set_visible(True)
        self.intro_started = False
        pg.mixer.music.stop()
        #self.background_music.setup(self.background_music_volume)
        
    def entry(self):
        pg.mouse.set_visible(False)
        if not self.intro_started:
            self.intro.load()
            pg.mixer.music.play()
            self.intro_started = True

