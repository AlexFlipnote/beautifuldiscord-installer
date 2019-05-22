import os
import requests
import sys

from utils import app as beautifuldiscord


class Installer:
    def __init__(self):
        self.line = "----------------------------------------"
        self.name = "BeautifulDiscord"
        self.theme_url = "https://raw.githubusercontent.com/AlexFlipnote/Discord_Theme/master/autotheme.css"
        self.choices = [1, 2, 3, 4, 5]

        saveDir = os.path.expanduser("~/Documents/DiscordTheme/")
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
            print("Created a new folder in your Documents called: DiscordTheme")

        self.location = saveDir
        self.filename = "autotheme.css"

        self.main_script()

    def printer(self, *lines):
        return print(
            "\n".join(lines)
        )

    def print_options(self):
        self.printer(
            "Welcome to BeautifulDiscord install tool",
            self.line,
            "1 - Install BeautifulDiscord with pre-made theme (AlexFlipnote/Discord_Theme)",
            "2 - Install BeautifulDiscord from scratch",
            "3 - Enable theme after Discord update (Sometimes Discord disables the theme, idk)",
            "4 - Uninstall theme from Discord",
            "5 - Close this window",
            self.line,
            "Enter the number choice you want and press enter"
        )

    def write_theme_file(self, download_theme: bool = True):
        if download_theme:
            file = self.get_file(self.theme_url)
        else:
            file = b"/* Add your own CSS inside here */"

        if not file:
            print("Failed to inject file, got nothing from downloader...")

        try:
            with open(self.location + self.filename, "wb") as f:
                f.write(file)
            return True
        except Exception as e:
            print(f"I have no clue what happened, but I failed to make a theme file...\nDEBUG: {e}")
            return False

    def inject_theme(self):
        exists = os.path.isfile(f'{self.location + self.filename}')
        if not exists:
            return False

        beautifuldiscord.main(
            f"--css '{self.location + self.filename}'"
        )

        return self.printer(
            self.line,
            f"Done adding theme, you can edit it at this location:",
            str(self.location + self.filename)
        )

    def get_file(self, url: str):
        print("Downloading file...")
        try:
            file = requests.get(url).content
            print("Download completed!")
            return file
        except Exception:
            print("Failed to download file...")
            return False

    def choose(self):
        userchoice = input("> ")
        try:
            num = int(userchoice)
        except ValueError:
            return False

        if num in self.choices:
            return num
        else:
            return False

    def main_script(self):
        while True:
            self.print_options()
            userchoice = self.choose()
            if userchoice:
                break

        if userchoice == 1:
            self.write_theme_file()
            self.inject_theme()
        if userchoice == 2:
            self.write_theme_file(download_theme=False)
            self.inject_theme()
        if userchoice == 3:
            inject = self.inject_theme()
            if not inject:
                print("Could not find the CSS file to inject, please try option 1 or 2 instead.")
        if userchoice == 4:
            beautifuldiscord.main("--revert")
        if userchoice == 5:
            sys.exit(0)

        input("\nYou can now close this window")


if __name__ == '__main__':
    try:
        Installer()
    except KeyboardInterrupt:
        print("Stopping process...")
