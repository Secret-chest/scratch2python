"""
Main Scratch2Python file

This file is used to run Scratch2Python and build the project based on the data given by s2p_unpacker.py

Copyright (C) 2021 Secret-chest

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
# Remember to install pygame and CairoSVG
import s2p_unpacker
from s2p_unpacker import *
import shutil
import scratch
import pygame
import tkinter as tk
# import zipfile as zf
from tkinter.messagebox import *
import os
from targetSprite import TargetSprite

version = "M5"

# Prepare project file
allSprites = pygame.sprite.Group()
projectToLoad = "projects/forever.sb3"  # change this to load a different project
targets, currentBgFile, project = s2p_unpacker.sb3_unpack(projectToLoad)
for t in targets:
    sprite = TargetSprite(t)
    t.sprite = sprite
    allSprites.add(sprite)
wn = tk.Tk()  # Start tkinter for popups
wn.withdraw()  # Hide main tkinter window
pygame.init()  # Start pygame
scratch.startProject()
# Set player size
HEIGHT = 360
WIDTH = 480
projectName = projectToLoad[:-4]  # Set the project name for use in the titlebar
icon = pygame.image.load("icon.png")
display = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(projectName + " - Scratch2Python")
pygame.display.set_icon(icon)
currentBg = scratch.loadSvg(currentBgFile)
# currentBgFile = project.read(target["costumes"][target["currentCostume"]]["md5ext"])
projectRunning = True

clock = pygame.time.Clock()
display.fill((255, 255, 255))
toExecute = []

for s in allSprites:
    for _, block in s.target.blocks.items():
        if block.opcode == "event_whenflagclicked":
            print("DEBUG: Running opcode", block.opcode)
            print("DEBUG: Running ID", block.blockID)
            nextBlock = scratch.execute(block, block.target.sprite)
            if nextBlock:
                toExecute.append(nextBlock)

scratch.setBackground(currentBg, display)
while projectRunning:
    for event in pygame.event.get():
        # Window quit (ALT-F4 / X button)
        if event.type == pygame.QUIT:
            projectRunning = False
        # Some controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F1]:  # Help
            showinfo("Work in progress", "Help not currently available")
        if keys[pygame.K_F2]:  # Scratch2Python options
            showinfo("Work in progress", "Options coming soon")
        if keys[pygame.K_F3]:  # Debug
            showinfo("Debug", "Showing debug info. Check the terminal.")
            print(project.namelist())
        if keys[pygame.K_F4]:  # Project info
            showinfo("Work in progress", "Project info coming soon")
        if keys[pygame.K_F5]:  # Project info
            confirm = askyesno("Extract", "Extract all project files?")
            if confirm:
                print("DEBUG: Extracting project")
                shutil.rmtree("assets")
                os.mkdir("assets")
                project.extractall("assets")
    display.fill((255, 255, 255))
    scratch.setBackground(currentBg, display)
    # Move all sprites to current position and direction, run blocks
    nextBlocks = []
    for block in toExecute:
        if block.waiting:
            print("DEBUG: Block execution time is", block.executionTime, "delay is", block.timeDelay)
            block.executionTime += clock.get_time()
            if block.executionTime >= block.timeDelay:
                block.waiting = False
                block.blockRan = True
                nextBlocks.append(block.target.blocks[block.next])
                block.executionTime, block.timeDelay = 0, 0
                print("DEBUG: Wait period ended")
        if not block.blockRan:
            print("DEBUG: Running opcode", block.opcode)
            print("DEBUG: Running ID", block.blockID)
            nextBlock = scratch.execute(block, block.target.sprite)
            if nextBlock:
                print("DEBUG: Next block is", nextBlock.opcode)
                nextBlocks.append(nextBlock)
    toExecute = nextBlocks[:]
    allSprites.draw(display)
    allSprites.update()
    pygame.display.flip()
    wn.update()
    clock.tick(30)
pygame.quit()
