import os
import requests

from utils import app as beautifuldiscord


class Installer:
    def __init__(self):
        self.line = "----------------------------------------"
        self.name = "BeautifulDiscord"
        self.theme_url = "https://raw.githubusercontent.com/AlexFlipnote/Discord_Theme/master/autotheme.css"
        self.choices = [1, 2, 3]

        saveDir = os.path.expanduser("~/Documents/DiscordTheme/")
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

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
            "1 - Download theme and install BeautifulDiscord",
            "2 - Enable theme after Discord update",
            "3 - Uninstall theme from Discord",
            self.line,
            "Enter the number choice you want and press enter"
        )

    def write_theme_file(self):
        file = self.get_file(self.theme_url)
        if not file:
            print("Failed to inject file, got nothing from downloader...")

        try:
            with open(self.location + self.filename, "wb") as f:
                f.write(file)
            return True
        except Exception:
            print("I have no clue what happened, but I failed to make a theme file...")
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
            choice = self.choose()
            if choice:
                break

        if choice == 1:
            self.write_theme_file()
            self.inject_theme()
        if choice == 2:
            inject = self.inject_theme()
            if not inject:
                print("Could not find the CSS file to inject, please try option 1 instead.")
        if choice == 3:
            beautifuldiscord.main("--revert")

        input("\nYou can now close this window")


Installer()
