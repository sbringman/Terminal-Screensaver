#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filename: engine.py
Author: Samuel Bringman
Date: 2025-11-03
Version: 1.0
Description: This script runs a game of life simulation from the
terminal.
License: MIT License
"""

import os
import copy
import numpy as np
from inputimeout import inputimeout, TimeoutOccurred
from colorama import Fore, Back, Style
import argparse
import random
import helper_funcs as hf

# This is the argument parser, which takes command line arguments
parser = argparse.ArgumentParser(
                    prog='Game of Life Terminal Screensaver',
                    description='This program creates a game of life simulation on the terminal screen.'
                    )

parser.add_argument('--start_file', help='Name of starting position file')
parser.add_argument('--rule', default='B3/S23', help='The rules for the game, in the format B###/S###')
parser.add_argument('--rave', action='store_true', help='Add color strobing')

args = parser.parse_args()

# Get the terminal size
terminal_size = os.get_terminal_size()

# Create the game world
world_array = np.zeros((terminal_size[1] - 3, terminal_size[0]))

# Either load an initial position or start with a random set
if args.start_file:
    start_file = args.start_file
    init_pos = np.loadtxt(f"./StartPositions/{start_file}.csv",delimiter=",",dtype=int)

    for position in init_pos:

        # Set cells that are inside of the boundaries,
        # but don't set cells outside the boundaries
        try:
            world_array[position[1]][position[0]] = 1
        except IndexError:
            pass

else:
    # Randomly set the cells as either alive or dead
    for row in range(terminal_size[1] - 3):
        for col in range(terminal_size[0]):
            if random.random() < 0.5:
                world_array[row][col] = 1
            else:
                world_array[row][col] = 0


born_rule, stay_rule = hf.set_rules(args.rule)


# These are for checking on whether the world has stopped evolving
world_minus_1 = None
world_minus_2 = None

pos_fore_colors = [
    Fore.RESET,
    Fore.BLACK,
    Fore.RED,
    Fore.GREEN,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.WHITE,
]

fore_color_index = 0

reset_countdown = 20

# Will stop on its own accord after one million iterations
for i in range(1_000_000):

    # Clear everything
    os.system('clear')

    # Produce the output image
    print(pos_fore_colors[fore_color_index])
    out_string = hf.make_output_string(world_array)

    print(out_string)

    # Check for stopping input
    try:
        user_input = inputimeout("Press return to stop: ", timeout=0.5)
    except TimeoutOccurred:
        user_input = "Keep Going!"
    
    if user_input != "Keep Going!":
        break
    
    # Check for resizing
    new_terminal_size = os.get_terminal_size()

    # If the terminal size has changed, resize the world
    if new_terminal_size != terminal_size:
        world_array = hf.resize_world(world_array, new_terminal_size)
        terminal_size = new_terminal_size
    

    # Save the previous worlds
    if i > 2:
        world_minus_2 = copy.deepcopy(world_minus_1)

    world_minus_1 = copy.deepcopy(world_array)
    world_array = hf.update_world(world_array, born_rule, stay_rule)

    # Check if the world is trapped in a 1 or 2 step cycle
    if i > 4 and (world_array.shape == world_minus_1.shape and world_array.shape == world_minus_2.shape):
        if (np.allclose(world_array, world_minus_1) or np.allclose(world_array, world_minus_2)):
            reset_countdown -= 1
    
    # Reset everything if the simulation has been stuck in a 
    # 1 or 2 move cycle for 20 turns
    if reset_countdown == 0:
        world_array = hf.reset_cells(world_array)
        reset_countdown = 20

    # Apply color change effects
    if args.rave:
        fore_color_index += 1
        fore_color_index = fore_color_index % 8

# Reset colors so the user doesn't end up with a weird terminal
print(Fore.RESET)
print(Back.RESET)

