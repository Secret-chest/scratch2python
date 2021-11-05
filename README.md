
![Logo](s2p.svg)

<img src="https://img.shields.io/github/languages/top/Secret-chest/Scratch2Python?labelColor=546e7a&color=26c6da&logo=python&logoColor=26c6da&style=flat-square"> <img alt="GitHub" src="https://img.shields.io/github/license/Secret-chest/Scratch2Python?style=flat-square&labelColor=546e7a&color=ffa000"> <img alt="GitHub issues" src="https://img.shields.io/github/issues/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&logo=github&logoColor=ffffff&style=flat-square"> <img alt="GitHub milestones" src="https://img.shields.io/github/milestones/open/Secret-chest/Scratch2Python?labelColor=546e7a&color=64dd17&style=flat-square"><a href="https://github.com/Secret-chest/scratch2python/network"> <img alt="GitHub forks" src="https://img.shields.io/github/forks/Secret-chest/scratch2python?labelColor=546e7a&color=ffc107&logo=github&logoColor=ffffff&style=flat-square"></a>

# Scratch2Python
Scratch2Python is a Python program that converts Scratch projects to Pygame code.

## Requirements
Install from requirements.txt (Scratch2Python also needs Python 3.6 or newer).

## Docs
[Read the wiki here](https://github.com/Secret-chest/scratch2python/wiki).

## Files
The table below lists all files in the project.

| File              | Description                                                                                      |
|-------------------|--------------------------------------------------------------------------------------------------|
| `main.py`         | Build the project based on the data, run blocks, listen to events                                |
| `s2p_unpacker.py` | Generate a dictionary from project.json, put objects in it and set them to the correct values    |
| `scratch.py`      | Scratch emulator, runs blocks on request, contains various Scratch-related functions             |
| `target.py`       | Sprite class                                                                                     |
| `block.py`        | Block class                                                                                      |
| `costume.py`      | Costume class                                                                                    |
| `monitor.py`      | Variable monitor class (currently unused)                                                        | 
| `sound.py`        | Sound class (currently unused)                                                                   |
| `variable.py`     | Variable class (currently unused)                                                                |
| `targetSprite.py` | Targets as pygame sprites                                                                        |
| `projects/*.sb3`  | Projects used for testing                                                                        |
| `requirements.txt`| List of requirements (install from this file)                                                    |
| `README.md`       | This file                                                                                        |
| `LICENSE`         | GPL-3.0 license                                                                                  |

## Naming conventions
Always use `mixedCase` (first letter is always lowercase) for variable, object, parameter, file, function and method names.
Use `CamelCase` (first letter is uppercase) for class names.

Note: Use underscores if the name may become unclear. For example: use `sb3_unpack` instead of `sb3Unpack`

## How to use 
Assuming that you installed all necessary requirements, place your sb3 files somewhere accesible, or in the Scratch2Python folder. You can use an absolute or relative path.
Then, change the projectToLoad variable to your project file.
Now, just run `python3 main.py` and the project will start!
