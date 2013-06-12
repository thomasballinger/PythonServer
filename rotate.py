import math
def rotate(x, y, angle):
    angle_in_radians = math.radians(angle)
    new_x = x * math.cos(angle_in_radians) - y * math.sin(angle_in_radians)
    new_y = x * math.sin(angle_in_radians) + y * math.cos(angle_in_radians)
    return new_x, new_y