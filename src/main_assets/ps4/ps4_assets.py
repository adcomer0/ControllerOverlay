import pygame
import pathlib

def load_image(path):
    return pygame.image.load(str(path))

def get_relative_position(base_size, original_position, scale=1):
    base_width, base_height = base_size
    x, y = original_position
    return (x / 700 * base_width * scale, y / 500 * base_height * scale)

class PS4Assets:
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
        self._files = pathlib.Path.cwd() / 'main_assets' / 'ps4' / 'pngs'

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
        self.left_trigger = {'img': load_image(self._files / 'left_trigger_pressed.png'), 'loc': get_relative_position(base_size, (113, 5), scale)}
        self.right_trigger = {'img': load_image(self._files / 'right_trigger_pressed.png'), 'loc': get_relative_position(base_size, (602, 5), scale)}
        bumper = load_image(self._files / 'bumper_pressed.png')
        joystick_up = load_image(self._files / 'stick_released.png')
        self._assets = {
            'southButton': {1: {'img': load_image(self._files / 'X_pressed.png'), 'loc': get_relative_position(base_size, (628, 279), scale)}},
            'eastButton': {1: {'img': load_image(self._files / 'Circle_pressed.png'), 'loc': get_relative_position(base_size, (686, 222), scale)}},
            'westButton': {1: {'img': load_image(self._files / 'Square_pressed.png'), 'loc': get_relative_position(base_size, (570, 222), scale)}},
            'northButton': {1: {'img': load_image(self._files / 'Triangle_pressed.png'), 'loc': get_relative_position(base_size, (628, 164), scale)}},
            'leftBumper': {1: {'img': bumper, 'loc': get_relative_position(base_size, (114, 99), scale)}},
            'rightBumper': {1: {'img': pygame.transform.flip(bumper, True, False), 'loc': get_relative_position(base_size, (603, 99), scale)}},
            'leftCenterButton': {1: {'img': load_image(self._files / 'share_pressed.png'), 'loc': get_relative_position(base_size, (232, 148), scale)}},
            'rightCenterButton': {1: {'img': load_image(self._files / 'options_pressed.png'), 'loc': get_relative_position(base_size, (556, 148), scale)}},
            'centerButton': {1: {'img': load_image(self._files / 'touchpad_pressed.png'), 'loc': get_relative_position(base_size, (277, 127), scale)}},
            'platformButton': {1: {'img': load_image(self._files / 'ps_pressed.png'), 'loc': get_relative_position(base_size, (387, 344), scale)}},
            'leftJoystick': {
                0: {'img': joystick_up, 'loc': get_relative_position(base_size, (235, 313), scale)},
                1: {'img': load_image(self._files / 'left_stick_pressed.png'), 'loc': get_relative_position(base_size, (235, 313), scale)}
            },
            'rightJoystick': {
                0: {'img': joystick_up, 'loc': get_relative_position(base_size, (491, 314), scale)},
                1: {'img': load_image(self._files / 'right_stick_pressed.png'), 'loc': get_relative_position(base_size, (491, 314), scale)}
            },
            'DPAD': {
                0: {
                    -1: {'img': load_image(self._files / 'dpad_left.png'), 'loc': get_relative_position(base_size, (98, 230), scale)},
                    1: {'img': load_image(self._files / 'dpad_right.png'), 'loc': get_relative_position(base_size, (168, 230), scale)}
                },
                1: {
                    -1: {'img': load_image(self._files / 'dpad_down.png'), 'loc': get_relative_position(base_size, (140, 259), scale)},
                    1: {'img': load_image(self._files / 'dpad_up.png'), 'loc': get_relative_position(base_size, (140, 186), scale)}
                }
            }
        }
        self._loaded = True

    class ButtonTranslator:
        ps4 = {
            0: 'westButton',
            1: 'southButton',
            2: 'eastButton',
            3: 'northButton',
            4: 'leftBumper',
            5: 'rightBumper',
            6: 'leftTrigger',
            7: 'rightTrigger',
            8: 'leftCenterButton',
            9: 'rightCenterButton',
            10: 'leftJoystick',
            11: 'rightJoystick',
            12: 'platformButton',
            13: 'centerButton',
            'LeftStickX': 0,
            'LeftStickY': 1,
            'RightStickX': 2,
            'RightStickY': 3
        }

        def __init__(self):
            pass

        def __call__(self, item):
            return self.ps4.get(item)
