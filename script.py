import pystray
import pyperclip
import pyautogui
import time
from PIL import Image, ImageDraw
from threading import Thread
from pynput import mouse

# Configuration
config = {
    'delay': 2,
    'typing_speed': 0.01,
    'auto_paste': True,
    'trigger_mode': 'click'  # 'delay' or 'click'
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

def paste_on_click(icon):
    """Wait for the next mouse click, then type clipboard content after 100ms"""
    icon.icon = create_icon_image('yellow')

    click_detected = False

    def on_click(x, y, button, pressed):
        nonlocal click_detected
        if pressed:
            click_detected = True
            return False  # Stop the listener

    # Listen for the next mouse click
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    if click_detected:
        icon.icon = create_icon_image('green')
        time.sleep(0.1)  # 100ms delay after click
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            pyautogui.write(clipboard_content, interval=config['typing_speed'])

    icon.icon = create_icon_image('blue')

def on_clicked(icon, item):
    """Handle tray icon click — dispatches based on trigger mode"""
    if config['trigger_mode'] == 'click':
        Thread(target=paste_on_click, args=(icon,), daemon=True).start()
    else:
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

def set_trigger_mode(icon, mode):
    """Set the trigger mode for pasting"""
    config['trigger_mode'] = mode
    label = 'Click + 100ms' if mode == 'click' else f'Timed ({config["delay"]}s)'
    icon.notify(f'Trigger mode: {label}')

def setup_tray():
    """Setup and run the system tray icon"""
    icon_image = create_icon_image()
    
    menu = pystray.Menu(
        pystray.MenuItem('Paste', on_clicked, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Trigger Mode', pystray.Menu(
            pystray.MenuItem(
                'Click + 100ms',
                lambda icon, item: set_trigger_mode(icon, 'click'),
                checked=lambda item: config['trigger_mode'] == 'click'
            ),
            pystray.MenuItem(
                'Timed Delay',
                lambda icon, item: set_trigger_mode(icon, 'delay'),
                checked=lambda item: config['trigger_mode'] == 'delay'
            )
        )),
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
