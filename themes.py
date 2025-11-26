#!/usr/bin/env python3
"""
Terminal Themes Module for Serenium
Beautiful color themes and formatting for enhanced terminal experience.
"""

import os
import sys
from typing import Dict, Any
from enum import Enum

class Color:
    """ANSI color codes for terminal formatting"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Bright background colors
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

class Theme(Enum):
    """Available terminal themes"""
    SERENIUM = "serenium"
    CYBERPUNK = "cyberpunk"
    OCEAN = "ocean"
    FOREST = "forest"
    SUNSET = "sunset"
    MONOCHROME = "monochrome"
    NEON = "neon"
    MATRIX = "matrix"

class TerminalTheme:
    """Terminal theme manager with beautiful color schemes"""
    
    def __init__(self, theme: Theme = Theme.SERENIUM):
        self.theme = theme
        self.colors = self._get_theme_colors()
        self.no_color = not sys.stdout.isatty() or os.getenv('NO_COLOR')
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """Get color scheme for selected theme"""
        themes = {
            Theme.SERENIUM: {
                'primary': Color.CYAN,
                'secondary': Color.BLUE,
                'accent': Color.GREEN,
                'warning': Color.YELLOW,
                'error': Color.RED,
                'success': Color.BRIGHT_GREEN,
                'info': Color.BRIGHT_BLUE,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BRIGHT_CYAN,
                'title': Color.BOLD + Color.CYAN,
                'prompt': Color.BOLD + Color.BLUE,
                'border': Color.BRIGHT_BLACK,
                'icon': Color.GREEN
            },
            Theme.CYBERPUNK: {
                'primary': Color.MAGENTA,
                'secondary': Color.BRIGHT_MAGENTA,
                'accent': Color.CYAN,
                'warning': Color.YELLOW,
                'error': Color.BRIGHT_RED,
                'success': Color.BRIGHT_GREEN,
                'info': Color.BRIGHT_CYAN,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BRIGHT_MAGENTA,
                'title': Color.BOLD + Color.MAGENTA,
                'prompt': Color.BOLD + Color.CYAN,
                'border': Color.MAGENTA,
                'icon': Color.CYAN
            },
            Theme.OCEAN: {
                'primary': Color.BLUE,
                'secondary': Color.CYAN,
                'accent': Color.BRIGHT_BLUE,
                'warning': Color.YELLOW,
                'error': Color.RED,
                'success': Color.BRIGHT_GREEN,
                'info': Color.BRIGHT_CYAN,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BRIGHT_BLUE,
                'title': Color.BOLD + Color.BLUE,
                'prompt': Color.BOLD + Color.CYAN,
                'border': Color.BLUE,
                'icon': Color.CYAN
            },
            Theme.FOREST: {
                'primary': Color.GREEN,
                'secondary': Color.BRIGHT_GREEN,
                'accent': Color.YELLOW,
                'warning': Color.YELLOW,
                'error': Color.RED,
                'success': Color.BRIGHT_GREEN,
                'info': Color.CYAN,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BRIGHT_GREEN,
                'title': Color.BOLD + Color.GREEN,
                'prompt': Color.BOLD + Color.BRIGHT_GREEN,
                'border': Color.GREEN,
                'icon': Color.BRIGHT_GREEN
            },
            Theme.SUNSET: {
                'primary': Color.YELLOW,
                'secondary': Color.RED,
                'accent': Color.MAGENTA,
                'warning': Color.YELLOW,
                'error': Color.BRIGHT_RED,
                'success': Color.BRIGHT_GREEN,
                'info': Color.BRIGHT_BLUE,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BRIGHT_YELLOW,
                'title': Color.BOLD + Color.YELLOW,
                'prompt': Color.BOLD + Color.RED,
                'border': Color.YELLOW,
                'icon': Color.MAGENTA
            },
            Theme.MONOCHROME: {
                'primary': Color.WHITE,
                'secondary': Color.BRIGHT_WHITE,
                'accent': Color.BOLD,
                'warning': Color.YELLOW,
                'error': Color.RED,
                'success': Color.GREEN,
                'info': Color.BLUE,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BOLD + Color.WHITE,
                'title': Color.BOLD + Color.WHITE,
                'prompt': Color.BOLD + Color.BRIGHT_WHITE,
                'border': Color.BRIGHT_BLACK,
                'icon': Color.WHITE
            },
            Theme.NEON: {
                'primary': Color.BRIGHT_MAGENTA,
                'secondary': Color.BRIGHT_CYAN,
                'accent': Color.BRIGHT_YELLOW,
                'warning': Color.BRIGHT_YELLOW,
                'error': Color.BRIGHT_RED,
                'success': Color.BRIGHT_GREEN,
                'info': Color.BRIGHT_BLUE,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BRIGHT_MAGENTA,
                'title': Color.BOLD + Color.BRIGHT_MAGENTA,
                'prompt': Color.BOLD + Color.BRIGHT_CYAN,
                'border': Color.BRIGHT_MAGENTA,
                'icon': Color.BRIGHT_CYAN
            },
            Theme.MATRIX: {
                'primary': Color.GREEN,
                'secondary': Color.BRIGHT_GREEN,
                'accent': Color.BLACK,
                'warning': Color.YELLOW,
                'error': Color.RED,
                'success': Color.BRIGHT_GREEN,
                'info': Color.CYAN,
                'muted': Color.BRIGHT_BLACK,
                'highlight': Color.BRIGHT_GREEN,
                'title': Color.BOLD + Color.GREEN,
                'prompt': Color.BOLD + Color.BRIGHT_GREEN,
                'border': Color.GREEN,
                'icon': Color.BRIGHT_GREEN
            }
        }
        return themes.get(self.theme, themes[Theme.SERENIUM])
    
    def colorize(self, text: str, color_type: str = 'primary') -> str:
        """Apply color to text"""
        if self.no_color:
            return text
        
        color = self.colors.get(color_type, Color.RESET)
        return f"{color}{text}{Color.RESET}"
    
    def success(self, text: str) -> str:
        """Format success message"""
        return self.colorize(f"✅ {text}", 'success')
    
    def error(self, text: str) -> str:
        """Format error message"""
        return self.colorize(f"❌ {text}", 'error')
    
    def warning(self, text: str) -> str:
        """Format warning message"""
        return self.colorize(f"⚠️  {text}", 'warning')
    
    def info(self, text: str) -> str:
        """Format info message"""
        return self.colorize(f"ℹ️  {text}", 'info')
    
    def title(self, text: str) -> str:
        """Format title text"""
        return self.colorize(text, 'title')
    
    def prompt(self, text: str) -> str:
        """Format prompt text"""
        return self.colorize(text, 'prompt')
    
    def muted(self, text: str) -> str:
        """Format muted text"""
        return self.colorize(text, 'muted')
    
    def highlight(self, text: str) -> str:
        """Format highlighted text"""
        return self.colorize(text, 'highlight')
    
    def border(self, text: str) -> str:
        """Format border text"""
        return self.colorize(text, 'border')
    
    def icon(self, text: str) -> str:
        """Format icon text"""
        return self.colorize(text, 'icon')
    
    def header(self, text: str, width: int = 60) -> str:
        """Create a formatted header"""
        padding = (width - len(text) - 4) // 2
        header_line = self.border('═' * width)
        content_line = f"{self.border('║')}{' ' * padding}{self.title(text)}{' ' * (width - len(text) - padding - 4)}{self.border('║')}"
        return f"{header_line}\n{content_line}\n{header_line}"
    
    def footer(self, text: str, width: int = 60) -> str:
        """Create a formatted footer"""
        footer_line = self.border('═' * width)
        content_line = f"{self.border('║')} {self.muted(text)}{' ' * (width - len(text) - 3)}{self.border('║')}"
        return f"{footer_line}\n{content_line}\n{footer_line}"
    
    def box(self, text: str, width: int = 60) -> str:
        """Create a box around text"""
        lines = text.split('\n')
        box_lines = []
        
        # Top border
        box_lines.append(self.border('┌' + '─' * (width - 2) + '┐'))
        
        # Content lines
        for line in lines:
            # Wrap long lines
            while len(line) > width - 4:
                box_lines.append(f"{self.border('│')} {line[:width-4]} {self.border('│')}")
                line = line[width-4:]
            # Pad short lines
            padding = width - 4 - len(line)
            box_lines.append(f"{self.border('│')} {line}{' ' * padding} {self.border('│')}")
        
        # Bottom border
        box_lines.append(self.border('└' + '─' * (width - 2) + '┘'))
        
        return '\n'.join(box_lines)
    
    def progress_bar(self, current: int, total: int, width: int = 40) -> str:
        """Create a progress bar"""
        if total == 0:
            return self.muted('[N/A]')
        
        percentage = current / total
        filled = int(width * percentage)
        empty = width - filled
        
        bar = self.icon('█') * filled + self.muted('░') * empty
        percentage_text = f"{percentage:.0%}"
        
        return f"[{bar}] {self.highlight(percentage_text)}"
    
    def list_item(self, text: str, icon: str = "•", indent: int = 0) -> str:
        """Format a list item"""
        spaces = ' ' * indent
        return f"{spaces}{self.icon(icon)} {text}"
    
    def separator(self, width: int = 60, char: str = '─') -> str:
        """Create a separator line"""
        return self.border(char * width)
    
    def show_theme_preview(self):
        """Display a preview of the current theme"""
        preview = f"""
{self.header('Theme Preview')}

