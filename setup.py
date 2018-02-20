import sys
from setuptools import setup
from cx_Freeze import setup, Executable

base = "Win32GUI"

executables = [Executable('track_fish.py', base=base)]
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

setup(
    name='fish-trainer',
    packages='',
    url='',
    license='',
    author='Owner',
    author_email='',
    options = '',
    version = '1.0',
    description = 'first build',
    executables = 'tracker_client/track_fish.py'
)
