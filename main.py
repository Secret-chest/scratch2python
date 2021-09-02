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


def load_svg(filename):
    new_bites = cairosvg.svg2png(url=filename)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)


def load_svg_bytes(svg_bytes):
    new_bites = cairosvg.svg2png(bytestring=svg_bytes)
    byte_io = io.BytesIO(new_bites)
    return pygame.image.load(byte_io)


def render(sprite, x, y):
    # convert Scratch coordinates into Pygame coordinates
    final_x = x + WIDTH // 2 - sprite.get_width() // 2
    final_y = HEIGHT // 2 - y - sprite.get_height() // 2
    display.blit(sprite, (final_x, final_y))


def set_background(bg):
    render(bg, 0, 0)


# prepare project file
targets, current_bg_file, project = s2p_unpacker.sb3_unpack("ifonedgebounce.sb3")  # change this to load a different project
wn = tk.Tk()
wn.withdraw()
# when needed
# wn.deiconify()
pygame.init()
scratch.startProject()
HEIGHT = 360
WIDTH = 480
project_name = "Scratch2Python"
icon = pygame.image.load("icon.png")
display = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(project_name)
pygame.display.set_icon(icon)
current_bg = load_svg_bytes(current_bg_file)
# current_bg_file = project.read(target["costumes"][target["currentCostume"]]["md5ext"])
project_running = True


while project_running:
    for event in pygame.event.get():
        # Window quit (ALT-F4 / X button)
        if event.type == pygame.QUIT:
            project_running = False
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
    # move all sprites to current position and direction
    set_background(current_bg)
    for target in targets:
        render(load_svg_bytes(target.costumes[target.currentCostume].file), target.x, target.y)
        for _, block in target.blocks.items():
            if not block.blockRan and block.opcode == "event_whenflagclicked":
                print("DEBUG: Running opcode", block.opcode)
                print("DEBUG: Running ID", block.blockID)
                print("DEBUG: Next ID", block.next)
                nextBlock = target.blocks[block.next]
                print("DEBUG: Next opcode", nextBlock.opcode)
                block.blockRan = True
    pygame.display.flip()
    wn.update()
pygame.quit()
