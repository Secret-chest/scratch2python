
![Logo](s2p.svg)
# Scratch2Python
Scratch2Python is a Python program that converts Scratch projects to Pygame code.
## Requirements
Run the following commands:
### Windows
    pip install pygame
    pip install CairoSVG
    pip install PySide6
    pip install qt-material
### Linux
    sudo pip3 install pygame
    sudo pip3 install CairoSVG
    sudo pip3 install PySide6
    sudo pip3 install qt-material
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
