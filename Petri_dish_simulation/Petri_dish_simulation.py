# -*- coding: utf-8 -*-
# Autor: Jiří Harvalík
# Author: Jiri Harvalik

from __future__ import annotations
import tkinter as tk
from time import time
from random import randint, shuffle, uniform
from math import pow, log10, floor
from statistics import median, mean
from itertools import count

ENERGY_UNIT_CONST = 1000
MAX_CELL_SIZE_CONST = 1000
IMAGE_NUMBER_CONST = 280

# trida hex pozice pro snazsi manipulaci
class Hex_Pos():
    """Class for hexagonal coordinate system. Hexagonal coordinates can be added together like arithmetic vectors."""
    row = 0
    col_l = 0
    col_r = 0

    def __init__(self, row:int, col_l:int, col_r:int = None):
        self.row = row
        self.col_l = col_l
        if col_r == None or col_r != - row - col_l:
            self.col_r = - self.row - self.col_l
        else:
            self.col_r = col_r

    def __repr__(self) -> str:
        return "Hex pos: " + str(self.row) + ", " + str(self.col_l) + ", " + str(self.col_r)
    
    def copy(self):
        return Hex_Pos(self.row, self.col_l)

# soucet hex pozic
def sum_hex_pos(pos_1:Hex_Pos, pos_2:Hex_Pos) -> Hex_Pos:
    """Sum of two hexagonal coordinates - one shoud be position, the other vector."""
    return Hex_Pos(pos_1.row + pos_2.row, pos_1.col_l + pos_2.col_l)

# trida pole obsahujici informace o poli
class Hex_Tile():
    """Class containing data about tile in the simulation."""
    hex_pos = Hex_Pos
    occupied = False
    tile_is_wall = False
    tile_energy = int
    max_tile_energy = int
    image = None
    pi_current_image = tk.PhotoImage
    pi_image_changed = False
    pimage_tiles = list[tk.PhotoImage]
    last_updated_image = tk.PhotoImage
    cells_on_tile = list
    canvas = tk.Canvas

    def __init__(self, pimage_tiles = list[tk.PhotoImage], cell_pos:Hex_Pos = Hex_Pos(0, 0, 0), max_tile_energy:int = 100):
        self.max_tile_energy = max_tile_energy
        self.hex_pos = cell_pos
        self.cells_on_tile = []
        self.pimage_tiles = pimage_tiles
        self.pi_current_image = pimage_tiles[0]
        self.tile_energy = max_tile_energy
    
    def __repr__(self) -> str:
        return "Tile: " + str(self.hex_pos.row) + ", " + str(self.hex_pos.col_l) + ", " + str(self.hex_pos.col_r) + " is wall: " + str(self.tile_is_wall) + ", occupied: " + str(self.occupied) + ", energy " + str(self.tile_energy) +  ", cells: " + str(self.cells_on_tile)
    
    def __str__(self) -> str:
        return "Tile: " + str(self.hex_pos.row) + ", " + str(self.hex_pos.col_l) + ", " + str(self.hex_pos.col_r) +  ", energy: " + str(self.tile_energy) + "/" + str(self.max_tile_energy)
    
    # vrati kopii tohoto hex pole
    def copy(self) -> Hex_Tile:
        """Returns new Hex_Tile class with copied values, cells stay same for both instances."""
        new_hex_tile = Hex_Tile(self.hex_pos)
        new_hex_tile.is_wall(self.tile_is_wall)
        new_hex_tile.occupied = self.occupied
        new_hex_tile.cells_on_tile = self.cells_on_tile.copy()
        new_hex_tile.tile_energy = self.tile_energy
        return new_hex_tile
    
    # okopiruje sve hodnoty do jineho pole
    def copy_to(self, other_tile:Hex_Tile):
        """Copies values of this Hex_Tile to other_tile, cells stay same for both instances."""
        other_tile.hex_pos = self.hex_pos
        other_tile.is_wall(self.tile_is_wall)
        other_tile.occupied = self.occupied
        other_tile.cells_on_tile = self.cells_on_tile.copy()
        other_tile.tile_energy = self.tile_energy

    # nastavení pole jako steny
    # rekne, zda je pole stenou
    def is_wall(self, is_wall:bool = None) -> bool:
        """Returns if the tile is a wall, can set the tile to be or stop being a wall."""
        if is_wall != None:
            self.tile_is_wall = is_wall
            if self.tile_is_wall:
                self.occupied = True
            elif self.cells_on_tile:
                self.occupied = True
            else:
                self.occupied = False
        return self.tile_is_wall
    
    def add_cell_to_tile(self, cell:Cell):
        """Adds cell to the tile and sets occupied to True."""
        self.cells_on_tile.append(cell)
        if not self.occupied:
            self.occupied = True

    def remove_cell_from_tile(self, cell:Cell):
        """Removes cell from the tile and if there are no cells left, then sets occupied to False."""
        if not cell in self.cells_on_tile:
            return
        self.cells_on_tile.remove(cell)
        if not self.cells_on_tile:
            self.occupied = False

    def change_energy(self, change) -> int:
        """Changes energy of the tile by given value. 
        If the result is less than 0 or greater than maximal tile energy, then returns excess energy of the change."""
        new_energy = self.tile_energy + change
        self.tile_energy = max(min(new_energy, self.max_tile_energy), 0)
        off = new_energy - self.tile_energy
        return off

    # nastavi obrazek na spravny obrazek
    def update_image(self):
        """Updates image of the tile based on the properties of the tile."""
        if self.cells_on_tile:
            if self.last_updated_image != self.cells_on_tile[0].cell_photo_image:
                self.pi_current_image = self.cells_on_tile[0].cell_photo_image
                self.last_updated_image = self.pi_current_image
                self.pi_image_changed = True
        elif self.tile_is_wall:
            if self.last_updated_image != self.pimage_tiles[-1]:
                self.pi_current_image = self.pimage_tiles[-1]
                self.last_updated_image = self.pi_current_image
                self.pi_image_changed = True
        else: 
            energy_on_level = self.max_tile_energy / 6
            list_pos = floor(self.tile_energy / energy_on_level)
            if self.last_updated_image != self.pimage_tiles[list_pos]:
                self.pi_current_image = self.pimage_tiles[list_pos]
                self.last_updated_image = self.pi_current_image
                self.pi_image_changed = True

