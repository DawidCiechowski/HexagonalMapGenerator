# views/renderer.py

import pygame
import math
from utils.hex_utils import hex_to_pixel, HEX_SIZE
from utils.settings import RED, BLUE, LIGHT_GRAY, GRAY, DARK_GRAY, WHITE


class Renderer:
    def __init__(self, screen, grid, selected_cell=None, game=None):
        self.screen = screen
        self.grid = grid
        self.selected_cell = selected_cell
        self.game = game
        self.font = pygame.font.SysFont(None, 24)

    def draw(self):
        self.screen.fill(GRAY)
        for cell in self.grid.cells.values():
            self.draw_hex(cell)
        self.draw_info()
        pygame.display.flip()

    def draw_info(self):
        if self.game.move_delay > 0:
            speed = 1000 // self.game.move_delay
        else:
            speed = "∞"
        
        speed_text = self.font.render(f"Speed: {speed} steps/sec", True, WHITE)
        self.screen.blit(speed_text, (10, 10))

        mode = "Automatic" if self.game.automatic else "Manual"
        mode_text = self.font.render(f"Mode: {mode}", True, WHITE)
        self.screen.blit(mode_text, (10, 30))

        paused = "Paused" if self.game.paused else "Running"
        paused_text = self.font.render(paused, True, WHITE)
        self.screen.blit(paused_text, (10, 50))

    def draw_hex(self, cell):
        x, y = hex_to_pixel(cell.q, cell.r, cell.s)

        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x_i = x + HEX_SIZE * math.cos(angle)
            y_i = y + HEX_SIZE * math.sin(angle) * 0.5  # Adjusted for isometric scaling
            points.append((x_i, y_i))
        # Determine the color based on the cell's state
        if cell.blocked:
            color = DARK_GRAY  # Dark gray for blocked cells
        elif cell == self.selected_cell:
            color = RED  # Red for selected cells
        else:
            color = LIGHT_GRAY  # Light gray for normal cells
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, (0, 0, 0), points, 1)
        if cell.unit:
            pygame.draw.circle(
                self.screen, BLUE, (int(x), int(y)), int(HEX_SIZE / 2)
            )
