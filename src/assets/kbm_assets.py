import pygame
import os
import pathlib
import sys

class MouseKeyboardAssets:
    def __init__(self):
        self._loaded = False
        self._assets = {}
        self._base = None
        self._files = self._get_assets_path() / 'main_assets' / 'kbm' / 'pngs'

    def _get_assets_path(self):
        if getattr(sys, 'frozen', False):  # Check if the program is running as a bundled executable
            return pathlib.Path(sys._MEIPASS)
        else:
            return pathlib.Path(__file__).resolve().parent.parent.parent

    def __getitem__(self, item):
        return self._assets[item]

    @property
    def loaded(self):
        return self._loaded

    def load(self, transparent=False):
        pygame.font.init()
        self._base = pygame.Surface((800, 600), pygame.SRCALPHA)
        self._base.fill((0, 0, 0, 0))

        font = pygame.font.SysFont(None, 24)
        keys = [
            ('w', (100, 100)), ('s', (100, 150)), ('a', (50, 150)), ('d', (150, 150)),
            ('leftshift', (50, 300)), ('spacebar', (200, 300)), ('leftctrl', (50, 350)),
            ('r', (150, 100)), ('1', (50, 50)), ('2', (100, 50)), ('3', (150, 50)), ('4', (200, 50)),
            ('g', (150, 200)), ('y', (200, 100)), ('f', (100, 200)), ('q', (50, 100)), ('e', (200, 150)),
            ('c', (50, 200)), ('x', (100, 250)), ('t', (200, 200)), ('u', (250, 150)), ('v', (150, 250)),
            ('leftalt', (50, 400)), ('b', (200, 250)), ('m', (250, 300)), ('capslock', (50, 450))
        ]

        for key, pos in keys:
            surface = font.render(key.upper(), True, (255, 255, 255))
            rect = surface.get_rect(topleft=pos)
            pygame.draw.rect(self._base, (255, 255, 255), rect.inflate(10, 10), 2)
            self._assets[key] = {'img': surface, 'loc': pos}

        self._assets['leftmouse'] = {'img': font.render('LMB', True, (255, 255, 255)), 'loc': (500, 100)}
        self._assets['middlemouse'] = {'img': font.render('MMB', True, (255, 255, 255)), 'loc': (550, 100)}
        self._assets['rightmouse'] = {'img': font.render('RMB', True, (255, 255, 255)), 'loc': (600, 100)}
        self._assets['scrollup'] = {'img': font.render('ScrollUp', True, (255, 255, 255)), 'loc': (550, 80)}
        self._assets['scrolldown'] = {'img': font.render('ScrollDown', True, (255, 255, 255)), 'loc': (550, 120)}

        self._loaded = True