# predstavuje virtualni hexagonalni sit
# pri simulaci se pouzivaji dve instance
#   - skutecna sit
#   - virtualni sit
class Hex_Grid():
    """Class containing list of lists of Hex_Tile in hexagonal-like shape and providing operations on the tiles in it."""
    # preddefinovane smery k sousedum v hex siti
    neighbour_directions = [Hex_Pos(1, 0, -1), Hex_Pos(1, -1, 0), Hex_Pos(0, -1, 1), Hex_Pos(-1, 0, 1), Hex_Pos(-1, 1, 0), Hex_Pos(0, 1, -1)]
    grid_diameter = int
    grid_radius = int
    max_tile_energy = int
    hexagonal_tile_grid = list[Hex_Tile]
    floor_tile_list = list[Hex_Tile]
    random_floor_indexes = list[int]
    pimage_tiles = set[tk.PhotoImage]
    cells_in_grid = list
    changed_hex_poses = set[Hex_Pos]

    def __init__(self, grid_radius:int, pimage_tiles:list[tk.PhotoImage], max_tile_energy:int = ENERGY_UNIT_CONST):
        self.pimage_tiles = pimage_tiles
        self.max_tile_energy = max_tile_energy
        self.cells_in_grid = []
        self.floor_tile_list = []
        self.random_floor_indexes = []
        self.changed_hex_poses = set()
        self.grid_radius = grid_radius
        self.grid_diameter = grid_radius * 2
        # generujeme 2D list pro Hex_Tile tak, aby jeden jeho radek byl jeden radek hex site,
        # tedy radky maji odlisné délky, ktere rostou do pulky a pote klesaji
        self.hexagonal_tile_grid = [[None for col in range(self.grid_diameter + 1) if col + row >= self.grid_radius and col + row <= 3 * self.grid_radius] for row in range(self.grid_diameter + 1)]
        # vyplneni 2D listu s Hex_Tile
        last_index = 0
        for row in range(self.grid_diameter + 1):
            # prvni a posledni radek jsou zdi
            if row == 0 or row == self.grid_diameter:
                for col in range(len(self.hexagonal_tile_grid[row])):
                    self.hexagonal_tile_grid[row][col] = Hex_Tile(self.pimage_tiles, self.array_to_hex(row, col), 0)
                    self.hexagonal_tile_grid[row][col].is_wall(True)
            # vyplneni ostatnich radku
            else:
                row_length = len(self.hexagonal_tile_grid[row])
                for col in range(row_length):
                    new_tile = Hex_Tile(self.pimage_tiles, self.array_to_hex(row, col), self.max_tile_energy)
                    self.hexagonal_tile_grid[row][col] = new_tile
                    # neni prvni ani posledni => neni zeď
                    if col > 0 and col < row_length - 1:
                        self.floor_tile_list.append(new_tile)
                        self.random_floor_indexes.append(last_index)
                        last_index += 1
                    # prvni a posledni Hex_Tile v radku jsou zdi
                    else:
                        new_tile.is_wall(True)
                        new_tile.change_energy(-self.max_tile_energy)

    def __repr__(self) -> str:
        return "Grid: diameter " + str(self.grid_diameter) + ", radius " + str(self.grid_radius) + ", cell amount " + str(len(self.cells_in_grid)) 

    # vrati kopii teto hex site s novymi hex poli
    def copy(self) -> Hex_Grid:
        """Creates a copy of the grid with NEW tile instances with SAME content (like cell classes, energy amount, ...)."""
        new_hex_grid = Hex_Grid(self.grid_radius, self.pimage_tiles, self.max_tile_energy)
        new_tile_grid = new_hex_grid.hexagonal_tile_grid
        new_hex_grid.cells_in_grid = self.cells_in_grid.copy()
        # prekopirovani obsahu poli
        for row in range(len(new_tile_grid)):
            for col_l in range(len(new_tile_grid[row])):
                self.hexagonal_tile_grid[row][col_l].copy_to(new_tile_grid[row][col_l])
        return new_hex_grid

    # prekopiruje sve hodnoty a pouze zmenena pole do jine site, vymaze zaznam o zmenenych polich
    def copy_changes_to_and_reset(self, other_grid:Hex_Grid) -> None:
        """Copies CHANGED properties of the grid to another with SAME diameter, similarly as copy()."""
        if self.grid_radius != other_grid.grid_radius:
            raise Exception("Grids have to have same radii.")
        other_grid.cells_in_grid = self.cells_in_grid.copy()
        # prekopirovani obsahu poli
        for tile in self.changed_hex_poses:
            pos = self.hex_to_array(tile)
            self.hexagonal_tile_grid[pos[0]][pos[1]].copy_to(other_grid.hexagonal_tile_grid[pos[0]][pos[1]])
        other_grid.changed_hex_poses = self.changed_hex_poses.copy()
        self.changed_hex_poses = set()

    # prevede pozici v hex siti na pozici pole v seznamu poli
    def hex_to_array(self, hex_pos:Hex_Pos) -> tuple:
        """Returns tuple containing coordinates of the tile with given hex position in the list of lists of tiles.
        Does not take in account, if the such a tile existts."""
        offset_col_l = 0
        # pro tato pole je potreba posunout souradnice
        if hex_pos.row <= self.grid_radius:
            offset_col_l = self.grid_radius - hex_pos.row
        return (hex_pos.row, hex_pos.col_l - offset_col_l)
    
    # prevede pozici pole v seznamu poli na pozici v hex siti
    def array_to_hex(self, arr_row:int, arr_col:int) -> Hex_Pos:
        """Returns class Hex_Pos corresponding to the hexagonal position
        of the tile in the list of lists of tiles at row arr_row and column arr_col.
        Does not take in account, if the such a tile existts."""
        offset_col_l = 0
        # pro tato pole je potreba posunout souradnice
        if arr_row <= self.grid_radius:
            offset_col_l = self.grid_radius - arr_row
        return Hex_Pos(arr_row, arr_col + offset_col_l)

    # vrati sousedy pole v hex siti
    def get_tile_neighbours(self, tile_pos:Hex_Pos) -> list[Hex_Tile]:
        """Returns all neighbouring tile to the tile at tile_pos in the hexagonal grid."""
        neighbours = []
        for dir in self.neighbour_directions:
            n_pos = self.hex_to_array(sum_hex_pos(dir, tile_pos))
            if n_pos[0] >= 0 and n_pos[0] <= len(self.hexagonal_tile_grid) and n_pos[1] >= 0 and n_pos[1] < len(self.hexagonal_tile_grid[n_pos[0]]):
                neighbours.append(self.hexagonal_tile_grid[n_pos[0]][n_pos[1]])
        return neighbours

    # vrati pocet volne sousedy pole v hex siti
    def get_number_free_tile_neighbours(self, tile_pos:Hex_Pos) -> int:
        """Returns number of tiles without cells around the tile at tile_pos in the hexagonal grid."""
        number = 0
        for dir in self.neighbour_directions:
            n_pos = self.hex_to_array(sum_hex_pos(dir, tile_pos))
            if n_pos[0] >= 0 and n_pos[0] <= len(self.hexagonal_tile_grid) and n_pos[1] >= 0 and n_pos[1] < len(self.hexagonal_tile_grid[n_pos[0]]):
                if not self.hexagonal_tile_grid[n_pos[0]][n_pos[1]].occupied:
                    number += 1
        return number
    
    # vrati list volnych poli v hex siti
    def get_free_tiles(self) -> list[Hex_Tile]:
        """Returns list of all tiles, which are not occupied."""
        free_tiles = []
        for tile in self.floor_tile_list:
            if not tile.occupied:
                free_tiles.append(tile)
        return free_tiles
    
    # vrati list volnych hex pozic v hex siti
    def get_free_hex_positions(self) -> list[Hex_Pos]:
        """Returns list of all hex positions of tiles, which are not occupied."""
        free_hex_positions = []
        for tile in self.floor_tile_list:
            if not tile.occupied:
                free_hex_positions.append(tile.hex_pos.copy())
        return free_hex_positions

    # vrati pole v hex siti
    def get_tile_at_hex_pos(self, hex_pos:Hex_Pos) -> Hex_Tile:
        """Returns tile with given hex position, if such tile exists."""
        n_pos = self.hex_to_array(hex_pos)
        if n_pos[0] >= 0 and n_pos[0] < len(self.hexagonal_tile_grid) and n_pos[1] >= 0 and n_pos[1] < len(self.hexagonal_tile_grid[n_pos[0]]):
            return self.hexagonal_tile_grid[n_pos[0]][n_pos[1]]
        return None
    
    def get_energy_from_tile_at_hex_pos(self, hex_pos:Hex_Pos, energy_amount:int) -> Hex_Tile:
        """Returns given amount of energy from the tile at give hex position, and decreases energy of that tile.
        If such a tile do not exists, returns 0. If tile exceeds its lower or upper energy limit, then the returned value
        is changed accordingly. Both positive and negative intput (and according output) is possible."""
        tile = self.get_tile_at_hex_pos(hex_pos)
        if tile:
            self.changed_hex_poses.add(tile.hex_pos)
            off = tile.change_energy(-energy_amount)
            tile.update_image()
            return energy_amount + off
        return 0

    # prida bunku na pole v hex siti
    def add_cell_to_hex_pos(self, cell:Cell, hex_pos:Hex_Pos) -> None:
        """Adds given cell on the tile at given hex position."""
        n_pos = self.hex_to_array(hex_pos)
        if n_pos[0] >= 0 and n_pos[0] <= len(self.hexagonal_tile_grid) and n_pos[1] >= 0 and n_pos[1] < len(self.hexagonal_tile_grid[n_pos[0]]):
            self.cells_in_grid.append(cell)
            list_pos = self.hex_to_array(hex_pos)
            tile = self.hexagonal_tile_grid[list_pos[0]][list_pos[1]]
            tile.add_cell_to_tile(cell)
            tile.update_image()
            self.changed_hex_poses.add(tile.hex_pos)
            cell.hex_pos = hex_pos
            cell.current_tile = tile

    # presune bunku mezi poli v hex siti
    def move_cell_between_tiles(self, cell, hex_pos_end:Hex_Pos) -> None:
        """Removes given cell from its current tile and adds it on tile on the given hex position, if such a tile exists."""
        list_pos_end = self.hex_to_array(hex_pos_end)
        if list_pos_end[0] >= 0 and list_pos_end[0] <= len(self.hexagonal_tile_grid) and list_pos_end[1] >= 0 and list_pos_end[1] < len(self.hexagonal_tile_grid[list_pos_end[0]]): 
            list_pos_start = self.hex_to_array(cell.hex_pos)
            start_tile = self.hexagonal_tile_grid[list_pos_start[0]][list_pos_start[1]]
            end_tile = self.hexagonal_tile_grid[list_pos_end[0]][list_pos_end[1]]
            start_tile.remove_cell_from_tile(cell)
            start_tile.update_image()
            end_tile.add_cell_to_tile(cell)
            end_tile.update_image()
            self.changed_hex_poses.add(start_tile.hex_pos)
            self.changed_hex_poses.add(end_tile.hex_pos)
            cell.hex_pos = hex_pos_end
            cell.current_tile = end_tile

    # smaze bunku z pole v hex siti
    def delete_cell(self, cell:Cell) -> None:
        """Removes given cell from its tile."""
        list_pos = self.hex_to_array(cell.hex_pos)
        tile = self.hexagonal_tile_grid[list_pos[0]][list_pos[1]]
        tile.remove_cell_from_tile(cell)
        tile.update_image()
        self.changed_hex_poses.add(tile.hex_pos)
        self.cells_in_grid.remove(cell)

    # funkce vyhodnoceni pohlcovani bunek na svych polich
    def cell_eating(self, real_grid:Hex_Grid) -> None:
        """Proceeds cell eating of all cell on the same tile."""
        cells_eaten = 0
        for cell in self.cells_in_grid:
            tile = self.get_tile_at_hex_pos(cell.hex_pos)
            tile_cells = tile.cells_on_tile.copy()
            cell_count = len(tile_cells)
            if cell_count < 2:
                continue
            tile_cells.sort(key = lambda cell: cell.size)
            index = cell_count - 1
            while index > 0:
                if tile_cells[index].alive:
                    tile_cells[index].eat_cell(tile_cells[index - 1], real_grid)
                    cells_eaten += 1
                    tile_cells[index - 1] = tile_cells[index]
                index -= 1
        return cells_eaten

    # doplneni energie do policek
    def refill_energy(self, tile_percentage:int, energy_flow:int):
        """Refills given percentage of tiles with the given energy amount. Refilled tiles are chosen randomly."""
        tile_percentage /= 100
        refill_amount = round(len(self.floor_tile_list) * tile_percentage)
        shuffle(self.random_floor_indexes)
        for index in range(len(self.random_floor_indexes)):
            if refill_amount <= 0 :
                break
            refill_amount -= 1 
            tile = self.floor_tile_list[self.random_floor_indexes[index]]
            if tile.tile_energy < self.max_tile_energy:
                tile.change_energy(energy_flow)
                tile.update_image()
                self.changed_hex_poses.add(tile.hex_pos)

    # nalezne a vrati velikosti vsech klastru bunek
    def find_cluster_sizes(self) -> list[int]:
        """Returns list of all cluster sizes. If two neighbours of one cell are also each others neigbours,
        then these three cells belong to one cluster."""
        unknown_cells = set(self.cells_in_grid)
        cell_clusters = {cell.cell_number : i for i, cell in enumerate(self.cells_in_grid, start = 0)} # seznam, jaká buňka je v jakém klastru (indexováno podle cells_in_grid)
        cell_amount = len(self.cells_in_grid)
        
        for cell_index in range(cell_amount):
            cell = self.cells_in_grid[cell_index]
            if cell not in unknown_cells:
                continue
            stack = [cell]
            while stack:
                stack_cell = stack.pop()
                unknown_cells.remove(stack_cell)
                cell_pos = stack_cell.hex_pos
                dir_amount = len(self.neighbour_directions)
                was_cell_before = False
                for index in range(dir_amount + 1):
                    dir =  self.neighbour_directions[index % dir_amount]
                    tile = self.get_tile_at_hex_pos(sum_hex_pos(cell_pos, dir))
                    if tile is None:
                        continue
                    if not tile.cells_on_tile:
                        was_cell_before = False
                        continue
                    neighbour_cell = tile.cells_on_tile[0]
                    if neighbour_cell in unknown_cells and was_cell_before:
                        for search_index in range(cell_amount):
                            if self.cells_in_grid[search_index] == neighbour_cell:
                                if cell_clusters[neighbour_cell.cell_number] != cell_clusters[stack_cell.cell_number]:
                                    cell_clusters[neighbour_cell.cell_number] = cell_clusters[stack_cell.cell_number]
                                    stack.append(neighbour_cell)
                    was_cell_before = True

        cluster_sizes = [0 for _ in range(len(self.cells_in_grid))]
        for cell in self.cells_in_grid:
            cluster_sizes[cell_clusters[cell.cell_number]] += 1
        clusters = []
        for index in range(len(self.cells_in_grid)):
            if cluster_sizes[index] > 1:
                clusters.append(cluster_sizes[index])
        return clusters

# trida pro uchovani aktualniho nastaveni bunek a stavu, vsechny bunky a stavy maji odkaz na jednu jeji instanci
class Cell_And_State_Settings():
    """Class containing informations about settings of the cells."""
    # nastaveni bunek
    energy_gain = round(0.16 * ENERGY_UNIT_CONST) # basic
    base_energy_loss = round(0.014 * ENERGY_UNIT_CONST) # basic 
    around_energy_loss = round(0.1 * ENERGY_UNIT_CONST) # basic
    max_energy_multiplier = 0.3 # advanced
    max_energy_base = round(0.5 * ENERGY_UNIT_CONST) # advanced
    energy_eat_fraction = 0.5 # advanced
    base_size_gain = 0.026 * MAX_CELL_SIZE_CONST # advanced
    around_size_gain = 0 * MAX_CELL_SIZE_CONST # advanced
    size_eat_fraction = 0.333 # advanced
    max_size = MAX_CELL_SIZE_CONST

    # nastaveni stavu
    share_mutation_amount = 20 # advanced
    min_share_per = 0 # advanced
    max_share_per = 99 # advanced

    divide_mutation_amount = 20 # advanced
    min_resources_per = 20 # advanced
    max_resources_per = 80 # advanced
    mutation_chance = 10 # advanced
    strong_mutation_chance = 20 # advanced
    divide_energy_cost = round(0.12 * ENERGY_UNIT_CONST) # advanced
    move_energy_cost = round(0.02 * ENERGY_UNIT_CONST) # advanced
    size_mutation_amount = round(0.1 * MAX_CELL_SIZE_CONST) # advanced
    energy_mutation_amount = round(0.05 * ENERGY_UNIT_CONST) # advanced

# zakladni trida akci
class State_Action():
    """Base action class. Every acion class derives from it."""
    state_settings = Cell_And_State_Settings

    def __init__(self, state_settings:Cell_And_State_Settings):
        self.state_settings = state_settings

    # funkce aktivace akce
    def action(self, cell, virtual_grid:Hex_Grid, real_grid:Hex_Grid):
        """Performs action of the class with given cell."""
        pass

    # nahodne zmeni parametry akce
    def mutate(self):
        """Changes properties of this action in manner given by assigned state settings class."""
        pass

    def randomize(self):
        """Changes properties of this action randomly."""
        pass
    
    def copy(self) -> State_Action:
        """Returns new insatnce of the action class with same properties and same instance of the state settings."""
        return None

# zakladni trida podminek
class State_Condition():
    """Base condition class. Every condition class derives from it."""
    state_settings = Cell_And_State_Settings

    def __init__(self, state_settings:Cell_And_State_Settings):
        self.state_settings = state_settings

    # funkce vyhodnoceni podminky
    def check_condition(cell:Cell, virtual_grid:Hex_Grid) -> bool:
        """Checks condition of the class with given cell. Returns True, if the condition is met."""
        return True
    
    # nahodne zmeni parametry podminky
    def mutate(self):
        """Changes properties of this condition in manner given by assigned state settings class."""
        pass

    def randomize(self):
        """Changes properties of this condition randomly."""
        pass

    def copy(self) -> State_Condition:
        """Returns new insatnce of the condition class with same properties and same instance of the state settings."""
        
        return None

# stav bunky
class Cell_State():
    """Class containing information of the one cell state."""
    state_number = int
    number_of_states = int
    state_actions_list = list[State_Action]
    state_conditions_list = list[State_Condition]
    state_action = State_Action
    state_condition = State_Condition
    next_state_A = int
    next_state_B = int

    def __init__(self, state_number:int, number_of_states:int, state_action:State_Action, state_actions_list:list[State_Action], state_condition:State_Condition, state_conditions_list:list[State_Condition], next_state_A:int, next_state_B:int):
        self.state_number = state_number
        self.number_of_states = number_of_states
        self.state_action = state_action
        self.state_actions_list = state_actions_list
        self.state_condition = state_condition
        self.state_conditions_list = state_conditions_list
        self.next_state_A = next_state_A
        self.next_state_B = next_state_B

    def __repr__(self) -> str:
        return "St: " + str(self.state_number) + " " + repr(self.state_action) + " " + repr(self.state_condition) + " A: " + str(self.next_state_A) + " B: " + str(self.next_state_B)

    def __str__(self) -> str:
        return str(self.state_number) + " " + str(self.state_action) + " " + str(self.state_condition) + " A: " + str(self.next_state_A) + " B: " + str(self.next_state_B)

    def copy(self):
        """Returns new insatnce of the state class with copied properties (ie. new class insatances)."""
        return Cell_State(self.state_number, self.number_of_states, self.state_action.copy(), self.state_actions_list, self.state_condition.copy(), self.state_conditions_list, self.next_state_A, self.next_state_B)

    def process_condition(self, cell:Cell, virtual_grid:Hex_Grid) -> int:
        """Checks, if the condition with the given cell is met. Then returns according cell state number."""
        if self.state_condition.check_condition(cell, virtual_grid):
            return self.next_state_A
        return self.next_state_B
    
    def action(self, cell, virtual_grid:Hex_Grid, real_grid:Hex_Grid):
        """Performs assignet action with the given cell."""
        self.state_action.action(cell, virtual_grid, real_grid)

    def randomize_action(self):
        """Randomly changes action of the state to a new, different one."""
        indexes = [x for x in range(len(self.state_actions_list))]
        current_index = 0
        while type(self.state_action) is not type(self.state_actions_list[current_index]):
            current_index += 1
        indexes.remove(current_index)
        index = indexes[randint(0, len(indexes) - 1)]
        self.state_action = self.state_actions_list[index].copy()
        self.state_action.randomize()

    def randomize_condition(self):
        """Randomly changes condition of the state to a new, different one."""
        indexes = [x for x in range(len(self.state_conditions_list))]
        current_index = 0
        while type(self.state_condition) is not type(self.state_conditions_list[current_index]):
            current_index += 1
        indexes.remove(current_index)
        index = indexes[randint(0, len(indexes) - 1)]
        self.state_condition = self.state_conditions_list[index].copy()
        self.state_condition.randomize()

    def randomize_next_states(self):
        """Randomly changes possible outputs of the process_condition() function."""
        self.next_state_A = randint(0, self.number_of_states - 1)
        self.next_state_B = randint(0, self.number_of_states - 1)

    def mutate_state(self, strong_mutation_chance:int):
        """Chooses one of the following: strong action, action, strong condition, condition, following states.
        Strong means whole class is replaced by a new instance, other possibilites are only changing values."""
        if uniform(0, 100) <= strong_mutation_chance:
            mutation = randint(0, 2)
            if mutation == 0:
                self.randomize_action()
            elif mutation == 1:
                self.randomize_condition()
            else:
                self.randomize_next_states()
        else:
            mutation = randint(0, 1)
            if mutation == 0:
                self.state_action.mutate()
            else:
                self.state_condition.mutate()