{self.list_item('Primary color: ' + self.colorize('Sample text', 'primary'), '🎨')}
{self.list_item('Secondary color: ' + self.colorize('Sample text', 'secondary'), '🎨')}
{self.list_item('Accent color: ' + self.colorize('Sample text', 'accent'), '🎨')}
{self.list_item('Success message: ' + self.success('Operation completed'), '✅')}
{self.list_item('Error message: ' + self.error('Something went wrong'), '❌')}
{self.list_item('Warning message: ' + self.warning('Be careful'), '⚠️')}
{self.list_item('Info message: ' + self.info('Information'), 'ℹ️')}

{self.box('This is a sample box with some content to demonstrate the theming system. It shows how text looks inside a bordered container.')}

{self.separator()}
{self.footer('Theme: ' + self.theme.value.upper())}
"""
        print(preview)

def get_available_themes() -> list:
    """Get list of available themes"""
    return [theme.value for theme in Theme]

def select_theme_interactive() -> Theme:
    """Interactive theme selection"""
    themes = get_available_themes()
    
    print("\n" + Color.BOLD + Color.CYAN + "Available Terminal Themes:" + Color.RESET)
    print(Color.BRIGHT_BLACK + "=" * 40 + Color.RESET)
    
    for i, theme in enumerate(themes, 1):
        print(f"{Color.CYAN}{i:2d}.{Color.RESET} {Color.BOLD}{theme.title()}{Color.RESET}")
    
    print()
    while True:
        try:
            choice = input(Color.BOLD + "Select theme (1-8) [default: 1]: " + Color.RESET).strip()
            if not choice:
                choice = 1
            else:
                choice = int(choice)
            
            if 1 <= choice <= len(themes):
                selected_theme = Theme(themes[choice - 1])
                print(f"\n{Color.GREEN}✓{Color.RESET} Selected theme: {Color.BOLD}{selected_theme.value.title()}{Color.RESET}")
                return selected_theme
            else:
                print(f"{Color.RED}✗{Color.RESET} Invalid choice. Please select 1-{len(themes)}.")
        except (ValueError, KeyboardInterrupt):
            print(f"\n{Color.YELLOW}→{Color.RESET} Using default theme: Serenium")
            return Theme.SERENIUM

# ASCII Art for different themes
ASCII_ART = {
    Theme.SERENIUM: """
    ╦ ╦╔═╗╔╗ ╔╦╗╔═╗╔╦╗╔═╗
    ║║║║╣ ╠╩╗ ║ ║╣  ║ ╚═╗
    ╚╩╝╚═╝╚═╝ ╩ ╚═╝ ╩ ╚═╝
    """,
    Theme.CYBERPUNK: """
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    █ ▄▄▄▄▄ █▀█ █▄█ █▄▄▄▄▄ █
    █ █   █ █▀▀▀█▀▀ █   █ █
    █ █▄▄▄█ █   █   █▄▄▄█ █
    █▄▄▄▄▄▄▄█▄▄▄█▄▄▄█▄▄▄▄▄█
    """,
    Theme.OCEAN: """
    ˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
    ~   O C E A N   T H E M E   ~
    ˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜˜
    """,
    Theme.FOREST: """
    🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
    🌲   F O R E S T   🌲
    🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
    """,
    Theme.SUNSET: """
    🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅
    🌅   S U N S E T   🌅
    🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅🌅
    """,
    Theme.NEON: """
    ⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡
    ⚡    N E O N    ⚡
    ⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡
    """,
    Theme.MATRIX: """
    01001000 01100101 01101100 01101100 01101111
    01001101 01100001 01110100 01110010 01101001
    01011001 00100000 01010100 01101000 01100101
    """
}

def get_ascii_art(theme: Theme) -> str:
    """Get ASCII art for theme"""
    return ASCII_ART.get(theme, ASCII_ART[Theme.SERENIUM])
