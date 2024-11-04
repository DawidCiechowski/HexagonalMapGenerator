
class Unit:
    def __init__(self, cell):
        self.cell = cell
        self.cell.unit = self
        self.path = []

    def set_path(self, path):
        self.path = path

    def move_along_path(self):
        if self.path:
            next_cell = self.path.pop(0)
            if not next_cell.unit and not next_cell.blocked:
                self.cell.unit = None
                self.cell = next_cell
                self.cell.unit = self
