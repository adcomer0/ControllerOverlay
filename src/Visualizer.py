import assets.assets as gamepad_assets
from assets.kbm_assets import MouseKeyboardAssets
import pygame
import os

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
COLOUR_KEY = (255, 0, 128)  # fuchsia

class Visualizer:
    def __init__(self, assets, gamepad_type: str, gamepad_number: int = 0, trigger_deadzone: float = 0.002, transparent: bool = False):
        self.asset_map = assets
        self.asset_map.load(transparent)
        
        self.running = False
        self.window_is_framed = not transparent
        self.trigger_deadzone = trigger_deadzone
        self.transparent = transparent
        
        pygame.joystick.init()
        if not isinstance(assets, MouseKeyboardAssets):
            self.controller = pygame.joystick.Joystick(gamepad_number)
            self.controller.init()
            self.BUTTON_TRANSLATION = gamepad_assets.get_button_translator(gamepad_type)
        
        pygame.init()
        size = self.asset_map._base.get_size()
        if transparent:
            self.window_size = (size[0] // 2 + 10, size[1] // 2 + 10)
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, pygame.display.Info().current_h - self.window_size[1])
            self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME | pygame.SRCALPHA)
            pygame.display.set_caption('Controller Visualisation Overlay')
            self.base_image = pygame.transform.scale(self.asset_map._base, (self.window_size[0] - 10, self.window_size[1] - 10))
            self.base_image.set_colorkey(COLOUR_KEY)
        else:
            self.window_size = (size[0] + 10, size[1] + 10)
            self.screen = pygame.display.set_mode(self.window_size)
            pygame.display.set_caption('Controller Visualisation Overlay')
            self.base_image = self.asset_map._base

        if not isinstance(assets, MouseKeyboardAssets):
            self.left_analog = self.asset_map[self.asset_map.left_analog][0]
            self.right_analog = self.asset_map[self.asset_map.right_analog][0]

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # right click to toggle window frame
                        self.toggle_window_frame()

            if not self.transparent:
                self.screen.fill(COLOUR_KEY)
            
            self.screen.blit(self.base_image, (5, 5))

            self.update_buttons_and_sticks()

            pygame.display.update()

    def toggle_window_frame(self):
        if not self.window_is_framed:
            self.window_is_framed = True
            self.screen = pygame.display.set_mode(self.window_size)
        else:
            self.window_is_framed = False
            self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME | pygame.SRCALPHA)

    def update_buttons_and_sticks(self):
        if isinstance(self.asset_map, MouseKeyboardAssets):
            self.update_mouse_keyboard()
        else:
            for button_num in range(self.controller.get_numbuttons()):
                button_is_pressed = self.controller.get_button(button_num)
                button_ID = self.BUTTON_TRANSLATION(button_num)
                if button_ID in self.asset_map.analogs:
                    self.update_analogs(button_ID, button_is_pressed)
                else:
                    self.update_buttons(button_ID, button_is_pressed)

            dpad_state = self.controller.get_hat(0)
            for im, loc in self.asset_map[dpad_state]:
                self.blit_scaled(im, loc)

            self.update_analog_stick_movement()

            self.update_triggers()

    def update_mouse_keyboard(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Draw the key grid
        for key, value in self.asset_map._assets.items():
            self.screen.blit(value['img'], value['loc'])

        for key, value in self.asset_map._assets.items():
            try:
                key_code = pygame.key.key_code(key)
                if key_code and keys[key_code]:
                    self.screen.blit(value['img'], value['loc'])
                elif key == 'leftmouse' and mouse_buttons[0]:
                    self.screen.blit(value['img'], value['loc'])
                elif key == 'middlemouse' and mouse_buttons[1]:
                    self.screen.blit(value['img'], value['loc'])
                elif key == 'rightmouse' and mouse_buttons[2]:
                    self.screen.blit(value['img'], value['loc'])
            except ValueError:
                continue

        pygame.draw.circle(self.screen, WHITE, (self.window_size[0]//2, self.window_size[1]//2), 50, 1)
        relative_mouse_pos = (mouse_pos[0] - self.window_size[0]//2, mouse_pos[1] - self.window_size[1]//2)
        pygame.draw.circle(self.screen, WHITE, (self.window_size[0]//2 + relative_mouse_pos[0]//2, self.window_size[1]//2 + relative_mouse_pos[1]//2), 5)
        
    def update_analogs(self, button_ID, button_is_pressed):
        if button_ID == self.asset_map.left_analog:
            self.left_analog = self.asset_map[button_ID][button_is_pressed]
        else:
            self.right_analog = self.asset_map[button_ID][button_is_pressed]

    def update_buttons(self, button_ID, button_is_pressed):
        try:
            btndat = self.asset_map[button_ID][button_is_pressed]
            self.blit_scaled(btndat['img'], btndat['loc'])
        except (KeyError, TypeError):
            pass

    def blit_scaled(self, img, loc):
        if not self.window_is_framed:
            img = pygame.transform.scale(img, (img.get_width() // 2, img.get_height() // 2))
            loc = (loc[0] // 2, loc[1] // 2)
        self.screen.blit(img, loc)

    def update_analog_stick_movement(self):
        left_ana_horiz, left_ana_verti = round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.left_stick_x)), 2), round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.left_stick_y)), 2)
        right_ana_horiz, right_ana_verti = round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.right_stick_x)), 2), round(self.controller.get_axis(self.BUTTON_TRANSLATION(self.asset_map.right_stick_y)), 2)

        if not self.window_is_framed:
            self.screen.blit(pygame.transform.scale(self.left_analog['img'], (self.left_analog['img'].get_width() // 2, self.left_analog['img'].get_height() // 2)), 
                             (self.left_analog['loc'][0] // 2 + (15 * left_ana_horiz), self.left_analog['loc'][1] // 2 + (15 * left_ana_verti)))
            self.screen.blit(pygame.transform.scale(self.right_analog['img'], (self.right_analog['img'].get_width() // 2, self.right_analog['img'].get_height() // 2)), 
                             (self.right_analog['loc'][0] // 2 + (15 * right_ana_horiz), self.right_analog['loc'][1] // 2 + (15 * right_ana_verti)))
        else:
            self.screen.blit(self.left_analog['img'], (self.left_analog['loc'][0] + (30 * left_ana_horiz), self.left_analog['loc'][1] + (30 * left_ana_verti)))
            self.screen.blit(self.right_analog['img'], (self.right_analog['loc'][0] + (30 * right_ana_horiz), self.right_analog['loc'][1] + (30 * right_ana_verti)))

    def update_triggers(self):
        lt = self.asset_map.left_trigger
        rt = self.asset_map.right_trigger
        if max(0, (self.controller.get_axis(5) + 1) / 2) > self.trigger_deadzone:
            self.blit_scaled(lt['img'], lt['loc'])
        if max(0, (self.controller.get_axis(4) + 1) / 2) > self.trigger_deadzone:
            self.blit_scaled(rt['img'], rt['loc'])
