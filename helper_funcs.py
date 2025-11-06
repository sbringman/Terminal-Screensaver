#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filename: helper_functions.py
Author: Samuel Bringman
Date: 2025-11-03
Version: 1.0
Description: This script provides the functions that allow engine.py
to run.
License: MIT License
"""

import numpy as np
import random

def set_rules(rule_set: str):
    """ Returns lists for the number of living neighbors required 
    for a dead cell to come to life and the number of living neighbors 
    required for a living cell to stay alive.

    Parameters
    ----------
    rule_set : str
        The rules for the game, in the format 'B###/S###'. As an example rule,
        B3/S23 means that cells are (B)orn if they have 3 living neighbors and
        (S)tay alive if they have 2 or 3 living neighbors

    Returns
    -------
    born_rule : list
        A list of the numbers of living neighbors required for a dead cell come to life
    
    stay_rule : list
        A list of the numbers of living neighbors required for a living cell 
        to stay alive
        
    """

    born_rule = []
    stay_rule = []

    born, stay = rule_set.split("/")

    for i in range(1, len(born)):
        born_rule.append(int(born[i]))
    
    for i in range(1, len(stay)):
        stay_rule.append(int(stay[i]))

    return born_rule, stay_rule


def sum_around(row: int, col: int, w_array: np.array):
    """ Returns the number of living neighbors of a cell

    Parameters
    ----------
    row, col : int
        The row and column location of the cell

    w_array : np.array
        The game world

    Returns
    -------
    sum : int
        The number of living neighbors
        
    """
    row_max = len(w_array[0])
    col_max = len(w_array)

    sum = w_array[(col-1)%col_max][(row-1)%row_max] + w_array[col%col_max][(row-1)%row_max] + w_array[(col+1)%col_max][(row-1)%row_max] + \
            w_array[(col-1)%col_max][row%row_max] + 0 + w_array[(col+1)%col_max][row%row_max] + \
            w_array[(col-1)%col_max][(row+1)%row_max] + w_array[(col)%col_max][(row+1)%row_max] + w_array[(col+1)%col_max][(row+1)%row_max]
    return sum


def update_world(w_array: np.array, b_rule: list, s_rule: list):
    """ Updates the game world according to the given rules

    Parameters
    ----------
    w_array : np.array
        The game world

    b_rule : list
        A list of allowable numbers of neighbors that will cause a dead cell
        to come to life
    
    s_rule : list
        A list of allowable numbers of neighbors that will cause a living cell
        to stay alive

    Returns
    -------
    new_world : int
        The updated game world
        
    """

    row_length = len(w_array[0])
    col_length = len(w_array)

    new_world = np.zeros_like(w_array)

    for col in range(col_length):
        for row in range(row_length):
            num_neighbors = sum_around(row, col, w_array)
            if w_array[col][row] == 0 and num_neighbors in b_rule:
                new_world[col][row] = 1
            elif w_array[col][row] == 1:
                if num_neighbors in s_rule:
                    new_world[col][row] = 1
                else:
                    new_world[col][row] = 0
    return new_world


def make_output_string(w_array: np.array):
    """ Makes an output string to be printed onto the screen to display 
    the game world

    Parameters
    ----------
    w_array : np.array
        The game world

    Returns
    -------
    output : str
        The formatted string to be printed out onto the screen
        
    """

    row_length = len(w_array[0])
    col_length = len(w_array)

    output = ""

    cell_char = "O"

    for col in range(col_length):
        for row in range(row_length):
            if w_array[col][row] == 0:
                output += f" "
            else:
                output += f"{cell_char}"
    
    return output


def reset_cells(world_array):
    """ Resets the game world to a random state

    Parameters
    ----------
    w_array : np.array
        The game world

    Returns
    -------
    world_array : str
        The new random game world
        
    """
    num_cols = len(world_array)
    num_rows = len(world_array[0])

    for col in range(num_cols):
        for row in range(num_rows):
            if random.random() < 0.5:
                world_array[col][row] = 1
            else:
                world_array[col][row] = 0
    
    return world_array


def resize_world(world_array, nts):
    """ Resizes the game world to fit a different terminal screen size.
    It cuts off parts of the world that are now out of bounds and creates
    dead cells to fill the new spaces that were not covered by the world before
    the size change.

    Parameters
    ----------
    w_array : np.array
        The game world
    
    nts : os.terminal_size object
        The new terminal size

    Returns
    -------
    world_array : str
        The adjusted game world
        
    """
    max_row = max(len(world_array), nts[1]-2)
    max_col = max(len(world_array[0]), nts[0])
    min_col = min(len(world_array[0]), nts[0])
    min_row = min(len(world_array), nts[1]-2)

    # Create a blank array to fit the new terminal
    new_world_array = np.zeros((nts[1]-3, nts[0]))

    # Put as much of the old world onto the new world as will fit
    # Cut out parts that would go out of the new bounds, and add in
    # dead cells where the new world is larger than the old world
    for row in range(min_row):
        strip = world_array[row][:max_col]
        fit_strip = np.zeros(nts[0])
        for col in range(min_col):
            fit_strip[col] = strip[col]

        new_world_array[row] = fit_strip

    # Pass off the new world to the correct array
    return new_world_array