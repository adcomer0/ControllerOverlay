from src.main_assets.ps4.ps4_assets import PS4Assets
from src.main_assets.xbox1.xbox1_assets import Xbox1Assets
from src.main_assets.wolverine.wolverine_assets import WolverineAssets
from src.main_assets.kbm.mouse_keyboard_assets import MouseKeyboardAssets

def get_assets(platform):
    if platform == 'ps4':
        return PS4Assets()
    elif platform == 'xbox1':
        return Xbox1Assets()
    elif platform == 'wolverine':
        return WolverineAssets()
    elif platform == 'mouse_keyboard':
        return MouseKeyboardAssets()
    return None

def get_button_translator(platform):
    if platform == 'ps4':
        return PS4Assets.ButtonTranslator()
    elif platform == 'xbox1':
        return Xbox1Assets.ButtonTranslator()
    elif platform == 'wolverine':
        return WolverineAssets.ButtonTranslator()
    return None
