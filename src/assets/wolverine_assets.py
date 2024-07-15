import pygame
import pathlib
import os
import sys

def load_image(path):
    return pygame.image.load(str(path))

def get_relative_position(base_size, original_position, scale=1):
    base_width, base_height = base_size
    x, y = original_position
    return (x / 700 * base_width * scale, y / 500 * base_height * scale)

class WolverineAssets:
    analogs = ('leftJoystick', 'rightJoystick')
    left_analog = 'leftJoystick'
    right_analog = 'rightJoystick'
    left_stick_x = 'LeftStickX'
    left_stick_y = 'LeftStickY'
    right_stick_x = 'RightStickX'
    right_stick_y = 'RightStickY'

    def __init__(self):
        self._loaded = False
        self._assets = {}
        self._files = self._get_assets_path() / 'main_assets' / 'wolverine' / 'pngs'

    def _get_assets_path(self):
        if getattr(sys, 'frozen', False):  # Check if the program is running as a bundled executable
            return pathlib.Path(sys._MEIPASS)
        else:
            return pathlib.Path(__file__).resolve().parent.parent.parent

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._assets[item]
        elif isinstance(item, tuple):
            imgs = []
            for idx, i in enumerate(item):
                if i != 0:
                    dat = self._assets['DPAD'][idx][i]
                    imgs.append((dat['img'], dat['loc']))
            return imgs

    @property
    def loaded(self):
        return self._loaded

    def load(self, transparent=False):
        self._base = load_image(self._files / 'controller_base.png')
        base_size = self._base.get_size()
        scale = 0.5 if transparent else 1
        self.left_trigger = {'img': load_image(self._files / 'R2_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
        self.right_trigger = {'img': load_image(self._files / 'L2_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
        self._assets = {
            'southButton': {
                1: {'img': load_image(self._files / 'A_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                0: {'img': load_image(self._files / 'A_released.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
            },
            'eastButton': {
                1: {'img': load_image(self._files / 'B_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                0: {'img': load_image(self._files / 'B_released.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
            },
            'westButton': {
                1: {'img': load_image(self._files / 'X_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                0: {'img': load_image(self._files / 'X_released.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
            },
            'northButton': {
                1: {'img': load_image(self._files / 'Y_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                0: {'img': load_image(self._files / 'Y_released.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
            },
            'leftBumper': {1: {'img': load_image(self._files / 'L1_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}},
            'rightBumper': {1: {'img': load_image(self._files / 'R1_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}},
            'leftCenterButton': {1: {'img': load_image(self._files / 'start_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}},
            'rightCenterButton': {1: {'img': load_image(self._files / 'select_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}},
            'leftJoystick': {
                0: {'img': load_image(self._files / 'L3_released.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                1: {'img': load_image(self._files / 'L3_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
            },
            'rightJoystick': {
                0: {'img': load_image(self._files / 'R3_released.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                1: {'img': load_image(self._files / 'R3_pressed.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
            },
            'DPAD': {
                0: {
                    -1: {'img': load_image(self._files / 'dpad_left.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                    1: {'img': load_image(self._files / 'dpad_right.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
                },
                1: {
                    -1: {'img': load_image(self._files / 'dpad_down.png'), 'loc': get_relative_position(base_size, (5, 5), scale)},
                    1: {'img': load_image(self._files / 'dpad_up.png'), 'loc': get_relative_position(base_size, (5, 5), scale)}
                }
            }
        }
        self._loaded = True

    class ButtonTranslator:
        wolverine = {
            0: 'southButton',
            1: 'eastButton',
            2: 'westButton',
            3: 'northButton',
            4: 'leftBumper',
            5: 'rightBumper',
            6: 'leftCenterButton',
            7: 'rightCenterButton',
            8: 'leftJoystick',
            9: 'rightJoystick',
            'LeftStickX': 0,
            'LeftStickY': 1,
            'RightStickX': 2,
            'RightStickY': 3
        }

        def __init__(self):
            pass

        def __call__(self, item):
            return self.wolverine.get(item)
