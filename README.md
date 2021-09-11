
![Logo](s2p.svg)

<img src="https://img.shields.io/github/languages/top/Secret-chest/Scratch2Python?labelColor=546e7a&color=26c6da&logo=python&logoColor=26c6da&style=flat-square"> <img alt="GitHub" src="https://img.shields.io/github/license/Secret-chest/Scratch2Python?style=flat-square&labelColor=546e7a&color=ffa000"> <img alt="GitHub issues" src="https://img.shields.io/github/issues/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub milestones" src="https://img.shields.io/github/milestones/open/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&style=flat-square"><a href="https://github.com/Secret-chest/scratch2python/network"> <img alt="GitHub forks" src="https://img.shields.io/github/forks/Secret-chest/scratch2python?labelColor=546e7a&color=ffc107&logo=github&logoColor=ffffff&style=flat-square"></a>

# Scratch2Python
Scratch2Python is a Python program that converts Scratch projects to Pygame code.
## Requirements
Run the following commands:
### Windows
    pip install pygame
    pip install CairoSVG
### Linux
    sudo pip3 install pygame
    sudo pip3 install CairoSVG
## Files
The files in the project are:
* `main.py` - run Scratch2Python, mainloop.
* `s2p_unpacker.py`  - unpack sb3 files and generate a dictionary from the project.json file
* `scratch.py` - contains various Scratch-related functions
* classes
  * `target.py`
  * `block.py`
  * `costume.py`
  * `monitor.py`
  * `sound.py`
  * `variable.py`
* many demo sb3 files
* README
## Naming conventions
Always use `mixedCase` (first letter is always lowercase) for variable and function names.
Use `Uppercase` for class names.

Note: Use underscores if the name may become unclear. For example: use `sb3_unpack` instead of `sb3Unpack`
## How to use 
Assuming that you installed all necessary requirements, place your sb3 files in the scratch2python folder where main.py is located.
Then, change the projectToLoad variable to your project file.
Now, just run `python3 main.py` and the project will start!
