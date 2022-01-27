"""
Main Scratch2Python file

This file is used to run Scratch2Python and build the project based on the data given by s2p_unpacker.py

Copyright (C) 2022 Secret-chest and other contributors (copyright applies for all files)

This program is free software: you can redistribute it and/or modify
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
import io
import s2p_unpacker
from s2p_unpacker import *
import shutil
import scratch
import pygame
import time
import tkinter as tk
from pathlib import Path
# import zipfile as zf
from tkinter.messagebox import *
import os
from targetSprite import TargetSprite

VERSION = "M10 (development version)"

# Change this to a different project file
PROJECT = "projects/Garden-rock.sb3"

# Get project data and create sprites
targets, project = s2p_unpacker.sb3_unpack(PROJECT)
allSprites = pygame.sprite.Group()
for t in targets:
    sprite = TargetSprite(t)
    t.sprite = sprite
    allSprites.add(sprite)
    sprite.setXy(t.x, t.y)

# Start tkinter for showing some popups, and hide main window
wn = tk.Tk()
wn.withdraw()

# Start Pygame, load fonts and print a debug message
pygame.init()
font = pygame.font.SysFont("pygame.font.get_default_font()", 16)
fontXl = pygame.font.SysFont("pygame.font.get_default_font()", 36)
scratch.startProject()

# Create paused message
paused = fontXl.render("Paused (Press F6 to resume)", 1, (0, 0, 0))
pausedWidth, pausedHeight = fontXl.size("Paused (Press F6 to resume)")

# Set player size and fps
HEIGHT = 360
WIDTH = 480
FPS = 30
KEY_DELAY = 500

# Get project name and set icon
projectName = Path(PROJECT).stem
icon = pygame.image.load("icon.svg")

# Create project player and window
display = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(projectName + " - Scratch2Python" + " " + VERSION)
pygame.display.set_icon(icon)

# Set running state
projectRunning = True
isPaused = False

# Initialize clock
clock = pygame.time.Clock()

# Clear display
display.fill((255, 255, 255))

# Create block execution queues
toExecute = []
eventHandlers = []
doScreenRefresh = False

# Start green flag scripts
for s in allSprites:
    for _, block in s.target.blocks.items():
        if block.opcode == "event_whenflagclicked":
            nextBlock = scratch.execute(block, block.target.sprite)
            # Error-proof by checking if the scripts are not empty
            if nextBlock:
                # Add the next block to the queue
                toExecute.append(nextBlock)
        elif block.opcode.startswith("event_"):  # add "when I start as a clone" code later
            eventHandlers.append(block)

# Mainloop
while projectRunning:
    # Process Pygame events
    for event in pygame.event.get():
        # Window quit (ALT-F4 / X button)
        if event.type == pygame.QUIT:
            projectRunning = False

        # Debug and utility functions
        keysRaw = pygame.key.get_pressed()
        keys = set(k for k in scratch.KEY_MAPPING.values() if keysRaw[k])

        if pygame.K_F1 in keys:  # Help
            showinfo("Work in progress", "Help not currently available")
        if pygame.K_F2 in keys:  # Scratch2Python options
            showinfo("Work in progress", "Options coming soon")
        if pygame.K_F3 in keys:  # Debug
            showinfo("Debug", "Showing debug info. Check the terminal.")
            print(project.namelist())
        if pygame.K_F4 in keys:  # Project info
            showinfo("Work in progress", "Project info coming soon")
        if pygame.K_F5 in keys:  # Extract
            confirm = askokcancel("Extract", "Extract all project files?")
            if confirm:
                print("DEBUG: Extracting project")
                shutil.rmtree("assets")
                os.mkdir("assets")
                project.extractall("assets")
        if pygame.K_F6 in keys:  # Pause
            isPaused = not isPaused

    display.fill((255, 255, 255))
    if toExecute:
        for block in toExecute:
            print("DEBUG: Block", block.blockID, "in queue")
    if not isPaused:
        for e in eventHandlers:
            if e.opcode == "event_whenkeypressed" and keys:
                nextBlock = scratch.execute(block, block.target.sprite, keys)
                if nextBlock:
                    if isinstance(nextBlock, list):
                        nextBlocks.extend(nextBlock)
                    else:
                        nextBlocks.append(nextBlock)
        while toExecute and not doScreenRefresh:
            # Run blocks
            nextBlocks = []
            for block in toExecute:
                if block.waiting:
                    print("DEBUG: Block execution time is", block.executionTime, "delay is", block.timeDelay)
                    block.executionTime += clock.get_time()
                    if block.executionTime >= block.timeDelay:
                        block.waiting = False
                        if block.opcode.startswith("event"):
                            block.blockRan = False
                        else:
                            block.blockRan = True
                        nextBlocks.append(block.target.blocks[block.next])
                        block.executionTime, block.timeDelay = 0, 0
                        print("DEBUG: Wait period ended")
                if not block.blockRan:
                    nextBlock = scratch.execute(block, block.target.sprite, keys)
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
    wn.update()
    doScreenRefresh = False
    clock.tick(FPS)
pygame.quit()
