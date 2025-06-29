# Automatic Wallpaper Changer

A Python script that automatically changes your Windows desktop wallpaper every 5 minutes with minimalistic images fetched from various online sources.

## Features

- **Automatic wallpaper rotation** every 5 minutes
- **Multiple image sources** with fallback support
- **Silent background operation** with optional debug mode
- **Minimalistic wallpapers** from curated sources
- **Instance management** - prevents multiple copies from running
- **Comprehensive logging** for troubleshooting
- **Clean shutdown** handling

## Requirements

- **Windows OS** (uses Windows API for wallpaper setting)
- **Python 3.6+**
- **Internet connection** for fetching wallpapers

## Dependencies

Install required packages:

```bash
pip install requests psutil
```

## Installation

1. **Clone or download** this repository
2. **Install dependencies** using pip
3. **Update the batch file** with your actual directory path
4. **Run the script** using one of the methods below

## Usage

### Method 1: Direct Python execution

```bash
# Run with visible output
python wallpaper_changer.py

# Run with debug information
python wallpaper_changer.py --debug

# Run silently (no console output)
python wallpaper_changer.py --silent
```

### Method 2: Using the batch launcher (Recommended)

1. **Edit `launch_wallpaper_changer.bat`**:
   - Replace `YOUR_USERNAME` with your actual Windows username
   - Update the full path to where you placed the script

2. **Run the batch file**:
   - Double-click `launch_wallpaper_changer.bat`
   - The script will run completely hidden in the background

## Image Sources

The script fetches wallpapers from:

1. **Primary**: `https://minimalistic-wallpaper.demolab.com/?random`
2. **Fallback sources**:
   - Picsum Photos (Lorem Picsum)
   - Unsplash minimal/abstract collections

## Files Created

The script creates several files in its directory:

- `current_wallpaper.jpg` - The current wallpaper image
- `wallpaper_changer.log` - Activity log with timestamps
- `wallpaper_changer.pid` - Process ID file (for instance management)

## Configuration

### Changing the interval

To modify the wallpaper change interval, edit line 165 in `wallpaper_changer.py`:

```python
time.sleep(300)  # 300 seconds = 5 minutes
```

### Adding custom image sources

Add URLs to the `fallback_urls` list in the `get_fallback_image()` method:

```python
fallback_urls = [
    "https://picsum.photos/1920/1080",
    "https://your-custom-source.com/image",
    # Add more sources here
]
```

## Stopping the Script

- **If running visibly**: Press `Ctrl+C`
- **If running in background**: 
  - Use Task Manager to end the `pythonw.exe` process
  - Or run the script again (it will automatically kill existing instances)

## Troubleshooting

### Check the log file
The script creates detailed logs in `wallpaper_changer.log`. Common issues:

**No internet connection**: The script will log network errors and retry with fallback sources.

**Permission errors**: Make sure the script directory is writable.

**Wallpaper not changing**: Check if the image file is being created and that Windows can access it.

### Debug mode
Run with `--debug` flag to see real-time output:

```bash
python wallpaper_changer.py --debug
```

### Manual testing
Test wallpaper setting manually:

```python
from wallpaper_changer import WallpaperChanger
changer = WallpaperChanger()
changer.change_wallpaper()
```

## System Requirements

- **OS**: Windows 7/8/10/11
- **Python**: 3.6 or higher
- **RAM**: Minimal (< 50MB)
- **Storage**: ~5MB for images and logs
- **Network**: Periodic internet access for downloading images

## Contributing

Feel free to:
- Report bugs or issues
- Suggest new wallpaper sources
- Improve error handling
- Add new features

## License

This project is open source. Feel free to modify and distribute.

## Startup Integration

To run automatically at Windows startup:

1. **Win + R** → type `shell:startup`
2. **Copy** `launch_wallpaper_changer.bat` to the startup folder
3. **Restart** your computer

The wallpaper changer will now start automatically when Windows boots.

---

**Note**: This script is designed specifically for Windows. For other operating systems, the wallpaper-setting mechanism would need to be adapted.
