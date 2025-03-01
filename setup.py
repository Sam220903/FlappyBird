import sys
import os

from cx_Freeze import setup, Executable

files = ['game_objects', 'assets', 'utils', 'game.py', 'config']

exe = Executable(script="main.py",
                 base="Win32GUI")

setup(name="SlappyBird",
        version="0.1",
        description="A Flappy Bird clone",
        options={"build_exe": {"include_files": files}},
        executables=[exe])
