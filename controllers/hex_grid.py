from models.hex_cell import HexCell
from utils.hex_utils import pixel_to_hex, HEX_DIRECTIONS
from utils.settings import GRID_RADIUS

class HexGrid:

    def __init__(self):
        self.cells = {}
        self.__create_grid()

    def __create_grid(self):
        for q in range(-GRID_RADIUS, GRID_RADIUS + 1):
            r1 = max(-GRID_RADIUS, -q - GRID_RADIUS)
            r2 = min(GRID_RADIUS, -q + GRID_RADIUS)
            for r in range(r1, r2 + 1):
                s = -q - r
                cell = HexCell(q, r, s)
                self.cells[(q, r, s)] = cell

    def get_cell(self, q, r, s):
        return self.cells.get((q, r, s))

    def get_neighbours(self, cell):
        neighbours = []
        for direction in HEX_DIRECTIONS:
            neighbour_coords = (cell.q + direction[0], cell.r + direction[1], cell.s + direction[2])
            neighbour = self.get_cell(*neighbour_coords)
            if neighbour:
                neighbours.append(neighbour)
        return neighbours

    def get_cell_by_pixel(self, x, y):
        q, r, s = pixel_to_hex(x, y)
        return self.get_cell(q, r, s)
