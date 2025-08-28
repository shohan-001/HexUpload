#!/usr/bin/env python3
from os import listdir
from importlib import import_module
from random import choice as rchoice
from bot import config_dict, LOGGER
from bot.helper.themes import kpsml_minimal, kpsml_cyber

# Available themes dictionary with proper imports
AVL_THEMES = {
    "minimal": kpsml_minimal, 
    "cyber": kpsml_cyber
}

# Auto-detect and import all theme files
for theme in listdir('bot/helper/themes'):
    if theme.startswith('kpsml_') and theme.endswith('.py'):
        theme_name = theme[5:-3]  # Remove 'kpsml_' prefix and '.py' suffix
        if theme_name not in AVL_THEMES:  # Avoid re-importing already defined themes
            try:
                AVL_THEMES[theme_name] = import_module(f'bot.helper.themes.{theme[:-3]}')
            except ImportError as e:
                LOGGER.error(f"Failed to import theme {theme}: {e}")

def BotTheme(var_name, **format_vars):
    text = None
    theme_ = config_dict.get('BOT_THEME', 'minimal')  # Default to minimal if not set
    
    if theme_ in AVL_THEMES:
        try:
            text = getattr(AVL_THEMES[theme_].KPSMLStyle(), var_name, None)
            if text is None:
                LOGGER.error(f"{var_name} not found in {theme_} theme. Using minimal theme as fallback.")
        except Exception as e:
            LOGGER.error(f"Error accessing {theme_} theme: {e}. Using minimal theme as fallback.")
            
    elif theme_ == 'random':
        try:
            rantheme = rchoice(list(AVL_THEMES.values()))
            theme_name = next(name for name, module in AVL_THEMES.items() if module == rantheme)
            LOGGER.info(f"Random Theme Chosen: {theme_name}")
            text = getattr(rantheme.KPSMLStyle(), var_name, None)
        except Exception as e:
            LOGGER.error(f"Error with random theme selection: {e}")
    else:
        LOGGER.warning(f"Theme '{theme_}' not found. Available themes: {list(AVL_THEMES.keys())}")
    
    # Fallback to minimal theme if text is still None
    if text is None:
        try:
            text = getattr(kpsml_minimal.KPSMLStyle(), var_name)
        except AttributeError:
            LOGGER.error(f"Critical: {var_name} not found in minimal theme either!")
            return f"ERROR: {var_name} not found"
    
    # Handle formatting safely
    try:
        return text.format(**format_vars) if format_vars else text
    except (KeyError, ValueError) as e:
        LOGGER.error(f"Error formatting text for {var_name}: {e}")
        return text  # Return unformatted text as fallback