# bunka
class Cell():
    """Class representing a cell, containing all its information."""
    iter_counter = count()
    cell_number = -1
    current_tile = Hex_Tile # pro snazsi pristup k poli
    hex_pos = Hex_Pos
    states = list[Cell_State]
    current_state = Cell_State
    cell_settings = Cell_And_State_Settings
    cell_photo_image = tk.PhotoImage
    pimage_cells = list[tk.PhotoImage]
    pimage_index = int
    info_list = list[str]
    energy = 0
    size = 0
    max_size = MAX_CELL_SIZE_CONST
    max_energy = int
    age_in_steps = 0
    alive = True

    def __init__(self, cell_states:list[Cell_State], energy:int, size:int, cell_settings:Cell_And_State_Settings, pimage_cells:list[tk.PhotoImage], cell_number:int = -1):
        self.cell_number = next(self.iter_counter)
        if len(cell_states) == 0:
            raise Exception("Cell " + str(self.cell_number) + " needs to have at least one state.")
        self.cell_settings = cell_settings
        self.states = cell_states
        self.current_state = cell_states[0]
        self.energy = energy
        self.size = size
        self.pimage_cells = pimage_cells
        self.pimage_index = 0
        self.cell_photo_image = pimage_cells[0]
        self.hex_pos = Hex_Pos(0, 0, 0)
        self.info_list = ["",""] + [str(state) for state in self.states]
        self.max_energy = self.cell_settings.max_energy_base + round(self.cell_settings.max_energy_multiplier * self.size)

    def __repr__(self) -> str:
        return "Cell - E: " + str(self.energy) + ", S: " + str(self.size) + ", A: " + str(self.alive)
    
    def __str__(self):
        return str(self.hex_pos) + " energy: " + str(self.energy) + " size: " + str(self.size) + " age: " + str(self.age_in_steps) + "\n" + str(self.current_state) + "\n" + "\n".join(self.states_repr_list)
    
    def get_info_list(self) -> list:
        """Returns list of strings. First contains information about the cell. Second contains description of its active state.
        Others contains descriptions of all states of the cell, each string one state."""
        self.info_list[0] = str(self.hex_pos) + " energy: " + str(self.energy) + "/" + str(self.max_energy) + " size: " + str(self.size) + " age: " + str(self.age_in_steps)
        self.info_list[1] = str(self.current_state)
        return self.info_list

    def copy(self) -> Cell:
        """Returns new instance of the cell with copied properties."""
        new_states = []
        for state in self.states:
            new_states.append(state.copy())
        new_cell = Cell(new_states, self.energy, self.size, self.cell_settings, self.pimage_cells)
        new_cell.pimage_index = self.pimage_index
        new_cell.cell_photo_image = self.cell_photo_image
        return new_cell

    def randomize_image(self) -> None:
        """Randomly selects new image (different from the current one) representing the cell."""
        current_index = self.pimage_index
        next_index = randint(0, len(self.pimage_cells) - 1)
        while next_index == current_index:
            next_index = randint(0, len(self.pimage_cells) - 1)
        self.pimage_index = next_index
        self.cell_photo_image = self.pimage_cells[self.pimage_index]

    # funkce zarizujici co ma bunka udelat na konci kroku
    def step(self, virtual_grid:Hex_Grid, real_grid:Hex_Grid):
        """Proceeds cell step, ie. energy change, size gain, actions, conditions, death, ..."""
        self.step_energy_size(virtual_grid, real_grid)
        if self.alive:
            self.action(virtual_grid, real_grid)
            self.process_condition(virtual_grid)
            self.age_in_steps += 1

    # ziskani energie, ztrata energie a rust
    def step_energy_size(self, virtual_grid:Hex_Grid, real_grid:Hex_Grid):
        """Proceeds basic energy change and size grow of the cell step."""
        number_free_tiles_around = virtual_grid.get_number_free_tile_neighbours(self.hex_pos)
        energy_loss = round(self.cell_settings.base_energy_loss + number_free_tiles_around / 6 * self.cell_settings.around_energy_loss)
        energy_change = real_grid.get_energy_from_tile_at_hex_pos(self.hex_pos, self.cell_settings.energy_gain) - energy_loss    
        self.change_energy(energy_change, real_grid)
        size_change = round(self.cell_settings.base_size_gain + number_free_tiles_around / 6 * self.cell_settings.around_size_gain)
        self.change_size(size_change, real_grid)

    # aktivace akce dane bunky
    def action(self, virtual_grid:Hex_Grid, real_grid:Hex_Grid):
        """Proceeds cell action"""
        self.current_state.action(self, virtual_grid, real_grid)

    # vyhodnoceni podminky a prepsani stavu dane bunky
    def process_condition(self, virtual_grid:Hex_Grid):
        """Proceeds cell condition"""
        next_state = self.current_state.process_condition(self, virtual_grid)
        self.current_state = self.states[next_state]

    # funkce pridani statu pri snezeni bunky
    def eat_cell(self, other_cell:Cell, real_grid:Hex_Grid):
        """The cell eats other_cell accordingly to the cell setting class, other_cell dies."""
        self.change_size(round(other_cell.size * self.cell_settings.size_eat_fraction), real_grid)
        self.change_energy(round(other_cell.energy * self.cell_settings.energy_eat_fraction), real_grid)
        other_cell.death(real_grid)

    def change_size(self, size_amount:int, real_grid:Hex_Grid):
        """Changes size of the cell by the given amount. Cannot exceeds lower or upper limit.
        If upper limit of the cell size is exceeded, then the cell dies."""
        self.size += size_amount
        if self.size > self.max_size:
            self.death(real_grid)
        if self.size <= 0:
            self.death(real_grid)

    def change_energy(self, energy_amount:int, real_grid:Hex_Grid):
        """Changes size of the cell by the given amount. Cannot exceeds lower or upper limit.
        If lower limit of the cell size is exceeded, then the cell dies."""
        self.max_energy = self.cell_settings.max_energy_base + round(self.cell_settings.max_energy_multiplier * self.size)
        self.energy += energy_amount
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        if self.energy <= 0:
            self.death(real_grid)

    # smrt a smazani bunky
    def death(self, real_grid:Hex_Grid):
        """Deletes cell from the given grid and sets its alive property to false."""
        if self.alive:
            self.alive = False
            real_grid.delete_cell(self)

class Action_Energy_Share(State_Action):
    """Derivation of the base action class, overrides some functions of it."""
    share_percentage = 50

    def __repr__(self) -> str:
        return "Act-share: percentage " + str(self.share_percentage) + "%"
    
    def __str__(self) -> str:
        return "SHARE: per: " + str(self.share_percentage) + "%"

    def copy(self) -> Action_Energy_Share:
        action = Action_Energy_Share(self.state_settings)
        action.share_percentage = self.share_percentage
        return action

    def action(self, cell:Cell, virtual_grid: Hex_Grid, real_grid: Hex_Grid) -> None:
        tiles_around = virtual_grid.get_tile_neighbours(cell.hex_pos)
        cells_around = []
        percentage = self.share_percentage / 100
        for tile in tiles_around:
            if tile.cells_on_tile:
                cells_around.append(tile.cells_on_tile[0])
        energy_share = round(cell.energy * percentage)
        if len(cells_around) > 0:
            cell.change_energy(-energy_share, real_grid)
            energy_bit = energy_share // len(cells_around)
            for other_cell in cells_around:
                other_cell.change_energy(energy_bit, real_grid)

    def mutate(self) -> None:
        amount = self.state_settings.share_mutation_amount
        new_share_per = round(self.share_percentage + uniform(-amount, amount), 1)
        min_per = self.state_settings.min_share_per
        max_per = self.state_settings.max_share_per
        self.share_percentage = min(max(new_share_per, min_per), max_per)

    def randomize(self):
        new_share_per = round(uniform(0, 100), 1)
        min_per = self.state_settings.min_share_per
        max_per = self.state_settings.max_share_per
        self.share_percentage = min(max(new_share_per, min_per), max_per)

class Action_Divide(State_Action):
    """Derivation of the base action class, overrides some functions of it."""
    divide_directions = [Hex_Pos(1, 0, -1), Hex_Pos(1, -1, 0), Hex_Pos(0, 1, -1), Hex_Pos(-1, 0, 1), Hex_Pos(-1, 1, 0), Hex_Pos(0, -1, 1)]
    current_direction = 0
    resources_percentage = 50

    def __init__ (self, state_settings:Cell_And_State_Settings, current_direction = 0):
        if current_direction < 0 or current_direction > len(self.divide_directions):
            raise Exception("Action_move can choose only from 0 to 5.")
        self.current_direction = current_direction
        super().__init__(state_settings)

    def __repr__(self) -> str:
        return "Act-divide: size " + str(self.resources_percentage) + "%, " + repr(self.divide_directions[self.current_direction])

    def __str__(self) -> str:
        return "DIV: dir: " + str(self.divide_directions[self.current_direction].row) + str(self.divide_directions[self.current_direction].col_l) + str(self.divide_directions[self.current_direction].col_r) + " per: " + str(self.resources_percentage) + "%"

    def copy(self) -> Action_Divide:
        action = Action_Divide(self.state_settings)
        action.current_direction = self.current_direction
        action.resources_percentage = self.resources_percentage
        return action
    
    # prepsana funkce aktivace akce
    def action(self, cell:Cell, virtual_grid:Hex_Grid, real_grid:Hex_Grid):
        energy_cost = self.state_settings.divide_energy_cost
        if cell.energy > energy_cost * 1.2:
            divide_dir = self.divide_directions[self.current_direction]
            new_hex_pos = sum_hex_pos(cell.hex_pos, divide_dir)
            new_tile = virtual_grid.get_tile_at_hex_pos(new_hex_pos)
            if new_tile and not new_tile.tile_is_wall:
                new_cell = cell.copy()
                real_grid.add_cell_to_hex_pos(new_cell, new_hex_pos)
                cell.change_energy(-energy_cost, real_grid)
                passed_energy = round(cell.energy * self.resources_percentage / 100)
                passed_size = round(cell.size * self.resources_percentage / 100)
                new_cell.change_energy(passed_energy, real_grid)
                new_cell.change_size(passed_size, real_grid)
                cell.change_energy(-passed_energy, real_grid)
                cell.change_size(-passed_size, real_grid)
                mutation_chance = self.state_settings.mutation_chance
                mutate = (mutation_chance > uniform(0, 100))
                if mutate:
                    new_cell.randomize_image()
                while mutate:
                    index = randint(0, len(new_cell.states) - 1)
                    new_cell.states[index].mutate_state(self.state_settings.strong_mutation_chance)
                    mutation_chance = round(mutation_chance / 2, 1)
                    mutate = (mutation_chance > uniform(0, 100))

    # prepsana funkce nahodne zmeny parametru, zde meni smer
    def mutate(self):
        self.current_direction = randint(0, 5)
        amount = self.state_settings.divide_mutation_amount
        new_resources_per = round(self.resources_percentage + uniform(-amount, amount), 1)
        min_per = self.state_settings.min_resources_per
        max_per = self.state_settings.max_resources_per
        self.resources_percentage = min(max(new_resources_per, min_per), max_per)

    def randomize(self):
        self.current_direction = randint(0, 5)
        new_resources_per = round(uniform(0, 100), 1)
        min_per = self.state_settings.min_resources_per
        max_per = self.state_settings.max_resources_per
        self.resources_percentage = min(max(new_resources_per, min_per), max_per)

class Action_Move(State_Action):
    """Derivation of the base action class, overrides some functions of it."""
    move_directions = [Hex_Pos(0, 0, 0), Hex_Pos(1, 0, -1), Hex_Pos(1, -1, 0), Hex_Pos(0, 1, -1), Hex_Pos(-1, 0, 1), Hex_Pos(-1, 1, 0), Hex_Pos(0, -1, 1)]
    current_direction = 0

    def __init__ (self, state_settings:Cell_And_State_Settings, current_direction = 0):
        if current_direction < 0 or current_direction > len(self.move_directions):
            raise Exception("Action_move can choose only from 0 to 5.")
        self.current_direction = current_direction
        super().__init__(state_settings)

    def __repr__(self) -> str:
        return "Act-move: " + repr(self.move_directions[self.current_direction])
    
    def __str__(self) -> str:
        return "MOVE: dir: " + str(self.move_directions[self.current_direction].row) + str(self.move_directions[self.current_direction].col_l) + str(self.move_directions[self.current_direction].col_r)

    # prepsana funkce aktivace akce
    def action(self, cell:Cell, virtual_grid:Hex_Grid, real_grid:Hex_Grid):
        energy_cost = self.state_settings.move_energy_cost
        if cell.energy > energy_cost * 1.2:
            if self.current_direction != 0:
                move_dir = self.move_directions[self.current_direction]
                new_hex_pos = sum_hex_pos(cell.hex_pos, move_dir)
                new_tile = virtual_grid.get_tile_at_hex_pos(new_hex_pos)
                if new_tile and not new_tile.tile_is_wall:
                    real_grid.move_cell_between_tiles(cell, new_hex_pos)
                    cell.change_energy(-energy_cost, real_grid)

    # prepsana funkce nahodne zmeny parametru, zde meni smer
    def mutate(self):
        self.current_direction = randint(0, 6)
    
    def randomize(self):
        self.current_direction = randint(0, 6)

    def copy(self) -> Action_Move:
        action = Action_Move(self.state_settings)
        action.current_direction = self.current_direction
        return action 

