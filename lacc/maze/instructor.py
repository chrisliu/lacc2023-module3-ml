from lacc.maze import DOWN, LEFT, Maze, RIGHT, UP


def can_explore(maze, direction):
    pos = maze.to_my(direction)
    return maze[pos] != Maze.WALL and not maze.have_we_explored(pos)


opp_dir = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    UP: DOWN,
    DOWN: UP,
}


def solve_maze(maze):
    if maze.have_we_explored(maze.me):
        return False

    maze.explore(maze.me)
    maze.snapshot()

    if maze[maze.me] == Maze.GOAL:
        return True

    for direction in [UP, DOWN, RIGHT, LEFT]:
        if not maze.have_we_explored(maze.to_my(direction)):
            if maze[maze.to_my(direction)] != Maze.WALL:
                maze.drop_breadcrumb()
                maze.move(direction)
                maze.snapshot()

                if solve_maze(maze):
                    return True

                maze.move(opp_dir[direction])
                maze.pick_up_breadcrumb()
                maze.snapshot()


def make_moves(maze, me, path):
    maze.me = me
    maze.explore(maze.me)
    for direction in path:
        maze.snapshot()
        maze.move(direction)
        maze.explore(maze.me)
    maze.snapshot()
