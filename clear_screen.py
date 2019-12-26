"""
Clears the terminal screen regardless of OS
"""
import platform
import os


def clear_screen():
    os.system("cls" if platform.system().lower() == "windows" else "clear")