class Action_Still(State_Action):
    """Derivation of the base action class, overrides some functions of it."""

    def __repr__(self) -> str:
        return "Act-still"
    
    def __str__(self) -> str:
        return "STILL"

    def copy(self) -> Action_Move:
        action = Action_Still(self.state_settings)
        return action

class Condition_Sensor(State_Condition):
    """Derivation of the base condition class, overrides some functions of it."""
    sensor_directions = [Hex_Pos(1, 0, -1), Hex_Pos(1, -1, 0), Hex_Pos(0, 1, -1), Hex_Pos(-1, 0, 1), Hex_Pos(-1, 1, 0), Hex_Pos(0, -1, 1)]
    current_direction = 0
    sensor_types = ["cell", "free", "ener"]
    current_type = 0

    def __init__(self, state_settings:Cell_And_State_Settings, current_direction:int = 0, current_type:int = 0) -> None:
        if current_direction < 0 or current_direction >= len(self.sensor_directions):
            raise Exception("Condition_sensor can choose direction only from 0 to " + str(len(self.sensor_directions) - 1)+ ".")
        self.current_direction = current_direction
        if current_type < 0 or current_type >= len(self.sensor_types):
            raise Exception("Condition_sensor can choose type only from 0 to " + str(len(self.sensor_types) - 1)+ ".")
        self.current_type = current_type
        super().__init__(state_settings)

    def __repr__(self) -> str:
        return "Cond-sensor: " + repr(self.sensor_directions[self.current_direction]) + ", type " + str(self.sensor_types[self.current_type])
    
    def __str__(self) -> str:
        return "SENS: dir: " + str(self.sensor_directions[self.current_direction].row) + str(self.sensor_directions[self.current_direction].col_l) + str(self.sensor_directions[self.current_direction].col_r) + " " + self.sensor_types[self.current_type]

    def copy(self) -> Condition_Sensor:
        condition = Condition_Sensor(self.state_settings, self.current_direction, self.current_type)
        return condition
    
    def check_condition(self, cell:Cell, virtual_grid:Hex_Grid) -> bool:
        position = sum_hex_pos(cell.hex_pos, self.sensor_directions[self.current_direction])
        if self.sensor_types[self.current_type] == "cell":
            return virtual_grid.get_tile_at_hex_pos(position).cells_on_tile
        elif self.sensor_types[self.current_type] == "free":
            return not virtual_grid.get_tile_at_hex_pos(position).occupied
        else:
            return virtual_grid.get_tile_at_hex_pos(position).tile_energy > virtual_grid.get_tile_at_hex_pos(cell.hex_pos).tile_energy 
    
    # prepsana funkce nahodne zmeny parametru
    def mutate(self) -> None:
        self.current_direction = randint(0, len(self.sensor_directions) - 1)
        self.current_type = randint(0, len(self.sensor_types) - 1)

    def randomize(self) -> None:
        self.current_direction = randint(0, len(self.sensor_directions) - 1)
        self.current_type = randint(0, len(self.sensor_types) - 1)

class Condition_Size(State_Condition):
    """Derivation of the base condition class, overrides some functions of it."""
    size_amount = 10
    negation = False

    def __init__ (self, state_settings:Cell_And_State_Settings, size_amount:int, negation:bool):
        self.size_amount = size_amount
        self.negation = negation
        super().__init__(state_settings)

    def __repr__(self) -> str:
        if self.negation:
            return "Cond-size: cell.size >= " + str(self.size_amount)
        return "Cond-size: cell.size < " + str(self.size_amount)

    def __str__(self) -> str:
        if self.negation:
            return "SIZE: si >= " + str(self.size_amount)
        return "SIZE: si < " + str(self.size_amount)

    def check_condition(self, cell:Cell, virtual_grid:Hex_Grid) -> bool:
        value = cell.size < self.size_amount
        if self.negation:
            return not value
        return value
    
    # prepsana funkce nahodne zmeny parametru
    def mutate(self) -> None:
        amount = self.state_settings.size_mutation_amount
        new_size_amount = self.size_amount + randint(-amount, amount)
        self.size_amount = min(max(new_size_amount, 0), MAX_CELL_SIZE_CONST)
        self.negation = randint(0, 100) < 50

    def randomize(self) -> None:
        self.size_amount = randint(0, MAX_CELL_SIZE_CONST)
        self.negation = randint(0, 100) < 50

    def copy(self) -> Condition_Size:
        condition = Condition_Size(self.state_settings, self.size_amount, self.negation)
        return condition

class Condition_Energy(State_Condition):
    """Derivation of the base condition class, overrides some functions of it."""
    energy_amount = int
    negation = False

    def __init__ (self, state_settings:Cell_And_State_Settings, energy_amount:int, negation:bool):
        self.energy_amount = energy_amount
        self.negation = negation
        super().__init__(state_settings)

    def __repr__(self) -> str:
        if self.negation:
            return "Cond-energy: cell.energy >= " + str(self.energy_amount)
        return "Cond-energy: cell.energy < " + str(self.energy_amount)

    def __str__(self) -> str:
        if self.negation:
            return "ENER: en >= " + str(self.energy_amount)
        return "ENER: en < " + str(self.energy_amount)

    def check_condition(self, cell:Cell, virtual_grid:Hex_Grid) -> bool:
        value = cell.energy < self.energy_amount
        if self.negation:
            return not value
        return value
    
    # prepsana funkce nahodne zmeny parametru
    def mutate(self) -> None:
        amount = self.state_settings.energy_mutation_amount
        new_energy_amount = self.energy_amount + randint(-amount, amount)
        self.energy_amount = min(max(new_energy_amount, 0), ENERGY_UNIT_CONST)
        self.negation = randint(0, 100) < 50

    def randomize(self) -> None:
        self.energy_amount = randint(0, ENERGY_UNIT_CONST)
        self.negation = randint(0, 100) < 50

    def copy(self) -> Condition_Energy:
        condition = Condition_Energy(self.state_settings, self.energy_amount, self.negation)
        return condition
    
# trida obsahujici a ridici jednu simulaci
class Dish_Experiment():
    """Class representing an experiment, handling simulation, statistics and creation of new cells.
    Contains all information about the experiment."""
    cell_actions = list[State_Action]
    cell_conditions = list[State_Condition]
    pi_64_cells = list[tk.PhotoImage]
    pi_32_cells = list[tk.PhotoImage]
    pi_16_cells = list[tk.PhotoImage]
    pimage_cells = list[tk.PhotoImage]
    pi_64_tiles = list[tk.PhotoImage]
    pi_32_tiles = list[tk.PhotoImage]
    pi_16_tiles = list[tk.PhotoImage]
    pimage_tiles = list[tk.PhotoImage]
    tile_resolution = tuple
    res_index = int
    experiment_number = int
    virtual_grid = Hex_Grid
    real_grid = Hex_Grid
    experiment_created = False
    simulating = False

    simulation_steps_duration = 0
    number_of_cells = 0
    cell_mid_age = 0
    cell_med_age = 0
    cell_sum_age = 0
    cell_max_age = 0
    cell_with_maxage = Cell
    max_cluster_size = 0
    mid_cluster_size = 0
    cells_eaten = 0

    last_update_time = float

    cell_and_state_settings = Cell_And_State_Settings
    refill_tile_percentage = int
    refill_energy_flow = int
    time_step = float

    def __init__ (self, pi_64_cells, pi_64_tiles, pi_32_cells, pi_32_tiles, pi_16_cells, pi_16_tiles, cell_and_state_settings:Cell_And_State_Settings, time_step:float = 0.4, experiment_number:int = -1):
        self.pi_64_cells = pi_64_cells
        self.pi_64_tiles = pi_64_tiles
        self.pi_32_cells = pi_32_cells
        self.pi_32_tiles = pi_32_tiles
        self.pi_16_cells = pi_16_cells
        self.pi_16_tiles = pi_16_tiles
        self.cell_and_state_settings = cell_and_state_settings
        self.experiment_number = experiment_number
        self.time_step = time_step
        self.cell_with_maxage = None
        self.cell_actions = [Action_Still(self.cell_and_state_settings), Action_Move(self.cell_and_state_settings), Action_Divide(self.cell_and_state_settings), Action_Energy_Share(self.cell_and_state_settings)]
        self.cell_conditions = [Condition_Energy(self.cell_and_state_settings, 0, False), Condition_Size(self.cell_and_state_settings, 0, False), Condition_Sensor(self.cell_and_state_settings, 0, 0)]

    def __repr__(self) -> str:
        return "Experiment: simulating " + str(self.simulating) + ", time step " + str(self.time_step) + ", r-grid " + repr(self.real_grid)

    # vytvoří nový experiment
    def create_experiment(self, grid_radius:int = 5, cell_percentage:float = 25, refill_energy_flow = 0.15, refill_tile_percentage:int = 70, predefined_cells:list[Cell] = None, number_of_cell_states:int = 10, initial_cell_energy:int = ENERGY_UNIT_CONST, initial_cell_size:int = 5):
        """Creates new experiment with cells either randomly generated or predefined in a list.
        Sets up everything needed for experiment to be ready to run."""
        if self.experiment_created:
            self.flush_experiment()
        self.refill_tile_percentage = refill_tile_percentage
        self.refill_energy_flow = refill_energy_flow
        self.experiment_created = True
        self.pimage_tiles = self.pi_64_tiles
        self.pimage_cells = self.pi_64_cells
        self.tile_resolution = (56, 64)
        if grid_radius > 7:
            self.pimage_tiles = self.pi_32_tiles
            self.pimage_cells = self.pi_32_cells
            self.tile_resolution = (28, 32)
        if grid_radius > 14:
            self.pimage_tiles = self.pi_16_tiles
            self.pimage_cells = self.pi_16_cells
            self.tile_resolution = (14, 16)
        if grid_radius > 30:
            grid_radius = 30
        self.real_grid = Hex_Grid(grid_radius, self.pimage_tiles)
        free_hex_positions = self.real_grid.get_free_hex_positions()
        self.number_of_cells = round(len(free_hex_positions) * cell_percentage / 100)
        if predefined_cells:
            cell_list = predefined_cells.copy()
            shuffle(cell_list)
            list_len = len(cell_list)
            index = 0
            for _ in range(self.number_of_cells): 
                cell = cell_list[index]
                hex_position = free_hex_positions[randint(0, len(free_hex_positions) - 1)]
                free_hex_positions.remove(hex_position)
                self.real_grid.add_cell_to_hex_pos(cell, hex_position)
                index = (index + 1) % list_len
        else:
            for _ in range(self.number_of_cells):
                cell = self.create_random_cell(self.pimage_cells, self.cell_and_state_settings, number_of_cell_states, initial_cell_energy, initial_cell_size)
                hex_position = free_hex_positions[randint(0, len(free_hex_positions) - 1)]
                free_hex_positions.remove(hex_position)
                self.real_grid.add_cell_to_hex_pos(cell, hex_position)
        self.virtual_grid = self.real_grid.copy()

    # smaže experiment
    def flush_experiment(self):
        """Deletes experiment and all its content."""
        self.decimate_culture(100)
        self.simulating = False
        self.experiment_created = False
        self.virtual_grid = None
        self.real_grid = None
        self.simulation_steps_duration = 0
        self.cells_eaten = 0

    def decimate_culture(self, percentage:int):
        """Kills given percentage of cells in experiment randomly."""
        number_to_kill = round(len(self.real_grid.cells_in_grid) * percentage / 100)
        cells = self.real_grid.cells_in_grid.copy()
        shuffle(cells)
        for count, cell in enumerate(cells, start = 1):
            if count > number_to_kill:
                break
            cell.death(self.real_grid)

    def kill_cells_at_hex_pos(self, hex_pos:Hex_Pos) -> None:
        """Removes all cells on the tile on the given hex position, if such a tile exists. Recommended way to kill cells externally."""
        tile = self.real_grid.get_tile_at_hex_pos(hex_pos)
        if tile:
            for cell in tile.cells_on_tile:
                cell.death(self.real_grid)

    def add_cell_to_hex_pos(self, cell:Cell, hex_pos:Hex_Pos):
        """Adds cell to the tile at given hex position. Recommended way to add cells externally."""
        self.real_grid.add_cell_to_hex_pos(cell, hex_pos)

    # vytvori nahodne generovanou bunku
    def create_random_cell(self, pimage_cells:list[tk.PhotoImage], cell_and_state_settings:Cell_And_State_Settings, number_of_cell_states:int = 10, initial_cell_energy:int = ENERGY_UNIT_CONST, initial_cell_size:int = 5) -> Cell:
        """Returns new cell with given parameters suitable for this experiment."""
        cell_states = [None for _ in range(number_of_cell_states)]
        for i in range(number_of_cell_states):
            action = self.cell_actions[randint(0, len(self.cell_actions) - 1)].copy()
            action.randomize()
            condition = self.cell_conditions[randint(0, len(self.cell_conditions) - 1)].copy()
            condition.randomize()
            cell_states[i] = Cell_State(i, number_of_cell_states, action, self.cell_actions, condition, self.cell_conditions, randint(0, number_of_cell_states - 1), randint(0, number_of_cell_states - 1))
        cell = Cell(cell_states, initial_cell_energy, initial_cell_size, cell_and_state_settings, pimage_cells)
        cell.randomize_image()
        return cell
    
    def create_cell_from_cell(self, cell:Cell, initial_energy:int = -1, initial_size:int = -1) -> Cell:
        """Returns new cell with parameters copied from the given cell, suitable for this experiment.
        That means resolution of its representing image corresponds to the grid radius."""
        if initial_energy == -1:
            initial_energy = cell.energy
        if initial_size == -1:
            initial_size = cell.size
        new_states = []
        for state in cell.states:
            new_states.append(state.copy())
        new_cell = Cell(new_states, initial_energy, initial_size, cell.cell_settings, self.pimage_cells)
        new_index = cell.pimage_index
        new_image = self.pi_64_cells[new_index]
        if self.tile_resolution[1] == 32:
            new_image = self.pi_32_cells[new_index]
        elif self.tile_resolution[1] == 16:
            new_image = self.pi_16_cells[new_index]
        new_cell.cell_photo_image = new_image
        return new_cell
    
    # pauzne/spusti simulaci, vrati bool, jestli probiha simulace
    def play_pause_simulation(self) -> bool:
        """Switches between play and pause simulation mode, if simulation was creaed.
        Returns current simulation mode: play - True, pause - False."""
        if not self.experiment_created:
            raise Exception("There has to be an experiment in order to process simulation.")
        else:
            self.simulating = not self.simulating
        return self.simulating

    # zmeri globalni statistiky, jako velikosti klastru a delky retezcu
    def fast_global_statistics(self):
        """Calculates fast-obtainable experiment statistics - everything but cluster sizes."""
        if self.number_of_cells == 0:
            self.cell_mid_age = 0
            self.cell_med_age = 0
            self.cell_max_age = 0
            return
        self.cell_sum_age = 0
        self.cell_max_age = 0
        ages = []
        for cell in self.real_grid.cells_in_grid:
            if cell.alive:
                self.cell_sum_age += cell.age_in_steps
                ages.append(cell.age_in_steps)
                if cell.age_in_steps > self.cell_max_age:
                    self.cell_max_age = cell.age_in_steps
                    self.cell_with_maxage = cell
        self.cell_med_age = median(ages)
        self.cell_mid_age = round(self.cell_sum_age / self.number_of_cells, 2)
        

    def slow_global_statistics(self):
        """Calculates slow-obtainable experiment statistics - cluster sizes."""
        clusters = self.real_grid.find_cluster_sizes()
        if clusters:
            self.max_cluster_size = max(clusters)
            self.mid_cluster_size = round(mean(clusters), 2)
        else:
            self.max_cluster_size = 0
            self.mid_cluster_size = 0
    
    # zahaji simulaci
    def start_simulation(self):
        """Sarts simulation if it is created."""
        if not self.experiment_created:
            raise Exception("There has to be an experiment in order to process simulation.")
        if not self.simulating:
            self.simulating = True
            self.last_update_time = time()

    # prubeh simulace, povolava se opakovane skrz vnejsi cyklus
    def simulate(self) -> bool:
        """Simulation loop, must be called from outside loop repeatedly.
        Calls simulation_uptade() if time between two simulation steps have passed."""
        if not self.simulating:
            return False
        if abs(self.last_update_time - time()) > self.time_step:
            self.last_update_time = time()
            self.simulation_steps_duration += 1
            self.simulation_update()
            self.number_of_cells = len(self.real_grid.cells_in_grid)
            return True
        return False

    def simulation_update(self):
        """Updates whole simulation."""
        cell_updates = self.real_grid.cells_in_grid.copy()
        for cell in cell_updates:
            cell.step(self.virtual_grid, self.real_grid)
        self.cells_eaten = self.real_grid.cell_eating(self.real_grid)
        self.real_grid.refill_energy(self.refill_tile_percentage, round(self.refill_energy_flow * ENERGY_UNIT_CONST))
        self.real_grid.copy_changes_to_and_reset(self.virtual_grid)

    # ukonci simulaci
    def stop_simulation(self):
        """Stops simulation."""
        if self.simulating:
            self.simulating = False

