import pygame
import pathlib

def load_image(path):
    return pygame.image.load(str(path))

def get_relative_position(base_size, original_position, scale=1):
    base_width, base_height = base_size
    x, y = original_position
    return (x / 700 * base_width * scale, y / 500 * base_height * scale)

class Xbox1Assets:
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
        self._files = pathlib.Path.cwd() / 'main_assets' / 'xbox1' / 'pngs'

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
        self.left_trigger = {'img': pygame.transform.flip(load_image(self._files / 'trigger_pressed.png'), True, False), 'loc': get_relative_position(base_size, (515, 6), scale)}
        self.right_trigger = {'img': pygame.transform.flip(self.left_trigger['img'], True, False), 'loc': get_relative_position(base_size, (156, 6), scale)}
        bumper = load_image(self._files / 'bumper_pressed.png')
        joystick_up = load_image(self._files / 'joystick_released.png')
        joystick_down = load_image(self._files / 'joystick_pressed.png')
        self._assets = {
            'southButton': {
                1: {'img': load_image(self._files / 'A_pressed.png'), 'loc': get_relative_position(base_size, (548, 311), scale)},
                0: {'img': load_image(self._files / 'A_released.png'), 'loc': get_relative_position(base_size, (548, 311), scale)}
            },
            'eastButton': {
                1: {'img': load_image(self._files / 'B_pressed.png'), 'loc': get_relative_position(base_size, (598, 261), scale)},
                0: {'img': load_image(self._files / 'B_released.png'), 'loc': get_relative_position(base_size, (598, 261), scale)}
            },
            'westButton': {
                1: {'img': load_image(self._files / 'X_pressed.png'), 'loc': get_relative_position(base_size, (497, 261), scale)},
                0: {'img': load_image(self._files / 'X_released.png'), 'loc': get_relative_position(base_size, (497, 261), scale)}
            },
            'northButton': {
                1: {'img': load_image(self._files / 'Y_pressed.png'), 'loc': get_relative_position(base_size, (547, 210), scale)},
                0: {'img': load_image(self._files / 'Y_released.png'), 'loc': get_relative_position(base_size, (547, 210), scale)}
            },
            'leftBumper': {1: {'img': bumper, 'loc': get_relative_position(base_size, (113, 134), scale)}},
            'rightBumper': {1: {'img': pygame.transform.flip(bumper, True, False), 'loc': get_relative_position(base_size, (477, 134), scale)}},
            'leftCenterButton': {1: {'img': load_image(self._files / 'start_pressed.png'), 'loc': get_relative_position(base_size, (311, 268), scale)}},
            'rightCenterButton': {1: {'img': load_image(self._files / 'select_pressed.png'), 'loc': get_relative_position(base_size, (418, 268), scale)}},
            'leftJoystick': {
                0: {'img': joystick_up, 'loc': get_relative_position(base_size, (150, 241), scale)},
                1: {'img': joystick_down, 'loc': get_relative_position(base_size, (150, 241), scale)}
            },
            'rightJoystick': {
                0: {'img': joystick_up, 'loc': get_relative_position(base_size, (436, 356), scale)},
                1: {'img': joystick_down, 'loc': get_relative_position(base_size, (436, 356), scale)}
            },
            'DPAD': {
                0: {
                    -1: {'img': load_image(self._files / 'dpad_left.png'), 'loc': get_relative_position(base_size, (228, 388), scale)},
                    1: {'img': load_image(self._files / 'dpad_right.png'), 'loc': get_relative_position(base_size, (283, 388), scale)}
                },
                1: {
                    -1: {'img': load_image(self._files / 'dpad_down.png'), 'loc': get_relative_position(base_size, (266, 406), scale)},
                    1: {'img': load_image(self._files / 'dpad_up.png'), 'loc': get_relative_position(base_size, (265, 350), scale)}
                }
            }
        }
        self._loaded = True

    class ButtonTranslator:
        xbox1 = {
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
            return self.xbox1.get(item)
