
import heapq
from itertools import count


class Pathfinder:
    def __init__(self, grid):
        self.grid = grid

    def heuristic(self, a, b):
        return (abs(a.q - b.q) + abs(a.r - b.r) + abs(a.s - b.s)) / 2

    def find_path(self, start, goal):
        frontier = []
        counter = count()  # Unique sequence count
        heapq.heappush(frontier, (0, next(counter), start))  # (priority, count, cell)
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_priority, current_count, current = heapq.heappop(frontier)

            if current == goal:
                break

            for neighbor in self.grid.get_neighbours(current):
                if neighbor.blocked:
                    continue
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, next(counter), neighbor))
                    came_from[neighbor] = current

        return self.reconstruct_path(came_from, start, goal)

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None:
                return []  # No path found
        path.reverse()
        return path