class Laboratory(tk.Tk):
    dish_experiments = list[Dish_Experiment]
    experiment_canvases = list[tk.Canvas]
    mark_images = list[tk.PhotoImage]
    mark_offsets = list[int]
    canvas_image_offset = (5, 5)
    current_experiment = 0
    laboratory_running = False
    pasting = True
    maxage_cell = Cell
    marked_cell = Cell
    cursor_cell = Cell
    copied_cell = Cell
    cycle_time_ms = 10
    last_im_update_coords = list[int]

    frm_hex_grid = tk.Frame
    frm_cell_information = tk.Frame
    frm_simulation_settings = tk.Frame
    frm_advanced_sim_settigs = tk.Frame
    frm_simulation_run = tk.Frame
    frm_initial_settings = tk.Frame
    lower_frame_type = 0

    scl_simulation_speed = tk.Scale
    scl_grid_radius = tk.Scale
    scl_initial_cell_per = tk.Scale
    scl_initial_cell_en_per = tk.Scale
    scl_initial_cell_size_per = tk.Scale
    scl_tile_perc_refill = tk.Scale
    scl_energy_refill_amount = tk.Scale
    scl_cell_energy_gain = tk.Scale
    scl_cell_energy_loss = tk.Scale
    scl_cell_around_en_loss = tk.Scale
    scl_decimate_percentage = tk.Scale

    sbx_cell_max_en_multip = tk.Spinbox
    sbx_cell_max_en_base = tk.Spinbox
    sbx_cell_en_eat_percentage = tk.Spinbox
    sbx_cell_base_size_gain = tk.Spinbox
    sbx_cell_around_size_gain = tk.Spinbox
    sbx_cell_size_eat_percentage = tk.Spinbox
    sbx_cell_share_mut_amount = tk.Spinbox
    sbx_cell_min_share_per = tk.Spinbox
    sbx_cell_max_share_per = tk.Spinbox
    sbx_cell_div_mut_amount = tk.Spinbox
    sbx_cell_min_res_per = tk.Spinbox
    sbx_cell_max_res_per = tk.Spinbox
    sbx_cell_mut_chance = tk.Spinbox
    sbx_cell_str_mut_chance = tk.Spinbox
    sbx_cell_div_cost = tk.Spinbox
    sbx_cell_move_cost = tk.Spinbox
    sbx_cell_size_con_mut_am = tk.Spinbox
    sbx_cell_en_con_mut_am = tk.Spinbox

    btn_flush_create_experiment = tk.Button
    btn_play_pause_experiment = tk.Button
    btn_switch_settings_cell_info = tk.Button
    btn_experiments = list[tk.Button]
    btn_decimate_culture = tk.Button
    btn_kill_all_cells = tk.Button
    btn_switch_paste_kill = tk.Button

    lbl_cell_counts = list[tk.Label]
    lbl_mid_age = tk.Label
    lbl_med_age = tk.Label
    lbl_max_age = tk.Label
    lbl_max_cluster = tk.Label
    lbl_mid_cluster = tk.Label
    lbl_cells_eaten = tk.Label
    lbl_simulation_duration = tk.Label
    lbl_cursor_cell_head = tk.Label
    lbl_cursor_cell = list[tk.Label]
    lbl_marked_cell_head = tk.Label
    lbl_marked_cell = list[tk.Label]

    pi_64_tiles = list[tk.PhotoImage]
    pi_64_cells = list[tk.PhotoImage]
    pi_64_mark = tk.PhotoImage
    pi_32_tiles = list[tk.PhotoImage]
    pi_32_cells = list[tk.PhotoImage]
    pi_32_mark = tk.PhotoImage
    pi_16_tiles = list[tk.PhotoImage]
    pi_16_cells = list[tk.PhotoImage]
    pi_16_mark = tk.PhotoImage

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.dish_experiments = [None] * 3
        self.experiment_canvases = [None] * 3
        self.mark_images = [None] * 3
        self.btn_experiments = [None] * 3
        self.mark_offsets = [None] * 3
        self.marked_cell = None
        self.cursor_cell = None
        self.copied_cell = None
        self.last_im_update_coords = [0, 0]

        self.create_interface()

        self.load_images()

        for i in range(3):
            self.dish_experiments[i] = Dish_Experiment(self.pi_64_cells, self.pi_64_tiles, self.pi_32_cells, self.pi_32_tiles, self.pi_16_cells, self.pi_16_tiles, Cell_And_State_Settings(), time_step = 0.4)

    def create_interface(self):
        """Help function, creates interface of the application and sets default values of settings sliders, spinboxes, ..."""
        self.title("Lab")
        self.minsize(1480, 750)
        self.geometry("0x0+20+20")
        self.columnconfigure([i for i in range(10)], weight = 1, minsize = 70)
        self.columnconfigure([i for i in range(11, 17)], weight = 1, minsize = 60)
        self.rowconfigure([i for i in range(10)], weight = 1, minsize = 60)

        self.bind("<Motion>", self.set_cursor_cell)
        self.bind("<Button-1>", self.mark_cursor_cell)
        self.bind("<Button-3>", self.right_mouse_button)

        frm_experiments = tk.Frame(relief = tk.RAISED, borderwidth = 1)
        frm_experiments.rowconfigure([0, 1, 2, 3, 4, 5], weight = 1)
        frm_experiments.columnconfigure(0, weight = 1)
        frm_experiments.grid(column = 11, row = 0, rowspan = 3, sticky = "news")

        self.btn_experiments[0] = tk.Button(master = frm_experiments, text = "EXPERIMENT 1", command = lambda : self.switch_to_experiment(0), bg = "red")
        self.btn_experiments[0].grid(row = 0)
        self.btn_experiments[1] = tk.Button(master = frm_experiments, text = "EXPERIMENT 2", command = lambda : self.switch_to_experiment(1))
        self.btn_experiments[1].grid(row = 2)
        self.btn_experiments[2] = tk.Button(master = frm_experiments, text = "EXPERIMENT 3", command = lambda : self.switch_to_experiment(2))
        self.btn_experiments[2].grid(row = 4)

        self.lbl_cell_counts = [None] * 3
        for i in range(3):
            self.lbl_cell_counts[i] = tk.Label(master = frm_experiments, text = "CELL COUNT:", height = 1, width = 15)
            self.lbl_cell_counts[i].grid(row = 1 + 2 * i)

        self.frm_hex_grid = tk.Frame(relief = tk.RAISED, borderwidth = 1)
        self.frm_hex_grid.columnconfigure([i for i in range(10)], weight = 1)
        self.frm_hex_grid.rowconfigure([i for i in range(10)], weight = 1)
        self.frm_hex_grid.grid(column = 0, row = 0, columnspan = 10, rowspan = 10, sticky = "news")

        self.frm_simulation_run = tk.Frame(relief = tk.RAISED, borderwidth = 1)
        self.frm_simulation_run.columnconfigure([0, 1, 2], weight = 1)
        self.frm_simulation_run.rowconfigure([x for x in range(8)], weight = 1)
        self.frm_simulation_run.grid(column = 13, row = 0, columnspan = 4, rowspan = 4, sticky = "news")

        self.lbl_mid_age = tk.Label(master=self.frm_simulation_run, text="MIDAGE: 0", anchor="w", relief=tk.RAISED, height=1, width=15)
        self.lbl_med_age = tk.Label(master=self.frm_simulation_run, text="MEDAGE: 0", anchor="w", relief=tk.RAISED, height=1, width=15)
        self.lbl_max_age = tk.Label(master=self.frm_simulation_run, text="MAXAGE: 0", anchor="w", relief=tk.RAISED, height=1, width=15)
        self.lbl_max_cluster = tk.Label(master=self.frm_simulation_run, text="MAXCLUS:", anchor="w", relief=tk.RAISED, height=1, width=15)
        self.lbl_mid_cluster = tk.Label(master=self.frm_simulation_run, text="MAXCLUS:", anchor="w", relief=tk.RAISED, height=1, width=15)
        self.lbl_cells_eaten = tk.Label(master=self.frm_simulation_run, text="CELLEAT:", anchor="w", relief=tk.RAISED, height=1, width=15)
        self.lbl_simulation_duration = tk.Label(master=self.frm_simulation_run, text="DURATION: 0", anchor="w", relief=tk.RAISED, height=1, width=15)

        self.lbl_mid_age.grid(column=0, row=1)
        self.lbl_med_age.grid(column=0, row=2)
        self.lbl_max_age.grid(column=0, row=3)
        self.lbl_max_cluster.grid(column=0, row=4)
        self.lbl_mid_cluster.grid(column=0, row=5)
        self.lbl_cells_eaten.grid(column=0, row=6)
        self.lbl_simulation_duration.grid(column=0, row=7)

        self.lbl_max_age.bind("<Button-1>", self.mark_maxage_cell)

        self.btn_play_pause_experiment = tk.Button(master = self.frm_simulation_run, text = "PAUSE", command = self.play_pause_simulation, width = 7, height = 2)
        self.btn_play_pause_experiment.grid(column=0, row=0)

        self.btn_decimate_culture = tk.Button(master = self.frm_simulation_run, text = "KILL CELL\nPERCENTAGE", command = self.button_decimate, width = 10, height = 2)
        self.btn_decimate_culture.grid(column=1, row=0)

        self.scl_decimate_percentage = tk.Scale(master = self.frm_simulation_run, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=300, width = 15)
        self.scl_decimate_percentage.set(10)
        self.scl_decimate_percentage.grid(column=1, row=1, rowspan = 7)

        tk.Label(master = self.frm_simulation_run, height = 3, width = 12, text = "SIMULATION\nSPEED:").grid(column=2, row=0)
        self.scl_simulation_speed = tk.Scale(master = self.frm_simulation_run, from_ = -1, to = 1, resolution = 0.1, relief=tk.RAISED, length=300, width = 15)
        self.scl_simulation_speed.set(0.5)
        self.scl_simulation_speed.grid(column=2, row=1, rowspan = 7)

        self.frm_initial_settings = tk.Frame(relief = tk.RAISED, borderwidth = 1)
        self.frm_initial_settings.columnconfigure([0, 1, 2, 3], weight = 1)
        self.frm_initial_settings.rowconfigure([0, 1, 2, 3, 4], weight = 1)

        tk.Label(master = self.frm_initial_settings, height = 3, width = 10, text = "GRID RADIUS:").grid(column=0, row=0)
        self.scl_grid_radius = tk.Scale(master = self.frm_initial_settings, from_ = 1, to = 30, resolution = 1, relief=tk.RAISED, length=300)
        self.scl_grid_radius.set(14)
        self.scl_grid_radius.grid(column=0, row=1, rowspan = 4)

        tk.Label(master = self.frm_initial_settings, height = 3, width = 10, text = "INITIAL CELL\nPERCENTAGE:").grid(column=1, row=0)
        self.scl_initial_cell_per = tk.Scale(master = self.frm_initial_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=300)
        self.scl_initial_cell_per.set(25)
        self.scl_initial_cell_per.grid(column=1, row=1, rowspan = 4)

        tk.Label(master = self.frm_initial_settings, height = 3, width = 10, text = "INITIAL CELL\nENERGY\nPERCENTAGE:").grid(column=2, row=0)
        self.scl_initial_cell_en_per = tk.Scale(master = self.frm_initial_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=300)
        self.scl_initial_cell_en_per.set(100)
        self.scl_initial_cell_en_per.grid(column=2, row=1, rowspan = 4)

        tk.Label(master = self.frm_initial_settings, height = 3, width = 10, text = "INITIAL CELL\nSIZE\nPERCENTAGE:").grid(column=3, row=0)
        self.scl_initial_cell_size_per = tk.Scale(master = self.frm_initial_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=300)
        self.scl_initial_cell_size_per.set(5)
        self.scl_initial_cell_size_per.grid(column=3, row=1, rowspan = 4)

        self.btn_flush_create_experiment = tk.Button(master = self, text = "FLUSH", command = self.flush_create_current_experiment, width = 7, height = 2)
        self.btn_flush_create_experiment.grid(column=12, row=0)

        self.btn_kill_all_cells = tk.Button(master = self, text = "KILL\nALL", command = self.kill_all_cells_in_current_experiment, width = 7, height = 2)
        self.btn_kill_all_cells.grid(column=12, row=1)

        self.btn_coppy_cell = tk.Button(master = self, text = "COPY", command = self.copy_marked_cell, width = 7, height = 2)
        self.btn_coppy_cell.grid(column=12, row=2)

        self.btn_switch_paste_kill = tk.Button(master = self, text = "MODE:\nPASTE", command = self.switch_paste_kill, width = 7, height = 2)
        self.btn_switch_paste_kill.grid(column=12, row=3)

        self.btn_switch_settings_cell_info = tk.Button(master = self, text = "SETTINGS", command = self.switch_settings_cell_info, width = 10, height = 2)
        self.btn_switch_settings_cell_info.grid(column=11, row=3)

        self.frm_simulation_settings = tk.Frame(master = self, relief = tk.RAISED, borderwidth = 1)
        self.frm_simulation_settings.columnconfigure([0, 1, 2, 3, 4], weight = 1, minsize = 104)
        self.frm_simulation_settings.rowconfigure([0, 1, 2, 3, 4], weight = 1, minsize = 50)

        tk.Label(master = self.frm_simulation_settings, height = 3, width = 12, text = "TILE REFILL\nPERCENTAGE:").grid(column=0, row=0)
        self.scl_energy_refill_amount = tk.Scale(master = self.frm_simulation_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=320, width = 12)
        self.scl_energy_refill_amount.set(20)
        self.scl_energy_refill_amount.grid(column=0, row=1, rowspan = 4)

        tk.Label(master = self.frm_simulation_settings, height = 3, width = 12, text = "PERCENTAGE\nOF REFILLED\nTILES:").grid(column=1, row=0)
        self.scl_tile_perc_refill = tk.Scale(master = self.frm_simulation_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=320, width = 12)
        self.scl_tile_perc_refill.set(35)
        self.scl_tile_perc_refill.grid(column=1, row=1, rowspan = 4)

        tk.Label(master = self.frm_simulation_settings, height = 3, width = 12, text = "CELL ENERGY\nABSORB\nPERCENTAGE:").grid(column=2, row=0)
        self.scl_cell_energy_gain = tk.Scale(master = self.frm_simulation_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=320, width = 12)
        self.scl_cell_energy_gain.set(16)
        self.scl_cell_energy_gain.grid(column=2, row=1, rowspan = 4)

        tk.Label(master = self.frm_simulation_settings, height = 3, width = 12, text = "CELL ENERGY\nCONSUMPTION\nPERCENTAGE:").grid(column=3, row=0)
        self.scl_cell_energy_loss = tk.Scale(master = self.frm_simulation_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=320, width = 12)
        self.scl_cell_energy_loss.set(7)
        self.scl_cell_energy_loss.grid(column=3, row=1, rowspan = 4)

        tk.Label(master = self.frm_simulation_settings, height = 3, width = 12, text = "CELL ENERGY\nTILE LOSS\nPERCENTAGE:").grid(column=4, row=0)
        self.scl_cell_around_en_loss = tk.Scale(master = self.frm_simulation_settings, from_ = 0, to = 100, resolution = 0.1, relief=tk.RAISED, length=320, width = 12)
        self.scl_cell_around_en_loss.set(8)
        self.scl_cell_around_en_loss.grid(column=4, row=1, rowspan = 4)

        self.frm_advanced_sim_settigs = tk.Frame(master = self, relief = tk.RAISED, borderwidth = 1)
        self.frm_advanced_sim_settigs.columnconfigure([0, 1, 2, 3], weight = 1, minsize = 130)
        self.frm_advanced_sim_settigs.rowconfigure([i for i in range(10)], weight = 1, minsize = 25)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MAX ENERGY\nBASE PERCENTAGE:").grid(column=0, row=0)
        self.sbx_cell_max_en_base = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 40), width = 12)
        self.sbx_cell_max_en_base.grid(column = 0, row = 1)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MAX ENERGY\nSIZE PERCENTAGE:").grid(column=0, row=2)
        self.sbx_cell_max_en_multip = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 30), width = 12)
        self.sbx_cell_max_en_multip.grid(column = 0, row = 3)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "ENERGY EAT\nPERCENTAGE:").grid(column=0, row=4)
        self.sbx_cell_en_eat_percentage = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 50), width = 12)
        self.sbx_cell_en_eat_percentage.grid(column = 0, row = 5)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "BASE SIZE\nGAIN PERCENTAGE:").grid(column=0, row=6)
        self.sbx_cell_base_size_gain = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 2.6), width = 12)
        self.sbx_cell_base_size_gain.grid(column = 0, row = 7)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "AROUND SIZE\nGAIN PERCENTAGE:").grid(column=0, row=8)
        self.sbx_cell_around_size_gain = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 0), width = 12)
        self.sbx_cell_around_size_gain.grid(column = 0, row = 9)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "SIZE EAT\nPERCENTAGE:").grid(column=1, row=0)
        self.sbx_cell_size_eat_percentage = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 33.3), width = 12)
        self.sbx_cell_size_eat_percentage.grid(column = 1, row = 1)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "SHARE MUTATION\nCHANGE PERCENTAGE:").grid(column=1, row=2)
        self.sbx_cell_share_mut_amount = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 20), width = 12)
        self.sbx_cell_share_mut_amount.grid(column = 1, row =3)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MIN SHARE\nPERCENTAGE:").grid(column=1, row=4)
        self.sbx_cell_min_share_per = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 0), width = 12)
        self.sbx_cell_min_share_per.grid(column = 1, row = 5)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MAX SHARE\nPERCENTAGE:").grid(column=1, row=6)
        self.sbx_cell_max_share_per = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 99), width = 12)
        self.sbx_cell_max_share_per.grid(column = 1, row = 7)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MOVE ENERGY\nCOST PERCENTAGE:").grid(column=1, row=8)
        self.sbx_cell_move_cost = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 2), width = 12)
        self.sbx_cell_move_cost.grid(column = 1, row = 9)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "DIVIDE MUTATION\nCHANGE PERCENTAGE:").grid(column=2, row=0)
        self.sbx_cell_div_mut_amount = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 20), width = 12)
        self.sbx_cell_div_mut_amount.grid(column = 2, row = 1)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MIN RESOURCES\nPERCENTAGE:").grid(column=2, row=2)
        self.sbx_cell_min_res_per = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 20), width = 12)
        self.sbx_cell_min_res_per.grid(column = 2, row = 3)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MAX RESOURCES\nPERCENTAGE:").grid(column=2, row=4)
        self.sbx_cell_max_res_per = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 80), width = 12)
        self.sbx_cell_max_res_per.grid(column = 2, row = 5)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "MUTATION CHANCE\nPERCENTAGE:").grid(column=2, row=6)
        self.sbx_cell_mut_chance = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 5), width = 12)
        self.sbx_cell_mut_chance.grid(column = 2, row = 7)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "STRONG MUTATION\nCHANCE PERCENTAGE:").grid(column=2, row=8)
        self.sbx_cell_str_mut_chance = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 45), width = 12)
        self.sbx_cell_str_mut_chance.grid(column = 2, row = 9)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "DIVIDE ENERGY\nCOST PERCENTAGE:").grid(column=3, row=0)
        self.sbx_cell_div_cost = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 12), width = 12)
        self.sbx_cell_div_cost.grid(column = 3, row = 1)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "CON SIZE MUTATION\nCHANGE PERCENTAGE:").grid(column=3, row=2)
        self.sbx_cell_size_con_mut_am = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 10), width = 12)
        self.sbx_cell_size_con_mut_am.grid(column = 3, row = 3)

        tk.Label(master = self.frm_advanced_sim_settigs, height = 3, width = 17, text = "CON EN MUTATION\nCHANGE PERCENTAGE:").grid(column=3, row=4)
        self.sbx_cell_en_con_mut_am = tk.Spinbox(master = self.frm_advanced_sim_settigs, from_ = 0, to = 100, increment = 0.1, textvariable = tk.DoubleVar(value = 5), width = 12)
        self.sbx_cell_en_con_mut_am.grid(column = 3, row = 5)

        self.frm_cell_information = tk.Frame(master = self, relief = tk.RAISED, borderwidth = 1)
        self.frm_cell_information.columnconfigure([0, 1], weight = 1, minsize = 260)
        self.frm_cell_information.rowconfigure([i for i in range(18)], weight = 1, minsize = 13.888)
        self.frm_cell_information.grid(column = 11, row = 4, columnspan = 6, rowspan = 6, sticky = "news")

        self.lbl_cursor_cell_head = tk.Label(master=self.frm_cell_information, text="Cursor cell:", anchor="w", height=1, bg="red")
        self.lbl_cursor_cell_head.grid(column=0, row=0, sticky="news")
        self.lbl_marked_cell_head = tk.Label(master=self.frm_cell_information, text="Marked cell:", anchor="w", height=1, bg="red")
        self.lbl_marked_cell_head.grid(column=1, row=0, sticky="news")

        self.lbl_cursor_cell = [None for _ in range(17)]
        self.lbl_marked_cell = [None for _ in range(17)]

        for i in range(len(self.lbl_cursor_cell)):
            self.lbl_cursor_cell[i] = tk.Label(master=self.frm_cell_information, bg="green", anchor="w", height=1)
            self.lbl_cursor_cell[i].grid(column=0, row=1+i, sticky="nswe")
            self.lbl_marked_cell[i] = tk.Label(master=self.frm_cell_information, bg="green", anchor="w", height=1)
            self.lbl_marked_cell[i].grid(column=1, row=1+i, sticky="nswe")

    def load_images(self):
        """Helper function, loads images from file to application."""
        self.pi_64_tiles = [None for _ in range(8)]
        self.pi_64_tiles[0] = tk.PhotoImage(file="Sprites/Tile_64_0.png")
        self.pi_64_tiles[1] = tk.PhotoImage(file="Sprites/Tile_64_1.png")
        self.pi_64_tiles[2] = tk.PhotoImage(file="Sprites/Tile_64_2.png")
        self.pi_64_tiles[3] = tk.PhotoImage(file="Sprites/Tile_64_3.png")
        self.pi_64_tiles[4] = tk.PhotoImage(file="Sprites/Tile_64_4.png")
        self.pi_64_tiles[5] = tk.PhotoImage(file="Sprites/Tile_64_5.png")
        self.pi_64_tiles[6] = tk.PhotoImage(file="Sprites/Tile_64_6.png")
        self.pi_64_tiles[7] = tk.PhotoImage(file="Sprites/Tile_64_wall.png")

        self.pi_32_tiles = [im.subsample(2) for im in self.pi_64_tiles]
        self.pi_16_tiles = [im.subsample(2) for im in self.pi_32_tiles]

        self.pi_64_cells = [None for _ in range(10)]
        self.pi_64_cells[0] = tk.PhotoImage(file="Sprites/Cell_64_0.png")
        self.pi_64_cells[1] = tk.PhotoImage(file="Sprites/Cell_64_1.png")
        self.pi_64_cells[2] = tk.PhotoImage(file="Sprites/Cell_64_2.png")
        self.pi_64_cells[3] = tk.PhotoImage(file="Sprites/Cell_64_3.png")
        self.pi_64_cells[4] = tk.PhotoImage(file="Sprites/Cell_64_4.png")
        self.pi_64_cells[5] = tk.PhotoImage(file="Sprites/Cell_64_5.png")
        self.pi_64_cells[6] = tk.PhotoImage(file="Sprites/Cell_64_6.png")
        self.pi_64_cells[7] = tk.PhotoImage(file="Sprites/Cell_64_7.png")
        self.pi_64_cells[8] = tk.PhotoImage(file="Sprites/Cell_64_8.png")
        self.pi_64_cells[9] = tk.PhotoImage(file="Sprites/Cell_64_9.png")

        self.pi_32_cells = [im.subsample(2) for im in self.pi_64_cells]
        self.pi_16_cells = [im.subsample(2) for im in self.pi_32_cells]

        self.pi_64_mark = tk.PhotoImage(file="Sprites/Mark_64.png")

        self.pi_32_mark = self.pi_64_mark.subsample(2)
        self.pi_16_mark = self.pi_32_mark.subsample(2)

        self.wm_iconphoto(False, self.pi_64_cells[0])

    def create_new_basic_experiment(self, experiment_number):
        """Creates new experiment on given index with properties set in application interface."""
        if experiment_number < 0 or experiment_number > 2:
            raise Exception("Current release supports max three experiments at the same time.")
        exp = self.dish_experiments[experiment_number]
        exp.create_experiment(number_of_cell_states = 10, grid_radius = int(self.scl_grid_radius.get()), cell_percentage = self.scl_initial_cell_per.get(), refill_tile_percentage = self.scl_tile_perc_refill.get(), refill_energy_flow = self.scl_energy_refill_amount.get() / 100, initial_cell_energy = int(self.scl_initial_cell_en_per.get() / 100 * ENERGY_UNIT_CONST), initial_cell_size = int(self.scl_initial_cell_size_per.get() / 100 * MAX_CELL_SIZE_CONST))
        self.dish_experiments[experiment_number] = exp
        self.create_experiment_canvas(exp)
        exp.start_simulation()
        exp.fast_global_statistics()
        exp.slow_global_statistics()
        self.show_statistics()

    def create_experiment_canvas(self, experiment:Dish_Experiment):
        """Creates new canvas in interface for experiment."""
        if self.experiment_canvases[self.current_experiment]:
            self.experiment_canvases[self.current_experiment].destroy()
        canvas = tk.Canvas(master=self.frm_hex_grid, bg="yellow")
        canvas.pack(fill=tk.BOTH, expand = True)  
        self.experiment_canvases[self.current_experiment] = canvas
        mark_im = canvas.create_image(0, 0, anchor="nw")
        self.mark_images[self.current_experiment] = mark_im
        canvas.itemconfig(mark_im, state=tk.HIDDEN)

        grid = experiment.real_grid
        virt_grid = experiment.virtual_grid
        img_tile = grid.pimage_tiles[0]
        w, h = img_tile.width(), img_tile.height()

        # jednoduche zobrazeni poli
        for cell_row in grid.hexagonal_tile_grid:
            for tile in cell_row:
                offset_x = self.canvas_image_offset[0]
                offset_y = self.canvas_image_offset[1]
                off_x = (tile.hex_pos.row - (grid.grid_radius)) * (w / 2)
                x = w * tile.hex_pos.col_l + off_x + offset_x
                y = h * 3/4 * tile.hex_pos.row + offset_y
                tile.image = canvas.create_image(x, y, anchor="nw")
                tile.canvas = canvas
                tile.update_image()
                virt_grid.get_tile_at_hex_pos(tile.hex_pos).image = tile.image
        pimage = self.pi_64_mark
        if experiment.tile_resolution[1] == 32:
            pimage = self.pi_32_mark
        elif experiment.tile_resolution[1] == 16:
            pimage = self.pi_16_mark
        canvas.itemconfig(self.mark_images[self.current_experiment], image=pimage)
        self.mark_offsets[self.current_experiment] = (pimage.height() - experiment.tile_resolution[1]) // 2
        canvas.lift(self.mark_images[self.current_experiment], grid.hexagonal_tile_grid[0][0].image)
        self.last_im_update_coords = [0, 0]

    # funkce povolana od Buttonu, povola funkci vytvoreni experimentu
    def create_basic_experiment(self):
        """Next-button function, creates new experiment and adjusts corresponding button in interface."""
        self.btn_flush_create_experiment.config(text="FLUSH")
        self.create_new_basic_experiment(self.current_experiment)

    def flush_current_experiment(self):
        """Next-button function, destroys currently shown experiment in the interface
        and adjusts corresponding button in interface."""
        self.btn_flush_create_experiment.config(text="CREATE\nNEW")
        self.dish_experiments[self.current_experiment].flush_experiment()
        if self.experiment_canvases[self.current_experiment]:
            self.experiment_canvases[self.current_experiment].destroy()
        self.play_pause_simulation()

    # povolavano od uzivatele
    def flush_create_current_experiment(self):
        """Button function, calls next-button functions depending on situation.
        Updates all statistics about experiment."""
        curr_exp = self.dish_experiments[self.current_experiment]
        if curr_exp and curr_exp.experiment_created:
            self.flush_current_experiment()
        else:
            self.create_basic_experiment()
        self.show_initial_settings_statistics()
        self.show_cell_counts()

    # povolavano od uzivatele
    def kill_all_cells_in_current_experiment(self):
        """Button function, kills all cell in experiment."""
        self.decimate_culture(100)

    # povolavano od uzivatele
    def button_decimate(self):
        """Button function, kills percentage of cells in experiment given by according slider value."""
        self.decimate_culture(self.scl_decimate_percentage.get())

    def decimate_culture(self, percentage):
        """Kills given percentage of cells in the experiment."""
        self.dish_experiments[self.current_experiment].decimate_culture(percentage)

    # povolavano od uzivatele
    def copy_marked_cell(self):
        """Button function, sets copied_cell to a copy of the marked_cell."""
        if self.marked_cell:
            self.copied_cell = self.marked_cell.copy()

    # povolavano od uzivatele
    def right_mouse_button(self, cursor):
        """Right mouse button function, calls next-right mouse button functions depending on situation."""
        if self.pasting:
            self.cursor_paste_copied_cell(cursor)
        else:
            self.cursor_kill_cell(cursor)

    # povolavano od uzivatele
    def cursor_paste_copied_cell(self, cursor):
        """Next-right mouse button function, inserts copied_cell to the shown experiment at tile under the mouse cursor."""
        if self.copied_cell:
            hex_pos = self.pixel_to_hex_position((cursor.x, cursor.y))
            exp = self.dish_experiments[self.current_experiment]
            initial_energy = round(self.scl_initial_cell_en_per.get() / 100 * ENERGY_UNIT_CONST)
            initial_size = round(self.scl_initial_cell_size_per.get() / 100 * MAX_CELL_SIZE_CONST)
            cell = exp.create_cell_from_cell(self.copied_cell, initial_energy, initial_size)
            exp.kill_cells_at_hex_pos(hex_pos)
            exp.add_cell_to_hex_pos(cell, hex_pos)

    def cursor_kill_cell(self, cursor):
        """Next-right mouse button function, kills all cells on the tile under the cursor in the shown experiment."""
        hex_pos = self.pixel_to_hex_position((cursor.x, cursor.y))
        exp = self.dish_experiments[self.current_experiment]
        exp.kill_cells_at_hex_pos(hex_pos)
        self.show_marked_cell()

    # povolavano od uzivatele
    def switch_paste_kill(self):
        """Switches between kill mode and paste mode on right mouse button."""
        if self.pasting:
            self.pasting = False
            self.btn_switch_paste_kill.config(text = "MODE:\nKILL")
        else:
            self.pasting = True
            self.btn_switch_paste_kill.config(text = "MODE:\nPASTE")

    def switch_to_experiment(self, experiment_number:int):
        """Button function, switches shown experiment to an experiment with given index
        and adjust all experiment settings sliders, spinboxes, ... accordingly."""
        if experiment_number < 0 or experiment_number > 2:
            raise Exception("Current release supports max three experiments at the same time.")
        self.last_im_update_coords = [0, 0]
        self.marked_cell = None
        self.current_experiment = experiment_number
        exp = self.dish_experiments[experiment_number]
        for btn in self.btn_experiments:
            btn.config(bg = "white")
        self.btn_experiments[experiment_number].config(bg = "red")
        for canvas in self.experiment_canvases:
            if canvas:
                canvas.pack_forget()
        self.show_initial_settings_statistics()
        if exp.experiment_created:
            self.experiment_canvases[experiment_number].pack(fill=tk.BOTH, expand = True)  
        if exp:
            if exp.experiment_created:
                self.btn_flush_create_experiment.config(text = "FLUSH")
                settings = exp.cell_and_state_settings
                self.scl_simulation_speed.set(self.speed_to_scale_convertion(exp.time_step))
                self.scl_tile_perc_refill.set(exp.refill_tile_percentage)
                self.scl_energy_refill_amount.set(exp.refill_energy_flow * 100)
                self.scl_cell_energy_gain.set(settings.energy_gain * 100 / ENERGY_UNIT_CONST)
                self.scl_cell_energy_loss.set(settings.base_energy_loss * 100 / ENERGY_UNIT_CONST)
                self.scl_cell_around_en_loss.set(settings.around_energy_loss * 100 / ENERGY_UNIT_CONST)

                self.sbx_cell_max_en_multip.config(textvariable = tk.DoubleVar(value = round(settings.max_energy_multiplier * 100, 1)))
                self.sbx_cell_max_en_base.config(textvariable = tk.DoubleVar(value = round(settings.max_energy_base * 100 / ENERGY_UNIT_CONST, 1)))
                self.sbx_cell_en_eat_percentage.config(textvariable = tk.DoubleVar(value = round(settings.energy_eat_fraction * 100, 1)))
                self.sbx_cell_base_size_gain.config(textvariable = tk.DoubleVar(value = round(settings.base_size_gain * 100 / MAX_CELL_SIZE_CONST, 1)))
                self.sbx_cell_around_size_gain.config(textvariable = tk.DoubleVar(value = round(settings.around_size_gain * 100 / MAX_CELL_SIZE_CONST, 1)))
                self.sbx_cell_size_eat_percentage.config(textvariable = tk.DoubleVar(value = round(settings.size_eat_fraction * 100, 1)))
                self.sbx_cell_share_mut_amount.config(textvariable = tk.DoubleVar(value = settings.share_mutation_amount))
                self.sbx_cell_min_share_per.config(textvariable = tk.DoubleVar(value = settings.min_share_per))
                self.sbx_cell_max_share_per.config(textvariable = tk.DoubleVar(value = settings.max_share_per))
                self.sbx_cell_div_mut_amount.config(textvariable = tk.DoubleVar(value = settings.divide_mutation_amount))
                self.sbx_cell_min_res_per.config(textvariable = tk.DoubleVar(value = settings.min_resources_per))
                self.sbx_cell_max_res_per.config(textvariable = tk.DoubleVar(value = settings.max_resources_per))
                self.sbx_cell_mut_chance.config(textvariable = tk.DoubleVar(value = settings.mutation_chance))
                self.sbx_cell_str_mut_chance.config(textvariable = tk.DoubleVar(value = settings.strong_mutation_chance))
                self.sbx_cell_div_cost.config(textvariable = tk.DoubleVar(value = round(settings.divide_energy_cost * 100 / ENERGY_UNIT_CONST, 1)))
                self.sbx_cell_move_cost.config(textvariable = tk.DoubleVar(value = round(settings.move_energy_cost * 100 / ENERGY_UNIT_CONST, 1)))
                self.sbx_cell_size_con_mut_am.config(textvariable = tk.DoubleVar(value = round(settings.size_mutation_amount * 100 / MAX_CELL_SIZE_CONST, 1)))
                self.sbx_cell_en_con_mut_am.config(textvariable = tk.DoubleVar(value = round(settings.energy_mutation_amount * 100 / ENERGY_UNIT_CONST, 1)))
            else:
                self.btn_flush_create_experiment.config(text = "CREATE\nNEW")

    def show_initial_settings_statistics(self):
        """Next-button function, switches between initial settings interface
        and statistics interface according to shown experiment state."""
        exp = self.dish_experiments[self.current_experiment]
        if exp is None:
            return
        if exp.experiment_created:
            self.frm_simulation_run.grid(column = 13, row = 0, columnspan = 4, rowspan = 4, sticky = "news")
            self.frm_initial_settings.grid_forget()
        else:
            self.frm_simulation_run.grid_forget()
            self.frm_initial_settings.grid(column = 13, row = 0, columnspan = 4, rowspan = 4, sticky = "news")

    def switch_settings_cell_info(self):
        """Button function, switches between cell information interface, basic settings interface
        and advanced settings interface according to currently shown interface."""
        if self.lower_frame_type == 0:
            self.lower_frame_type = 1
            self.btn_switch_settings_cell_info.config(text = "ADVANCED\nSETTINGS")
            self.frm_simulation_settings.grid(column = 11, row = 4, columnspan = 6, rowspan = 6, sticky = "news")
            self.frm_cell_information.grid_forget()
        elif self.lower_frame_type == 1:
            self.lower_frame_type = 2
            self.btn_switch_settings_cell_info.config(text = "CELL STATS")
            self.frm_advanced_sim_settigs.grid(column = 11, row = 4, columnspan = 6, rowspan = 6, sticky = "news")
            self.frm_simulation_settings.grid_forget()
        else:
            self.lower_frame_type = 0
            self.btn_switch_settings_cell_info.config(text = "SETTINGS")
            self.frm_cell_information.grid(column = 11, row = 4, columnspan = 6, rowspan = 6, sticky = "news")
            self.frm_advanced_sim_settigs.grid_forget()

    def pixel_to_hex_position(self, pixel_position:tuple) -> Hex_Pos:
        """Returns hex position given by pixel position in the window (from left and from top) and by shown experiment."""
        if not self.dish_experiments[self.current_experiment].experiment_created:
            return
        current_hex_grid = self.dish_experiments[self.current_experiment].real_grid
        current_radius = current_hex_grid.grid_radius
        current_tile_width = self.dish_experiments[self.current_experiment].tile_resolution[0]
        current_tile_height = self.dish_experiments[self.current_experiment].tile_resolution[1]
        simple_height = current_tile_height * 3 / 4
        offset_x = self.canvas_image_offset[0]
        offset_y = self.canvas_image_offset[1] + (current_tile_height - simple_height) / 2
        hex_row = floor((pixel_position[1] - offset_y) / simple_height)
        hex_col_l = floor((pixel_position[0] - offset_x - (hex_row - current_radius) * current_tile_width // 2) / current_tile_width)
        return Hex_Pos(hex_row, hex_col_l)

    def show_cursor_cell(self):
        """Updates information about the cursor_cell in the cell information interface."""
        if self.cursor_cell and self.cursor_cell.alive:
            info_list = self.cursor_cell.get_info_list()
            curr_state = info_list[1][0]
            for i in range(len(info_list)):
                self.lbl_cursor_cell[i].config(text=info_list[i], width=35)
                if curr_state == info_list[i][0]:
                    self.lbl_cursor_cell[i].config(bg="yellow", width=35)
                elif i > 1 and self.marked_cell and info_list[i] != self.marked_cell.get_info_list()[i]:
                    self.lbl_cursor_cell[i].config(bg="red", width=35)
                else:
                    self.lbl_cursor_cell[i].config(bg="green", width=35)
        elif self.lbl_cursor_cell[0] != "":
            self.cursor_cell = None
            for i in range(len(self.lbl_cursor_cell)):
                self.lbl_cursor_cell[i].config(text="")
                self.lbl_cursor_cell[i].config(bg="green", width=35)

    # povolavano od uzivatele
    def set_cursor_cell(self, cursor):
        """Cursor movement function, sets cursor_cell to the cell in the shown experiment under the cursor."""
        if cursor.widget == self.experiment_canvases[self.current_experiment] and self.dish_experiments[self.current_experiment].experiment_created:
            current_hex_grid = self.dish_experiments[self.current_experiment].real_grid
            cell_hex_pos = self.pixel_to_hex_position((cursor.x, cursor.y))
            hex_tile = current_hex_grid.get_tile_at_hex_pos(cell_hex_pos)
            if hex_tile:
                self.lbl_cursor_cell_head.config(text = "Cursor cell at " + str(hex_tile) + ":")
            elif self.lbl_cursor_cell_head["text"] != "Cursor cell:":
                self.lbl_cursor_cell_head.config(text = "Cursor cell:")
            if hex_tile and hex_tile.cells_on_tile:
                self.cursor_cell = hex_tile.cells_on_tile[0]
            else:
                self.cursor_cell = None
        elif self.lbl_cursor_cell_head["text"] != "Cursor cell:":
            self.lbl_cursor_cell_head.config(text = "Cursor cell:")

    def show_marked_cell(self):
        """Updates information about the marked_cell in the cell information interface."""
        if self.marked_cell and self.marked_cell.alive and self.dish_experiments[self.current_experiment].experiment_created:
            info_list = self.marked_cell.get_info_list()
            curr_state = info_list[1][0]
            for i in range(len(info_list)):
                self.lbl_marked_cell[i].config(text=info_list[i], width=35)
                if curr_state == info_list[i][0]:
                    self.lbl_marked_cell[i].config(bg="yellow", width=35)
                else:
                    self.lbl_marked_cell[i].config(bg="green", width=35)
            mark_im = self.mark_images[self.current_experiment]
            canvas = self.experiment_canvases[self.current_experiment]
            canvas.itemconfig(mark_im, state=tk.NORMAL)
            position = canvas.coords(self.marked_cell.current_tile.image)
            offset = self.mark_offsets[self.current_experiment]
            canvas.coords(mark_im, [position[0] - offset, position[1] - offset])
            canvas.lift(mark_im)
            hex_tile = self.marked_cell.current_tile
            self.lbl_marked_cell_head.config(text = "Marked cell at " + str(hex_tile) + ":", width=35)
        elif self.lbl_marked_cell[0] != "":
            self.marked_cell = None
            for i in range(len(self.lbl_marked_cell)):
                self.lbl_marked_cell[i].config(text="")
                self.lbl_marked_cell[i].config(bg="green", width=35)
            mark_im = self.mark_images[self.current_experiment]
            self.experiment_canvases[self.current_experiment].itemconfig(mark_im, state=tk.HIDDEN)
            self.lbl_marked_cell_head.config(text = "Marked cell:", width=35)

    # povolavano od uzivatele
    def mark_cursor_cell(self, cursor):
        """Left mouse button function, sets marked_cell to the cell in the shown experiment under the cursor."""
        if cursor.widget == self.experiment_canvases[self.current_experiment]:
            self.marked_cell = self.cursor_cell
            self.show_marked_cell()

    def mark_maxage_cell(self, cursor):
        """Button function, sets marked_cell to the cell in the shown experiment with the highest age."""
        self.marked_cell = self.maxage_cell
        self.show_marked_cell()

    def scale_to_speed_convertion(self, value:float) -> float:
        """Returns simulation speed given by slider value."""
        return pow(10, value) / 2
    
    def speed_to_scale_convertion(self, value:float) -> float:
        """Returns slider value given by simulation speed."""
        return log10(value * 2)

    def set_simulation_settings(self):
        """Adjusts simulation settings of the shown simulation according to the sliders and spinboxes in settings interfaces."""
        experiment = self.dish_experiments[self.current_experiment]

        # basic
        speed = self.scale_to_speed_convertion(self.scl_simulation_speed.get())
        experiment.time_step = speed
        refill_per = self.scl_tile_perc_refill.get()
        experiment.refill_tile_percentage = refill_per
        refill_am = self.scl_energy_refill_amount.get() / 100
        experiment.refill_energy_flow = refill_am
        settings = experiment.cell_and_state_settings
        settings.energy_gain = round(self.scl_cell_energy_gain.get() / 100 * ENERGY_UNIT_CONST)
        settings.base_energy_loss = round(self.scl_cell_energy_loss.get() / 100 * ENERGY_UNIT_CONST)
        settings.around_energy_loss = round(self.scl_cell_around_en_loss.get() / 100 * ENERGY_UNIT_CONST)

        # advanced
        val = self.convert_clip_percentage_value(self.sbx_cell_max_en_multip.get()) 
        settings.max_energy_multiplier = val / 100
        val = self.convert_clip_percentage_value(self.sbx_cell_max_en_base.get())
        settings.max_energy_base = round(val / 100 * ENERGY_UNIT_CONST)
        val = self.convert_clip_percentage_value(self.sbx_cell_en_eat_percentage.get())
        settings.energy_eat_fraction = val / 100
        val = self.convert_clip_percentage_value(self.sbx_cell_base_size_gain.get())
        settings.base_size_gain = round(val / 100 * MAX_CELL_SIZE_CONST)
        val = self.convert_clip_percentage_value(self.sbx_cell_around_size_gain.get())
        settings.around_size_gain = round(val / 100 * MAX_CELL_SIZE_CONST)
        val = self.convert_clip_percentage_value(self.sbx_cell_size_eat_percentage.get())
        settings.size_eat_fraction = val / 100
        val = self.convert_clip_percentage_value(self.sbx_cell_share_mut_amount.get())
        settings.share_mutation_amount = val
        val = self.convert_clip_percentage_value(self.sbx_cell_min_share_per.get())
        settings.min_share_per = val
        val = self.convert_clip_percentage_value(self.sbx_cell_max_share_per.get())
        settings.max_share_per = val
        val = self.convert_clip_percentage_value(self.sbx_cell_div_mut_amount.get())
        settings.divide_mutation_amount = val
        val = self.convert_clip_percentage_value(self.sbx_cell_min_res_per.get())
        settings.min_resources_per = val
        val = self.convert_clip_percentage_value(self.sbx_cell_max_res_per.get())
        settings.max_resources_per = val
        val = self.convert_clip_percentage_value(self.sbx_cell_mut_chance.get())
        settings.mutation_chance = val
        val = self.convert_clip_percentage_value(self.sbx_cell_str_mut_chance.get())
        settings.strong_mutation_chance = val
        val = self.convert_clip_percentage_value(self.sbx_cell_div_cost.get())
        settings.divide_energy_cost = round(val / 100 * ENERGY_UNIT_CONST)
        val = self.convert_clip_percentage_value(self.sbx_cell_move_cost.get())
        settings.move_energy_cost = round(val / 100 * ENERGY_UNIT_CONST)
        val = self.convert_clip_percentage_value(self.sbx_cell_size_con_mut_am.get())
        settings.size_mutation_amount = round(val / 100 * MAX_CELL_SIZE_CONST)
        val = self.convert_clip_percentage_value(self.sbx_cell_en_con_mut_am.get())
        settings.energy_mutation_amount = round(val / 100 * ENERGY_UNIT_CONST)

    def convert_clip_percentage_value(self, value:str) -> float:
        """Returns value between 0 and 100 given by a string value.
        If a string can not be converted to a float, then returns 0."""
        try:
            value = float(value)
            if value > 100:
                return 100
            elif value < 0:
                return 0
            else:
                return value
        except:
            return 0

    def show_statistics(self):
        """Sets text values of labels in statistics interface according to the shown experiment."""
        curr_exp = self.dish_experiments[self.current_experiment]
        self.lbl_mid_age.config(text="MIDAGE: " + str(curr_exp.cell_mid_age))
        self.lbl_med_age.config(text="MEDAGE: " + str(curr_exp.cell_med_age))
        self.lbl_max_age.config(text="MAXAGE: " + str(curr_exp.cell_max_age))
        self.lbl_max_cluster.config(text="MAXCLUS: " + str(curr_exp.max_cluster_size))
        self.lbl_mid_cluster.config(text="MIDCLUS: " + str(curr_exp.mid_cluster_size))
        self.maxage_cell = curr_exp.cell_with_maxage
        self.lbl_cells_eaten.config(text="CELLEAT: " + str(curr_exp.cells_eaten))
        self.lbl_simulation_duration.config(text="DURATION: " + str(curr_exp.simulation_steps_duration))

    def show_cell_counts(self):
        """Sets text values of labels under the buttons in choose experiment interface according to the shown experiment."""
        for i in range(3):
            exp = self.dish_experiments[i]
            if exp and exp.experiment_created:
                amount = exp.number_of_cells
                self.lbl_cell_counts[i].config(text = "CELL COUNT: " + str(amount))
            else:
                self.lbl_cell_counts[i].config(text = "CELL COUNT: 0")

    # povolavano od uzivatele
    def play_pause_simulation(self):
        """Button function, switches between play and pause mode of the shown experiment,
        adjusts corresponding button accordingly. If pausing then shows statistics."""
        experiment = self.dish_experiments[self.current_experiment]
        if experiment and experiment.experiment_created:
            if experiment.play_pause_simulation():
                self.btn_play_pause_experiment.config(text="PAUSE")
            else:
                self.btn_play_pause_experiment.config(text="PLAY")
                experiment.slow_global_statistics()
                self.show_statistics()
        else:
            self.btn_play_pause_experiment.config(text="PAUSE")

    def update_canvas(self):
        """Updates canvas in the interface according to the shown experiment.
        Update is divided into more steps to slightly improve interactivity."""
        current_exp = self.dish_experiments[self.current_experiment]
        if current_exp is None or not current_exp.experiment_created:
            return
        current_grid = current_exp.real_grid
        current_hexagonal_grid = current_grid.hexagonal_tile_grid
        current_canvas = self.experiment_canvases[self.current_experiment]
        maximal_changes = IMAGE_NUMBER_CONST - current_grid.grid_radius * current_grid.grid_radius // 5
        coords = self.last_im_update_coords
        for _ in range(maximal_changes):
            tile = current_hexagonal_grid[coords[0]][coords[1]]
            if tile.pi_image_changed:
                tile.pi_image_changed = False
                tile_image = tile.image
                photo_image = tile.pi_current_image
                current_canvas.itemconfig(tile_image, image = photo_image)
            coords[1] += 1
            coords[1] %= len(current_hexagonal_grid[coords[0]])
            if coords[1] == 0:
                coords[0] += 1
                coords[0] %= len(current_hexagonal_grid)

    def start_laboratory(self):
        """Starts laboratory."""
        self.stat_delay = 1
        self.sim_turns = 0

        if not self.laboratory_running:
            self.laboratory_running = True
            self.cycle_laboratory()
            self.mainloop()

    def cycle_laboratory(self):
        """Laboratory cycle called by loop somwhere in tkinter library.
        Updates canvas, simulates all experiments, shows statistics."""
        if not self.dish_experiments:
            return
        for dish in self.dish_experiments:
            if dish is None:
                continue
            if dish.simulate():
                self.show_cell_counts()
                if self.dish_experiments[self.current_experiment] == dish:
                    self.sim_turns += 1
                    if self.sim_turns == self.stat_delay:
                        dish.slow_global_statistics()
                        self.sim_turns = 0
                    dish.fast_global_statistics()
                    self.show_statistics()
                    self.show_marked_cell()
        self.update_canvas()
        self.after(self.cycle_time_ms, self.cycle_laboratory)
        self.show_cursor_cell()
        self.set_simulation_settings()

    def stop_laboratory(self):
        """Stops laboratory."""
        if self.laboratory_running:
            self.laboratory_running = False

def main():
    # vytvoreni laboratore
    window = Laboratory()

    # vytvoreni vychoziho zakladniho experimentu
    window.create_new_basic_experiment(0)

    # spusteni laboratore
    window.start_laboratory()

if __name__ == "__main__":
    main()