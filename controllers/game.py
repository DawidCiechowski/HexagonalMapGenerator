import pygame as pg
from controllers.hex_grid import HexGrid
from controllers.pathfinder import Pathfinder
from views.renderer import Renderer
from models.unit import Unit
from utils.settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.hex_grid = HexGrid()
        self.pathfinder = Pathfinder(self.hex_grid)
        self.units = []
        self.selected_unit = None
        self.turn = 0
        self.automatic = True
        self.paused = False
        self.move_delay = 500
        self.last_move_time = pg.time.get_ticks()

        center_cell = self.hex_grid.get_cell(0, 0, 0 )
        self.selected_unit = Unit(center_cell)
        self.units.append(self.selected_unit)

        self.selected_cell = None
        self.renderer = Renderer(self.screen, self.hex_grid, self.selected_cell, self)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            self.handle_events()
            self.update(dt)
            self.renderer.selected_cell = self.selected_cell
            self.renderer.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if not self.paused and not self.automatic:
                        self.turn += 1
                        self.process_turn()
                elif event.key == pg.K_SPACE:
                    self.automatic = not self.automatic
                    self.last_move_time = pg.time.get_ticks()
                elif event.key == pg.K_p:
                    self.paused = not self.paused
                elif event.key == pg.K_PLUS or event.key == pg.K_EQUALS:
                    self.move_delay = max(100, self.move_delay - 100) 
                elif event.key == pg.K_MINUS or event.key == pg.K_UNDERSCORE:
                    self.move_delay += 100 
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos, event.button)

    def process_turn(self):
        for unit in self.units:
            unit.move_along_path()

    def handle_mouse_click(self, pos, button):
        cell = self.hex_grid.get_cell_by_pixel(*pos)

        if cell:
            if button == 1:
                if not cell.blocked:
                    path = self.pathfinder.find_path(self.selected_unit.cell, cell)
                    if path:
                        self.selected_unit.set_path(path)
                        self.selected_cell = cell
            elif button == 3:  
                if cell != self.selected_unit.cell:
                    cell.blocked = not cell.blocked
                    if cell == self.selected_cell:
                        self.selected_cell = None

    def update(self, dt):
        current_time = pg.time.get_ticks()
        if self.paused:
            return
        if not self.automatic:
            return
        
        if current_time - self.last_move_time >= self.move_delay:
            self.selected_unit.move_along_path()
            self.last_move_time = current_time