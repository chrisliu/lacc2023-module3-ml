import collections
import math

from ipycanvas import Canvas, hold_canvas
from ipywidgets import widgets

from lacc.maze import Maze
from lacc.render import star_coords


def _get_offset(grid_px, debug):
    return 2 * grid_px if debug else 0


def _draw_maze_impl(maze, canvas, grid_px, debug, only_visible):
    offset_px = _get_offset(grid_px, debug)
    center_px = grid_px / 2

    def to_px(coord, center=False, offset=True):
        r, c = coord
        x_px = c * grid_px
        y_px = r * grid_px
        if center:
            x_px += center_px
            y_px += center_px
        if offset:
            x_px += offset_px
            y_px += offset_px
        return x_px, y_px

    # Draw explored.
    canvas.fill_style = "lightgreen"
    for coord in maze.explored:
        x_px, y_px = to_px(coord)
        canvas.fill_rect(x_px, y_px, grid_px)

    # Get grid coordinates of each cell type.
    grid_coords = collections.defaultdict(list)
    for r, row in enumerate(maze):
        for c, ty in enumerate(row):
            coord = (r, c)
            if not only_visible or maze.have_we_explored(coord):
                grid_coords[ty].append(coord)

    # Fill styles.
    fill_styles = {
        Maze.WALL: "gray",
        Maze.START: "green",
        Maze.GOAL: "red",
    }

    # Draw each type.
    for ty, fill in fill_styles.items():
        canvas.fill_style = fill
        for coord in grid_coords[ty]:
            canvas.fill_rect(*to_px(coord), grid_px)

    # Draw breadcrumbs.
    canvas.fill_style = "brown"
    for coord in maze.breadcrumbs:
        x_px, y_px = to_px(coord, center=True)
        canvas.fill_circle(x_px, y_px, center_px * 0.5)

    # Draw me.
    x_px, y_px = to_px(maze.me, center=True)
    canvas.fill_style = "yellow"
    # canvas.fill_circle(x_px, y_px, center_px * 0.8)
    canvas.fill_polygon(star_coords(radius=center_px * 0.8, center=(x_px, y_px)))

    # Draw any highlighted cells.
    for coord in maze.highlights:
        x_px, y_px = to_px(coord)
        canvas.stroke_style = "darkorchid"
        canvas.line_width = grid_px * 0.1
        canvas.stroke_rect(x_px, y_px, grid_px)

    # Draw debug information.
    if debug:
        canvas.fill_style = "black"
        canvas.font = f"{grid_px}px Courier"
        canvas.text_align = "center"
        canvas.text_baseline = "middle"
        for r in range(maze.num_rows):
            x_px, y_px = to_px((r + 2, 1), offset=False, center=True)
            canvas.fill_text(str(r), x_px, y_px)

        for c in range(maze.num_cols):
            x_px, y_px = to_px((1, c + 2), offset=False, center=True)
            canvas.fill_text(str(c), x_px, y_px)

        # X label
        x_px = offset_px + maze.num_cols * grid_px / 2
        y_px = center_px
        canvas.fill_text("Column", x_px, y_px)

        # Y label
        x_px = center_px
        y_px = offset_px + maze.num_rows * grid_px / 2
        canvas.translate(x_px, y_px)
        canvas.rotate(math.radians(-90))
        canvas.fill_text("Row", 0, 0)
        canvas.rotate(math.radians(90))
        canvas.translate(-x_px, -y_px)


def _draw_maze_new_canvas(maze, grid_px, debug, only_visible):
    offset = _get_offset(grid_px, debug)
    width = maze.num_cols * grid_px + offset + 5  # RPadding
    height = maze.num_rows * grid_px + offset + 5  # RPadding
    canvas = Canvas(width=width, height=height)
    _draw_maze_impl(maze, canvas, grid_px, debug, only_visible)
    return canvas


def draw_maze(maze, grid_px=60, debug=True, only_visible=False):
    canvas = _draw_maze_new_canvas(maze, grid_px, debug, only_visible)
    return canvas


def animate_maze(maze, grid_px=60, debug=True, only_visible=False):
    play = widgets.Play(
        value=0, min=0, max=len(maze.snapshots) - 1, interval=250, disabled=False
    )
    slider = widgets.IntSlider(
        value=0,
        min=0,
        max=len(maze.snapshots) - 1,
        step=1,
        disabled=False,
        continuous_update=False,
        orientation="horizontal",
    )
    prev = widgets.Button(
        description="<",
        disabled=False,
    )
    nxt = widgets.Button(
        description=">",
        disabled=False,
    )

    def dec(b):
        slider.value = max(slider.value - 1, slider.min)

    def inc(b):
        slider.value = min(slider.value + 1, slider.max)

    prev.on_click(dec)
    nxt.on_click(inc)

    canvas = _draw_maze_new_canvas(maze.snapshots[0], grid_px, debug, only_visible)

    def handle(change):
        idx = change["new"]
        with hold_canvas(canvas):
            canvas.clear()
            _draw_maze_impl(maze.snapshots[idx], canvas, grid_px, debug, only_visible)

    slider.observe(handle, names="value")
    widgets.jslink((play, "value"), (slider, "value"))
    control = widgets.HBox([play, slider, prev, nxt])
    render = widgets.Box([canvas], layout=widgets.Layout(width=f"{canvas.width}px"))
    view = widgets.VBox([render, control])
    return view
