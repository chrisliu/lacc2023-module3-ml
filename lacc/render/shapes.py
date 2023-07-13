import math


def star_coords(radius, center=None, offset_angle=None, n=5):
    assert n >= 5
    if center is None:
        x_center, y_center = 0, 0
    else:
        x_center, y_center = center

    if offset_angle is None:
        offset_angle = math.radians(-90)

    angles = [2 * math.pi / n * i for i in range(n)]
    outer_points = [
        (
            radius * math.cos(angle + offset_angle),
            radius * math.sin(angle + offset_angle),
        )
        for angle in angles
    ]

    def dist(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    internal_angle = math.pi * (n - 2) / n
    x1, y1 = outer_points[0]
    x2, y2 = outer_points[1]
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2
    opp = dist((x1, y1), (x_mid, y_mid))
    theta = internal_angle / 2
    adj = opp / math.tan(theta)
    dist_midpt = dist((0, 0), (x_mid, y_mid))

    inner_radius = dist_midpt - adj
    assert inner_radius > 0

    inner_angle_offset = (2 * math.pi / n) / 2
    inner_points = [
        (
            inner_radius * math.cos(angle + inner_angle_offset + offset_angle),
            inner_radius * math.sin(angle + inner_angle_offset + offset_angle),
        )
        for angle in angles
    ]

    points = [None] * (2 * n)
    points[::2] = outer_points
    points[1::2] = inner_points
    coords = [(x + x_center, y + y_center) for x, y in points]
    return coords
