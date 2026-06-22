import pygame
import math

def draw_pixel_block(screen, x, y, color, pixel_size, direction, width):
    px = int(round(x)) * pixel_size
    py = int(round(y)) * pixel_size
    if px < 0: px += width
    elif px >= width: px -= width
    pygame.draw.rect(screen, color, (px, py, pixel_size, pixel_size))

def draw_blob(screen, char_x, cx, cy, rx, ry, color, pixel_size, direction, width):
    start_x = int(math.floor(cx - rx - 1))
    end_x = int(math.ceil(cx + rx + 1))
    start_y = int(math.floor(cy - ry - 1))
    end_y = int(math.ceil(cy + ry + 1))
    
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            dx = x - cx
            dy = y - cy
            if (dx*dx) / (rx*rx if rx > 0 else 1) + (dy*dy) / (ry*ry if ry > 0 else 1) <= 1.0:
                local_offset_x = x - char_x
                flipped_x = char_x + (local_offset_x * direction)
                draw_pixel_block(screen, flipped_x, y, color, pixel_size, direction, width)

def draw_pixel_line(screen, char_x, x1, y1, x2, y2, color, pixel_size, direction, width):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(int(round(max(abs(dx), abs(dy)))) * 2, 1)
    
    for i in range(steps + 1):
        t_val = i / steps
        curr_x = x1 + dx * t_val
        curr_y = y1 + dy * t_val
        local_offset_x = curr_x - char_x
        flipped_x = char_x + (local_offset_x * direction)
        draw_pixel_block(screen, flipped_x, curr_y, color, pixel_size, direction, width)
