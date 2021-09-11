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
import cairosvg
import io
import json
import time


# Basic functions
# Those functions are used for basic sprite tasks. They will probably be moved to scratch.py.
# Load SVG in pygame
def loadSvg(svg_bytes):
    newBites = cairosvg.svg2png(bytestring=svg_bytes)
    byteIo = io.BytesIO(newBites)
    return pygame.image.load(byteIo)


# Render a sprite at its coordinates
def render(sprite, x, y, direction):
    # upscale sprite
    sprite = pygame.transform.scale(sprite, (sprite.get_width() * 2, sprite.get_height() * 2))
    # set direction
    sprite = pygame.transform.rotate(sprite, 90 - direction)
    # convert Scratch coordinates into Pygame coordinates
    finalX = x + WIDTH // 2 - sprite.get_width() // 2
    finalY = HEIGHT // 2 - y - sprite.get_height() // 2
    display.blit(sprite, (finalX, finalY))


# Set the stage background
def setBackground(bg):
    render(bg, 0, 0, 90)


# Prepare project file
projectToLoad = "gotoxy2.sb3"  # change this to load a different project
targets, currentBgFile, project = s2p_unpacker.sb3_unpack(projectToLoad)
wn = tk.Tk()  # Start tkinter for popups
wn.withdraw()  # Hide main tkinter window
allSprites = pygame.sprite.Group()
# when needed
# wn.deiconify()
pygame.init()  # Start pygame
scratch.startProject()
# Set player size
HEIGHT = 720
WIDTH = 960
projectName = projectToLoad[:-4] # Set the project name
icon = pygame.image.load("icon.png")
display = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(projectName + " - Scratch2Python" )
pygame.display.set_icon(icon)
currentBg = loadSvg(currentBgFile)
# currentBgFile = project.read(target["costumes"][target["currentCostume"]]["md5ext"])
projectRunning = True

display.fill((255, 255, 255))
setBackground(currentBg)
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
    setBackground(currentBg)
    # Move all sprites to current position and direction, run blocks
    for target in targets:
        render(loadSvg(target.costumes[target.currentCostume].file), target.x * 2, target.y * 2, target.direction)
        for _, block in target.blocks.items():
            if not block.blockRan:
                print("DEBUG: Running opcode", block.opcode)
                print("DEBUG: Running ID", block.blockID)
                if block.next:
                    print("DEBUG: Next ID", block.next)
                    nextBlock = target.blocks[block.next]
                    print("DEBUG: Next opcode", nextBlock.opcode)
                else:
                    print("DEBUG: Last block")
                scratch.execute(block, target)
                block.blockRan = True
    allSprites.draw(display)
    allSprites.update()
    pygame.display.flip()
    wn.update()
pygame.quit()
