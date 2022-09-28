"""
Main Scratch2Python file

This file is used to run Scratch2Python and build the project based on the data given by sb3Unpacker.py

Copyright (C) 2022 Secret-chest and other contributors (copyright applies for all files)

Scratch2Python is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "v0.2.0"
__author__ = "Secret-chest"

import tkinter.simpledialog
from platform import system, platform
import os
import sys
import i18n
import config
import time

if system() == "Linux":
    OS = "linux"
elif system() == "Darwin":
    OS = "macOSX"
elif system() == "Windows":
    OS = "windows"
else:
    OS = "unknown"

i18n.set("locale", config.language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")
_ = i18n.t

if not config.enableTerminalOutput:
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
if not config.enableDebugMessages:
    sys.stderr = open(os.devnull, "w")

print(_("start", version=__version__, os=OS))

if OS == "windows":
    os.environ["path"] += r";cairolibs"

if OS == "unknown":
    print(_("unrecognized-os", platform=platform(), url="https://github.com/Secret-chest/scratch2python/issues"),
          file=sys.stderr)

if not config.pygameWelcomeMessage:
    sys.stdout = open(os.devnull, "w")
import sb3Unpacker
import downloader
from sb3Unpacker import *
import shutil
import scratch
import pygame
import tkinter as tk
from pathlib import Path
from tkinter.messagebox import *
from tkinter.simpledialog import *
from tkinter import filedialog
from targetSprite import TargetSprite

sys.stdout = sys.__stdout__

if not config.enableTerminalOutput:
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
if not config.enableDebugMessages:
    sys.stderr = open(os.devnull, "w")


# Define a dialog class for screen resolution
class SizeDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=widthPrompt).grid(row=0)
        tk.Label(master, text=heightPrompt).grid(row=1)

        self.width = tk.Entry(master)
        self.height = tk.Entry(master)

        self.width.grid(row=0, column=1)
        self.height.grid(row=1, column=1)

        return self.width

    def okPressed(self):
        self.setWidth = self.width.get()
        self.setHeight = self.height.get()
        self.destroy()

    def cancelPressed(self):
        self.destroy()

    def buttonbox(self):
        self.okButton = tk.Button(self, text=okText, width=5, command=self.okPressed)
        self.okButton.pack(side="left")
        cancelButton = tk.Button(self, text=cancelText, width=5, command=self.cancelPressed)
        cancelButton.pack(side="right")
        self.bind("<Return>", lambda event: self.okPressed())
        self.bind("<Escape>", lambda event: self.cancelPressed())


# Start tkinter for showing some popups, and hide main window
mainWindow = tk.Tk()
mainWindow.withdraw()

# Clean the cache if limit is exceeded
downloads = sorted(Path("./download/").iterdir(), key=os.path.getmtime)
downloadsToDelete = downloads[config.cachedDownloads:]
for f in downloadsToDelete:
    os.remove(f)

# Get project file name based on options and arguments
if len(sys.argv) > 1:
    setProject = sys.argv[1]
else:
    if config.testMode:
        if not config.projectFileName.endswith(".sb3"):
            if "http" not in config.projectFileName\
               or "https" not in config.projectFileName:
                setProject = downloader.downloadByID(config.projectFileName, "./download")
            else:
                setProject = downloader.downloadByURL(config.projectFileName, "./download")
        else:
            setProject = config.projectFileName
    else:
        fileTypes = [(_("sb3-desc"), ".sb3"), (_("all-files-desc"), ".*")]
        setProject = filedialog.askopenfilename(parent=mainWindow,
                                                initialdir=os.getcwd(),
                                                title=_("choose-project-title"),
                                                filetypes=fileTypes)

# Get project data and create sprites
targets, project = sb3Unpacker.sb3Unpack(setProject)
allSprites = pygame.sprite.Group()
for t in targets:
    sprite = TargetSprite(t)
    t.sprite = sprite
    allSprites.add(sprite)
    sprite.setXy(t.x, t.y)
    sprite.setCostume(sprite.target.currentCostume)

# Start pygame and load fonts
pygame.mixer.pre_init(22050, -16, 1, 12193)

pygame.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 16)
fontXl = pygame.font.SysFont(pygame.font.get_default_font(), 36)

# Create paused message
paused = fontXl.render(_("paused-message", keybind="F6"), True, (0, 0, 0))
pausedWidth, pausedHeight = fontXl.size(_("paused-message", keybind="F6"))

# Set player size and key delay
HEIGHT = config.projectScreenHeight
WIDTH = config.projectScreenWidth

# Get project name and set icon
projectName = Path(setProject).stem
icon = pygame.image.load("icon.svg")

# Create project player and window
display = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(_("window-title", projectName=projectName, s2pVersionString="Scratch2Python " + __version__))
pygame.display.set_icon(icon)

# Extract if requested
if config.extractOnProjectRun:
    print(_("extracting-project"))
    shutil.rmtree("assets")
    os.mkdir("assets")
    project.extractall("assets")

# Set running state
projectRunning = True
isPaused = False

# Initialize clock
clock = pygame.time.Clock()

# Clear display
display.fill((255, 255, 255))

doScreenRefresh = False

# Define some strings
widthPrompt = _("screen-width-prompt") + " "
heightPrompt = _("screen-height-prompt") + " "
okText = _("ok")
cancelText = _("cancel")
playerClosedText = _("player-closed")
nothingToSeeHere = _("nothing-to-see-here")
helpTitle, extractTitle, projectInfoTitle, fpsTitle, screenTitle = _("help-title"), _("extract-title"), _("project-info-title"), _("fps-title"), _("screen-title")
fpsPrompt, fpsMessage = _("fps-prompt"), _("fps-message")
extractPrompt, extractMessage = _("extract-prompt"), _("extracting-project")
screenMessage = _("screen-message")
redrawMessage = _("redraw-message")


# Start project
toExecute = []
eventHandlers = []
print(_("project-started"))
blocksHash = {}

# Start green flag scripts
for s in allSprites:
    for _, block in s.target.blocks.items():
        blocksHash[block.blockID] = block
        if block.opcode == "event_whenflagclicked":
            nextBlock = scratch.execute(block, block.target.sprite, set(), set())
            # Error-proof by checking if the scripts are not empty
            if nextBlock:
                # Add the next block to the queue
                toExecute.append(nextBlock)
        elif block.opcode.startswith("event_"):  # add “when I start as a clone” code later
            eventHandlers.append(block)
s = None  # so we don't mix it up

# Prepare keyboard
pygame.key.set_repeat(config.keyDelay, 1000 // config.projectMaxFPS)
keyEvents = set()

# Mainloop
framesCounter = 0
while projectRunning:
    print(f"Counter is {framesCounter}")
    framesCounter += 1

    # Process Pygame events
    for event in pygame.event.get():
        # Window quit (ALT-F4 / X button / etc.)
        if event.type == pygame.QUIT:
            print(playerClosedText)
            projectRunning = False

        # Debug and utility functions
        # TODO why are the events correct here but not in execute???
        keyEvents = set()
        if event.type == pygame.KEYDOWN:
            keyEvents.add(event.key)
            print("new key event", time.time_ns())
        keysRaw = pygame.key.get_pressed()
        keys = set(k for k in scratch.KEY_MAPPING.values() if keysRaw[k])

        if pygame.K_F1 in keys:  # Help
            showinfo(helpTitle, nothingToSeeHere)
        if pygame.K_F4 in keys:  # Project info
            showinfo(projectInfoTitle, nothingToSeeHere)
        if pygame.K_F3 in keys:  # Extract
            confirm = askokcancel(extractTitle, extractPrompt)
            if confirm:
                print(extractMessage)
                shutil.rmtree("assets")
                os.mkdir("assets")
                project.extractall("assets")
        if pygame.K_F6 in keys:  # Pause
            isPaused = not isPaused
        if pygame.K_F7 in keys:  # Set new FPS
            # Open dialog
            newFPS = askinteger(title=fpsTitle, prompt=fpsPrompt)
            if newFPS is not None:
                print(fpsMessage, newFPS)
                config.projectMaxFPS = newFPS
            pygame.key.set_repeat(1000, 1000 // config.projectMaxFPS)
        if pygame.K_F8 in keys:  # Set new screen resolution
            try:
                # Open special dialog
                dialog = SizeDialog(mainWindow, title=screenTitle)
                if dialog.setWidth and dialog.setHeight:
                    config.projectScreenWidth = int(dialog.setWidth)
                    config.projectScreenHeight = int(dialog.setHeight)

                # Redraw everything and recalculate sprite operations
                display = pygame.display.set_mode([config.projectScreenWidth, config.projectScreenHeight])
                HEIGHT = config.projectScreenHeight
                WIDTH = config.projectScreenWidth
                scratch.refreshScreenResolution()
                for s in allSprites:
                    s.setXy(s.x, s.y)
                print(screenMessage, str(HEIGHT) + "x" + str(WIDTH))
            except ValueError:
                pass
        if pygame.K_F5 in keys:  # Redraw
            # Redraw everything and recalculate sprite operations
            display = pygame.display.set_mode([config.projectScreenWidth, config.projectScreenHeight])
            HEIGHT = config.projectScreenHeight
            WIDTH = config.projectScreenWidth
            scratch.refreshScreenResolution()
            for s in allSprites:
                s.setXy(s.x, s.y)
            print(redrawMessage)

    display.fill((255, 255, 255))
    if toExecute:
        for block in toExecute:
            pass
    if not isPaused:
        print(len(eventHandlers))
        for e in eventHandlers:
            if e.opcode == "event_whenkeypressed" and keyEvents and not e.blockRan:
                e.blockRan = True
                print(keyEvents)
                nextBlock = scratch.execute(e, e.target.sprite, keys, keyEvents)
                if nextBlock and isinstance(nextBlock, list):
                    toExecute.extend(nextBlock)
                elif nextBlock:
                    toExecute.append(nextBlock)

            if e.opcode == "event_whenkeypressed":
                # print(s.target.blocks, e.script)
                if not e.script or all(blocksHash[b].blockRan for b in e.script):
                    e.blockRan = False
                    for b in e.script:
                        blocksHash[b].blockRan = False
        while toExecute and not doScreenRefresh:
            # Run blocks
            nextBlocks = []
            for block in toExecute:
                if block.waiting:
                    block.executionTime += clock.get_time()
                    if block.executionTime >= block.timeDelay:
                        block.waiting = False
                        block.blockRan = True
                        nextBlocks.append(block.target.blocks[block.next])
                        block.executionTime, block.timeDelay = 0, 0
                if not block.blockRan and not block.opcode.startswith("event"):  # TODO add broadcast blocks
                    nextBlock = scratch.execute(block, block.target.sprite, keys, keyEvents)
                    if not block.next \
                       and block.top \
                       and block.top.opcode.startswith("event") \
                       and block.top.opcode != "event_whenflagclicked":
                        waitFinished = False
                        waitFinishedFor = set()
                        for b in block.top.script:
                            if not blocksHash[b].waiting and not blocksHash[b].blockRan:
                                waitFinishedFor.add(blocksHash[b])
                        if len(waitFinishedFor) == len(block.top.script):
                            block.top.blockRan = False
                    if nextBlock:
                        if isinstance(nextBlock, list):
                            nextBlocks.extend(nextBlock)
                        else:
                            nextBlocks.append(nextBlock)
                if block.screenRefresh:
                    doScreenRefresh = True
            toExecute = list(set(nextBlocks))

        allSprites.draw(display)
        allSprites.update()
    else:
        display.blit(paused, (WIDTH // 2 - pausedWidth // 2, WIDTH // 2 - pausedHeight // 2))
    pygame.display.flip()
    mainWindow.update()
    doScreenRefresh = False
    clock.tick(config.projectMaxFPS)
pygame.quit()
