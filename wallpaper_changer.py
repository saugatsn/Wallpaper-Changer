import requests
import os
import time
import ctypes
import sys
import psutil
from pathlib import Path
import json

class WallpaperChanger:
    def __init__(self):
        self.script_dir = Path(__file__).resolve().parent
        self.wallpaper_filename = self.script_dir / "current_wallpaper.jpg"
        self.log_file = self.script_dir / "wallpaper_changer.log"
        self.pid_file = self.script_dir / "wallpaper_changer.pid"
        self.api_url = "https://minimalistic-wallpaper.demolab.com/?random"
        self.current_wallpaper = None
        self.debug_mode = '--debug' in sys.argv

        # Clean up existing log and wallpaper
        self.cleanup_previous_files()

    def cleanup_previous_files(self):
        """Delete previous image and log if present"""
        try:
            if self.log_file.exists():
                self.log_file.unlink()
            if self.wallpaper_filename.exists():
                self.wallpaper_filename.unlink()
        except Exception as e:
            print(f"Error cleaning previous files: {e}")

    def log(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except:
            pass
        if self.debug_mode:
            print(log_message)

    def kill_existing_instances(self):
        current_pid = os.getpid()
        script_name = "wallpaper_changer.py"
        killed = 0

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['pid'] != current_pid and proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if script_name in cmdline and 'python' in cmdline.lower():
                            self.log(f"Killing existing instance: PID {proc.info['pid']}")
                            proc.kill()
                            killed += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if killed > 0:
                self.log(f"Killed {killed} existing instance(s)")
            else:
                self.log("No existing instances found")

        except Exception as e:
            self.log(f"Error checking for existing instances: {e}")

    def create_pid_file(self):
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
            self.log(f"Created PID file: {self.pid_file}")
        except Exception as e:
            self.log(f"Error creating PID file: {e}")

    def cleanup_pid_file(self):
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
                self.log("Removed PID file")
        except Exception as e:
            self.log(f"Error removing PID file: {e}")

    def get_image_url_from_api(self):
        try:
            self.log("Fetching image URL from API...")
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            })

            response = session.get(self.api_url, timeout=15, allow_redirects=True)
            self.log(f"API Response Status: {response.status_code}")
            self.log(f"Final URL after redirects: {response.url}")

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                self.log(f"Content-Type: {content_type}")

                if 'image' in content_type:
                    return response.url, response.content
                else:
                    try:
                        data = response.json()
                        self.log(f"JSON Response: {data}")
                        if 'url' in data:
                            img_response = session.get(data['url'], timeout=15)
                            if img_response.status_code == 200:
                                return data['url'], img_response.content
                    except:
                        pass
                    self.log(f"Response content preview: {response.text[:200]}...")
            return None, None

        except requests.RequestException as e:
            self.log(f"Network error fetching from API: {e}")
            return None, None
        except Exception as e:
            self.log(f"Unexpected error fetching from API: {e}")
            return None, None

    def get_fallback_image(self):
        fallback_urls = [
            "https://picsum.photos/1920/1080",
            "https://source.unsplash.com/1920x1080/?minimal",
            "https://source.unsplash.com/1920x1080/?abstract"
        ]

        for url in fallback_urls:
            try:
                self.log(f"Trying fallback URL: {url}")
                response = requests.get(url, timeout=15, allow_redirects=True)
                if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
                    self.log(f"Fallback successful: {url}")
                    return response.url, response.content
            except:
                continue
        return None, None

    def save_image(self, image_content, source_url):
        try:
            with open(self.wallpaper_filename, 'wb') as f:
                f.write(image_content)
            self.log(f"Saved wallpaper: {self.wallpaper_filename.name} ({len(image_content)} bytes)")
            return str(self.wallpaper_filename)
        except Exception as e:
            self.log(f"Error saving image: {e}")
            return None

    def set_wallpaper(self, image_path):
        try:
            abs_path = os.path.abspath(image_path)
            self.log(f"Setting wallpaper: {abs_path}")

            if not os.path.exists(abs_path):
                self.log("Wallpaper file does not exist")
                return False

            if os.path.getsize(abs_path) == 0:
                self.log("Wallpaper file is empty")
                return False

            SPI_SETDESKWALLPAPER = 20
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                abs_path,
                3
            )

            if result:
                self.log("Wallpaper set successfully")
                self.current_wallpaper = abs_path
                return True
            else:
                error_code = ctypes.windll.kernel32.GetLastError()
                self.log(f"Failed to set wallpaper. Windows error code: {error_code}")
                return False

        except Exception as e:
            self.log(f"Error setting wallpaper: {e}")
            return False

    def change_wallpaper(self):
        self.log("=" * 50)
        self.log("Starting wallpaper change process")

        image_url, image_content = self.get_image_url_from_api()
        if not image_content:
            self.log("Main API failed, trying fallback...")
            image_url, image_content = self.get_fallback_image()

        if not image_content:
            self.log("All image sources failed")
            return False

        image_path = self.save_image(image_content, image_url)
        if not image_path:
            self.log("Failed to save image")
            return False

        return self.set_wallpaper(image_path)

    def run(self):
        self.log("Wallpaper Changer started")
        self.log(f"Debug mode: {self.debug_mode}")
        self.log(f"Log file: {self.log_file}")

        self.kill_existing_instances()
        self.create_pid_file()

        try:
            if not self.change_wallpaper():
                self.log("Initial wallpaper change failed")
            while True:
                self.log("Waiting 5 minutes for next change...")
                time.sleep(300)
                self.change_wallpaper()
        except KeyboardInterrupt:
            self.log("Stopped by user")
        except Exception as e:
            self.log(f"Unexpected error: {e}")
            import traceback
            self.log(f"Traceback: {traceback.format_exc()}")
        finally:
            self.cleanup_pid_file()
            self.log("Wallpaper changer terminated")

if __name__ == "__main__":
    if '--silent' in sys.argv and '--debug' not in sys.argv:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    changer = WallpaperChanger()
    changer.run()
