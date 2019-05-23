import os
import requests
import sys
import ctypes

from utils import app as beautifuldiscord


class Installer:
    def __init__(self):
        self.version = "1.0.4"
        self.line = "----------------------------------------"
        self.name = "BeautifulDiscord"
        self.theme_url = "https://raw.githubusercontent.com/AlexFlipnote/Discord_Theme/master/autotheme.css"
        self.choices = [1, 2, 3, 4, 5, 6, 7, 8]

        self.location = os.path.expanduser("~/Documents/DiscordTheme/")
        self.filename = "autotheme.css"

        self.main_script()

    def printer(self, *lines: str):
        """ Make it easier to print multiple lines """
        return print(
            "\n".join(lines)
        )

    def print_options(self):
        """ The lovely main menu (start of script print) """
        self.printer(
            f"Welcome to BeautifulDiscord install tool | {self.version}",
            self.line,
            "1 - Install BeautifulDiscord with pre-made theme",
            "2 - Install BeautifulDiscord from scratch",
            "3 - [Advance] Install BeautifulDiscord with pre-made theme on custom path",
            "4 - [Advance] Install BeautifulDiscord from scratch on custom path",
            "5 - Enable theme after Discord update (Sometimes Discord disables the theme, idk)",
            "6 - Enable theme after Discord update [Custom path]",
            "7 - Uninstall theme from Discord",
            "8 - Close this window",
            "\nPre-made theme provided by: https://github.com/AlexFlipnote/Discord_Theme",
            self.line,
            "Enter the number choice you want and press enter"
        )

    def write_theme_file(self, custom_path: str = None, download_theme: bool = True):
        """ Write the .css file inside Documents folder """
        if download_theme:
            file = self.get_file(self.theme_url)
        else:
            file = b"/* Add your own CSS inside here */"

        if not file:
            print("Failed to inject file, got nothing from downloader...")
            return False

        if custom_path:
            location = custom_path
        else:
            location = self.location

        try:
            with open(location + self.filename, "wb") as f:
                f.write(file)
            return True
        except Exception as e:
            print(f"I have no clue what happened, but I failed to make a theme file...\nDEBUG: {e}")
            return False

    def inject_theme(self, custom_path: str = None):
        """ Inject the theme powered by BeautifulDiscord """
        if custom_path:
            path = f'{custom_path + self.filename}'
        else:
            path = f'{self.location + self.filename}'

        exists = os.path.isfile(path)
        if not exists:
            return False

        beautifuldiscord.main(f"--css '{path}'")

        return self.printer(
            self.line,
            f"Done adding theme, you can edit it at this location:",
            path
        )

    def create_default_path(self):
        if not os.path.exists(self.location):
            os.makedirs(self.location)
            print("Created a new folder in your Documents called: DiscordTheme")

    def get_file(self, url: str):
        """ Download file from URL """
        print("Downloading file...")
        try:
            file = requests.get(url).content
            print("Download completed!")
            return file
        except Exception:
            print("Failed to download file...")
            return False

    def choose(self):
        """ Choice validation in numbers """
        userchoice = input("> ")
        try:
            num = int(userchoice)
        except ValueError:
            return False

        if num in self.choices:
            return num
        else:
            return False

    def define_path(self):
        userchoice = input("Paste in the path you wish to use: ")

        if userchoice.endswith("\\"):
            path = str(userchoice)
        else:
            path = f"{userchoice}\\"

        try:
            with open("custom_path.txt", "w") as f:
                f.write(path)
            return path
        except Exception:
            return False

    def read_custom_path(self):
        try:
            with open("custom_path.txt", "r") as f:
                return f.readline()
        except Exception:
            return False

    def main_script(self):
        """ Starts with __init__ """
        ctypes.windll.kernel32.SetConsoleTitleW(f"BeautifulDiscord install tool | {self.version}")
        while True:
            self.print_options()
            userchoice = self.choose()
            if userchoice:
                break

        if userchoice == 1:
            self.create_default_path()
            self.write_theme_file()
            self.inject_theme()
        if userchoice == 2:
            self.create_default_path()
            self.write_theme_file(download_theme=False)
            self.inject_theme()
        if userchoice == 3:
            path = self.define_path()
            self.write_theme_file(custom_path=path)
            self.inject_theme(custom_path=path)
        if userchoice == 4:
            path = self.define_path()
            self.write_theme_file(custom_path=path, download_theme=False)
            self.inject_theme(custom_path=path)

        if userchoice == 5:
            inject = self.inject_theme()
            if not inject:
                self.printer(
                    "Could not find the CSS file to inject..",
                    "Are you sure you have the correct path?"
                )

        if userchoice == 6:
            path = self.read_custom_path()
            if not path:
                print("I couldn't find a file called: custom_path.txt")
            else:
                inject = self.inject_theme(custom_path=path)
                if not inject:
                    self.printer(
                        "Could not find the CSS file to inject..",
                        "Are you sure you have the correct path inside custom_path.txt?"
                    )

        if userchoice == 7:
            beautifuldiscord.main("--revert")
        if userchoice == 8:
            sys.exit(0)

        input("\nYou can now close this window")


if __name__ == '__main__':
    try:
        Installer()
    except KeyboardInterrupt:
        print("Stopping process...")
