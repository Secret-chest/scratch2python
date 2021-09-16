"""
Main Scratch2Python file

This file is used to run Scratch2Python and build the project based on the data given by s2p_unpacker.py
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


# Prepare project file
allSprites = pygame.sprite.Group()
projectToLoad = "wait_gotoxy.sb3"  # change this to load a different project
targets, currentBgFile, project = s2p_unpacker.sb3_unpack(projectToLoad)
for t in targets:
    allSprites.add(TargetSprite(t))
wn = tk.Tk()  # Start tkinter for popups
wn.withdraw()  # Hide main tkinter window
# when needed
# wn.deiconify()
pygame.init()  # Start pygame
scratch.startProject()
# Set player size
HEIGHT = 360
WIDTH = 480
projectName = projectToLoad[:-4] # Set the project name
icon = pygame.image.load("icon.png")
display = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(projectName + " - Scratch2Python" )
pygame.display.set_icon(icon)
currentBg = scratch.loadSvg(currentBgFile)
# currentBgFile = project.read(target["costumes"][target["currentCostume"]]["md5ext"])
projectRunning = True

display.fill((255, 255, 255))
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
    for s in allSprites:
        for _, block in s.target.blocks.items():
            if not block.blockRan:
                print("DEBUG: Running opcode", block.opcode)
                print("DEBUG: Running ID", block.blockID)
                if block.next:
                    print("DEBUG: Next ID", block.next)
                    nextBlock = s.target.blocks[block.next]
                    print("DEBUG: Next opcode", nextBlock.opcode)
                else:
                    print("DEBUG: Last block")
                scratch.execute(block, s)
                block.blockRan = True
    # for target in targets:
    #     scratch.render(scratch.loadSvg(target.costumes[target.currentCostume].file), target.x * 2, target.y * 2, target.direction, display)
    #     for _, block in target.blocks.items():
    #         if not block.blockRan:
    #             print("DEBUG: Running opcode", block.opcode)
    #             print("DEBUG: Running ID", block.blockID)
    #             if block.next:
    #                 print("DEBUG: Next ID", block.next)
    #                 nextBlock = target.blocks[block.next]
    #                 print("DEBUG: Next opcode", nextBlock.opcode)
    #             else:
    #                 print("DEBUG: Last block")
    #             scratch.execute(block, target)
    #             block.blockRan = True
    allSprites.draw(display)
    allSprites.update()
    pygame.display.flip()
    wn.update()
pygame.quit()
