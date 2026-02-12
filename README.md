# Clipboard Paster

A lightweight Windows system tray application that pastes clipboard content with keyboard simulation.

## Features

- **One-Click Paste**: Left-click the tray icon to paste clipboard content
- **Configurable Delay**: Choose 1-5 second delay before pasting
- **Adjustable Typing Speed**: Fast, Normal, or Slow typing simulation
- **Visual Feedback**: Icon changes color (blue → green) during operation
- **Clipboard Preview**: View current clipboard content from the menu

## Installation

1. Clone this repository:
```cmd
git clone https://github.com/yourusername/clipboard-paster.git
cd clipboard-paster
```

2. Install dependencies:
```cmd
pip install -r requirements.txt
```

## Usage

Run the script:
```cmd
python script.py
```

The application will appear in your system tray with a blue square icon.

### Controls

- **Left-click**: Activate paste (waits configured delay, then types clipboard content)
- **Right-click**: Open menu with options

### Menu Options

- **Paste**: Manually trigger paste operation
- **Delay**: Set wait time (1, 2, 3, or 5 seconds)
- **Typing Speed**: Adjust simulation speed (Fast/Normal/Slow)
- **Show Clipboard**: Preview current clipboard content
- **Auto Paste**: Toggle auto-paste feature (coming soon)
- **Exit**: Close the application

## How It Works

1. Click the tray icon
2. Icon turns green indicating activation
3. Wait for configured delay (default: 2 seconds)
4. Application simulates keyboard typing of clipboard content
5. Icon returns to blue when complete

The delay gives you time to click where you want the text to appear.

## Requirements

- Python 3.6+
- Windows OS
- Dependencies listed in `requirements.txt`

## License

MIT
