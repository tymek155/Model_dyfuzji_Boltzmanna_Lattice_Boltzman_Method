class Czastka:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self, grid):
        if self.dy != 0:
            next_y = self.y + self.dy
            if grid[next_y][self.x] == 0:
                self.dy = -self.dy
            else:
                grid[self.y][self.x] = 1
                self.y = next_y
                grid[self.y][self.x] = 2
        else:
            next_x = self.x +self.dx
            if grid[self.y][next_x] == 0:
                self.dx = -self.dx
            else:
                grid[self.y][self.x] = 1
                self.x = next_x
                grid[self.y][self.x] = 2

def solve_collision(coord, czastk_list):
    collisions = []
    for czastka in czastk_list:
        if czastka.x == coord[0] and czastka.y == coord[1]:
            collisions.append(czastka)

    if len(collisions) == 2:
        if collisions[0].dx != 0 and collisions[0].dx == -collisions[1].dx:
            collisions[0].dy = collisions[0].dx
            collisions[0].dx = 0

            collisions[1].dy = collisions[1].dx
            collisions[1].dx = 0

        elif collisions[0].dy != 0 and collisions[0].dy == -collisions[1].dy:
            collisions[0].dx = collisions[0].dy
            collisions[0].dy = 0

            collisions[1].dx = collisions[1].dy
            collisions[1].dy = 0


def collision(czastk_list):
    coord_count = {}

    for czastka in czastk_list:
        coord = (czastka.x, czastka.y)
        if coord in coord_count:
            coord_count[coord] += 1
        else:
            coord_count[coord] = 1

    collision_coords = [coord for coord, count in coord_count.items() if count > 1]

    for coord in collision_coords:
        solve_collision(coord, czastk_list)
