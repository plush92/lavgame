import pygame
import random
import heapq

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bar Escape: Hometown Honkey Tonk")

# Define directions for A* algorithm (4 directions + diagonal)
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

class Bouncer:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = 1.4
        self.can_move = False
        self.path_finding_timer = 0
        self.stuck_timer = 0
        self.last_position = (x, y)
        self.path = []  # A* path
        self.path_index = 0  # Keeps track of the current point in the A* path

    def start_moving(self):
        self.can_move = True

    def heuristic(self, current, target):
        """Manhattan distance heuristic (could be Euclidean for diagonal efficiency)"""
        return abs(current[0] - target[0]) + abs(current[1] - target[1])

    def a_star(self, start, goal, walls):
        """A* algorithm for pathfinding"""
        open_list = []
        closed_list = set()
        heapq.heappush(open_list, (0 + self.heuristic(start, goal), 0, start))  # (f, g, pos)
        g_costs = {start: 0}
        came_from = {}

        while open_list:
            _, g, current = heapq.heappop(open_list)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            closed_list.add(current)
            for direction in DIRECTIONS:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if neighbor in closed_list or not self.is_passable(neighbor, walls):
                    continue
                tentative_g = g + 1  # Assuming uniform cost for all moves
                if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                    g_costs[neighbor] = tentative_g
                    f_cost = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, tentative_g, neighbor))
                    came_from[neighbor] = current
        return []  # No path found

    def is_passable(self, position, walls):
        """Checks if a position is within bounds and not colliding with any walls"""
        x, y = position
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return False
        return not any(pygame.Rect(x, y, 20, 20).colliderect(w) for w in walls)

    def move_towards_player(self, player, walls):
        if not self.can_move:
            return

        current_pos = (self.rect.x, self.rect.y)
        self.path_finding_timer += 1

        if self.path_finding_timer >= 30 or self.stuck_timer >= 10:
            self.path_finding_timer = 0

            start = (self.rect.x, self.rect.y)
            goal = (player.rect.x, player.rect.y)

            # Perform A* to get a path to the player
            self.path = self.a_star(start, goal, walls)
            self.path_index = 0

        # Follow the next point in the path
        if self.path and self.path_index < len(self.path):
            next_point = self.path[self.path_index]
            dx = next_point[0] - self.rect.x
            dy = next_point[1] - self.rect.y

            # Move towards the next point on the path
            self.rect.x += (dx / max(1, abs(dx))) * self.speed
            self.rect.y += (dy / max(1, abs(dy))) * self.speed

            if abs(dx) < 2 and abs(dy) < 2:
                self.path_index += 1  # Move to the next point in the path

        # Ensure the bouncer stays within screen bounds
        self.rect.clamp_ip(pygame.Rect(20, 20, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40))

        self.last_position = (self.rect.x, self.rect.y)

