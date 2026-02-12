import pystray
import pyperclip
import pyautogui
import time
from PIL import Image, ImageDraw
from threading import Thread

# Configuration
config = {
    'delay': 2,
    'typing_speed': 0.01,
    'auto_paste': True
}

def create_icon_image(color='blue'):
    """Create a simple icon for the system tray"""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill=color)
    return image

def paste_clipboard(icon):
    """Wait configured delay then type the clipboard content"""
    icon.icon = create_icon_image('green')
    time.sleep(config['delay'])
    clipboard_content = pyperclip.paste()
    if clipboard_content:
        pyautogui.write(clipboard_content, interval=config['typing_speed'])
    icon.icon = create_icon_image('blue')

def on_clicked(icon, item):
    """Handle tray icon click"""
    Thread(target=paste_clipboard, args=(icon,), daemon=True).start()

def set_delay(icon, seconds):
    """Set the delay before pasting"""
    config['delay'] = seconds
    icon.notify(f'Delay set to {seconds} seconds')

def set_typing_speed(icon, speed):
    """Set the typing speed"""
    config['typing_speed'] = speed
    speed_name = {0.001: 'Fast', 0.01: 'Normal', 0.05: 'Slow'}
    icon.notify(f'Typing speed set to {speed_name.get(speed, "Custom")}')

def toggle_auto_paste(icon, item):
    """Toggle auto paste on clipboard change"""
    config['auto_paste'] = not item.checked
    status = 'enabled' if config['auto_paste'] else 'disabled'
    icon.notify(f'Auto paste {status}')

def show_clipboard(icon, item):
    """Show current clipboard content"""
    content = pyperclip.paste()
    preview = content[:50] + '...' if len(content) > 50 else content
    icon.notify(f'Clipboard: {preview}' if content else 'Clipboard is empty')

def setup_tray():
    """Setup and run the system tray icon"""
    icon_image = create_icon_image()
    
    menu = pystray.Menu(
        pystray.MenuItem('Paste', on_clicked, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Delay', pystray.Menu(
            pystray.MenuItem('1 second', lambda icon, item: set_delay(icon, 1)),
            pystray.MenuItem('2 seconds', lambda icon, item: set_delay(icon, 2)),
            pystray.MenuItem('3 seconds', lambda icon, item: set_delay(icon, 3)),
            pystray.MenuItem('5 seconds', lambda icon, item: set_delay(icon, 5))
        )),
        pystray.MenuItem('Typing Speed', pystray.Menu(
            pystray.MenuItem('Fast', lambda icon, item: set_typing_speed(icon, 0.001)),
            pystray.MenuItem('Normal', lambda icon, item: set_typing_speed(icon, 0.01)),
            pystray.MenuItem('Slow', lambda icon, item: set_typing_speed(icon, 0.05))
        )),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Show Clipboard', show_clipboard),
        pystray.MenuItem('Auto Paste', toggle_auto_paste, checked=lambda item: config['auto_paste']),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Exit', lambda icon, item: icon.stop())
    )
    
    icon = pystray.Icon('clipboard_paster', icon_image, 'Clipboard Paster', menu)
    icon.run()

if __name__ == '__main__':
    setup_tray()
